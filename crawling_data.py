# need pip install: request bs4
import requests
import os
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
 

# 写入 CSV TODO: 完善
def write_to_excel(page, ball):
    f = open('双色球开奖结果.csv', 'a', encoding='utf_8_sig')
    f.write(f'第{page}期,{ball[0]},{ball[1]},{ball[2]},{ball[3]},{ball[4]},{ball[5]},{ball[6]}\n')
    f.close()


# 爬取类基类 
# param1 start_id: 0 为最新一期，依次类推
# param2 end_id:   0 为最新一期，依次类推
class Crawling(ABC):
    @abstractmethod
    def __init__(self, start_id, end_id):
        self.__start_id = start_id
        self.__end_id = end_id
        # self.__id_map = {}              # Key: id       Value: issue
        # self.__data_map = {}            # Key: issue    Value: num_list
        self.__id_map, self.__data_map = self._turn_page(begin=self.__start_id, end=self.__end_id)

    # 解析数据
    def _parsing_data(self, url, page):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        list = soup.select('div.ball_box01 ul li')
        ball = []
        for li in list:
            ball.append(li.string)

        int_ball_list = [int(x) for x in ball]

        return page, int_ball_list
    
    
    # 打开页面
    def _turn_page(self, begin, end):
        # url = "http://kaijiang.500.com/ssq.shtml"
        # url = "http://kaijiang.500.com/dlt.shtml"
        url = self._url
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        pageList = soup.select("div.iSelectList a")
    
        # 获取指定期的页码  0：最新一期 依次类推
        recent_pages = pageList[begin:end]
    
        data_map = {}   # 保存结果
        id_map = {}
        id_index = begin

        for p in recent_pages:
            url = p['href']
            page = p.string
            cur_id, value = self._parsing_data(url, page)
            data_map[cur_id] = value
            id_map[id_index] = cur_id
            id_index = id_index + 1

        return id_map, data_map


    def print_to_csv(self):
        # TODO
        print("TODO")

    def get_ball_num(self, id_index):
        if isinstance(id_index, int):
            issue = self.__id_map.get(id_index, None)
            return self.__data_map.get(issue, None), issue
        elif isinstance(id_index, str):
            return self.__data_map.get(id_index, None), id_index
        else:
            return None
 

# Ball 爬取类 
# param1 start_id: 0 为最新一期，依次类推
# param2 end_id:   0 为最新一期，依次类推
class BallCrawling(Crawling):
    def __init__(self, start_id, end_id):
        self._url = "http://kaijiang.500.com/ssq.shtml"
        super().__init__(start_id, end_id)


# Lotto 爬取类 
# param1 start_id: 0 为最新一期，依次类推
# param2 end_id:   0 为最新一期，依次类推
class LottoCrawling(Crawling):
    def __init__(self, start_id, end_id):
        self._url = "http://kaijiang.500.com/dlt.shtml"
        super().__init__(start_id, end_id)
        


if __name__ == '__main__':
    pobj = BallCrawling(0, 10)
    temp = pobj.get_ball_num(0)
    print(temp)
    pobj2 = LottoCrawling(0, 10)
    temp = pobj2.get_ball_num(0)
    print(temp)