# -*- coding: utf-8 -*-
#coding=utf-8
from DBTool import DB
from bs4 import BeautifulSoup as bs
from CommonFunc import urlHelper
from CommonFunc import bsHelper
from CommonFunc import function

class picSpider(object):
    url='http://www.mmjpg.com/home/1'
    imgArr=list()
    # http://www.mmjpg.com/  妹纸图片 type=1
    def get_mmjpg(self):
        soup=bs(urlHelper.urlOpen(self.url),"html.parser")
        div=soup.find('div',{"class":"pic"})
        ul=div.ul
        for li in bsHelper.findAllTagWithName('li',ul):
            dic={}
            dic['picId']=li.a['href']
            img=li.a.img
            dic['image']=img['src']
            dic['title']=img['alt']
            dic['releaseTime']=li.span.next_sibling.get_text()
            dic['type']='1'
            self.imgArr.append(dic)
        totalPage=soup.find('em',{"class":"info"})
        temp=totalPage.get_text()
        page=int(temp[1:-1])
        currantPage=int(self.url.split('/')[-1])
        if currantPage<page:
            tempArr=self.url.split('/')
            tempArr.pop(-1)
            self.url='/'.join(tempArr)+'/'+str(currantPage+1)
            self.get_mmjpg()
        else:
            print '   爬虫结束   总共获取 '+ str(len(self.imgArr))+'条数据!'
            spider.imgArr.reverse()
            function.prettyArr(self.imgArr)
    def get_mmjpg_detail(self):
        detailImgs=list()
        for dic in self.imgArr:
            self.url=dic['picId']
            imgs=list()
            dataDic={}
            while 1:
                soup = bs(urlHelper.urlOpen(self.url), "html.parser")
                img=soup.find('div',{"id":"content"}).img
                imgs.append(img['src'])
                page_a =soup.find('a',{"class":"ch next"})
                if page_a and '张' in page_a.get_text():
                    self.url='http://www.mmjpg.com'+page_a['href']
                else: break
            dataDic['images']=','.join(imgs)
            dataDic['type']=dic['type']
            dataDic['title']=dic['title']
            dataDic['picId']=dic['picId']
            detailImgs.append(dataDic)
        return detailImgs
    # 2.5 韩日精选 http://www.77tuba.com/1020/list_1308_1.shtml 1020  http://www.77tuba.com
    #
    # http://www.rentifang.net/0004/ type  2.1 国模私拍 2.2 嫩模私拍 2.3 头条女神 2.4欧西美女 2.5 韩日精选 2.6pans写真 2.7韩国风俗娘
    # image.tv 2.8  美媛馆 2.9 尤果网 2.10 嫩模美腿 2.11
    def get_rentifang(self):
        soup=bs(urlHelper.urlOpen(self.url),"html.parser",from_encoding='gbk')
        tds=soup.find_all('td',{"bgcolor":"#FFFFFF"})
        for td in tds:
            if '1020' in td.a['href']:
                dic={}
                dic['picId']='http://www.77tuba.com'+td.a['href']
                img=td.a.img
                dic['image']='http://www.77tuba.com'+img['src']
                a_tags=soup.find_all('a',{"href":td.a['href']})
                a=a_tags[-1]
                dic['title']=a.get_text()
                dic['type']='2.5'


                self.imgArr.append(dic)
        uls=soup.find('ul',{"class":"page"})
        for a in bsHelper.findAllTagWithName('a',uls):

            if '下一页' in  a.get_text():
                tempArr=self.url.split('/')
                tempArr.pop(-1)
                self.url='/'.join(tempArr)+'/'+a['href']
                # self.get_rentifang()
                break
    # type 2.1 国模私拍
    def get_rentifang_detail(self):
        detailImgs = list()
        for dic in self.imgArr:
            print '第' +str(self.imgArr.index(dic))+'次' +'共  '+str(len(self.imgArr))
            self.url = dic['picId']
            imgs = list()
            dataDic = {}
            while 1:
                try:
                    soup = bs(urlHelper.urlOpen(self.url), "html.parser")
                except:break
                tds=soup.find_all('td',{"valign":"top"})
                for td in tds:
                    if td.img:
                        img=td.img

                        if('http://' not in img['src']):
                            if '.com' in self.url:
                                url=self.url.split('.com').pop(0)
                                url+='.com'
                            elif '.net' in self.url:
                                url = self.url.split('.net').pop(0)
                                url += '.net'
                            imgs.append(url+img['src'])

                        else:
                            imgs.append(img['src'])
                        print imgs[-1];

                ul=soup.find('ul',{"class":"image"})
                con = False
                for a in bsHelper.findAllTagWithName('a',ul):
                    if a.get_text().strip()=='下一页':
                        tempArr=self.url.split('/')
                        tempArr.pop(-1)
                        con=True
                        self.url = '/'.join(tempArr)+'/' + a['href']

                if con:print
                else:break
            dataDic['images'] = ','.join(imgs)
            dataDic['type'] = dic['type']
            dataDic['title'] = dic['title']
            dataDic['picId'] = dic['picId']
            detailImgs.append(dataDic)
        print '获取完成  共'+str(len(detailImgs))+'条'
        return detailImgs
    # http://www.88rt.org/index1.html  type=3
    def get_88rt(self):
        soup = bs(urlHelper.urlOpen(self.url), "html.parser",from_encoding='gbk')
        divs = soup.find_all('div', {"class": "imgholder"})
        for div in divs:
            dic={}
            dic['picId']='http://www.88rt.org/'+div.a['href']
            dic['title']=div.a['title']
            dic['image']=div.a.img['src']
            dic['type']='3'
            # par=div.parent
            # p=par.p
            # tempStr=p.get_text()
            # tempStr=tempStr.split('共').pop(-1)
            # total=tempStr[0:-2]
            # dic['releaseTime']=total
            # print dic
            self.imgArr.append(dic)

        page_div = soup.find('div', {"class": "pagelist"})
        for a in bsHelper.findAllTagWithName('a', page_div):

            if '下一页' in a.get_text():
                tempArr = self.url.split('/')
                tempArr.pop(-1)
                self.url = '/'.join(tempArr) + '/' + a['href']
                self.get_88rt()
                break
    def get_88rt_detail(self):
        detailImgs = list()
        for dic in self.imgArr:
            print '第' + str(self.imgArr.index(dic)) + '次' + '共  ' + str(len(self.imgArr))
            self.url = dic['picId']
            imgs = list()
            dataDic = {}
            while 1:
                try:
                    soup = bs(urlHelper.urlOpen(self.url), "html.parser",from_encoding='gbk')
                except:
                    break
                div = soup.find('div', {"id": "content"})
                img=div.a.img
                print img['src'];
                imgs.append(img['src'])

                tempStr=img['src'].split('/').pop(-1)
                try:
                    currentIndex=int(tempStr[0:-4])
                except:break

                div=soup.find('div',{"class":"wrapper photo-tit clearfix"})
                span=div.h3.span
                tempStr=span.get_text().strip()
                tempStr=tempStr.split('/')[-1]
                print span.get_text()
                total=int(tempStr[0:-1])
                while total>1:
                    currentIndex+=1
                    tempArr=img['src'].split('/')
                    tempArr.pop(-1)
                    image='/'.join(tempArr)+'/'+str(currentIndex)+'.jpg'
                    imgs.append(image)
                    total-=1
                break
            dataDic['images'] = ','.join(imgs)
            dataDic['type'] = dic['type']
            dataDic['title'] = dic['title']
            dataDic['picId'] = dic['picId']
            # print dataDic
            detailImgs.append(dataDic)
        print '获取完成  共' + str(len(detailImgs)) + '条'
        return detailImgs
    # 1 iphone7/6 plus  2  iphone7/6  3  inphoe5  4  iphone4
    # type  10.1  爱情 10.2 科技 10.3  体育  10.4 萌宠 10.5 帅哥
    def getTongbu_bizhi(self):
        soup = bs(urlHelper.urlOpen(self.url), "html.parser",from_encoding='gbk')
        imgs=soup.find_all('a',{"class":"img-bounced"})
        for img in imgs:
            dic={}
            dic['image']=img['href']
            dic['title']=img['data-tag']
            dic['picId']=img['href']
            dic['type']='10.11.2'
            self.imgArr.append(dic)
        a=soup.find('a',{"class":"paginate current"})
        a=a.next_sibling.next_sibling

        if a and a.name=='a':
            self.url=a['href']
            self.getTongbu_bizhi()













