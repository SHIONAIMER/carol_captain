import requests
import time
import re
import json
import csv

Headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 52.0 .2743 .116 Safari / 537.36 '}

start_url = 'https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid=22634198&page=1&ruid=351609538&page_size=30'
root_uel = 'https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList'

params = {
    'roomid': 22634198,
    'page': 1,
    'ruid': 351609538,
    'page_size': 30
}

def get_info():
    html = requests.get(start_url, headers=Headers)
    info = json.loads(html.content)["data"]["info"]
    return info["page"]

def get_all_captain(page_num):
    csvfile = open('captains.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['uid', 'ruid', 'rank', 'username', 'face', 'is_alive', 'guard_level', 'guard_sub_level'])
    for i in range(1, page_num+1):
        params['page'] = i
        html = requests.get(root_uel, headers=Headers, params=params)
        if i == 1:
            top3 = json.loads(html.content)["data"]["top3"]
            for captain in top3:
                captain_info = json2list(captain)
                writer.writerow(captain_info)
        captain_list = json.loads(html.content)["data"]["list"]
        for captain in captain_list:
            captain_info = json2list(captain)
            writer.writerow(captain_info)
    csvfile.close()

def json2list(captain):
    captain_info = list(captain.values())[0:8]
    #print(captain_info)
    return captain_info

if __name__ == '__main__':
    page_num = get_info()
    get_all_captain(page_num)