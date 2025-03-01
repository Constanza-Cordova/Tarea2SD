
## 🦁🔎 NestJS x ElasticSearch

Breve proyecto para demostrar el uso de ElasticSearch junto a NestJS. Tiene como propósito acercar a los estudiantes a la indexación de documentos, junto a su posterior análisis a través de Kibana.

### Cómo correr el proyecto

Clona el repositorio

```bash
git clone https://github.com/cesarmunozr/SD-2024-2.git
```

Utiliza la branch de elastic-search
```
git checkout elastic-search
```

Instala las dependencias
```
npm i 
```

Inicia los contenedores
```
docker compose up
```

Inicia el proyecto
```
npm run start:dev
```

Eso es todo, happy coding. ✨ 

### Diagramas de flujo relevantes
<img src='/docs/images/indexation-fd.png' height='450'/>

Para poder gestionar las dependencias de Node.js, se debe utilizar el comando npm install y para verificar la instalación se debe usar ls node_modules 
