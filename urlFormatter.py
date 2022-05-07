import datetime


def getDate(nextDay: bool) -> list:
    if nextDay:
        delta = 1
    else:
        delta = 0

    dateNow = datetime.datetime.now()

    dateNowYear = (dateNow  + datetime.timedelta(days=+delta)).strftime('%Y')
    dateNowMonth = (dateNow  + datetime.timedelta(days=+delta)).strftime('%m')
    if dateNowMonth[0] == '0':
        dateNowMonth = dateNowMonth[1]
    dateNowDay = (dateNow  + datetime.timedelta(days=+delta)).strftime('%d')
    if dateNowDay[0] == '0':
        dateNowDay = dateNowDay[1]

    return [dateNowYear, dateNowMonth, dateNowDay]


def getFormattedDate(nextDay: bool) -> str:
    dateRes = getDate(nextDay)
    return dateRes[0] + '/' + dateRes[1] + '/' + dateRes[2]


def getFloor(libFloor: int) -> str:
    if libFloor <= 0 or libFloor >= 5:
        raise Exception('Library Floor exceed bound. Floor should within 2 to 4.')
    roomIdCode = ['191', '192', '193', '182']
    return roomIdCode[libFloor - 2]


def getUrlSeatSelecting(libFloor: int, nextDay: bool) -> str:
    return 'http://seat.lib.dlut.edu.cn/yanxiujian/client/orderSeat.php?method=addSeat&room_id=' + getFloor(libFloor) + '&area_id=35&curdate=' + getFormattedDate(nextDay)