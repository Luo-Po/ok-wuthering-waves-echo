#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import win32con
import win32gui


def get_active_window():
    """
    获取当前活动窗口的句柄
    
    返回:
        int: 当前活动窗口的句柄
    """
    return win32gui.GetForegroundWindow()


def set_window_topmost(hwnd: int, topmost: bool = True):
    """
    设置窗口置顶状态
    
    参数:
        hwnd (int): 窗口句柄
        topmost (bool): True=置顶, False=取消置顶
    """
    flag = win32con.HWND_TOPMOST if topmost else win32con.HWND_NOTOPMOST
    win32gui.SetWindowPos(
        hwnd,
        flag,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )


def is_window_topmost(hwnd: int) -> bool:
    """
    检查窗口是否置顶
    
    参数:
        hwnd (int): 窗口句柄
    
    返回:
        bool: 如果窗口置顶则返回True，否则返回False
    """
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    return bool(style & win32con.WS_EX_TOPMOST)
