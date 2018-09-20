from lxml import etree
import requests
import time

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}
start_url = "http://piao.qunar.com/"

def get_city(url):
    response = requests.get(url,headers=headers).text
    # print(response)
    mytree = etree.HTML(response)
    cityList = mytree.xpath('//div[@class="mp-sidebar-section"]/ul//li/a/text()')
    cityUrlList = mytree.xpath('//div[@class="mp-sidebar-section"]/ul//li/a/@href')
    cityUrlList1 = []
    for cityUrl in cityUrlList:
        cityUrl = 'http://piao.qunar.com'+cityUrl
        cityUrlList1.append(cityUrl)
    cityInfoList = list(zip(cityList,cityUrlList1))
    cityInfoList = cityInfoList[:20]
    # print(cityList,cityUrlList1)
    return cityInfoList

def get_travel_message(url):
    response = requests.get(url, headers=headers).text

    mytree = etree.HTML(response)

    mp_charact_desc = mytree.xpath('//div[@id="mp-charact"]/div/div[@class="mp-charact-intro"]/div[@class="mp-charact-desc"]/p/text()')
    mp_charact_timeList = mytree.xpath('//div[@id="mp-charact"]/div/div[@class="mp-charact-time"]/div[@class="mp-charact-content"]/div[@class="mp-charact-desc"]/p/text()')
    mp_characteristic_imgUrlList = mytree.xpath('//div[@id="mp-charact"]/div/div[@class="mp-charact-event"]/div[@class="mp-event"]/img/@src')
    mp_characteristic_imgNameList = mytree.xpath('//div[@id="mp-charact"]/div/div[@class="mp-charact-event"]/div[@class="mp-event"]/img/@alt')
    mp_characteristic_img_descList = mytree.xpath('//div[@id="mp-charact"]/div/div[@class="mp-charact-event"]/div[@class="mp-event"]/div[@class="mp-event-desc"]/p/text()')
    mp_littletips_titleList = mytree.xpath('//div[@id="mp-charact"]/div[@class="mp-charact-littletips"]/div[@class="mp-littletips"]/h2/text()')
    mp_littletips_itemTitleList = mytree.xpath('//div[@id="mp-charact"]/div[@class="mp-charact-littletips"]/div[@class="mp-littletips"]/div[@class="mp-littletips-item"]/div[@class="mp-littletips-itemtitle"]/text()')
    mp_littletips_itemList = mytree.xpath('//div[@id="mp-charact"]/div[@class="mp-charact-littletips"]/div[@class="mp-littletips"]/div[@class="mp-littletips-item"]/div[@class="mp-littletips-desc"]/p/text()')
    mp_transfer_titleList = mytree.xpath('//div[@id="mp-traffic"]/div[@class="mp-traffic-transfer"]/div[@class="mp-transfer-title"]/text()')
    mp_transfer_title_descList = mytree.xpath('//div[@id="mp-traffic"]/div[@class="mp-traffic-transfer"]/div[@class="mp-transfer-desc"]/text()')
    mpList = [mp_charact_desc,mp_charact_timeList,mp_characteristic_imgUrlList,mp_characteristic_imgNameList,
              mp_characteristic_img_descList,mp_littletips_titleList,mp_littletips_itemTitleList,
              mp_littletips_itemList,mp_transfer_titleList,mp_transfer_title_descList]
    return mpList

def get_city_travel(city,url):
    response = requests.get(url, headers=headers).text
    # print(response)
    mytree = etree.HTML(response)
    dataId = mytree.xpath('//div[@id="sku-menu"]/a/@data-type-id')
    recommendList = mytree.xpath('//div[@id="sku-menu"]/a/text()')
    recommendInfo = list(zip(dataId,recommendList))
    # print(dataId)
    # print(recommendInfo)
    dataIdList = []
    for id in dataId:
        # print(id)
        jsUrl = "http://piao.qunar.com/ticket/list.json?keyword={}&region=&from=mps_search_suggest&sku={}&page=1&subject=&sort=pp".format(city,id)
        # print(jsUrl)
        data = requests.get(jsUrl)
        data = data.json()
    #     # print(data)
        dataList = data['data']['sightList']
        # print(dataList)
        for msg in dataList:
            sightId = msg.get('sightId')
            dataIdList.append(sightId)
    # print(len(dataIdList))
    allPlaceInfoList = []
    valuesList = []
    i = 0
    for item in recommendInfo:
        # print(key,values)
        # print(len(recommendInfo))
        placeInfoList = []
        categoryUrl = 'http://piao.qunar.com/ticket/list.htm?keyword={}&from=mpshouye_hotcity&sku={}&page=1&subject='.format(city,item[0])
        # print(categoryUrl)
        res = requests.get(categoryUrl).text
        # print(res)
        mytree1 = etree.HTML(res)

        travelInfoList = mytree1.xpath('//div[@id="search-list"]/div/div')
        # print(len(travelInfoList))
        for travelInfo in travelInfoList:
            nameUrl = travelInfo.xpath('./div[@class="sight_item_about"]/h3/a/@href')[0]
            nameUrl = 'http://piao.qunar.com'+nameUrl
            name = travelInfo.xpath('./div[@class="sight_item_about"]/h3/a/text()')[0]
            starList = travelInfo.xpath('./div[@class="sight_item_about"]/div/div[@class="clrfix"]/span[@class="level"]/text()')
            if starList:
                star = starList[0]
            else:
                star = None
            area = travelInfo.xpath('./div[@class="sight_item_about"]/div/div[@class="clrfix"]/span[@class="area"]/a/text()')[0]
            address = travelInfo.xpath('./div[@class="sight_item_about"]/div/p/span/@title')[0]
            priceList = travelInfo.xpath('./div[@class="sight_item_pop"]/table/tr/td/span[@class="sight_item_price"]/em/text()')
            if priceList:
                price = priceList[0]
            else:
                price = None
            salesList = travelInfo.xpath('./div[@class="sight_item_pop"]/table/tr/td[@class="sight_item_sold-num"]/span/text()')
            if salesList:
                sales = salesList[0]
            else:
                sales = None
            describeList = travelInfo.xpath('./div[@class="sight_item_about"]/div/div[@class="intro"]/@title')
            if describeList:
                describe = describeList[0]
            else:
                describe = None
            # print("*********")
            # starTime = time.time()
            # print(starTime)
            mpList = get_travel_message(nameUrl)
            i +=156
            # print(time.time()-starTime)
            # print("********")
            placeInfoList.append([name, star, area, address, price, sales, describe,mpList])
        # print(placeInfoList)
        allPlaceInfoList.append({item[1]:placeInfoList})
        valuesList.append(item[1])
    return valuesList,allPlaceInfoList





cityList = get_city(start_url)
# print(cityList)
for item in cityList:
    # print(item[0],item[1])
    valuesList, placeInfoList = get_city_travel(item[0],item[1])
    print(placeInfoList)
            # commentlist =

