# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
import os
from .settings import save_file_name


class BaiduSogouImagesPipeline(ImagesPipeline):
    COUNT = 0
    # E:\Users\ASUS\PycharmProjects\webspider\test_scrapy\baidu_sogou_images\images\rabbit
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        # self.save_file_name = item['imageName']
        for image_url in item["imageLinkList"]:
            yield scrapy.Request(image_url)

    def item_completed(self, result, item, info):
        # 取出results里面图片信息种的图片路径值
        # image_path_list = [x["path"] for ok, x in result if ok]

        # for image_path in image_path_list:
        #     try:
        #         print(self.IMAGES_STORE)
        # print(self.IMAGES_STORE + os.sep + image_path.replace('/', os.sep))
        # print(self.IMAGES_STORE + os.sep + save_file_name + '.' + str(self.COUNT) + '.jpg')
        # os.chdir(self.IMAGES_STORE + os.sep + "full")
        # os.rename(image_path.replace('full/', ''),
        #           self.IMAGES_STORE + os.sep + save_file_name + str(self.COUNT) + '.jpg')
        # except Exception as e:
        #     print('错误：', e)
        # finally:
        #     self.COUNT += 1

        return item

    def re_name_file(self, dir_name, new_file_name):
        """
        对文件夹中的文件进行命名，文件夹跳过
        :param dir_name: 需要对文件夹中的文件进行重命名的文件夹路径名
        :param new_file_name:新文件名
        :return:none
        """
        filelist = os.listdir(dir_name)  # 该文件夹下所有的文件（包括文件夹）
        count_file = 0
        for file in filelist:  # 遍历所有文件
            old_dir = os.path.join(dir_name, file)  # 原来的文件路径
            if os.path.isdir(old_dir):  # 如果是文件夹则跳过
                continue
            # filename = os.path.splitext(file)[0]  # 文件名
            # print('文件名：', filename)
            filetype = os.path.splitext(file)[1]  # 文件扩展名
            # print('文件类型：', filetype)
            new_dir = os.path.join(self.IMAGES_STORE, new_file_name + str(count_file) + filetype)
            os.rename(old_dir, new_dir)  # 重命名
            count_file += 1

    def close_spider(self, spider):
        self.re_name_file(self.IMAGES_STORE + os.sep + 'full', save_file_name)

        try:
            os.removedirs(self.IMAGES_STORE + os.sep + 'full')
        except Exception as e:
            print('错误：', e)
