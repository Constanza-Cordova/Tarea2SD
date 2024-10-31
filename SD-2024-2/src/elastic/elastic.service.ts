import { Injectable } from '@nestjs/common';
import { ElasticsearchService } from '@nestjs/elasticsearch';

@Injectable()
export class ElasticService {
  constructor(private readonly elasticSearchService: ElasticsearchService) { }

  async indexData(index: string, document: any) {
    return this.elasticSearchService.index({
      index,
      body: document,
    });
  }
  async search(index: string, query: any) {
    return this.elasticSearchService.search({
      index,
      query: {
        ...query
      }

    });
  }
}
