# -*- coding: utf-8 -*-
#coding=utf-8
from DBTool import DB
from bs4 import BeautifulSoup as bs
from CommonFunc import urlHelper
from CommonFunc import bsHelper
from CommonFunc import function

class Spider(object):
    url = 'http://app.xueui.cn/category/start/page/1'
    imgArr = list()
    def getUIPic(self):
        soup=bs(urlHelper.urlOpen(self.url),"html.parser")
        div=soup.find('div',{"id":"post-area"})
        divs=bsHelper.findAllTagWithName('div',div)
        for item in divs:
            if 'status-publish' in item['class']:
                dic={}
                imgDiv=bsHelper.findClass('gridly-image',item)
                dic['imgUrl']=imgDiv.a['href']
                img=imgDiv.a.img
                dic['image']=img['src']
                textDiv=bsHelper.findClass('gridly-copy',item)
                dic['infor']=textDiv.get_text()
                self.imgArr.append(dic)
                temp= self.url.split('/')
                dic['category']=temp[-3]
                print dic
        currentPage=soup.find('span',{"class":"current"})
        if currentPage:
            next =currentPage.next_sibling
            if next  and bsHelper.isTag(next):
                self.url=next['href']
                self.getUIPic()


if __name__ == '__main__':
    db=DB(host='60.***.***.86',user='mac',passwd='ACrpbJHZYsyjAAce',db='uipic',charset='utf8')
    urls=['http://app.xueui.cn/category/download/page/1'
         ,'http://app.xueui.cn/category/details-page/page/1','http://app.xueui.cn/category/feedback/page/1','http://app.xueui.cn/category/settings/page/1','http://app.xueui.cn/category/data/page/1'
         ,'http://app.xueui.cn/category/about/page/1','http://app.xueui.cn/category/other/page/1']
    spider = Spider()
    for url in urls:
        spider.url=url
        spider.imgArr=list()
        spider.getUIPic()
        db.inserData(spider.imgArr,'pic_list','imgUrl')




