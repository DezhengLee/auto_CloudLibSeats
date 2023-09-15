from selenium import webdriver
import time
import datetime
import schedule

import urlFormatter as uf
import urlTools as ut
import mailTool as mt
from AccountInfo import USERINFO

nextDay = True


def work():
    startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    errorFlag = True
    retryMax = 15
    retryCounter = 0
    errorMassage = 'No Error.'
    while errorFlag and retryCounter <= retryMax:
        errorFlag = False
        try:
            driver = webdriver.Chrome()
            # Login
            ut.login(driver=driver, userAccNum=USERINFO.getAccountNumber(), userPW=USERINFO.getPassword())
            loginTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Select Seat
            successFlag = False
            altSeats = []

            prefFOrderList = USERINFO.getPreferredFloorOrder()
            libFloor = prefFOrderList.pop(0)
            dateVec = uf.getDate(nextDay=nextDay)

            while not successFlag and not libFloor == 'end':
                seatSelUrl = uf.getUrlSeatSelecting(libFloor, nextDay=nextDay)
                driver.get(seatSelUrl)
                time.sleep(0.9)
                # get all available seats
                altSeats.extend(ut.checkSeatAvl(libFloor, dateVec[0], dateVec[1], dateVec[2]))
                time.sleep(0.9)
                if len(altSeats) == 0:
                    libFloor = prefFOrderList.pop(0)
                else:
                    tempSeat = ut.checkTabuSeatPop(floor=libFloor, altSeat=altSeats)
                    dialogText = ut.chooseSeats(driver=driver, seatCord=tempSeat)
                    successFlag = ut.successCheck(dialogText=dialogText)
                    time.sleep(1)
            driver.quit()
        except Exception as e:
            errorFlag = True
            retryCounter += 1
            errorMassage = 'Error raised: ' + str(e) + '.'
            altSeats = []
            loginTime = ''
            dialogText = ''
            successFlag = False
            print(errorMassage)
    endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check the reserved seat number
    floor_seat = ut.getNextDayFloor_SeatNum(userAccNum=USERINFO.getAccountNumber(), userPW=USERINFO.getPassword())

    if successFlag == True:
        resultStr = 'Get a Seat for next day.'
        mailText = 'Server Response: ' + dialogText + ' 座位号为: ' + floor_seat[0] + ' ' + floor_seat[1] + ' ' \
                   + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' , works well. Start at ' + startTime \
                   + ', login at ' + loginTime + ', end at ' + endTime + '. Result: Successful. ' + errorMassage
        mt.mailAndCheck(mailText=mailText, mailSubject=mailText, mailSender=USERINFO.getEmailAddress(),
                        mailVPW=USERINFO.getEmailVPW())
    else:
        if len(altSeats) == 0:
            resultStr = 'Didn\'t get a Seat for next day, as there is no sufficient seats.'
            mailText = 'Server Response: ' + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + ' , works well. Start at ' + startTime + ', login at ' + loginTime + ', end at ' + endTime + '. Result: Unsuccessful,  no sufficient seat. ' + errorMassage
            mt.mailAndCheck(mailText=mailText, mailSubject=mailText, mailSender=USERINFO.getEmailAddress(),
                            mailVPW=USERINFO.getEmailVPW())
        else:
            resultStr = 'Didn\'t get a Seat for next day, for unknown reason.'
            mailText = 'Server Response: ' + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + ' , works well. Start at ' + startTime + ', login at ' + loginTime + ', end at ' + endTime + '. Result: Unsuccessful, unknown reason. ' + errorMassage
            mt.mailAndCheck(mailText=mailText, mailSubject=mailText, mailSender=USERINFO.getEmailAddress(),
                            mailVPW=USERINFO.getEmailVPW())
    print('Program Finished, ' + resultStr + ' ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


schedule.every().day.at("06:29:52").do(work)
while True:
    schedule.run_pending()  
    time.sleep(1) 

