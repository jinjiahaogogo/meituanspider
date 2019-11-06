import re
import requests
import json
import requests


class Meitaunspider:
    def __init__(self):
        self.baseurl = 'https://sh.meituan.com/meishi/pn'
        self.page = 0
        self.cookies = {'_lxsdk_cuid':'16e3a900889c8-05618340f672a5-b363e65-1fa400-16e3a900889c8',
                        '_lx_utm':'utm_source%3DBaidu%26utm_medium%3Dorganic',
                        '_hc.v':'87a2e071-091b-fe44-8e61-7a168720d970.1572940987',
                        'client-id':'7d3bfd7a-f0dc-4c04-aea5-e982867a9fab; ci=10',
                        'rvct':'10%2C151',
                        '__mta':'46035739.1572940772912.1572947541536.1572947556635.3',
                        '_lxsdk':'16e3a900889c8-05618340f672a5-b363e65-1fa400-16e3a900889c8',
                        'uuid':'846c0379-a1b8-46b5-b7ff-5dec1504a3b3',
                        '_lxsdk_s':'16e3fbad7c6-8ef-29-e52%7C%7C3'
                        }
        self.headers = {
                "Host": "sh.meituan.com",
                'Connection': 'keep-alive',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9'
                }
        self.PROXY_POOL_URL = 'http://127.0.0.1:5555/random'
        self.db = pymysql.connect("localhost","root","123456",charset="utf8")
        self.cursor = self.db.cursor()


    def get_proxy(self):
        """
        从代理池获取代理
        :return:
        """
        try:
            response = requests.get(self.PROXY_POOL_URL)
            if response.status_code == 200:
                print('Get Proxy', response.text)
                return response.text
            return None
        except:
            return None


    def loadPage(self,url):

        res = requests.get(url=url, headers=self.headers, timeout=30, cookies=self.cookies,proxies = self.proxies).text
        res.encoding = "utf-8"
        html = res.text
        self.parsePage(html)


    def parsePage(self,html):
        json_data = json.loads(re.findall('window._appState = (.*?);</script>',html)[0])
        totalCounts=int(json_data['poiLists']['totalCounts'])
        pageObjects=len(json_data['poiLists']['poiInfos'])
        print(totalCounts,pageObjects)
        r_list = list()
        for k in json_data['poiLists']['poiInfos']:
            shopL = list()
            print(i,'店铺',k['title'],',得分:',k['avgScore'],',评论数:',k['allCommentNum'],',地址:',k['address'])
            shopL.append(k['title'])
            shopL.append(k['avgScore'])
            shopL.append(k['allCommentNum'])
            shopL.append(k['address'])
            r_list.append(shopL)
        print("页面解析完成,正在存入数据库...")
        self.writeTomysql(r_list)


    def writeTomysql(self,r_list):
        '''
            将数据存入mysql
            自动构成数据库
        '''
        c_db = "create database if not exists Meituandb \
                character set utf8"
        u_db = "use Meituandb"
        c_tab = "create table if not exists shop( \
                 id int primary key auto_increment,\
                 title varchar(50), \
                 avgScore int, \
                 allCommentNum int, \
                 address varchar(50))charset=utf8"
        warnings.filterwarnings("ignore")
        try:
            self.cursor.execute(c_db)
            self.cursor.execute(u_db)
            self.cursor.execute(c_tab)
        except Warning:
            pass
        ins = "insert into housePrice(title,avgScore,allCommentNum,address) \
               values(%s,%s,%s,%s)"
        for r_tuple in r_list:
            title = r_tuple[0].strip()
            avgScore = int(r_tuple[1].strip())
            allCommentNum = int(r_tuple[2].strip())
            address = r_tuple[3].strip()
            L = [title,avgScore,allCommentNum,address]
            self.cursor.execute(ins,L)
            self.db.commit()
        print("存入数据库成功")


    def work_On(self):
        '''
        启动爬虫程序
        获取代理
        构成url
        '''
        while True:
            c = input("爬取请按y(y/n):")
            if c.strip().lower() == "y":
                self.offset = self.page + 1
                if self.offset == 60:
                    print('爬取完成')
                    break
                url = self.baseurl + str(self.offset) +'/'
                proxy = self.get_proxy()
                if proxy:
                    self.proxies = {'https':'https://' + proxy}
                self.loadPage(url)
                self.page += 1
            else:
                print("爬取结束,谢谢使用!")
                break


if __name__ == '__main__':
    meituan = Meitaunspider()
    meituan.work_On()
   


# ip被封,高匿代理仍然会存在这个问题,还是建议哈斯用付费的
# requests.exceptions.ConnectionError: 
# HTTPSConnectionPool(host='sh.meituan.com', port=443):
# Max retries exceeded with url: /meishi/pn1/ (Caused by ProxyError
#    ('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response',)))

        
        
        
        
        
        