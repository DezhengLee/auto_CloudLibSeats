# -*- coding: utf-8 -*-
import requests
import random
import time
import numpy as np
import re

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

from urlFormatter import getFloor

mapArrayDic = {'4': ((4, 6), (11, 9)), '3': ((6, 7), (12, 8)), '2': ((2, 7), (12, 9)), '1': ((7, 11), (31, 14))}  #
# For N and W seats


def getResponseText(url: str, Cookie: str = '') -> str:
    useragentlist = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/78.0.3904.108Safari / 537.36"
    ]
    useragent = random.choice(useragentlist)
    head = {"User-Agent": useragent,
            "Cookie": Cookie
            }
    response = requests.get(url=url, headers=head)
    response.encoding = response.apparent_encoding
    html = response.text
    return html


def getSeatTable(libFloor: int, year: str, mon: str, day: str) -> np.ndarray:
    baseUrl = 'http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=querySeatMap&order_date=' + year + '%2F' + mon + '%2F' + day + '&room_id=' + getFloor(
        libFloor) + '&_='
    timeStample = str(int(time.time())) + '000'
    url = baseUrl + timeStample
    html = getResponseText(url)
    return np.array(eval(html))


def checkSeatAvl(libFloor: int, year: str, mon: str, day: str) -> list:
    seatTable = getSeatTable(libFloor, year, mon, day)
    if libFloor == 4:
        flag = '4'
    elif libFloor == 3:
        flag = '3'
    elif libFloor == 2:
        flag = '2'
    elif libFloor == 1:
        flag = '1'
    else:
        raise Exception('Invalid libFloor ' + str(libFloor) + '.')

    reslist = []
    arrayRowTuple = mapArrayDic[flag][0]
    arrayColTuple = mapArrayDic[flag][1]
    for i in range(arrayRowTuple[0], arrayColTuple[0] + 1):
        for j in range(arrayRowTuple[1], arrayColTuple[1] + 1):
            if seatTable[i][j]['seat_order_status'] == 1 and seatTable[i][j]['seat_type'] == '1':
                reslist.append([i + 1, j + 1, seatTable[i][j]["seat_label"]])
    return reslist


def getNextDayFloor_SeatNum(userAccNum: str, userPW: str) -> list:
    option = webdriver.ChromeOptions()
    option.add_argument("--auto-open-devtools-for-tabs")
    option.add_argument('--headless')
    driver = webdriver.Chrome(options=option)
    loginUrl = "https://sso.dlut.edu.cn/cas/login?service=http://seat.lib.dlut.edu.cn/yanxiujian/client/login.php?redirect=index.php"
    driver.get(loginUrl)
    driver.find_element(by=By.XPATH, value='//*[@id="un"]').send_keys(userAccNum)
    driver.find_element(by=By.XPATH, value='//*[@id="pd"]').send_keys(userPW)
    driver.find_element(by=By.XPATH, value='//*[@id="index_login_btn"]').click()
    time.sleep(0.3)
    baseUrl = 'http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=myOrderList&order=asc&offset=0&limit=1&_='
    timeStaple = str(int(time.time())) + '000'
    url = baseUrl + timeStaple
    driver.get(url)
    htmlText = driver.page_source
    res = [re.findall(r"\"space_name\":\"(.+?)\",\"seat_label", htmlText)[0],
           re.findall(r"\"seat_label\":\"(.+?)\",\"all_users", htmlText)[0]]
    driver.quit()
    return res


def chooseSeats(driver: selenium.webdriver.chrome.webdriver.WebDriver, seatCord: list) -> str:
    driver.find_element(by=By.XPATH, value='//*[@id="tb_departments"]/tbody/tr[' + str(seatCord[0]) + ']/td[' + str(
        seatCord[1]) + ']/div/i').click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value='//*[@id="btn_submit_addorder"]').click()
    time.sleep(2)
    dialogText = driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/div[2]/div').get_property(
        'innerText')
    return dialogText


def successCheck(dialogText: str) -> bool:
    if dialogText == '预约成功！' or dialogText == '已经存在预约记录，不能重复预约！':
        return True
    else:
        return False


