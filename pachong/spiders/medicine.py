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
            time.sleep(1)
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
            print(cont_item.extract())
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
                part_list = cont_item.xpath(".//p[@class='MuiTablePagination-displayedRows css-wkurnt']/text()").extract_first()
                if part_list is not None:
                    cols = part_list.replace("\u2013","-").strip()
                    dict_element['Known Drugs'] = cols

        if len(dict_element) > 0:
            json_string = json.dumps(dict_element)
            #json_string = json.dumps(out_list, indent=4)

            # 写入到文件中
            with open('D:\\pachong\\pachong\\output.json', 'a') as json_file:
                json_file.write(json_string + ",\n")
                json_file.flush()

        yield json_string
# https://platform.opentargets.org/target/ENSG00000143627
