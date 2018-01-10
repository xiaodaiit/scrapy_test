# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import json
try:
    import urlparse as parse
except:
    from urllib import parse

from scrapy.loader import  ItemLoader
from ArticleSpider.items  import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    # start_urls = ['https://www.zhihu.com/question/264209353/answer/281911676']
    #question的第一页的answers
    #start_answer = 'https://www.zhihu.com/api/v4/questions/60820895/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=3&offset=3'
    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}'
    header = {
        "HOST" : "www.zhihu.com",
        "Rrferer":"https://www.zhihu.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
    }

    custom_settings = { #自定义设置
        "COOKIES_ENAGLED":True
    }

    def parse(self, response):
        """
        提取出html页面中的所有url 并跟踪这些url进行下一步爬取
        如果提取的url格式是/question/xxx那就下载后直接进入解析函数
        :param response:
        :return:
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x:True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com.question/(\d+))(/|$).*", url)
            if match_obj:
                #如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.header,callback=self.parse_question)
            else:
                pass
                #如果不是question页面则直接进一步跟踪
               # yield scrapy.Request(url, headers=self.header, callback=self.parse)


    def parse_question(self,response):
        #处理question页面 从页面中提取具体question item
        if "QuestionHeader-title" in response.text:
            #处理新版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*",response.url)
            if match_obj:
                question_id = int(match_obj.group(2))
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", "div.QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("comments_num", "div.QuestionHeader-actions button::text")
            item_loader.add_css("answer_num", "h4.List-headerText span::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::text")
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")

            question_item = item_loader.load_item()
        else:
            #处理老版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))
            t = 0
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
           # item_loader.add_xpath("title", "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            # item_loader.add_xpath("watch_user_num", "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
     #       item_loader.add_value("watch_user_num", t)
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()
        yield question_item
        # yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers==self.header, callback=self.parse_answer)
       # yield scrapy.Request(self.start_answer_url.format(question_id, 20 ,0), headers=self.header, callback=self.parse_answer)
       # yield question_item



    def parse_answer(self, response):
        #处理question的answer
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        #提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item['zhihu_id'] = answer['id']
            answer_item['url'] = answer['url']
            answer_item['question_id'] = answer['question']['id']
            answer_item['author_id'] = answer['author']['id'] if "id" in answer['author'] else None
            answer_item['content'] = answer['content'] if "content" in answer else None
            answer_item['parise_num'] = answer['voteup_count']
            answer_item['comments_num'] = answer['comment_count']
            answer_item['create_time'] = answer['created_time']
            answer_item['update_time'] = answer['updated_time']
            answer_item['crawl_time'] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.header, callback=self.parse_answer)

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#sigin', headers=self.header,
                               cookies={
                                   '_zap':'a8d4039c-ea44-4168-a640-6bca63430f72',
                                   'd_c0':'AJBAjW1HNwqPTloDehA6xV9QqC28cAjWbDE=|1468288403',
                                   '_za' :'93866b57-56d6-465e-b3a7-a05f987e53eb',
                                   '_ga' :'GA1.2.1739770305.1473390665',
                                   'q_c1' :'c9afad19909246deb723e7e468ecc9cc|1507512307000|1468288403000',
                                   'r_cap_id':'NDVlMDZiYjdiZjQxNGZjZjlkOTFiNmQzYWJkYTU4MGY=|1514190891|ef001f5e131e4e8565b4a7c67804685d54558a4d',
                                   'cap_id' :'YTE2MmQwYWE5NWM0NDZiODhiNjBiOTFmZWZiMjU5ZTc=|1514190891|aae7d573f64bf554337541dc85a811f296afa53f',
                                   'z_c0':'Mi4xQWhGNUFnQUFBQUFBa0VDTmJVYzNDaGNBQUFCaEFsVk5Pd1l1V3dCeTNCN0FfbEVxZER3NFVxY3JlS1l5WHlyM3dn|1514190907|47246a9fce7eaf97aa810a7de52ef96bbb4b6c5b',
                                   '__utma':'51854390.1739770305.1473390665.1513930442.1513930442.1',
                                   '__utmz':'51854390.1513930442.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
                                   '__utmv':'51854390.100--|2=registration_date=20160113=1^3=entry_date=20160113=1',
                                   'aliyungf_tc':'AQAAAHB2q3+EgQ0AIkgadgsa66qLiNt+',
                                   'l_cap_id':'YzU1YzMyY2NiY2IwNDhhNWIxZmY2OTQxNWVlYzAyZTU=|1514172693|cd89e4f68c83571cbf82bbfb4b2a777fab840e46',
                                   '_xsrf':'fad7977c-bb95-4d5b-8803-a5cc3f82fbab'
                               },
                               callback=self.parse)] #.login

    def login(self, response):
        response_text = response.text #.replace("\n","")
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL) #在DOTALL 模式下 匹配了换行符
        xsrf = ''
        if match_obj:
            xsrf = match_obj.group(1)

        if xsrf:
            post_url = 'https://www.zhihu.com/login/phone_num'
            post_data = {
                "_xsrf" : xsrf,
                "phone_num" : "",
                "password" : "",
                "captcha" : ""
            }

            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url, headers=self.header, meta={"post_data":post_data},
                                 callback=self.login_after_captcha)


    def login_after_captcha(self, response):
        with open('captcha.jpg', 'wb') as  f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass


        captcha = input("请输入验证码\n>")
        post_data = response.meta.get("post_data", {})
        post_url = "https://www.zhihu.com/login/phone_num"
        return [scrapy.FormRequest(
            url = post_url,
            formdata = post_data,
            headers = self.header,
            callback = self.check_login
        )]

    def check_login(self, response):
        #验证服务器返回的数据是否成功
        text_josn = json.loads(response.text)
        if "msg" in text_josn and text_josn["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.header)
        pass













