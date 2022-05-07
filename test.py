# import random
#
# import re
#
# import lxml as lxml
# import requests
# import datetime
# #
# # dateYear = datetime.now().strftime('%Y')
# # dateMonth = datetime.now().strftime('%m')
# # if dateMonth[0] == '0':
# #     dateMonth = dateMonth[1]
# # dateDay = datetime.now().strftime('%d')
# # if dateDay[0] == '0':
# #     dateDay = dateDay[1]
# #
# # dateCode = dateYear + '\\' + dateMonth + '\\' + dateDay
# #
# # roomIdCode = ['191', '192', '193']  # 191：二楼， 192：三楼，193：四楼
# #
# # a = [[1, 2, 3], [2, 2, 3], [1, 2, 3]]
# # print(a[0:2][0:1])
#
# # from selenium import webdriver
# # import time
# # driver = webdriver.Chrome()
# # driver.get('https://www.baidu.com')
# # time.sleep(10)
# # driver.get('https://www.bilibili.com')
# # time.sleep(15)
#
# # a = '{"total":"197","rows":[{"order_id":"3097655","order_type":"2","space_name":"盘锦图书馆二层阅览室","seat_label":"A02-3","all_users":null,"order_start_time":"2022-04-24 08:00:00","area_id":"35","order_date":"2022-04-24","back_time":"00:00:00","order_end_time":"未完成","order_users":"201926038","order_admin_user":"201926038","order_time":"2022-04-23 20:24:43","order_process":"审核通过","punish_status":"0"}]}'
# # a = a.replace('"all_users":null,', '')
# # a = eval(a)
# # temp = a['rows'][0]
# # print(temp['seat_label'])
# # print(temp["order_date"])
# # t = (datetime.datetime.now() + datetime.timedelta(days=+0)).strftime('%Y-%m-%d')
# # print(t)
# # print(t == temp["order_date"])
# #
# # print('dd'+datetime.datetime.now().strftime('%Y-%m-%d'))
#
# from selenium import webdriver
# import time
# import pyperclip
# from selenium.webdriver.common.by import By
#
# import keysOperation as kon
# import urlFormatter as uf
# import urlTools as ut
# import datetime
# import schedule
#
#
# # driver = webdriver.Chrome()
# # option = webdriver.ChromeOptions()
# # option.add_argument("--auto-open-devtools-for-tabs")
# # driver = webdriver.Chrome(chrome_options=option)
# #
# # ######################## Login Block ########################
# # loginUrl = "https://sso.dlut.edu.cn/cas/login?service=http://seat.lib.dlut.edu.cn/yanxiujian/client/login.php?redirect=index.php"
# # driver.get(loginUrl)
# # time.sleep(1)
# #
# # kon.comboKeys(17, 192)  # 打开devtools的Console
# # pyperclip.copy('document.getElementById(\'un\').value = 201926038;document.getElementById(\'pd\').value = \'QwQX97^3\'; document.getElementById(\'index_login_btn\').click()')
# # time.sleep(0.3)
# #
# # kon.comboKeys(17, 86)  # Ctrl + v
# # time.sleep(0.3)
# #
# # kon.tapKey(13)  # Enter
# # time.sleep(1)
# # cookie = driver.get_cookie('PHPSESSID')
# #
# # baseUrl = 'http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=myOrderList&order=asc&offset=0&limit=1&_='
# # timeStample = str(int(time.time())) + '000'
# # url = baseUrl + timeStample
# # # driver.get(url)
# # time.sleep(2)
# #
# # useragentlist = [
# #         "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
# #         "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
# #         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
# #         "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
# #         "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
# #         "Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/78.0.3904.108Safari / 537.36"
# #     ]
# # useragent = random.choice(useragentlist)
# # head = {"User-Agent": useragent,
# #         "Cookie": cookie['name'] + '=' + cookie['value']
# #         }
# # response = requests.get(url=url, headers=head)
# # print(response.text)
# # driver.quit()
#
# # 检查预约到的座位号
# libFloor = 4
# nextDay = True
# altSeats = []
#
# dateVec = uf.getDate(nextDay=nextDay)
#
# option = webdriver.ChromeOptions()
# option.add_argument("--auto-open-devtools-for-tabs")
# # option.add_argument('--headless')
# driver = webdriver.Chrome(options=option)
# loginUrl = "https://sso.dlut.edu.cn/cas/login?service=http://seat.lib.dlut.edu.cn/yanxiujian/client/login.php?redirect=index.php"
# driver.get(loginUrl)
# print(type(driver))
# driver.find_element(by=By.XPATH, value='//*[@id="un"]').send_keys('201926038')
# driver.find_element(by=By.XPATH, value='//*[@id="pd"]').send_keys('QwQX97^3')
# driver.find_element(by=By.XPATH, value='//*[@id="index_login_btn"]').click()
# time.sleep(0.1)
#
#
# seatSelUrl = uf.getUrlSeatSelecting(libFloor, nextDay=nextDay)
# driver.get(seatSelUrl)
# time.sleep(0.3)
# altSeats.extend(ut.checkSeatAvl(libFloor, dateVec[0], dateVec[1], dateVec[2]))
# tempSeat = altSeats.pop()
# tempSeat = altSeats.pop()
# print(tempSeat)
# driver.find_element(by=By.XPATH, value='//*[@id="tb_departments"]/tbody/tr[' + str(tempSeat[0]) + ']/td[' + str(tempSeat[1]) + ']/div/i').click()
# print(altSeats)
# time.sleep(0.5)
# driver.find_element(by=By.XPATH, value='//*[@id="btn_submit_addorder"]').click()
# time.sleep(1)
# html = driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/div[2]/div')
# print(html.get_property('innerText'))
# time.sleep(1000)
#
#
# # baseUrl = 'http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=myOrderList&order=asc&offset=0&limit=1&_='
# # timeStample = str(int(time.time())) + '000'
# # url = baseUrl + timeStample
# # driver.get(url)
# # htmlText = driver.page_source
# # res = [re.findall(r"\"space_name\":\"(.+?)\",\"seat_label", htmlText)[0], re.findall(r"\"seat_label\":\"(.+?)\",\"all_users", htmlText)[0]]
# # print(res[0])
# # print(res[1])
# driver.quit()
#
# from AccountInfo import USERINFO
# print(USERINFO)
# print(USERINFO)
# print(USERINFO)
# with open('dfa.pkl') as f:
#     print(f)

for i in range(1, 30):
    for j in range(1, 5):
        if i < 10:
            temp = '0' + str(i)
        else:
            temp = str(i)
        print('\'W' + temp + '-' + str(j) + '\': False, ')