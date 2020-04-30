from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import qtawesome
import json
import requests
from PIL import Image
from io import BytesIO
import time
class MainUi(QtWidgets.QMainWindow):
    #构造函数
    def __init__(self):
        super().__init__()
        self.baseItemlist = []
        self.Itemlist = []
        self.ItemLinklist = []
        self.move_flag = False
        self.HeroList = []
        self.RaceList = []
        self.JobList = []
        self.synergyList = []
        self.LoadData()
        self.init_ui()

    def LoadData(self):
        try:
            f =open("./source/json/baseItem.json",encoding='UTF-8')
            self.baseItemlist = json.load(f)
            f.close()
        except IOError:
            print("无法找到baseItem.json文件")

        try:
            f =open("./source/json/Item.json",encoding='UTF-8')
            self.Itemlist = json.load(f)
            f.close()
        except IOError:
            print("无法找到Item.json文件")

        try:
            f =open("./source/json/ItemLink.json",encoding='UTF-8')
            self.ItemLinklist = json.load(f)
            f.close()
        except IOError:
            print("无法找到ItemLink.json文件")


        try:
            f =open("./source/json/Race.json",encoding='UTF-8')
            self.RaceList = json.load(f)
            f.close()
        except IOError:
            print("无法找到Race.json文件")

        try:
            f =open("./source/json/Job.json",encoding='UTF-8')
            self.JobList = json.load(f)
            f.close()
        except IOError:
            print("无法找到Job.json文件")

        try:
            f =open("./source/json/Hero.json",encoding='UTF-8')
            self.HeroList = json.load(f)
            f.close()
        except IOError:
            print("无法找到Hero.json文件")

        try:
            f =open("./source/json/synergy.json",encoding='UTF-8')
            self.synergyList = json.load(f)
            f.close()
        except IOError:
            print("无法找到synergy.json文件")

    #基础装备爬取
    def getBaseItem(self,driver,splash,content):
        try:
            driver.get('https://101.qq.com/tft/index.shtml?ADTAG=cooperation.glzx.tft&type=items')
            time.sleep(2)
            content.setText("基础装备爬取...")
            QtWidgets.qApp.processEvents()
            div =driver.find_elements("css selector", "#base_equip_list .item")
            minitemlen = len(div)
            baseItemList = []
            for i in range(0,minitemlen):
                driver.execute_script("arguments[0].click();", div[i])
                time.sleep(1)
                baseItem = {
                    "name":driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.item-active > p > span:nth-child(1)")[0].text,
                    "attr":driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.item-active > p > span:nth-child(2)")[0].text,
                    "id":driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.item-active > div")[0].get_attribute("data-id"),
                    "img":driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.item-active > div > img")[0].get_attribute("src"),
                }
                print(baseItem["name"])
                baseItemList.append(baseItem)
            jsonstr = json.dumps(baseItemList,ensure_ascii=False)
            try:
                f =open("./source/json/baseItem.json",'r')
                f.close()
            except IOError:
                f = open("./source/json/baseItem.json",'w')
                content.setText("新建了文件baseItem.json")
            f = open("./source/json/baseItem.json",'w+',encoding='utf-8')
            f.write(jsonstr)
            f.close()
            content.setText("基础装备信息保存成功")
            QtWidgets.qApp.processEvents()

        except Exception as e:
            MessageBox=QtWidgets.QMessageBox.information(splash,"错误",str(e),QtWidgets.QMessageBox.Yes)
            driver.quit()
            splash.finish(self)
            self.LoadData()

    #装备爬取
    def getItem(self,driver,splash,content):
        try:
            driver.get('https://101.qq.com/tft/index.shtml?ADTAG=cooperation.glzx.tft&type=items')
            time.sleep(2)
            content.setText("合成装备爬取...")
            QtWidgets.qApp.processEvents()
            div =driver.find_elements("css selector", "#base_form_list > .item")#获取合成装备集合html
            minitemlen = len(div)#获取集合长度
            ItemList = []
            LinkList = []
            for i in range(0,minitemlen):
                driver.execute_script("arguments[0].click();", div[i])
                time.sleep(1)
                Item = {
                    "name":driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.item-active > p > span:nth-child(1)")[0].text,
                    "attr":driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.item-active > p > span:nth-child(2)")[0].text,
                    "id":driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.item-active > div")[0].get_attribute("data-id"),
                    "img":driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.item-active > div > img")[0].get_attribute("src"),
                }
                link = [
                    driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.table-combination > div.combination-list.scroll-list > div > div.formula > div:nth-child(1)")[0].get_attribute("data-id"),
                    driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.table-combination > div.combination-list.scroll-list > div > div.formula > div:nth-child(2)")[0].get_attribute("data-id"),
                    driver.find_elements("css selector", "#item_tab3 > div > div.g-items-right > div.items-right > div > div.table-combination > div.combination-list.scroll-list > div > div.compound > div")[0].get_attribute("data-id"),
                ]
                print(Item["name"])
                ItemList.append(Item)
                LinkList.append(link)
            jsonstr1 = json.dumps(ItemList,ensure_ascii=False)#转json
            jsonstr2 = json.dumps(LinkList,ensure_ascii=False)#转json
            #写入保存
            try:
                f =open("./source/json/Item.json",'r')
                f.close()
            except IOError:
                f = open("./source/json/Item.json",'w')
                content.setText("新建了文件Item.json...")
                QtWidgets.qApp.processEvents()
            f = open("./source/json/Item.json",'w+',encoding='utf-8')
            f.write(jsonstr1)
            f.close()

            #写入保存
            try:
                f =open("./source/json/ItemLink.json",'r')
                f.close()
            except IOError:
                f = open("./source/json/ItemLink.json",'w')
                print("新建了文件ItemLink.json")
            f = open("./source/json/ItemLink.json",'w+',encoding='utf-8')
            f.write(jsonstr2)
            f.close()
            content.setText("合成装备信息保存成功...")
            QtWidgets.qApp.processEvents()

        except Exception as e:
            MessageBox=QtWidgets.QMessageBox.information(splash,"错误",str(e),QtWidgets.QMessageBox.Yes)
            driver.quit()
            splash.finish(self)
            self.LoadData()

    #爬取特质
    def getRace(self,driver,splash,content):
        try:
            driver.get('https://101.qq.com/tft/index.shtml?ADTAG=cooperation.glzx.tft&type=database2')
            time.sleep(2)
            content.setText("爬取特质...")
            QtWidgets.qApp.processEvents()
            ul =driver.find_elements("css selector", "#raceDatabaseList > ul > li")#获取特质集合
            List = []
            for i in range(0,len(ul)):
                name = ul[i].find_elements("css selector","div.trait-1 > div div.name")[0].text
                img = ul[i].find_elements("css selector","div.trait-1 > div > div.pic > img")[0].get_attribute("src")
                desc = ul[i].find_elements("css selector","div.trait-2 > div.desc")[0].text
                Raceid =  str(img).split(".")[-2].split("/")[-1]
                effectsList = []
                for j in range(0,len(ul[i].find_elements("css selector","div.trait-2 > div.effects span"))):
                    num = ul[i].find_elements("css selector","div.trait-2 > div.effects span")[j].find_elements("css selector","b")[0].text
                    effect = ul[i].find_elements("css selector","div.trait-2 > div.effects span")[j].text
                    effect = effect[len(num):]
                    effectitem = {"num":num,"effect":effect}
                    effectsList.append(effectitem)

                heroList = []
                for j in range(0,len(ul[i].find_elements("css selector","div.trait-3 > div.champion-pic"))):
                    id = ul[i].find_elements("css selector","div.trait-3 > div.champion-pic")[j].find_elements("css selector","img")[0].get_attribute("data-id")
                    heroList.append(id)
                item = {"id":Raceid,"name":name,"img":img,"desc":desc,"effectsList":effectsList,"heroList":heroList}
                List.append(item)
            jsonstr = json.dumps(List,ensure_ascii=False)#转json
            print("爬取结果：--------")
            print(jsonstr)
            #写入保存
            try:
                f =open("./source/json/Race.json",'r')
                f.close()
            except IOError:
                f = open("./source/json/Race.json",'w')
                print("新建了文件Race.json")
            f = open("./source/json/Race.json",'w+',encoding='utf-8')
            f.write(jsonstr)
            f.close()
            content.setText("特质信息保存成功")
            QtWidgets.qApp.processEvents()

        except Exception as e:
            MessageBox=QtWidgets.QMessageBox.information(splash,"错误",str(e),QtWidgets.QMessageBox.Yes)
            driver.quit()
            splash.finish(self)
            self.LoadData()

    #爬取职业
    def getJob(self,driver,splash,content):
        try:
            driver.get('https://101.qq.com/tft/index.shtml?ADTAG=cooperation.glzx.tft&type=database3')
            time.sleep(2)
            content.setText("职业爬取...")
            QtWidgets.qApp.processEvents()
            ul =driver.find_elements("css selector", "#jobDatabaseList > ul > li")#获取特质集合
            List = []
            for i in range(0,len(ul)):
                name = ul[i].find_elements("css selector","div.trait-1 > div div.name")[0].text
                img = ul[i].find_elements("css selector","div.trait-1 > div > div.pic > img")[0].get_attribute("src")
                Jobid =  str(img).split(".")[-2].split("/")[-1]
                desc = ul[i].find_elements("css selector","div.trait-2 > div.desc")[0].text

                effectsList = []
                for j in range(0,len(ul[i].find_elements("css selector","div.trait-2 > div.effects span"))):
                    num = ul[i].find_elements("css selector","div.trait-2 > div.effects span")[j].find_elements("css selector","b")[0].text
                    effect = ul[i].find_elements("css selector","div.trait-2 > div.effects span")[j].text
                    effect = effect[len(num):]
                    effectitem = {"num":num,"effect":effect}
                    effectsList.append(effectitem)

                heroList = []
                for j in range(0,len(ul[i].find_elements("css selector","div.trait-3 > div.champion-pic"))):
                    id = ul[i].find_elements("css selector","div.trait-3 > div.champion-pic")[j].find_elements("css selector","img")[0].get_attribute("data-id")
                    heroList.append(id)
                item = {"id":Jobid,"name":name,"img":img,"desc":desc,"effectsList":effectsList,"heroList":heroList}
                List.append(item)
            jsonstr = json.dumps(List,ensure_ascii=False)#转json
            print("爬取结果：--------")
            print(jsonstr)
            #写入保存
            try:
                f =open("./source/json/Job.json",'r')
                f.close()
            except IOError:
                f = open("./source/json/Job.json",'w')
                print("新建了文件Job.json")
            f = open("./source/json/Job.json",'w+',encoding='utf-8')
            f.write(jsonstr)
            f.close()
            content.setText("职业信息保存成功")
            QtWidgets.qApp.processEvents()

        except Exception as e:
            MessageBox=QtWidgets.QMessageBox.information(splash,"错误",str(e),QtWidgets.QMessageBox.Yes)
            driver.quit()
            splash.finish(self)
            self.LoadData()

    #爬取英雄
    def CrowlHero(self,driver,splash,content):
        try:
            driver.get('https://101.qq.com/tft/index.shtml?ADTAG=cooperation.glzx.tft&type=database0')
            time.sleep(2)
            content.setText("英雄爬取...")
            QtWidgets.qApp.processEvents()
            ul =driver.find_elements("css selector", "#heroOverallDatabaseList > li")#获取特质集合
            List = []
            for i in range(0,len(ul)):
                name = ul[i].find_elements("css selector","div.hero-info > div.name")[0].text
                id = ul[i].find_elements("css selector","div.hero-info > div.champion-pic > img")[0].get_attribute("data-id")
                img = ul[i].find_elements("css selector","div.hero-info > div.champion-pic > img")[0].get_attribute("src")
                price = ul[i].find_elements("css selector","div.hero-price > span")[0].text
                rece = ul[i].find_elements("css selector","div:nth-child(3) > div > div.name")[0].text

                #爬取英雄详细资料
                other = self.getHeroDetails(driver,ul[i].find_elements("css selector","div.hero-info > div.champion-pic")[0])
                JobList = []
                #heroOverallDatabaseList > li:nth-child(3) > div:nth-child(4) > div:nth-child(1)
                #heroOverallDatabaseList > li:nth-child(3) > div:nth-child(4) > div:nth-child(1) > div.name
                for j in range(0,len(ul[i].find_elements("css selector","div:nth-child(4) > div"))):
                    job = ul[i].find_elements("css selector","div:nth-child(4) > div")[j].find_elements("css selector","div.name")[0].text
                    JobList.append(job)

                item = {
                    "id":id,"name":name,"img":img,"price":price,"rece":rece,"JobList":JobList,
                    "skillname":other['skillname'],
                    "skillimg":other['skillimg'],
                    "skilldesc":other['skilldesc'],
                    "itemList":other['itemList'],
                    "attrList":other['attrList'],
                }
                print(name)
                List.append(item)

            jsonstr = json.dumps(List,ensure_ascii=False)#转json
            print("爬取结果：--------")
            print(jsonstr)
            #写入保存
            try:
                f =open("./source/json/Hero.json",'r')
                f.close()
            except IOError:
                f = open("./source/json/Hero.json",'w')
                print("新建了文件Hero.json")
            f = open("./source/json/Hero.json",'w+',encoding='utf-8')
            f.write(jsonstr)
            f.close()
            content.setText("英雄信息保存成功")
            QtWidgets.qApp.processEvents()

        except Exception as e:
            MessageBox=QtWidgets.QMessageBox.information(splash,"错误",str(e),QtWidgets.QMessageBox.Yes)
            driver.quit()
            splash.finish(self)
            self.LoadData()

    #爬取英雄个人信息
    def getHeroDetails(self,driver,div):
        divimg = div.find_elements("css selector", "img")[0]
        driver.execute_script("arguments[0].click();", divimg)

        HeroDiv = driver.find_elements("css selector", "#pop1")[0]

        skillname = HeroDiv.find_elements("css selector", "div.center > div.skill > div > p.name > span:nth-child(1)")[0].text
        skillimg = HeroDiv.find_elements("css selector", "div.center > div.skill > div > img")[0].get_attribute("src")
        skilldesc = HeroDiv.find_elements("css selector", "div.center > div.skill > div > p.description")[0].text

        itemList = []
        itemDiv = HeroDiv.find_elements("css selector", "div.left > div.recommend > div > img")
        for i in range(0,len(itemDiv)):
            imgsrc = itemDiv[i].get_attribute("src")
            itemList.append(str(imgsrc).split(".")[-2].split("/")[-1])

        attrList = []
        attrDiv = HeroDiv.find_elements("css selector", "div.left > div.attribute > ul li")
        for i in range(0,len(attrDiv)):
            attrList.append(attrDiv[i].text)

        closeBtn = driver.find_elements("css selector", "#pop1 > a")[0]
        driver.execute_script("arguments[0].click();", closeBtn)
        #closeBtn.click()
        item = {
            "skillname":skillname,
            "skillimg":skillimg,
            "skilldesc":skilldesc,
            "itemList":itemList,
            "attrList":attrList,
        }
        return item

    #爬取阵容
    def getSynergies(self,driver,splash,content):
        try:
            driver.get('https://101.qq.com/tft/index.shtml?ADTAG=cooperation.glzx.tft&type=synergies')
            while True:#跳到最下面以求获取全部阵容
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                height1 = driver.execute_script("return document.body.scrollHeight;")
                time.sleep(2)
                height2 = driver.execute_script("return document.body.scrollHeight;")
                if height1 == height2:
                    break
            content.setText("阵容爬取...")
            QtWidgets.qApp.processEvents()
            div =driver.find_elements("css selector", "#recommendSynergies > div.group-box > div > div")
            resultList = []
            for i in range(0,len(div)):
                print("进度"+str(i)+"/"+str(len(div)))
                name = div[i].find_elements("css selector", "div.tier.tier1 > div.info > p")[0].text

                #获取完整阵容(英雄，装备，站位)
                championsList = []
                championsDiv = div[i].find_elements("css selector", "div.tier.tier1 > div.champions > div")
                for j in range(0,len(championsDiv)):
                    #获取完整阵容的英雄id
                    cid = championsDiv[j].find_elements("css selector", "div.champion-pic > img")[0].get_attribute("data-id")
                    #获取英雄装备集合
                    ItemDiv = championsDiv[j].find_elements("css selector", "div.cost-skills > img")
                    itemList = []
                    for k in range(0,len(ItemDiv)):
                        itemid = ItemDiv[k].get_attribute("data-id")
                        itemList.append(itemid)

                    #获取英雄站位
                    stanceList = []
                    stanceDiv = div[i].find_elements("css selector", "div.tier.tier3 > div.stance > img")
                    for k in range(0,len(stanceDiv)):
                        if cid == stanceDiv[k].get_attribute("data-id"):
                            classname = stanceDiv[k].get_attribute("class")
                            stanceList =str(classname).split("position")[1].split("-")
                    item = {"id":cid,"itemList":itemList,"stanceList":stanceList}
                    championsList.append(item)

                #获取前期阵容
                earlierDiv = div[i].find_elements("css selector", "div.tier.tier2 > div.earlier > div")
                earlierList = []
                for j in range(0,len(earlierDiv)):
                    #获取完整阵容的英雄id
                    eid = earlierDiv[j].find_elements("css selector", "div.champion-pic > img")[0].get_attribute("data-id")
                    earlierList.append(eid)

                #获取中期阵容
                interimDiv = div[i].find_elements("css selector", "div.tier.tier2 > div.interim > div")
                interimList = []
                for j in range(0,len(interimDiv)):
                    #获取中期阵容的英雄id
                    iid = interimDiv[j].find_elements("css selector", "div.champion-pic > img")[0].get_attribute("data-id")
                    interimList.append(iid)

                traitsDiv = div[i].find_elements("css selector", "div.tier.tier3 > div.traits > div")
                traitsList = []
                for j in range(0,len(traitsDiv)):
                    #获取中期阵容的英雄id
                    trait = traitsDiv[j].find_elements("css selector", "span")[0].text
                    traitsList.append(trait)

                explainDiv = div[i].find_elements("css selector", "div.tier.tier2 > div.explain")[0]
                # webdriver.ActionChains(driver).move_to_element(explainDiv)
                driver.execute_script("arguments[0].click();", explainDiv)

                explainList = []
                explainitemDiv = driver.find_elements("css selector", "body > div.explain-box.show > div")
                for j in range(0,len(explainitemDiv)):
                    title = explainitemDiv[j].find_element("css selector","p.title").text
                    description = explainitemDiv[j].find_element("css selector","p.description").text
                    explain ={title:description}
                    explainList.append(explain)

                synergy ={"name":name,"championsList":championsList,"earlierList":earlierList,"interimList":interimList,"traitsList":traitsList,"explainList":explainList}
                resultList.append(synergy)
            jsonstr = json.dumps(resultList,ensure_ascii=False)#转json
            print("爬取结果：--------")
            print(jsonstr)
            #写入保存
            try:
                f =open("./source/json/synergy.json",'r')
                f.close()
            except IOError:
                f = open("./source/json/synergy.json",'w')
                print("新建了文件synergy.json")
            f = open("./source/json/synergy.json",'w+',encoding='utf-8')
            f.write(jsonstr)
            f.close()
            content.setText("阵容信息保存成功")
            QtWidgets.qApp.processEvents()

        except Exception as e:
            MessageBox=QtWidgets.QMessageBox.information(splash,"错误",str(e),QtWidgets.QMessageBox.Yes)
            driver.quit()
            splash.finish(self)
            self.LoadData()

    def downItemIco(self,splash,content):
        self.LoadData()
        try:
            list = self.Itemlist
            for i in range(0,len(list)):
                id = list[i]["id"]
                img = list[i]["img"]
                imgres = requests.get(img)
                image = Image.open(BytesIO(imgres.content))
                image.save('./source/item/{}.png'.format(id))

            list =self.HeroList
            for i in range(0,len(list)):
                id = list[i]["id"]
                img = list[i]["img"]
                skillimg = list[i]["skillimg"]
                imgres = requests.get(img)
                image = Image.open(BytesIO(imgres.content))
                image.save('./source/hero/{}.png'.format(id))

                imgres = requests.get(skillimg)
                image = Image.open(BytesIO(imgres.content))
                image.save('./source/skill/{}.png'.format(id))

            list = self.RaceList+self.JobList
            for i in range(0,len(list)):
                name = list[i]["name"]
                img = list[i]["img"]
                imgres = requests.get(img)
                image = Image.open(BytesIO(imgres.content))
                image.save('./source/RaceAndJob/{}.png'.format(name))

        except Exception as e:
            MessageBox=QtWidgets.QMessageBox.information(splash,"错误",str(e),QtWidgets.QMessageBox.Yes)
            splash.finish(self)

    #更新
    def Update_UI(self):
        splash = QtWidgets.QSplashScreen()
        splash.setGeometry(600, 300,200, 130)
        splashLabel =QtWidgets.QLabel("",splash)
        splashgif = QtGui.QMovie("./source/Loading.gif")
        splashLabel.setMovie(splashgif)
        splashLabel.setGeometry(65, 10,65,65)
        content =QtWidgets.QLabel("爬取启动中...",splash)
        content.setGeometry(0, 80,200,20)
        content.setAlignment(QtCore.Qt.AlignCenter)
        ProgressBar = QtWidgets.QProgressBar(splash)
        ProgressBar.setGeometry(0, 110, 200, 20)
        ProgressBar.setAlignment(QtCore.Qt.AlignCenter)
        ProgressBar.setValue(0)

        splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        splash.setWindowFlag(QtCore.Qt.FramelessWindowHint) # 隐藏边框
        splashgif.start()
        splash.show()                           # 显示启动界面
        QtWidgets.qApp.processEvents()

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options =chrome_options)
        # driver = webdriver.Chrome(executable_path="C:\FTF_Tool\chromedriver.exe")

        self.getBaseItem(driver,splash,content)
        ProgressBar.setValue(10)
        self.getItem(driver,splash,content)
        ProgressBar.setValue(30)
        self.CrowlHero(driver,splash,content)
        ProgressBar.setValue(50)
        self.getSynergies(driver,splash,content)
        ProgressBar.setValue(70)
        self.getRace(driver,splash,content)
        ProgressBar.setValue(80)
        self.getJob(driver,splash,content)
        ProgressBar.setValue(99)
        driver.quit()
        self.downItemIco(splash,content)
        ProgressBar.setValue(100)
        splash.finish(self)
        self.LoadData()



    #获取基本装备的属性
    def getBaseItemAttr(self,id):
        for i in range(0,len(self.baseItemlist)):
            if id == self.baseItemlist[i]["id"]:
                return self.baseItemlist[i]
    #根据id获取英雄
    def getHero(self,id):
        for i in range(0,len(self.HeroList)):
            if id == self.HeroList[i]["id"]:
                return self.HeroList[i]
    #根据羁绊名获取英雄列表
    def getRaceAndJob_HeroList(self,name):
        list = self.RaceList+self.JobList
        for i in range(0,len(list)):
            if name == list[i]["name"]:
                return list[i]["heroList"]
    #获取装备的属性
    def getItemAttr(self,id):
        for i in range(0,len(self.Itemlist)):
            if id == self.Itemlist[i]["id"]:
                return self.Itemlist[i]

    #关闭弹窗
    def Close_UI(self):
        splash = QtWidgets.QSplashScreen()
        splash.setGeometry(600, 300,200, 200)
        Label= QtWidgets.QLabel("本工具由【清枫冥月】制作",splash)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setWeight(75)
        Label.setFont(font)
        Label.setAlignment(QtCore.Qt.AlignCenter)
        Label.setGeometry(0, 0,200,25)

        icoBtn = QtWidgets.QPushButton(splash)
        icoBtn_icon = QIcon()
        req = requests.get("http://resource.ink-cloud.xyz/lpf/paycode.png")
        img  = QPixmap()
        img.loadFromData(req.content)
        icoBtn_icon.addPixmap(img, QIcon.Normal, QIcon.Off)
        icoBtn.setIcon(icoBtn_icon)
        icoBtn.setIconSize(QSize(100, 100))
        icoBtn.setGeometry(50, 30, 100, 100)

        Label= QtWidgets.QLabel("如果觉得不错，扫码赞助一下如何？",splash)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(8)
        Label.setFont(font)
        Label.setAlignment(QtCore.Qt.AlignCenter)
        Label.setGeometry(0, 140,200,25)

        closeBtn = QtWidgets.QPushButton("确定",splash)
        closeBtn.setObjectName('showBtn')
        closeBtn.setProperty("id","closeBtnTrue")
        closeBtn.setGeometry(50, 170,100,30)

        splash.show()
        QtWidgets.qApp.processEvents()
        time.sleep(2)
        splash.finish(self)

    #显示装备界面
    def showBaseItem_UI(self):
        #清空top_layout所以控件
        for i in range(0,self.top_layout.count()):
            self.top_layout.itemAt(i).widget().deleteLater()
        for i in range(0,len(self.baseItemlist)):
            name = self.baseItemlist[i]["name"]
            id = self.baseItemlist[i]["id"]
            attr = self.baseItemlist[i]["attr"]
            self.itembtn = QtWidgets.QPushButton()
            #self.itembtn.setText(name)
            itembtn_icon = QIcon()
            itembtn_icon.addPixmap(QPixmap('./source/item/{}.png'.format(id)), QIcon.Normal, QIcon.Off)
            self.itembtn.setIcon(itembtn_icon)
            self.itembtn.setToolTip(name+'['+attr+']')
            self.itembtn.setProperty("id",id)
            self.itembtn.setProperty("class",'item')
            self.itembtn.setIconSize(QSize(64, 64))
            self.itembtn.setObjectName(id)
            self.itembtn.installEventFilter(self)
            self.top_layout.addWidget(self.itembtn, 0, i)
        self.top_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
        ''')

    #显示羁绊界面
    def showRaceAndJob_UI(self):
        list = self.RaceList+self.JobList

        #清空top_layout所以控件
        for i in range(0,self.top_layout.count()):
            self.top_layout.itemAt(i).widget().deleteLater()

        for i in range(0,len(list)):
            name = list[i]["name"]
            desc = list[i]["desc"]
            self.itembtn = QtWidgets.QPushButton()
            #self.itembtn.setText(name)
            itembtn_icon = QIcon()
            itembtn_icon.addPixmap(QPixmap('./source/RaceAndJob/{}.png'.format(name)), QIcon.Normal, QIcon.Off)
            self.itembtn.setIcon(itembtn_icon)
            self.itembtn.setToolTip(name+'['+desc+']')
            self.itembtn.setProperty("id",name)
            self.itembtn.setProperty("class",'RaceAndJob')
            self.itembtn.setIconSize(QSize(32, 32))
            self.itembtn.setObjectName(name)
            self.itembtn.installEventFilter(self)
            self.top_layout.addWidget(self.itembtn, i/18, i%18)
        self.top_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
        ''')

    #显示英雄界面
    def showHero_UI(self):
        list = self.HeroList

        #清空top_layout所以控件
        for i in range(0,self.top_layout.count()):
            self.top_layout.itemAt(i).widget().deleteLater()

        for i in range(0,len(list)):
            id = list[i]["id"]
            name = list[i]["name"]
            price = list[i]["price"]
            self.itembtn = QtWidgets.QPushButton()
            #self.itembtn.setText(name)
            itembtn_icon = QIcon()
            itembtn_icon.addPixmap(QPixmap('./source/hero/{}.png'.format(id)), QIcon.Normal, QIcon.Off)
            self.itembtn.setIcon(itembtn_icon)
            self.itembtn.setToolTip(name+'['+price+']')
            self.itembtn.setProperty("id",id)
            self.itembtn.setProperty("class",'Hero')
            self.itembtn.setIconSize(QSize(32, 32))
            self.itembtn.setObjectName(id)
            self.itembtn.installEventFilter(self)
            self.top_layout.addWidget(self.itembtn, i/18, i%18)
        self.top_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
        ''')

    def showSynergy_UI(self):
        list = self.synergyList
        #清空top_layout所以控件
        for i in range(0,self.top_layout.count()):
            self.top_layout.itemAt(i).widget().deleteLater()

        for i in range(0,len(list)):
            id = i
            name = str(list[i]["name"]).split("】")[0]
            name = name[1:len(name)]
            self.itembtn = QtWidgets.QPushButton()
            self.itembtn.setText(name)
            self.itembtn.setToolTip(list[i]["name"])
            self.itembtn.setProperty("id",str(id))
            self.itembtn.setProperty("class",'Synergy')
            self.itembtn.setObjectName(str(id))
            self.itembtn.installEventFilter(self)
            self.top_layout.addWidget(self.itembtn, i/6, i%6)
        self.top_widget.setStyleSheet('''
                QPushButton{
                    background:white;
                    border:1px solid white;
                    border-radius:25px;
                }
                QPushButton:hover{
                    border:0;
                    background:white;
                }
        ''')

    #显示装备的详情界面
    def showItemDetails(self,id):
        list = []
        #清空bottom_layout所以控件
        for i in range(0,self.bottom_layout.count()):
            self.bottom_layout.itemAt(i).widget().deleteLater()

        for i in range(0,len(self.ItemLinklist)):
            if self.ItemLinklist[i][0] == id:
                list.append(self.ItemLinklist[i])
                continue
            if self.ItemLinklist[i][1] == id:
                list.append(self.ItemLinklist[i])
                continue

        for i in range(0 , len(list)):
            item = [self.getBaseItemAttr(list[i][0]),self.getBaseItemAttr(list[i][1]),self.getItemAttr(list[i][2])]
            for j in range(0,len(item)):
                itembtn = QtWidgets.QPushButton()
                itembtn_icon = QIcon()
                itembtn_icon.addPixmap(QPixmap('./source/item/{}.png'.format(item[j]["id"])), QIcon.Normal, QIcon.Off)
                itembtn.setIcon(itembtn_icon)
                itembtn.setToolTip(item[j]["name"]+'['+item[j]["attr"]+']')
                itembtn.setIconSize(QSize(32, 32))
                itembtn.setObjectName(item[j]["id"])
                self.bottom_layout.addWidget(itembtn, i, j)
            itemLabel= QtWidgets.QLabel(item[2]["attr"])
            itemLabel.adjustSize()
            itemLabel.setWordWrap(True)
            itemLabel.setFont(qtawesome.font('fa', 16))
            self.bottom_layout.addWidget(itemLabel, i, 3)
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.9)
        self.bottom_widget.setGraphicsEffect(op)
        self.bottom_widget.setAutoFillBackground(True)
        self.bottom_widget.setStyleSheet('''
                QWidget#bottom_widget{
                    background:gray;
                    border:1px solid white;
                    border-radius:10px;
                }
                QPushButton{border:none;color:white;}
            ''')

    #显示羁绊的详情界面
    def showRaceAndJobDetails(self,id):
        list = self.RaceList+self.JobList
        item = {}
        for i in range(0,len(list)):
            if list[i]["name"] == id:
                item = list[i]
                continue
        #清空bottom_layout所以控件
        for i in range(0,self.bottom_layout.count()):
            self.bottom_layout.itemAt(i).widget().deleteLater()

        Main_Widget = QtWidgets.QWidget()
        Main_Widget.setObjectName('RaceAndJob_Widget')
        self.bottom_layout.addWidget(Main_Widget, 0, 0,1,1)

        icoBtn = QtWidgets.QPushButton(Main_Widget)
        icoBtn_icon = QIcon()
        icoBtn_icon.addPixmap(QPixmap('./source/RaceAndJob/{}.png'.format(item["name"])), QIcon.Normal, QIcon.Off)
        icoBtn.setIcon(icoBtn_icon)
        icoBtn.setToolTip(item["name"]+'['+item["desc"]+']')
        icoBtn.setIconSize(QSize(42, 42))
        icoBtn.setObjectName(item["name"])
        icoBtn.setGeometry(10, 10, 42, 42)

        nameLabel= QtWidgets.QLabel(item["name"],Main_Widget)
        nameLabel.adjustSize()
        nameLabel.setWordWrap(True)
        nameLabel.setFont(qtawesome.font('fa', 26))
        nameLabel.setGeometry(70, 20,560,30)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        nameLabel.setFont(font)

        Label= QtWidgets.QLabel("羁绊效果：",Main_Widget)
        Label.adjustSize()
        Label.setWordWrap(True)
        Label.setFont(qtawesome.font('fa', 16))
        Label.setGeometry(10, 50, 100, 30)


        descLabel= QtWidgets.QLabel(item["desc"],Main_Widget)
        descLabel.adjustSize()
        descLabel.setWordWrap(True)
        descLabel.setFont(qtawesome.font('fa', 16))
        hight = (int(len(item["desc"])/22)+1) * descLabel.fontMetrics().lineSpacing()
        descLabel.setGeometry(QRect(10, 80,275, hight))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        descLabel.setFont(font)
        descLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        descLabel.setWordWrap(True)

        for i in range(0,len(item["effectsList"])):
            num = item["effectsList"][i]["num"]
            effect = item["effectsList"][i]["effect"]
            effectLabel= QtWidgets.QLabel(num+":"+effect,Main_Widget)
            effectLabel.setWordWrap(True)
            effectLabel.adjustSize()
            font = QtGui.QFont()
            font.setFamily("宋体")
            font.setPointSize(12)
            font.setBold(False)
            font.setItalic(False)
            font.setUnderline(False)
            font.setWeight(50)
            effectLabel.setFont(font)
            effecthight = (int(len(effect)/20)+1) * effectLabel.fontMetrics().lineSpacing()
            effectLabel.setGeometry(QRect(10, hight+80+i*effecthight,275, effecthight))
            effectLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
            effectLabel.setWordWrap(True)

        for i in range(0,len(item["heroList"])):
            Hero = self.getHero(item["heroList"][i])
            HeroBtn = QtWidgets.QToolButton(Main_Widget)
            HeroBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            HeroBtn.setText(Hero["name"])
            HeroBtn_icon = QIcon()
            HeroBtn_icon.addPixmap(QPixmap('./source/hero/{}.png'.format(item["heroList"][i])), QIcon.Normal, QIcon.Off)
            HeroBtn.setIcon(HeroBtn_icon)
            HeroBtn.setToolTip(Hero["name"]+'['+Hero["price"]+']')
            HeroBtn.setIconSize(QSize(70, 70))
            HeroBtn.setObjectName(Hero["name"])
            HeroBtn.setGeometry(300 + int(i%3)*80, 80 + int(i/3)*100, 100, 100)


        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.9)
        self.bottom_widget.setGraphicsEffect(op)
        self.bottom_widget.setAutoFillBackground(True)
        self.bottom_widget.setStyleSheet('''
                    QWidget#bottom_widget{
                        background:gray;
                        border:1px solid white;
                        border-radius:10px;
                    }
                    #RaceAndJob_Widget QToolButton{
                        border:none;
                        background:none;
                    }
                    QPushButton{border:none;color:white;}
                ''')

    #显示英雄的详情界面
    def showHeroDetails(self,id):
        list = []
        #清空bottom_layout所以控件
        for i in range(0,self.bottom_layout.count()):
            self.bottom_layout.itemAt(i).widget().deleteLater()

        item = self.getHero(id)

        Main_Widget = QtWidgets.QWidget()
        Main_Widget.setObjectName('HeroDetails_Widget')
        self.bottom_layout.addWidget(Main_Widget, 0, 0,1,1)

        icoBtn = QtWidgets.QPushButton(Main_Widget)
        icoBtn_icon = QIcon()
        icoBtn_icon.addPixmap(QPixmap('./source/hero/{}.png'.format(item["id"])), QIcon.Normal, QIcon.Off)
        icoBtn.setIcon(icoBtn_icon)
        icoBtn.setIconSize(QSize(42, 42))
        icoBtn.setGeometry(10, 10, 42, 42)

        nameLabel= QtWidgets.QLabel(item["name"],Main_Widget)
        nameLabel.adjustSize()
        nameLabel.setWordWrap(True)
        nameLabel.setFont(qtawesome.font('fa', 26))
        nameLabel.setGeometry(70, 20,560,30)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        nameLabel.setFont(font)

        Label= QtWidgets.QLabel("推荐装备：",Main_Widget)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        Label.setFont(font)
        Label.setGeometry(10, 50, 100, 30)

        for i in range(0,len(item["itemList"])):
            itemBtn = QtWidgets.QToolButton(Main_Widget)
            itemBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            itemBtn_icon = QIcon()
            itemBtn_icon.addPixmap(QPixmap('./source/item/{}.png'.format(item["itemList"][i])), QIcon.Normal, QIcon.Off)
            itemBtn.setIcon(itemBtn_icon)
            itemBtn.setIconSize(QSize(25, 25))
            itemBtn.setGeometry(10 + int(i%3)*32, 80, 25, 25)

        Label= QtWidgets.QLabel("属性：",Main_Widget)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        Label.setFont(font)
        Label.setGeometry(10, 100, 100, 35)
        for i in range(0,len(item["attrList"])):
            attrLabel = QtWidgets.QLabel(item["attrList"][i],Main_Widget)
            attrLabel.adjustSize()
            attrLabel.setWordWrap(True)
            font = QtGui.QFont()
            font.setFamily("宋体")
            font.setPointSize(10)
            attrLabel.setFont(font)
            attrLabel.setGeometry(10, 130+i*25, 180, 30)

        SkillicoBtn = QtWidgets.QPushButton(Main_Widget)
        SkillicoBtn_icon = QIcon()
        SkillicoBtn_icon.addPixmap(QPixmap('./source/skill/{}.png'.format(item["id"])), QIcon.Normal, QIcon.Off)
        SkillicoBtn.setIcon(SkillicoBtn_icon)
        SkillicoBtn.setIconSize(QSize(42, 42))
        SkillicoBtn.setGeometry(265, 10, 42, 42)

        SkillnameLabel= QtWidgets.QLabel(item["skillname"],Main_Widget)
        SkillnameLabel.adjustSize()
        SkillnameLabel.setWordWrap(True)
        SkillnameLabel.setGeometry(315, 20,180,30)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        SkillnameLabel.setFont(font)

        SkilldescLabel= QtWidgets.QLabel(item["skilldesc"],Main_Widget)
        SkilldescLabel.adjustSize()
        SkilldescLabel.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        SkilldescLabel.setFont(font)
        hight = (int(len(item["skilldesc"])/22)+1) * SkilldescLabel.fontMetrics().lineSpacing()
        SkilldescLabel.setGeometry(QRect(265, 62,275, hight))
        SkilldescLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        SkilldescLabel.setWordWrap(True)

        race = item["rece"]
        Label= QtWidgets.QLabel("特质：",Main_Widget)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        Label.setFont(font)
        Label.setGeometry(265, 72+hight,100, 30)

        icoBtn = QtWidgets.QToolButton(Main_Widget)
        icoBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        icoBtn.setText(race)
        icoBtn_icon = QIcon()
        icoBtn_icon.addPixmap(QPixmap('./source/RaceAndJob/{}.png'.format(race)), QIcon.Normal, QIcon.Off)
        icoBtn.setIcon(icoBtn_icon)
        icoBtn.setIconSize(QSize(32, 32))
        icoBtn.setGeometry(265+20, 62 + hight, 120, 52)

        list = self.getRaceAndJob_HeroList(race)
        for i in range(0,len(list)):
            Hero = self.getHero(list[i])
            HeroBtn = QtWidgets.QToolButton(Main_Widget)
            HeroBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            HeroBtn.setText(Hero["name"])
            HeroBtn_icon = QIcon()
            HeroBtn_icon.addPixmap(QPixmap('./source/hero/{}.png'.format(Hero["id"])), QIcon.Normal, QIcon.Off)
            HeroBtn.setIcon(HeroBtn_icon)
            HeroBtn.setIconSize(QSize(32, 32))
            HeroBtn.setGeometry(230+ int(i%5)*65, 112 + hight + int(i/5)*52, 100, 52)


        Label= QtWidgets.QLabel("职业：",Main_Widget)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        Label.setFont(font)
        Label.setGeometry(265, 212+hight,100, 30)

        for i in range(0,len(item["JobList"])):
            job = item["JobList"][i]
            icoBtn = QtWidgets.QToolButton(Main_Widget)
            icoBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            icoBtn.setText(job)
            icoBtn_icon = QIcon()
            icoBtn_icon.addPixmap(QPixmap('./source/RaceAndJob/{}.png'.format(job)), QIcon.Normal, QIcon.Off)
            icoBtn.setIcon(icoBtn_icon)
            icoBtn.setIconSize(QSize(32, 32))
            icoBtn.setGeometry(230, 242 + hight + i*100, 100, 52)

            list = self.getRaceAndJob_HeroList(job)
            for j in range(0,len(list)):
                Hero = self.getHero(list[j])
                HeroBtn = QtWidgets.QToolButton(Main_Widget)
                HeroBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
                HeroBtn.setText(Hero["name"])
                font = QtGui.QFont()
                font.setFamily("等线")
                font.setPointSize(9)
                font.setBold(False)
                font.setItalic(False)
                font.setUnderline(False)
                font.setWeight(75)
                HeroBtn.setFont(font)
                HeroBtn_icon = QIcon()
                HeroBtn_icon.addPixmap(QPixmap('./source/hero/{}.png'.format(Hero["id"])), QIcon.Normal, QIcon.Off)
                HeroBtn.setIcon(HeroBtn_icon)
                HeroBtn.setIconSize(QSize(30, 30))
                HeroBtn.setGeometry(320+ int(j%5)*40, 242 + hight + i*105 + int(j/5)*50, 50, 50)


        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.9)
        self.bottom_widget.setGraphicsEffect(op)
        self.bottom_widget.setAutoFillBackground(True)
        self.bottom_widget.setStyleSheet('''
                            QWidget#bottom_widget{
                                background:gray;
                                border:1px solid white;
                                border-radius:10px;
                            }
                            #HeroDetails_Widget QToolButton{
                                border:none;
                                background:none;
                            }
                            QPushButton{border:none;color:white;}
                        ''')

    def showSynergyDetails(self,id):
        item = self.synergyList[int(id)]
        #清空bottom_layout所以控件
        for i in range(0,self.bottom_layout.count()):
            self.bottom_layout.itemAt(i).widget().deleteLater()
        Main_Widget = QtWidgets.QWidget()
        Main_Widget.setObjectName('SynergyDetails_Widget')
        self.bottom_layout.addWidget(Main_Widget, 0, 0,1,1)



        Label= QtWidgets.QLabel("前期阵容：",Main_Widget)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        font.setWeight(75)
        Label.setFont(font)
        Label.setGeometry(10, 10,100, 30)
        earlierList = item["earlierList"]
        for i in range(0,len(earlierList)):
            Hero = self.getHero(earlierList[i])
            HeroBtn = QtWidgets.QToolButton(Main_Widget)
            HeroBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            HeroBtn.setText(Hero["name"])
            font = QtGui.QFont()
            font.setFamily("等线")
            font.setPointSize(6)
            font.setWeight(75)
            HeroBtn.setFont(font)
            HeroBtn_icon = QIcon()
            HeroBtn_icon.addPixmap(QPixmap('./source/hero/{}.png'.format(Hero["id"])), QIcon.Normal, QIcon.Off)
            HeroBtn.setIcon(HeroBtn_icon)
            HeroBtn.setIconSize(QSize(30, 30))
            HeroBtn.setGeometry(10+ i*40, 35, 40, 46)

        Label= QtWidgets.QLabel("中期阵容：",Main_Widget)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        font.setWeight(75)
        Label.setFont(font)
        Label.setGeometry(10, 80,100, 30)
        interimList = item["interimList"]
        for i in range(0,len(interimList)):
            Hero = self.getHero(interimList[i])
            HeroBtn = QtWidgets.QToolButton(Main_Widget)
            HeroBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            HeroBtn.setText(Hero["name"])
            font = QtGui.QFont()
            font.setFamily("等线")
            font.setPointSize(8)
            font.setWeight(75)
            HeroBtn.setFont(font)
            HeroBtn_icon = QIcon()
            HeroBtn_icon.addPixmap(QPixmap('./source/hero/{}.png'.format(Hero["id"])), QIcon.Normal, QIcon.Off)
            HeroBtn.setIcon(HeroBtn_icon)
            HeroBtn.setIconSize(QSize(40, 40))
            HeroBtn.setGeometry(10+ int(i%3)*50, 105 +  int(i/3)*60, 50, 60)


        Label= QtWidgets.QLabel("完整阵容：",Main_Widget)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        Label.setFont(font)
        Label.setGeometry(10, 220,100, 30)

        championsList = item["championsList"]
        for i in range(0,len(championsList)):
            Hero = self.getHero(championsList[i]["id"])
            HeroBtn = QtWidgets.QToolButton(Main_Widget)
            HeroBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            HeroBtn.setText(Hero["name"])
            font = QtGui.QFont()
            font.setFamily("等线")
            font.setPointSize(9)
            font.setBold(False)
            font.setItalic(False)
            font.setUnderline(False)
            font.setWeight(75)
            HeroBtn.setFont(font)
            HeroBtn_icon = QIcon()
            HeroBtn_icon.addPixmap(QPixmap('./source/hero/{}.png'.format(Hero["id"])), QIcon.Normal, QIcon.Off)
            HeroBtn.setIcon(HeroBtn_icon)
            HeroBtn.setIconSize(QSize(50, 50))
            HeroBtn.setGeometry(10+ int(i%3)*60, 245 +  int(i/3)*75, 60, 70)

            #英雄站位
            stanceList = championsList[i]["stanceList"]
            icoBtn = QtWidgets.QToolButton(Main_Widget)
            icoBtn.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            icoBtn_icon = QIcon()
            icoBtn_icon.addPixmap(QPixmap('./source/hero/{}.png'.format(Hero["id"])), QIcon.Normal, QIcon.Off)
            icoBtn.setIcon(icoBtn_icon)
            icoBtn.setIconSize(QSize(30, 30))
            if int(stanceList[0])%2 == 0:
                icoBtn.setGeometry(200+(int(stanceList[1])-1)*43.5+21 , 10+(int(stanceList[0])-1)*40.5, 43,45)
            else:
                icoBtn.setGeometry(200+(int(stanceList[1])-1)*43.5 , 10+(int(stanceList[0])-1)*40.5,43,45)


            itemList = championsList[i]["itemList"]
            for j in range(0,len(itemList)):
                icoBtn = QtWidgets.QToolButton(Main_Widget)
                icoBtn_icon = QIcon()
                icoBtn_icon.addPixmap(QPixmap('./source/item/{}.png'.format(itemList[j])), QIcon.Normal, QIcon.Off)
                icoBtn.setIcon(icoBtn_icon)
                icoBtn.setIconSize(QSize(16, 16))
                icoBtn.setGeometry(10 + int(i%3)*60, 245 +  int(i/3)*75 + j*20, 20, 20)

        stanceBG = QtWidgets.QToolButton(Main_Widget)
        stanceBG_icon = QIcon()
        stanceBG_icon.addPixmap(QPixmap('./source/{}.png'.format("stance-bg")), QIcon.Normal, QIcon.Off)
        stanceBG.setIcon(stanceBG_icon)
        stanceBG.setIconSize(QSize(324, 164))
        stanceBG.setGeometry(200, 10, 324, 164)

        explainList = item["explainList"]
        for i in range(0,len(explainList)):
            title = list(explainList[i].keys())[0]
            desc = explainList[i][list(explainList[i].keys())[0]]
            Label= QtWidgets.QLabel(title,Main_Widget)
            Label.adjustSize()
            Label.setWordWrap(True)
            font = QtGui.QFont()
            font.setFamily("等线")
            font.setPointSize(10)
            Label.setFont(font)
            Label.setGeometry(200, 200+i*50,30, 30)

            Label= QtWidgets.QLabel(desc,Main_Widget)
            Label.adjustSize()
            Label.setWordWrap(True)
            font = QtGui.QFont()
            font.setFamily("等线")
            font.setPointSize(8)
            Label.setFont(font)
            Label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
            Label.setWordWrap(True)
            Label.setGeometry(230, 200+i*50,340, 50)

        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.9)
        self.bottom_widget.setGraphicsEffect(op)
        self.bottom_widget.setAutoFillBackground(True)
        self.bottom_widget.setStyleSheet('''
                            QWidget#bottom_widget{
                                background:gray;
                                border:1px solid white;
                                border-radius:10px;
                            }
                            #SynergyDetails_Widget QToolButton{
                                border:none;
                                background:none;
                            }
                            QPushButton{border:none;color:white;}
                        ''')

    def hideDetails(self):
        #清空bottom_layout所以控件
        for i in range(0,self.bottom_layout.count()):
            self.bottom_layout.itemAt(i).widget().deleteLater()
        self.bottom_widget.setStyleSheet('''
                    QWidget#bottom_widget{
                        background:none;
                        border:1px solid white;
                        border-radius:10px;
                        border:0;
                    }
                ''')

    def mousePressEvent(self, event):
        self.move_flag = True
        self.move_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
        event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if self.move_flag:
            self.move(QMouseEvent.globalPos() - self.move_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.move_flag = False

    def enterEvent(self, QMouseEvent):
        self.setWindowOpacity(0.9)

    def leaveEvent(self, QMouseEvent):
        self.setWindowOpacity(0.3)


    #事件监听
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Enter and object.objectName() == 'showBtn':
            object.setCursor(Qt.PointingHandCursor)
            return True
        if event.type() == QtCore.QEvent.Leave and object.objectName() == 'showBtn':
            object.setCursor(Qt.PointingHandCursor)
            return True
        if event.type() == QtCore.QEvent.MouseButtonPress and object.objectName() == 'showBtn':
            if object.property("id") == "closeBtn":
                self.Close_UI()
                self.close()
            if  object.property("id") == 'UpdateBtn':
                self.Update_UI()
            if object.property("id") == "showItemBtn":
                self.showBaseItem_UI()
            if object.property("id") == "showTiesBtn":
                self.showRaceAndJob_UI()
            if object.property("id") == "showHeroBtn":
                self.showHero_UI()
            if object.property("id") == "showSynergyBtn":
                self.showSynergy_UI()
            return True

        if event.type() == QtCore.QEvent.Enter:
            id = object.property("id")
            classname = object.property("class")
            if classname == 'item':
                self.showItemDetails(id)
            if classname == 'RaceAndJob':
                self.showRaceAndJobDetails(id)
            if classname == 'Hero':
                self.showHeroDetails(id)
            if classname == 'Synergy':
                self.showSynergyDetails(id)


            return True
        elif event.type() == QtCore.QEvent.Leave:
            self.hideDetails()
            return True
        return False

    #初始化界面
    def init_ui(self):
        self.setFixedSize(600,700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.title_widget = QtWidgets.QWidget()  # 创建上侧部件
        self.title_widget.setObjectName('title_widget')
        self.title_layout = QtWidgets.QGridLayout()  # 创建上侧部件的网格布局层
        self.title_widget.setLayout(self.title_layout) # 设置上侧部件布局为网格

        self.top_widget = QtWidgets.QWidget()  # 创建上侧部件
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QtWidgets.QGridLayout()  # 创建上侧部件的网格布局层
        self.top_widget.setLayout(self.top_layout) # 设置上侧部件布局为网格

        self.bottom_widget = QtWidgets.QWidget()  # 创建下侧部件
        self.bottom_widget.setObjectName('bottom_widget')
        self.bottom_layout = QtWidgets.QGridLayout()  # 创建下侧部件的网格布局层
        self.bottom_widget.setLayout(self.bottom_layout) # 设置下侧部件布局为网格

        self.showBaseItem_UI()

        self.main_layout.addWidget(self.title_widget,0,0,1,9)
        self.main_layout.addWidget(self.top_widget,1,0,1,9) # 上侧部件在第0行第0列，占1行9列
        self.main_layout.addWidget(self.bottom_widget,2,0,9,9) # 右侧部件在第1行第0列，占9行9列

        self.showItemBtn = QtWidgets.QPushButton("装备",self.main_widget)
        self.showItemBtn.setObjectName('showBtn')
        self.showItemBtn.setProperty("id","showItemBtn")
        self.showTiesBtn = QtWidgets.QPushButton("羁绊",self.main_widget)
        self.showTiesBtn.setObjectName('showBtn')
        self.showTiesBtn.setProperty("id","showTiesBtn")
        self.showHeroBtn = QtWidgets.QPushButton("英雄",self.main_widget)
        self.showHeroBtn.setObjectName('showBtn')
        self.showHeroBtn.setProperty("id","showHeroBtn")
        self.showSynergyBtn = QtWidgets.QPushButton("阵容",self.main_widget)
        self.showSynergyBtn.setObjectName('showBtn')
        self.showSynergyBtn.setProperty("id","showSynergyBtn")
        self.closeBtn = QtWidgets.QPushButton(qtawesome.icon('fa.times', color='#F76677'),"",self.main_widget)
        self.closeBtn.setObjectName('showBtn')
        self.closeBtn.setProperty("id","closeBtn")
        self.UpdateBtn = QtWidgets.QPushButton("更新",self.main_widget)
        self.UpdateBtn.setObjectName('showBtn')
        self.UpdateBtn.setProperty("id","UpdateBtn")
        self.showItemBtn.installEventFilter(self)
        self.showSynergyBtn.installEventFilter(self)
        self.showHeroBtn.installEventFilter(self)
        self.UpdateBtn.installEventFilter(self)
        self.closeBtn.installEventFilter(self)
        self.showTiesBtn.installEventFilter(self)
        self.showItemBtn.setGeometry(20, 45, 100, 25)
        self.showTiesBtn.setGeometry(130, 45, 100,25)
        self.showHeroBtn.setGeometry(240, 45, 100, 25)
        self.showSynergyBtn.setGeometry(350, 45, 100, 25)
        self.closeBtn.setGeometry(560, 45, 20, 20)
        self.UpdateBtn.setGeometry(490, 42, 60, 25)

        self.myName = QtWidgets.QLabel("【清枫冥月】制作",self.main_widget)
        self.myName.setGeometry(460, 54, 100, 25)

        self.main_widget.setStyleSheet('''
            QPushButton#showBtn{
                background:gray;
                border:1px solid darkGray;
                border-radius:10px;
            }
            QPushButton#showBtn:hover{
                border:0;
                background:white;
            }
            QWidget#top_widget{
                background:gray;
                border:1px solid white;
                border-radius:10px;
            }
            QWidget#bottom_widget{
               border:0;
            }
            QWidget#title_widget{
               border:0;
            }
        ''')


        self.setCentralWidget(self.main_widget) # 设置窗口主部件
        self.setWindowOpacity(0.3) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint) # 隐藏边框


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())