'''
Update: 2022/5/4, 14:01
Add functions:
Add a tabu list to ban unwanted seats.
Add a method to check if the popped seat is unwanted seat and then pop/not pop this seat.
'''
tabuSeat = {'4': {'N01': False, 'N02': False, 'N03': False, 'N04': False, 'N05': False, 'N06': True, 'N07': True,
                  'N08': True, 'N09': True, 'N10': True, 'N11': True, 'N12': False, 'N13': False, 'N14': False,
                  'N15': False, 'N16': False, 'N17': False, 'N18': False, 'N19': False, 'N20': False, 'N21': False,
                  'N22': False, 'N23': False, 'N24': False, 'N25': False, 'N26': False, 'N27': False, 'N28': False,
                  'N29': False, 'N30': False, 'N31': False, 'N32': False},

            '3': {'N01': False, 'N02': False, 'N03': False, 'N04': False, 'N05': False, 'N06': False, 'N07': False,
                  'N08': False, 'N09': False, 'N10': False, 'N11': False, 'N12': False, 'N13': False, 'N14': False,
                  'N15': False, 'N16': False, 'N17': False, 'N18': False, 'N19': False, 'N20': False, 'N21': False,
                  'N22': False, 'N23': False, 'N24': False, 'N25': False, 'N26': False, 'N27': False, 'N28': False},

            '2': {'N01': False, 'N02': False, 'N03': False, 'N04': False, 'N05': False, 'N06': False, 'N07': False,
                  'N08': False, 'N09': False, 'N10': False, 'N11': False, 'N12': False, 'N13': False, 'N14': False,
                  'N15': False, 'N16': False, 'N17': False, 'N18': False, 'N19': False, 'N20': False, 'N21': False,
                  'N22': False, 'N23': False},

            '1': {'W01-1': False, 'W01-2': False, 'W01-3': False, 'W01-4': False, 'W02-1': False, 'W02-2': False,
                  'W02-3': False, 'W02-4': False, 'W03-1': False, 'W03-2': False, 'W03-3': False, 'W03-4': False,
                  'W04-1': False, 'W04-2': False, 'W04-3': False, 'W04-4': False, 'W05-1': False, 'W05-2': False,
                  'W05-3': False, 'W05-4': False, 'W06-1': False, 'W06-2': False, 'W06-3': False, 'W06-4': False,
                  'W07-1': False, 'W07-2': False, 'W07-3': False, 'W07-4': False, 'W08-1': False, 'W08-2': False,
                  'W08-3': False, 'W08-4': False, 'W09-1': False, 'W09-2': False, 'W09-3': False, 'W09-4': False,
                  'W10-1': False, 'W10-2': False, 'W10-3': False, 'W10-4': False, 'W11-1': False, 'W11-2': False,
                  'W11-3': False, 'W11-4': False, 'W12-1': False, 'W12-2': False, 'W12-3': False, 'W12-4': False,
                  'W13-1': False, 'W13-2': False, 'W13-3': False, 'W13-4': False, 'W14-1': False, 'W14-2': False,
                  'W14-3': False, 'W14-4': False, 'W15-1': False, 'W15-2': False, 'W15-3': False, 'W15-4': False,
                  'W16-1': False, 'W16-2': False, 'W16-3': False, 'W16-4': False, 'W17-1': False, 'W17-2': False,
                  'W17-3': False, 'W17-4': False, 'W18-1': False, 'W18-2': False, 'W18-3': False, 'W18-4': False,
                  'W19-1': False, 'W19-2': False, 'W19-3': False, 'W19-4': False, 'W20-1': False, 'W20-2': False,
                  'W20-3': False, 'W20-4': False, 'W21-1': False, 'W21-2': False, 'W21-3': False, 'W21-4': False,
                  'W22-1': False, 'W22-2': False, 'W22-3': False, 'W22-4': False, 'W23-1': False, 'W23-2': False,
                  'W23-3': False, 'W23-4': False, 'W24-1': False, 'W24-2': False, 'W24-3': False, 'W24-4': False,
                  'W25-1': False, 'W25-2': False, 'W25-3': False, 'W25-4': False, 'W26-1': False, 'W26-2': False,
                  'W26-3': False, 'W26-4': False, 'W27-1': False, 'W27-2': False, 'W27-3': False, 'W27-4': False,
                  'W28-1': False, 'W28-2': False, 'W28-3': False, 'W28-4': False, 'W29-1': False, 'W29-2': False,
                  'W29-3': False, 'W29-4': False}
            }


def checkTabuSeatPop(floor: int, altSeat: list) -> list:
    tempSeat = altSeat.pop(0)
    temp_seat_label = tempSeat[2]
    floorFlag = str(floor)
    TBSFloorDic = tabuSeat[floorFlag]
    while TBSFloorDic[temp_seat_label] and not len(altSeat) == 0:
        tempSeat = altSeat.pop(0)
    return tempSeat


'''
Update: 2022/5/7, 10:19
Add functions:
method: login(), concentrated login module
'''


def login(driver: selenium.webdriver.chrome.webdriver.WebDriver, userAccNum: str, userPW: str):
    loginUrl = "https://sso.dlut.edu.cn/cas/login?service=http://seat.lib.dlut.edu.cn/yanxiujian/client/login.php?redirect=index.php"
    driver.get(loginUrl)
    driver.find_element(by=By.XPATH, value='//*[@id="un"]').send_keys(userAccNum)
    driver.find_element(by=By.XPATH, value='//*[@id="pd"]').send_keys(userPW)
    driver.find_element(by=By.XPATH, value='//*[@id="index_login_btn"]').click()
    time.sleep(0.8)
