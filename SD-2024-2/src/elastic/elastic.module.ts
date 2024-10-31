import { Module } from '@nestjs/common';
import { ElasticService } from './elastic.service';
import { ElasticController } from './elastic.controller';
import { ElasticsearchModule } from '@nestjs/elasticsearch';

@Module({
  imports: [
    ElasticsearchModule.register({
      node: 'http://localhost:9200',
    }),
  ],
  controllers: [ElasticController],
  providers: [ElasticService],
})
export class ElasticModule { }
