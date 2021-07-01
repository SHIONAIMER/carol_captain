import requests
import time
import re
import json
import csv
import numpy as np
from tqdm import tqdm

Headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    'Cookie': "_uuid=290736BA-0E81-1A66-B9BB-AEAA4916745B34637infoc; buvid3=62A0C7D6-CB27-4579-927A-B7CFCBC8D44218557infoc; buvid_fp=62A0C7D6-CB27-4579-927A-B7CFCBC8D44218557infoc; buvid_fp_plain=62A0C7D6-CB27-4579-927A-B7CFCBC8D44218557infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(mmRm~~lum0J'uYu~)R~Y~~; LIVE_BUVID=AUTO7116178886626057; CURRENT_QUALITY=116; finger=3f3919d0; bsource=search_baidu; _dfcaptcha=e36eafe512fea1f863215b7e28a278fa; fingerprint3=e0e885eaa331d8e565446fa4ff3433d3; bp_video_offset_165292524=542351651052169617; bp_t_offset_165292524=542399007365006460; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1625125841; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1624697128,1624938984,1625117116,1625125841; fingerprint=cf0569f8b694618e17cc69c85245639f; fingerprint_s=fa29720166971d2a5b391abe653d71a7; PVID=11; SESSDATA=e265fa9d,1640681313,0ceb4*71; bili_jct=2f701be94438063939b50d5d0b9da5bb; DedeUserID=1183234747; DedeUserID__ckMd5=516a50a0f1b640f1; sid=bznzbq9d"
}

root_url = 'https://api.bilibili.com/x/relation/same/followings'

params = {
    'vmid': 9902958
}

asoul = ["嘉然今天吃什么", "向晚大魔王", "贝拉kira", "乃琳Queen"]

csv_path = './captains.csv'

def uid_from_csv(path=csv_path):
    with open(path,'rt',encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        column = [row['uid'] for row in reader]
    return column

def get_samefollow(vmid):
    captain = np.zeros(6)
    captain[0] = vmid
    params['vmid'] = vmid
    html = requests.get(root_url, headers=Headers, params=params)
    if json.loads(html.content)["message"] == '0':
        captain[5] = 1
        samefollow = json.loads(html.content)["data"]["list"]
        for up in samefollow:
            name = up['uname']
            for i in range(4):
                if name == asoul[i]:
                    captain[i+1] = 1
                    break
        #print(captain)
        return captain
    else:
        #print(captain)
        return captain

def main():
    i = 0
    csvfile = open('follows.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['uid', '嘉然', '向晚', '贝拉', '乃琳', '关闭关注'])
    uids = uid_from_csv()
    for uid in tqdm(uids):
        if i == 10:
            time.sleep(1)
            i = 0
        captain = get_samefollow(int(uid))
        #print(captain)
        writer.writerow(captain)
        i = i + 1

if __name__ == '__main__':
    main()