#!/usr/bin/python
# -*- coding: utf-8 -*- #
import requests,sys,re
import MySQLdb
import mysql

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

mysql=mysql.Mysql()


print '正在从活动家抓取数据......'
headers = {'content-type': 'application/json',
           'Host': 'www.huodongjia.com',
           'Referer': 'https://www.huodongjia.com/it/',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        }
for page in range(150):
    # url='https://www.huodongjia.com/beijing/it/page-9'
    url='https://www.huodongjia.com/beijing/it/page-'+str(page+1)+'/'
    print '---------------------------正在爬取第'+str(page+1)+'页......--------------------------------'
    html=requests.get(url,headers=headers)
    html.raise_for_status()
    try:
        soup=BeautifulSoup(html.text,'lxml')
        #[s.extract() for s in soup('div')]
        #print soup.h3.a
        #title=str(soup.h3.a.string) # 利用正则表达式需要将网页文本转换成字符串
        #title=re.compile(r'<h3>(.*)</h3>')
        #names=re.findall(title,soup)
        #print title
        event_lists=soup.select('.eventList')
        href=soup.select('.eventList h3 a')
        # titles=soup.select('.eventList h3 a')
        # tags=soup.select('.meeting_tag')
        # addresses=soup.select('.address')
        # prices=soup.select('.pc')
        # times=soup.find(re.compile(""))
        for i in range(12):
            if(event_lists[i].get_text().split('\n')[11]!=''):
                data = {
                    #'event_id':href[i].get('href'),
                    'event_id':re.findall(r'\d+',href[i].get('href'))[0],
                    'title':event_lists[i].get_text().split('\n')[6].strip('u\''),
                    'tag':event_lists[i].get_text().split('\n')[7],
                    'address':event_lists[i].get_text().split('\n')[9],
                    'price':event_lists[i].get_text().split('\n')[11],
                    'time':event_lists[i].get_text().split('\n')[14],
                    'heat':event_lists[i].get_text().split('\n')[15],
                    'link':'https://www.huodongjia.com'+href[i].get('href')
                }
            elif(event_lists[i].get_text().split('\n')[10]=='已结束'):
                 data = {
                    #'event_id':href[i].get('href'),
                    'event_id':re.findall(r'\d+',href[i].get('href'))[0],
                    'title':event_lists[i].get_text().split('\n')[6].strip('u\''),
                    'tag':event_lists[i].get_text().split('\n')[7],
                    'address':event_lists[i].get_text().split('\n')[9],
                    'price':'已结束',
                    'time':event_lists[i].get_text().split('\n')[13],
                    'heat':event_lists[i].get_text().split('\n')[14],
                    'link':'https://www.huodongjia.com'+href[i].get('href')
                }
            else:
                data = {
                    #'event_id':href[i].get('href'),
                    'event_id':re.findall(r'\d+',href[i].get('href'))[0],
                    'title':event_lists[i].get_text().split('\n')[6].strip('u\''),
                    'tag':event_lists[i].get_text().split('\n')[7],
                    'address':event_lists[i].get_text().split('\n')[9],
                    'price':'',
                    'time':event_lists[i].get_text().split('\n')[12],
                    'heat':event_lists[i].get_text().split('\n')[13],
                    'link':'https://www.huodongjia.com'+href[i].get('href')
                }
            mysql.insertData('spider',data)
            # print title.get_text()
            # print data
            # print data['time']== ''

    except Exception as e:
        print e
    print '第'+str(page+1)+'页 complete'
print '爬取完毕！'




# if __name__=='__main__':
#     InsertData('spider',data)