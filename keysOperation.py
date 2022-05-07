import win32api
import win32con


def comboKeys(key1: int, key2: int):
    win32api.keybd_event(key1, 0, 0, 0)
    win32api.keybd_event(key2, 0, 0, 0)
    win32api.keybd_event(key2, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(key1, 0, win32con.KEYEVENTF_KEYUP, 0)


def tapKey(key: int):
    win32api.keybd_event(key, 0, 0, 0)
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
