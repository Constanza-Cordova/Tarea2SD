import { Body, Controller, Get, Post, Query } from '@nestjs/common';
import { ElasticService } from './elastic.service';


@Controller('elastic')
export class ElasticController {
  constructor(private readonly elasticService: ElasticService) { }

  @Post('document')
  async indexData(@Body() data: { index: string, document: any }) {
    return this.elasticService.indexData(data.index, data.document);
  }

  @Get('document')
  async searchData(@Query('index') index: string, @Query('query') query: string) {
    return this.elasticService.search(index, JSON.parse(query));
  }

}
