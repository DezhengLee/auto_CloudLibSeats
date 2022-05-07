import pickle
import os
import AccountInfo


fileName = 'Data.pkl'

try:
    with open(fileName, 'rb') as file:
        USERINFO = pickle.load(file)
    if not AccountInfo.checkSavedDataInfo(USERINFO):
        os.remove(fileName)
        USERINFO: AccountInfo = AccountInfo.inputSaveUserInfoData(fileName=fileName)
except FileNotFoundError:
    USERINFO: AccountInfo = AccountInfo.inputSaveUserInfoData(fileName=fileName)

print(USERINFO)