if __name__ == '__main__':
    spider=picSpider()
    # spider.url='http://www.mmjpg.com/home/1'
    # spider.get_mmjpg()
    db=DB(host='60.205.206.86',user='mac',passwd='fVTC4PMD7ubTzpzS',db='girlpic',charset='utf8')
    # db.inserData(spider.imgArr,'imgs_list','picId')
    # spider.imgArr=db.getData('imgs_list ',' where   type= 1 ')
    # spider.imgArr=spider.get_mmjpg_detail()
    # function.prettyArr(spider.imgArr)
    # db.inserData(spider.imgArr, 'detail_img', 'picId')

    # spider.url='http://www.77tuba.com/1020/list_1308_1.shtml'
    # spider.imgArr=list()
    # spider.get_rentifang()
    # db.inserData(spider.imgArr,'imgs_list','picId')

    # spider.imgArr=db.getData('imgs_list ',' where   type= \'2.5\' order by \'id\' ')
    # spider.imgArr=spider.imgArr[0:20];
    # arr = list();
    # for dic in spider.imgArr:
    #     print dic
    #
    #     # print temp
    #     if len(dic['images'])==0:
    #         arr.append(dic)
    # spider.imgArr=arr
    # print arr
    # spider.imgArr= spider.get_rentifang_detail()
    #
    # db.inserData(spider.imgArr,'detail_img', 'picId')
# http://www.88rt.org/index1.html
#     spider.url='http://www.88rt.org/index1.html'
#     spider.get_88rt()
#     db.inserData(spider.imgArr,'imgs_list','picId')
#     spider.imgArr=db.getData('imgs_list ',' where   type= 3 ')
#     spider.imgArr= spider.get_88rt_detail()
#     db.inserData(spider.imgArr, 'detail_img', 'picId')
    spider.url='http://app.tongbu.com/bizhi/iphone6-jingwu-all-hot-1'
    spider.getTongbu_bizhi()
    db.inserData(spider.imgArr,'imgs_list','picId')







