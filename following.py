from bs4 import BeautifulSoup
from urllib import request
import os
import re
import urllib
import requests

class Person:
    following_number = 0
    following_id = []
    following_fans_number = []
    area_number = {}
    area_score = {}
    area = {}
    invalid_number = 0
    average_fans = 0
    def __init__(self):
        return



ID = '2168045'
url = "https://api.bilibili.com/x/relation/stat?vmid="+ID+"&pn=1&ps=0&order=desc&jsonp=jsonp"
person = Person()
headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Host": "api.bilibili.com",
        "Referer": "https://www.bilibili.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }
res = requests.get(url, headers=headers)
online_dic = res.json()

print("----get basic following numbers----")
page = int(0)
person.following_number = online_dic["data"]["following"]
if person.following_number%50 == 0:
    page = online_dic["data"]["following"]//50
else:
    page = online_dic["data"]["following"]//50+1

for i in range(1, min(page+1, 6)):
    url = "https://api.bilibili.com/x/relation/followings?vmid="+ID+"&pn="+str(i)+"&ps=50&order=desc&jsonp=jsonp"
    res = requests.get(url, headers=headers)
    online_dic = res.json()
    lst = (online_dic["data"]["list"])
    for item in lst:
       person.following_id.append(item["mid"])

print("----count followings----")
for fan_id in person.following_id:
    url = "https://api.bilibili.com/x/space/arc/search?mid="+str(fan_id)+"&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp"
    res = requests.get(url, headers=headers)
    online_dic = res.json()
    tot_upload = 0
    if online_dic["data"]["list"]["tlist"] == None:
        #print(fan_id)
        person.invalid_number+=1
        continue
    mx = -1
    area = ""
    for item in online_dic["data"]["list"]["tlist"]:
        tot_upload += online_dic["data"]["list"]["tlist"][item]["count"]
        if online_dic["data"]["list"]["tlist"][item]["count"]>mx:
            mx = online_dic["data"]["list"]["tlist"][item]["count"]
            area = online_dic["data"]["list"]["tlist"][item]["name"]
    same = 0
    for item in online_dic["data"]["list"]["tlist"]:
        if online_dic["data"]["list"]["tlist"][item]["count"] == mx:
            same+=1
    if same == 1:
        if area not in person.area:
            person.area[area] = 0
        person.area[area]+=1
    else :
        if "不务正业" not in person.area:
            person.area["不务正业"] = 0
        person.area["不务正业"] += 1
    for item in online_dic["data"]["list"]["tlist"]:
        area = online_dic["data"]["list"]["tlist"][item]["name"]
        if area == " " or area == "":
            continue
        if area not in person.area_number:
            person.area_number[area] = 0
            person.area_score[area] = 0
        person.area_number[area] += online_dic["data"]["list"]["tlist"][item]["count"]
        person.area_score[area] += online_dic["data"]["list"]["tlist"][item]["count"]/tot_upload
        
            
    url = "https://api.bilibili.com/x/relation/stat?vmid="+str(fan_id)+"&pn=1&ps=0&order=desc&jsonp=jsonp"
    res = requests.get(url, headers=headers)
    online_dic = res.json()
    person.average_fans += online_dic["data"]["follower"]
        

temp = sorted(person.area_score.items(), key=lambda item:item[1], reverse=True)
for i in range(len(temp)):
    print(temp[i][0], ": ", temp[i][1])

temp = sorted(person.area.items(), key=lambda item:item[1], reverse=True)
for i in range(len(temp)):
    print(temp[i][0], ": ", temp[i][1])

print("好友数:")
print(person.invalid_number)
print("关注平均粉丝数:")
print(person.average_fans/(min(person.following_number, 250)-person.invalid_number))

print('okk!')