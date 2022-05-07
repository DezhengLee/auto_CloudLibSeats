import pickle
import os

fileName = 'Data.pkl'


class AccountInfo(object):
    def __init__(self):
        account_number: str = input('Your DUT number: ')
        password: str = input('Your password: ')
        email_address: str = input('Your E-mail address: ')
        email_verification_password: str = input('Your E-mail verification password: ')
        preferFloorOrder: str = input('Your preferred floor order, use \',\' to separate: ')
        self.__account_number: str = account_number
        self.__password: str = password
        self.__email_address: str = email_address
        self.__email_verification_password: str = email_verification_password
        self.__preferFloorOrder: list = eval('[' + preferFloorOrder + ', \'end\']')

    def checkInfo(self) -> bool:
        print('Please check your personal information: ')
        print('Account Number: ' + self.__account_number)
        print('Account Password: ' + self.__password)
        print('E-mail Address: ' + self.__email_address)
        print('E-mail Verification password: ' + self.__email_verification_password)
        print('Preferred Floor order: ' + str(self.__preferFloorOrder[0:-1]))
        verifyFlag: str = input('Are these information correct? Y/N: ')
        if verifyFlag == 'Y' or verifyFlag == 'y' or verifyFlag == 'yes':
            return True
        else:
            return False

    def getAccountNumber(self) -> str:
        return self.__account_number

    def getPassword(self) -> str:
        return self.__password

    def getEmailAddress(self) -> str:
        return self.__email_address

    def getEmailVPW(self) -> str:
        return self.__email_verification_password

    def getPreferredFloorOrder(self) -> list:
        return self.__preferFloorOrder

    def __str__(self) -> str:
        return 'AccountNo: ' + self.__account_number + ', PW: ' + self.__password + ', Email: ' + self.__email_address \
               + ', EmailVPW: ' + self.__email_verification_password + ', prefFloorOrder: ' + str(
            self.__preferFloorOrder) + '.'


def interfaceInputCheckInfo() -> AccountInfo:
    print('Please complete your personal information: ')
    Flag: bool = False
    temp: object = object
    while not Flag:
        temp: AccountInfo = AccountInfo()
        Flag = temp.checkInfo()
    return temp


def checkSavedDataInfo(USERINFO: AccountInfo) -> bool:
    print('Is this your account and your E-mail address?')
    print('Account number: ' + USERINFO.getAccountNumber())
    print('E-mail address: ' + USERINFO.getEmailAddress())
    print('Preferred floor order: ' + str(USERINFO.getPreferredFloorOrder()[0:-1]))
    Flag = input('Is these yours? Y/N:')
    if Flag == 'Y' or Flag == 'y' or Flag == 'yes':
        return True
    else:
        return False


def inputSaveUserInfoData(fileName: str) -> AccountInfo:
    userInfo: AccountInfo = interfaceInputCheckInfo()
    encodedUserinfo = pickle.dumps(userInfo)
    with open(fileName, 'wb') as file:
        file.write(encodedUserinfo)
    return userInfo


try:
    with open(fileName, 'rb') as file:
        USERINFO = pickle.load(file)
    if not checkSavedDataInfo(USERINFO):
        os.remove(fileName)
        USERINFO = inputSaveUserInfoData(fileName=fileName)
except FileNotFoundError:
    USERINFO = inputSaveUserInfoData(fileName=fileName)
