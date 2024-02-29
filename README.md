# scrapy-selenium爬取动态网页


## 1、googledriver下载
https://googlechromelabs.github.io/chrome-for-testing/ 121版本
https://chromedriver.storage.googleapis.com/index.html old版本

chromedriver.exe放到python.exe同级目录

## 2、google-chrome浏览器下载，版本一致
我是122.0.6261.70版本
## 3、python环境安装

```
pip install scrapy
pip install selenium
scrapy startproject pachong
cd pachong
scrapy genspider medicine js.sgcc.com.cn
其中“medicine”是指爬虫的名称，“js.sgcc.com.cn”爬虫的域名
```



## 4、修改setting.py的配置
> BOT_NAME = "pachong"
> 
> SPIDER_MODULES = ["pachong.spiders"]
> NEWSPIDER_MODULE = "pachong.spiders"
>  
> #爬虫协议，基本无视之，毕竟你遵循了协议就啥也爬不到
> ROBOTSTXT_OBEY=False
>  
> DOWNLOAD_DELAY = 5 #最小延迟
> 
> COOKIES_ENABLED=False #是否支持cookie，cookiejar进行操作cookie，默认开启
> 
> DOWNLOADER_MIDDLEWARES = {
>     "pachong.middlewares.PachongDownloaderMiddleware": 543,
> }
> 
> ITEM_PIPELINES={
> ‘jsdl.pipelines.JsdlPipeline’:300, #使用pipelines.py中哪个方法
> }
> 
> REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
> TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
> FEED_EXPORT_ENCODING = "utf-8"
> LOG_LEVEL = "WARNING"

## 5、修改spiders\medicine.py

```
import scrapy
import json,time
from selenium import webdriver
from selenium.webdriver.common.by import By

class MedicineSpider(scrapy.Spider):
    name = "medicine"
    allowed_domains = ["platform.opentargets.org"]
    start_urls = ["https://platform.opentargets.org"]
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # chrome = webdriver.Chrome(options=options)

    def parse(self, response, **kwargs):
        with open('D:\\pachong\\pachong\\target.txt', 'r') as file:
            lines = file.readlines()
        for i_item in lines:
            time.sleep(15)
            print(i_item)
            yield scrapy.Request(i_item,callback=self.parse_more) #跳转url

    def parse_more(self, response):
        ## Known Drugs
        ## Tractability

        # print("==============================================111111111111111111111")
        # print(response.text)
        # print(response.status)
        all_list_content = response.xpath("//div[@class='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 css-15j76c0']")
        # all_list_content = chrome.find_elements(By.XPATH, "//div[@class='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 css-15j76c0']")
        print("==============================================22222222222222222222222")
        print(all_list_content)
        dict_element = {}
        dict_element['url'] = response.url

        for cont_item in all_list_content:

            print("333333333333333333333333333333333333333333333333333333333333333333333333333")
            # print(cont_item.extract())
            title = cont_item.xpath(".//p[@class='MuiTypography-root MuiTypography-body1 jss78 jss79 css-okbma4']/text()").extract_first()

            if title is None:
                print("===================title is None===========================")
                continue
            else:
                title = title.strip()

            print("==============================================" + title+"===")
            if title == 'Tractability' :

                print("yyyyyy"*20)

                # list div
                tlist = []  # n column
                part_list = cont_item.xpath(".//div[@class='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-6 MuiGrid-grid-sm-3 css-3zx7e6']")
                for part in part_list:
                    print("66666"*20)
                    print(part.extract())

                    tdict = {} # key:list
                    key = part.xpath("./h6/text()").extract_first()  #Small molecule
                    print("=key:===={}====".format(key))
                    values = []
                    zlist = part.xpath(".//div[@title]")
                    for z in zlist:
                        text = z.xpath("./text()").extract_first()
                        if text is not None:
                            values.append(text.replace("\r\n", "").replace("\u3000", "").strip())
                    print(values)
                    tdict[key] = values
                    tlist.append(tdict)

                dict_element['Tractability'] = tlist

            if title == 'Known Drugs' :

                print("kkkkkk"*20)

                # list div
                klist = []  # n column
                part_list = cont_item.xpath(".//div[@class='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-6 MuiGrid-grid-sm-3 css-3zx7e6']")
                for part in part_list:
                    print("66666"*20)
                    print(part.extract())

                    tdict = {} # key:list
                    key = part.xpath("./h6/text()").extract_first()  #Small molecule
                    print("=key:===={}====".format(key))
                    values = []
                    zlist = part.xpath(".//div[@title]")
                    for z in zlist:
                        text = z.xpath("./text()").extract_first()
                        if text is not None:
                            values.append(text.replace("\r\n", "").replace("\u3000", "").strip())
                    print(values)
                    tdict[key] = values
                    klist.append(tdict)

                dict_element['Known Drugs'] = klist

        if len(dict_element) > 0:
            json_string = json.dumps(dict_element)
            #json_string = json.dumps(out_list, indent=4)

            # 写入到文件中
            with open('D:\\pachong\\pachong\\output.json', 'a') as json_file:
                json_file.write(json_string + ",\n")
```

## 6、修改middlewares.py

```
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
import time

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class PachongSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class PachongDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # 当下载器中间件开始工作时，自动打开一个浏览器
    def __init__(self):
        self.driver = webdriver.Chrome()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        # 下面这一行需要手动添加，作用是调用关闭浏览器的函数
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        self.driver.get(request.url) # 使用浏览器打开请求的URL
        time.sleep(3)
        body = self.driver.page_source # 获取网页HTML源码
        return HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8', request=request)

        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    def spider_closed(self, spider):
        self.driver.close()
        spider.logger.info("Spider closed: %s" % spider.name)
```


## 7、pipelines.py

```
from itemadapter import ItemAdapter


class PachongPipeline:
    def process_item(self, item, spider):
        return item

    def _handle_error(self, failue, item, spider):
        print(failue)
```



## 8、运行scrapy
cmd命令下进入pachong项目目录后执行：

>scrapy crawl medicine
