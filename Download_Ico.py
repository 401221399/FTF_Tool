import json
import requests
from PIL import Image
from io import BytesIO

def downItemIco():
    list = []
    try:
        f =open("./source/json/baseItem.json",encoding='UTF-8')
        list = json.load(f)
        f.close()
    except IOError:
        print("无法找到baseItem.json文件")
    try:
        f =open("./source/json/Item.json",encoding='UTF-8')
        list = list + json.load(f)
        f.close()
    except IOError:
        print("无法找到baseItem.json文件")

    for i in range(0,len(list)):
        id = list[i]["id"]
        img = list[i]["img"]
        imgres = requests.get(img)
        image = Image.open(BytesIO(imgres.content))
        image.save('./source/item/{}.png'.format(id))
    print("下载完毕")

def downHeroIco():
    list = []
    try:
        f =open("./source/json/Hero.json",encoding='UTF-8')
        list = json.load(f)
        f.close()
    except IOError:
        print("无法找到Hero.json文件")

    for i in range(0,len(list)):
        id = list[i]["id"]
        img = list[i]["img"]
        imgres = requests.get(img)
        image = Image.open(BytesIO(imgres.content))
        image.save('./source/hero/{}.png'.format(id))
    print("下载完毕")

def downSkillIco():
    list = []
    try:
        f =open("./source/json/Hero.json",encoding='UTF-8')
        list = json.load(f)
        f.close()
    except IOError:
        print("无法找到Hero.json文件")

    for i in range(0,len(list)):
        id = list[i]["id"]
        img = list[i]["skillimg"]
        imgres = requests.get(img)
        image = Image.open(BytesIO(imgres.content))
        image.save('./source/skill/{}.png'.format(id))
    print("下载完毕")

def downRaceAndJobIco():
    list = []
    try:
        f =open("./source/json/Race.json",encoding='UTF-8')
        list = json.load(f)
        f.close()
    except IOError:
        print("无法找到Race.json文件")
    try:
        f =open("./source/json/Job.json",encoding='UTF-8')
        list = list + json.load(f)
        f.close()
    except IOError:
        print("无法找到Job.json文件")

    for i in range(0,len(list)):
        name = list[i]["name"]
        img = list[i]["img"]
        imgres = requests.get(img)
        image = Image.open(BytesIO(imgres.content))
        image.save('./source/RaceAndJob/{}.png'.format(name))
    print("下载完毕")
if __name__ == '__main__':
    #downItemIco()
    #downHeroIco()
    downSkillIco()
    downRaceAndJobIco()

