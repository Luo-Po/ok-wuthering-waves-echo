#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def scroll_echo_list(task, direction: str = "down", amount: int = 3) -> bool:
    """
    滚动回音列表
    
    参数:
        task: 任务对象，用于执行滚动和睡眠操作
        direction (str): 滚动方向，可选值为 "down"（向下）或 "up"（向上），默认为 "down"
        amount (int): 滚动量，默认为 3
    
    返回:
        bool: 始终返回 True，表示滚动操作已执行
    """
    if direction == "down":
        task.scroll(930, 693, -amount)
        task.sleep(0.2)
    elif direction == "up":
        task.scroll(930, 693, amount)
        task.sleep(0.2)

    return True


def click_echo_box(task, x: int, y: int):
    """
    点击指定位置的回音框
    
    参数:
        task: 任务对象，用于执行点击操作
        x (int): 回音框的列索引（1-6）
        y (int): 回音框的行索引（1-4）
    
    返回:
        bool: 始终返回 True，表示点击操作已执行
    """
    xls = {
        1: 278,
        2: 500,
        3: 722,
        4: 945,
        5: 1167,
        6: 1389
    }
    xrs = {
        1: 470,
        2: 692,
        3: 914,
        4: 1137,
        5: 1359,
        6: 1581
    }
    yts = {
        1: 166,
        2: 439,
        3: 713,
        4: 986
    }
    ybs = {
        1: 400,
        2: 674,
        3: 947,
        4: 1220
    }
    cx = int((xls[x] + xrs[x]) / 2)
    cy = int((yts[y] + ybs[y]) / 2)
    task.click(x=cx, y=cy)
    return True
