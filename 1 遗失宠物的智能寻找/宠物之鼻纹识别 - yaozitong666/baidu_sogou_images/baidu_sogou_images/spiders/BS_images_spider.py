# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
import json
from ..items import BaiduSogouImagesItem
from ..settings import search_word


class BsImagesSpiderSpider(scrapy.Spider):
    name = 'BS_images_spider'
    allowed_domains = ['image.baidu.com', 'pic.sogou.com']

    # 对要搜索的字段进行转码
    search_word = quote(search_word)
    # 开始页码为0
    sogou_offset = 0
    baidu_offset = 0
    # 搜狗图片基本地址
    sogou_base_url = 'http://pic.sogou.com/pics?query={0}&start={1}&reqType=ajax&reqFrom=result&tn=0'
    # 百度图片的基本地址
    baidu_base_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&queryWord={0}&word={0}&pn={1}&rn=60'
    # 开始地址
    start_urls = [sogou_base_url.format(search_word, sogou_offset)]

    def parse(self, response):
        """
        处理搜狗图片的响应，提取出图片链接并交给管道处理
        :param response: 搜狗的响应
        :return: 图片链接item
        """
        # 把json格式的数据转换为python格式，items段是列表
        if self.is_json(response.text):
            data = json.loads(response.text, strict=False).get("items")
            if data is not None:
                # 遍历每一个列表
                for each in data:
                    item = BaiduSogouImagesItem()

                    # 图片链接列表
                    item["imageLinkList"] = []
                    if each.get("pic_url") is not None:
                        item["imageLinkList"].append(each.get("pic_url"))

                    # 字图片链接
                    if each.get("simdata") is not None:
                        for each_simLink in each.get("simdata"):
                            if len(each_simLink) >= 5:
                                item["imageLinkList"].append(each_simLink[4])

                    # 把item交给管道
                    yield item

        if self.sogou_offset < -1:  # 48
            self.sogou_offset += 48
            yield scrapy.Request(self.sogou_base_url.format(search_word, self.sogou_offset), callback=self.parse)
        else:
            # 处理完搜狗图片，开始处理百度图片
            yield scrapy.Request(self.baidu_base_url.format(search_word, 0), callback=self.baidu_parse)

    def baidu_parse(self, response):
        """
        处理百度图片的响应，提取出图片链接并交给管道处理
        :param response: 搜狗的响应
        :return: 图片链接item
        """
        # 把json格式的数据转换为python格式，items段是列表
        data = json.loads(response.text, strict=False).get("data")
        if data is not None:
            # 遍历每一个列表
            for each in data:
                item = BaiduSogouImagesItem()

                # 图片链接列表
                item["imageLinkList"] = []
                if each.get("thumbURL") is not None:
                    item["imageLinkList"].append(each.get("thumbURL"))

                elif each.get("middleURL") is not None:
                    item["imageLinkList"].append(each.get("middleURL"))

                # 把item交给管道
                yield item

        if self.baidu_offset < -1:  # 1900
            self.baidu_offset += 60
            yield scrapy.Request(self.baidu_base_url.format(search_word, self.baidu_offset), callback=self.baidu_parse)
        else:
            print('收工！')

    def is_json(self,myjson):
        try:
            json.loads(myjson)
        except ValueError:
            return False
        return True

