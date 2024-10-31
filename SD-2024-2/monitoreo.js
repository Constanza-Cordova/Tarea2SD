const { Kafka } = require('kafkajs');
const { Client } = require('@elastic/elasticsearch');  // Asegúrate de instalar el cliente de Elasticsearch

const kafka = new Kafka({
    clientId: 'mi-aplicacion',
    brokers: ['localhost:9093'] // Asegúrate de que este sea el puerto correcto para tu broker Kafka
});

const consumer = kafka.consumer({ groupId: 'grupo-consumidor1' });
const client = new Client({ node: 'http://localhost:9200' }); // Conexión a Elasticsearch

let totalMessages = 0;
let totalLatency = 0; // Variable para acumular la latencia
const startTime = Date.now(); // Marca el tiempo de inicio

const consume = async () => {
    await consumer.connect();
    console.log('Conectado al broker Kafka');

    // Suscribirse a múltiples tópicos
    const topics = ['procesando', 'preparacion', 'enviado', 'entregado', 'finalizado'];
    await Promise.all(topics.map(topic => consumer.subscribe({ topic, fromBeginning: true })));

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            const key = message.key ? message.key.toString() : 'N/A';
            const value = message.value.toString();
            console.log(`Mensaje recibido del tópico '${topic}': key=${key}, value=${value}, partition=${partition}`);

            // Aquí puedes calcular la latencia si es necesario
            const startProcessingTime = Date.now(); // Marca el inicio del procesamiento
            // Simulación de procesamiento de mensaje
            await new Promise(resolve => setTimeout(resolve, Math.random() * 100)); // Simulación de latencia

            // Calcular la latencia para este mensaje
            const latency = Date.now() - startProcessingTime;
            totalLatency += latency; // Acumula la latencia
            totalMessages++; // Incrementa el contador de mensajes

            // Producir el mensaje en el siguiente tópico
            await producer.produce(topic, value.encode('utf-8'));
            await producer.flush();

            // Confirmar el commit del offset
            await consumer.commitOffsets([{ topic, partition, offset: message.offset + 1 }]);
            console.log(`Mensaje producido en ${topic}: ${value}`);

            // Enviar métricas a Elasticsearch cada 10 mensajes procesados
            if (totalMessages % 10 === 0) {
                const elapsedTime = (Date.now() - startTime) / 1000; // tiempo en segundos
                const throughput = totalMessages / elapsedTime; // mensajes por segundo

                // Enviar latencia y throughput a Elasticsearch
                const metrics = {
                    service: 'monitoreo_service',
                    latency: totalLatency / totalMessages, // promedio de latencia
                    throughput: throughput,
                    timestamp: new Date(),
                };

                await client.index({
                    index: 'metrics_notificaciones',  // índice para las métricas de notificaciones
                    document: metrics,
                });

                console.log(`Métricas enviadas a Elasticsearch: Latencia promedio=${metrics.latency} ms, Throughput=${metrics.throughput} msg/s`);

                // Reiniciar contadores
                totalMessages = 0;
                totalLatency = 0;
            }
        },
    });
};

consume().catch(console.error);
