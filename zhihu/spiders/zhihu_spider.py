#coding="utf-8"
import  re
import json


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from zhihu.items import *
from zhihu.misc.log import *
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


###URL2_ARTICLE_TITLE = {}

#z_c0 _xsrf is key cookie 
class zhihuSpider(CrawlSpider):

    MAX_PARSE_PEOPLE_NUM = 100

    BASE = "https://www.zhihu.com"

    headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            'Cookie':'_za=4b956b4d-8cff-4792-9234-8664705d39e1; _ga=GA1.2.1587300214.1426873059; _xsrf=690df446d818f5d6d886c86f82537a1f; aliyungf_tc=AQAAAKT8JBPTLAgALH0lO5dy2VapF2sS; q_c1=227156c6a82e4ee498033e4a8028c03f|1453865718000|1422968419000; cap_id="Y2NlNjAxZjBhN2YwNGE3Y2I5ZDk1Zjg3ZDk3NTZlOTA=|1453875846|7a462792d1fb18e72f11536e7e9640703dcb7be8"; z_c0="QUFDQU8tWXFBQUFYQUFBQVlRSlZUWlh2ejFaVWJ2eW9lcTBuaElVRW41Yk9peVEwUExDUHpnPT0=|1453875861|2d91185bc590aa519ca004ba93d5f1966fcfd34c"; n_c=1; __utmt=1; __utma=51854390.1587300214.1426873059.1453865721.1453875863.2; __utmb=51854390.11.9.1453875867872; __utmc=51854390; __utmz=51854390.1453875863.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/du-gu-chui-xue/collections; __utmv=51854390.100-1|2=registration_date=20140405=1^3=entry_date=20140405=1',
            "DNT":'1',
            "Host":"www.zhihu.com",
            "Refer":"https://www.zhihu.com/people/du-gu-chui-xue",
            "Upgrade-Insecure-Requests":'1',
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
            }

    cookies = {
            "_ga": "GA1.2.1587300214.1426873059",
            "_xsrf":"690df446d818f5d6d886c86f82537a1f",
            "_za":"4b956b4d-8cff-4792-9234-8664705d39e1",
            "aliyungf_tc":"AQAAAKT8JBPTLAgALH0lO5dy2VapF2sS",
            "cap_id":"Y2NlNjAxZjBhN2YwNGE3Y2I5ZDk1Zjg3ZDk3NTZlOTA=|1453875846|7a462792d1fb18e72f11536e7e9640703dcb7be8",
            "z_c0":"QUFDQU8tWXFBQUFYQUFBQVlRSlZUWlh2ejFaVWJ2eW9lcTBuaElVRW41Yk9peVEwUExDUHpnPT0=|1453875861|2d91185bc590aa519ca004ba93d5f1966fcfd34c",
            "q_c1":"227156c6a82e4ee498033e4a8028c03f|1451206156000|1422968419000"
            }

    follow_cookies = {
            "_ga": "GA1.2.1587300214.1426873059",
            "_xsrf":"690df446d818f5d6d886c86f82537a1f",
            "_za":"4b956b4d-8cff-4792-9234-8664705d39e1",
            "aliyungf_tc":"AQAAAKT8JBPTLAgALH0lO5dy2VapF2sS",
            "cap_id":"Y2NlNjAxZjBhN2YwNGE3Y2I5ZDk1Zjg3ZDk3NTZlOTA=|1453875846|7a462792d1fb18e72f11536e7e9640703dcb7be8",
            "z_c0":"QUFDQU8tWXFBQUFYQUFBQVlRSlZUWlh2ejFaVWJ2eW9lcTBuaElVRW41Yk9peVEwUExDUHpnPT0=|1453875861|2d91185bc590aa519ca004ba93d5f1966fcfd34c",
            "q_c1":"227156c6a82e4ee498033e4a8028c03f|1451206156000|1422968419000"
            }

    follow_header = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
            "Cache-Control":"max-age=0",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            'Cookie':'_za=4b956b4d-8cff-4792-9234-8664705d39e1; _ga=GA1.2.1587300214.1426873059; _xsrf=690df446d818f5d6d886c86f82537a1f; aliyungf_tc=AQAAAKT8JBPTLAgALH0lO5dy2VapF2sS; q_c1=227156c6a82e4ee498033e4a8028c03f|1453865718000|1422968419000; cap_id="Y2NlNjAxZjBhN2YwNGE3Y2I5ZDk1Zjg3ZDk3NTZlOTA=|1453875846|7a462792d1fb18e72f11536e7e9640703dcb7be8"; z_c0="QUFDQU8tWXFBQUFYQUFBQVlRSlZUWlh2ejFaVWJ2eW9lcTBuaElVRW41Yk9peVEwUExDUHpnPT0=|1453875861|2d91185bc590aa519ca004ba93d5f1966fcfd34c"; n_c=1; __utmt=1; __utma=51854390.1587300214.1426873059.1453865721.1453875863.2; __utmb=51854390.11.9.1453875867872; __utmc=51854390; __utmz=51854390.1453875863.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/du-gu-chui-xue/collections; __utmv=51854390.100-1|2=registration_date=20140405=1^3=entry_date=20140405=1',
            "DNT":'1',
            "Host":"www.zhihu.com",
            "Origin":"https://www.zhihu.com",
            "Referer":"https://www.zhihu.com/people/du-gu-chui-xue/followees",
            "User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
            "X-Requested-With":'XMLHttpRequest'
            }


    BASE_POPLE = "https://www.zhihu.com/people/"
    COLLECTION = "collections"
    name = "zhihu" #here is the key to name spider,if not match will throw spider not found error
    allowed_domains = ["zhihu.com"]
    start_urls = [
            #"https://www.zhihu.com/collection/39830435",
            "https://www.zhihu.com/people/du-gu-chui-xue/followees",
            "https://www.zhihu.com/node/ProfileFolloweesListV2",
            #"https://www.zhihu.com/collection/78718117"
            #program zhuan lan
    ]
    rules = [
        Rule(sle(allow=("/followees")), follow=True, callback='parse_follow'),
        Rule(sle(allow=("/collections")), follow=True, callback='parse_collection'),
    ]


    max_page_limit = 10
    
    follow_post_data = {
            "method":"next",
            "params": '{"offset":20,"order_by":"created","hash_id":"12170bbbc2d78484741daccc5fd6bc09"}',
            "_xsrf":"690df446d818f5d6d886c86f82537a1f"
            }

    people_id_set = set()
    answer_dict = dict()



    def __init__(self):
        info('init start')
        return

    def start_requests(self): 
        info("start url:"+ self.start_urls[0])
        yield  scrapy.Request(url=self.start_urls[0],callback=self.parse_follow, headers=self.headers,cookies=self.cookies);
        #yield  scrapy.Request(url=self.start_urls[0],callback=self.parse_collection_list, headers=self.headers,cookies=self.cookies);


    def constructNextPeopleCollection(self, people_id):
        url = BASE_PEOPLE + people_id + COLLECTION; 
        return url


    def parse_follow_id(self, id_url):
        id_url = id_url[1:]
        str_list = id_url.split("/");
        return str_list[1]


    #def get_collection(self, people_id):
        #https://www.zhihu.com/people/du-gu-chui-xue/collections


    def parse_collection_dir(self,response):
        info("collection rsp url:"+ response.url);
        selectorList = response.xpath("//a[@class='zm-profile-fav-item-title']/@href")
        for   selector in selectorList:
            #/collection/id
            hrefStr = selector.extract()
            info("fav dir:"+ hrefStr)
            collection_dir = self.BASE + hrefStr; 
            yield  scrapy.Request(url=collection_dir,callback=self.parse_collection_list, headers=self.headers,cookies=self.cookies);



    def is_answer_in_dict(self, url):
        if self.answer_dict.has_key(url):
            self.answer_dict[url] += 1
            return True
        else:
            self.answer_dict[url] = 1
            return False

    #collection list get detail answer url
    def parse_collection_list(self,response):
       info("parse collection list:"+response.url)
       selector_list = response.xpath("//a[@class='toggle-expand']/@href");
       for selector in selector_list:
           answer_url = self.BASE + str(selector.extract()) 
           info("answer url:"+ answer_url)
           if (False == self.is_answer_in_dict(answer_url)):
                yield  scrapy.Request(url=answer_url,callback=self.parse_answer_detail, headers=self.headers,cookies=self.cookies);

    def parse_answer_detail(self, response):
       answer_url = response.url
       answer = response.xpath("//h2[@class='zm-item-title zm-editable-content']/a/text()").extract()
       info("answer url:"+ answer_url )
       info("answer :"+ answer[0].decode() )
       meta = Answer()
       meta['title'] = answer[0].decode()
       meta['url'] = answer_url 
       return meta




    def is_people_in_set(self, people_id):
        if people_id in self.people_id_set: 
            return True
        if(len(self.people_id_set) <= self.MAX_PARSE_PEOPLE_NUM ):
            self.people_id_set.add(people_id)
            return False
        #exceed max craw limit
        return True    


    def parse_follow(self, response):
        info("follow url:"+response.url)
        base_url = get_base_url(response)
        selectorList = response.xpath("//a[@class='zm-item-link-avatar']/@href")
        for   selector in selectorList:
            #/people/people_id
            hrefStr = selector.extract()
            # del first '/' and split by '/'
            people_id = self.parse_follow_id(hrefStr)
            info("follow url info:" + people_id);
            collection_url = "https://www.zhihu.com/people/"+ people_id + "/collections"
            info("collection url:" + collection_url)
            yield  scrapy.Request(url=collection_url,callback=self.parse_collection_dir, headers=self.headers,cookies=self.cookies);

        yield  scrapy.FormRequest(url=self.start_urls[1],callback=self.parse_followlist, cookies=self.follow_cookies,formdata=self.follow_post_data,headers=self.follow_header);
            #hrefList = hrefStr.split("people")
            #yield  scrapy.Request(href,self.parse_article_list)


    def clear_follow_data(self, data):
        data = data.strip("[")
        data = data.strip("]")
        data = data.replace("\\","");
        return data

    def parse_followlist(self, response):
        info("followlist url  :"+response.url + "-------> body len: " + str(len(response.body)));
        msg_dict = json.loads(response.body); 
        follow_data = str(msg_dict["msg"]);
        rsp_follow = self.clear_follow_data(follow_data)
        #info("follow :" + rsp_follow) 
        #info("body:"+response.body)
        selectorList = Selector(text=rsp_follow).xpath("//a[@class='zg-link-gray-normal']/@href")
        for   selector in selectorList:
            #/people/people_id
            hrefStr = selector.extract()
            # del first '/' and split by '/'
            people_id = self.parse_follow_id(hrefStr)
            info("follow Next  method id :" + people_id);
            if (False == self.is_people_in_set(people_id)):
                followlist = "https://www.zhihu.com/people/" + people_id + "/followees"
                yield  scrapy.FormRequest(url=followlist,callback=self.parse_followlist, cookies=self.follow_cookies,formdata=self.follow_post_data,headers=self.follow_header);
                collection_url = "https://www.zhihu.com/people/"+ people_id + "/collections"
                info("collection url:" + collection_url)
                yield  scrapy.Request(url=collection_url,callback=self.parse_collection_dir, headers=self.headers,cookies=self.cookies);
            else:
                info("duplicate or exceed people_id:" + people_id )


    #def parse_article_list(self, response):
    #    global URL2_ARTICLE_TITLE
    #    info("parse article list  url:"+response.url)
    #    base_url = get_base_url(response)
    #    selectorList = response.xpath("//h4/a[contains(@href,'p')]")
    #    for selector in selectorList:
    #        hrefStr = selector.extract()
    #        hrefList = hrefStr.split("\"") 
    #        href = base_url + hrefList[1]
    #        info("article href:"+href)
    #        name = self.extractContentFromAElement(hrefList[4])
    #        name = name.encode("utf-8")
            ###URL2_ARTICLE_TITLE[href] = name
    #        yield  scrapy.Request(href,self.parse_article)



    #def parse_article(self, response):
      #  article = Article()
      #  url = response.url
      #  title = response.xpath("//h1[@class='title']/text()").extract()
      #  article['title'] = title[0].encode("utf-8")
      #  info("article name:"+ article['title'] )
      #  article['content']  = response.body
      #  article["url"]  = response.url
      #  return article

    def _process_request(self, request):
        info('process ' + str(request))
        return request

