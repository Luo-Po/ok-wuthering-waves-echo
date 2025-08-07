#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import List

from ok import Box

from src.Echo import Echo, EchoAttr
from src.data import cost_list
from src.echo_scorer import sum_sub_scores, sum_main_score

# 属性映射字典，将游戏中显示的属性名称映射为内部使用的属性名称
cases = {
    "攻击": "大攻击",
    "生命": "大生命",
    "防御": "大防御",
    "共鸣效率": "共鸣效率",
    "普攻伤害加成": "普攻伤害",
    "重击伤害加成": "重击伤害",
    "共鸣技能伤害加成": "技能伤害",
    "共鸣解放伤害加成": "解放伤害",
    "暴击伤害": "暴伤",
    "暴击": "暴击",
    "治疗效果加成": "治疗",
    "衍射伤害加成": "属伤",
    "行射伤害加成": "属伤",
    "气动伤害加成": "属伤",
    "热熔伤害加成": "属伤",
    "冷凝伤害加成": "属伤",
    "灭伤害加成": "属伤",
    "湮灭伤害加成": "属伤",
    "导电伤害加成": "属伤",
}

# 界面元素坐标区域字典，定义游戏中各个界面元素的位置和大小
box_list = {
    "page": Box(0, 0, to_x=700, to_y=300),
    "echo_change": {
        "name": Box(1880, 195, to_x=2426, to_y=240),
        # "cost": Box(1894, 233, to_x=2051, to_y=285),
        "level": Box(1880, 278, to_x=1968, to_y=311),
        "main": Box(1930, 307, to_x=2436, to_y=417),
        "sub": Box(1930, 411, to_x=2436, to_y=643)
    },
    "echo_upgrade": {
        "name": Box(251, 152, to_x=635, to_y=201),
        "level": Box(230, 229, to_x=325, to_y=290),
        "main": Box(287, 312, to_x=918, to_y=372),
        "sub": Box(287, 422, to_x=918, to_y=704)
    },
    "bag_echos": {
        "name": Box(1738, 154, to_x=2469, to_y=227),
        "level": Box(2349, 322, to_x=2449, to_y=382),
        "sonata": Box(1923, 424, 28, 28),
        "main": Box(1827, 566, to_x=2450, to_y=677),
        "sub": Box(1827, 681, to_x=2450, to_y=960)
    }

}

# 正则表达式匹配字典，用于识别游戏中的各种文本信息
match_list = {
    "cost": re.compile(
        r'^COST [134]$'),
    "level": re.compile(
        r'^\+([0-9]|1[0-9]|2[0-5])$'),
    "main": re.compile(
        r'^((.*\d{1,3}(?:\.\d%)?)|暴击|暴击伤害|攻击|生命|防御|共鸣效率|治疗效果加成|((([衍行])射|气动|热熔|冷凝|(湮灭|灭)|导电)伤害加成))$'),
    "sub": re.compile(
        r'^((.*\d{1,3}(?:\.\d%)?)|暴击|暴击伤害|攻击|生命|防御|共鸣效率|((普攻|重击|共鸣技能|共鸣解放)伤害加成))$'),
    "page": re.compile(
        r'^(属性详情|武器|技能|共鸣链|档案|数据坞|声骸图鉴|合鸣图鉴|数据融合|数据重构|声骸强化|声骸调谐|COST|((武器|声骸|补给|资源|素材|任务|特殊)|\d{1,4}/[123]000))$')
}

sonata_list = [
    "凝夜白霜",
    "熔山裂谷",
    "浮星祛暗",
    "沉日劫明",
    "啸谷长风",
    "彻空冥雷",
    "不绝余音",
    "轻云出月",
    "隐世回光",
    "凌冽决断之心",
    "高天共奏之曲",
    "此间永驻之光",
    "幽夜隐匿之帷",
    "无惧浪涛之勇",
    "流云逝尽之空",
    "奔狼燎原之焰",
    "愿戴荣光之旅",
    "失序彼岸之梦"
]

# 页面映射字典，将游戏中显示的页面名称映射为内部使用的页面标识
pages = {
    "属性详情": "role_attr",
    "武器": "role_weapon",
    "声骸": "role_echo",
    "技能": "role_forte",
    "共鸣链": "role_chain",
    "档案": "role_information",
    "武器1/2000": "bag_weapons",
    "声骸1/3000": "bag_echos",
    "补给1/1000": "bag_supplies",
    "资源1/1000": "bag_materials",
    "素材1/1000": "bag_resources",
    "任务1/1000": "bag_quest_items",
    "特殊1/1000": "bag_valuables",
    "数据坞": "data_bank",
    "声骸图鉴": "echo_gallery",
    "合鸣图鉴": "sonata_gallery",
    "数据融合": "echo_merge",
    "数据重构": "echo_modify",
    "声骸强化": "echo_upgrade",
    "声骸调谐": "echo_tuning",
    "COST": "echo_change"
}


def is_page(task, page):
    """
    检查当前页面是否为指定页面
    
    参数:
        task: 任务对象，用于执行OCR操作
        page (str): 要检查的页面标识
    
    返回:
        bool: 如果当前页面是指定页面则返回True，否则返回False
    """
    return page == which_page(task)


def which_page(task) -> str:
    """
    获取当前页面的标识
    
    参数:
        task: 任务对象，用于执行OCR操作
    
    返回:
        str: 当前页面的标识，如果无法识别则返回空字符串
    """
    page_boxs = task.ocr(match=match_list["page"], box=box_list["page"])
    if len(page_boxs) == 0:
        return ""
    elif len(page_boxs) == 1:
        page = page_boxs[0].name
    else:
        if re.match(r'\d{1,3}/[123]000', page_boxs[1].name):
            page = page_boxs[0].name + page_boxs[1].name
        else:
            page = page_boxs[0].name

    page = pages[re.sub(r'(\d+/)', "1/", page)]
    return page


def ocr_echo(task, page) -> Echo:
    """
    从游戏界面扫描并解析声骸(回声)数据
    
    参数:
        task: 任务对象，用于执行OCR操作和获取角色信息
        page (str): 页面标识，指定要扫描的页面类型
    
    返回:
        Echo: 解析后的声骸(回声)对象，如果解析失败则返回空对象
    """
    echo = Echo()
    try:
        name = ocr_name(task, page).replace("梦魔", "梦魇")
        echo.set_name(name)
        task.log_info(f'name: {name}')
        # print(f'{name}')
        cost = 0
        for b in cost_list:
            if b["name"] == name:
                cost = b["type"]
        echo.set_cost(cost)
        # print(f'{cost}')
        level = ocr_level(task, page)
        echo.set_level(level)
        # print(f'{level}')
        main_attr = ocr_main(task, page)
        echo.set_main(main_attr)
        # print(f'{main_attr}')
        sub_attrs = ocr_sub_attr(task, page)
        echo.set_sub_attrs(sub_attrs)
        # print(f'{sub_attrs}')
        if page == "bag_echos":
            sonata = ocr_sonata(task, page)
            echo.set_sonata(sonata)
        else:
            role = task.role

            main_score = sum_main_score(echo, role)
            echo.set_main_score(main_score)

            sub_score = sum_sub_scores(echo, role)
            echo.set_sub_score(sub_score)

            score = main_score + sub_score
            echo.set_score(score)


    except BaseException as e:
        print(f'ocr_echo failed for {e.args}')
    return echo


def ocr_name(task, page, i=0) -> str:
    """
    从游戏界面扫描并解析声骸(回声)名称
    
    参数:
        task: 任务对象，用于执行OCR操作
        page (str): 页面标识，指定要扫描的页面类型
        i (int): 递归重试次数，默认为0
    
    返回:
        str: 解析后的声骸(回声)名称
    
    异常:
        BaseException: 如果重试4次后仍解析失败则抛出异常
    """
    try:
        name_boxs = task.ocr(box=box_list[page]["name"])
        name = name_boxs[0].name

    except BaseException:
        if i == 4:
            raise
        name = ocr_name(task, page, i + 1)
    return name


def ocr_sonata(task, page, i=0) -> str:
    try:
        sonata = ""
        for s in sonata_list:
            sonata_box = task.find_one(s, box=box_list[page]["sonata"])
            if sonata_box is not None:
                sonata = sonata_box.name
        if sonata == "":
            raise
    except BaseException as e:
        if i == 4:
            raise
        sonata = ocr_sonata(task, page, i + 1)

    return sonata


def ocr_level(task, page, i=0):
    """
    从游戏界面扫描并解析声骸(回声)等级
    
    参数:
        task: 任务对象，用于执行OCR操作
        page (str): 页面标识，指定要扫描的页面类型
        i (int): 递归重试次数，默认为0
    
    返回:
        int or None: 解析后的声骸(回声)等级，如果重试4次后仍解析失败则返回None
    """
    try:
        level_boxs = task.ocr(box=box_list[page]["level"])
        return int(level_boxs[0].name.lstrip('+'))
    except BaseException:
        if i == 4:
            return None
        return ocr_level(task, page, i + 1)


def ocr_main(task, page, i=0):
    """
    从游戏界面扫描并解析声骸(回声)主属性
    
    参数:
        task: 任务对象，用于执行OCR操作
        page (str): 页面标识，指定要扫描的页面类型
        i (int): 递归重试次数，默认为0
    
    返回:
        EchoAttr or None: 解析后的声骸(回声)主属性对象，如果重试4次后仍解析失败则返回None
    """
    try:
        main_attr_boxs = task.ocr(match=match_list["main"], box=box_list[page]["main"])
        # print(f'main_attr_boxs:{len(main_attr_boxs)},{[box for box in main_attr_boxs]}')
        return EchoAttr(cases[main_attr_boxs[0].name], main_attr_boxs[1].name)
    except BaseException:
        if i == 4:
            return None
        return ocr_main(task, page, i + 1)


def ocr_sub_attr(task, page, i=0) -> List[EchoAttr]:
    """
    从游戏界面扫描并解析声骸(回声)副属性列表
    
    参数:
        task: 任务对象，用于执行OCR操作
        page (str): 页面标识，指定要扫描的页面类型
        i (int): 递归重试次数，默认为0
    
    返回:
        List[EchoAttr]: 解析后的声骸(回声)副属性列表
    
    异常:
        BaseException: 如果重试4次后仍解析失败则抛出异常
    """
    try:
        a = True
        attr = ""
        echo_attrs: List[EchoAttr] = []
        sub_boxs = task.ocr(match=match_list["sub"], box=box_list[page]["sub"])
        # print(f'sub_boxs:{len(sub_boxs)},{[box.name for box in sub_boxs]}')
        for sub in sub_boxs:

            if a:
                attr = sub.name
                a = False
            else:
                value = sub.name.lstrip('.·')
                if value.endswith("%"):
                    attr = cases[attr]
                else:
                    if attr == "生命":
                        attr = "小生命"
                    elif attr == "防御":
                        attr = "小防御"
                    elif attr == "攻击":
                        attr = "小攻击"
                # print(f'attr:{attr},value:{value}')
                echo_attrs.append(EchoAttr(attr, value))
                a = True
    except Exception as e:
        if i == 4:
            return None
        task.log_error(f'重新执行扫描')
        echo_attrs = ocr_sub_attr(task, page, i + 1)
    return echo_attrs


def extract_percentage(s):
    """
    从OCR字符串中提取百分数值，返回格式化后的百分数字符串

    参数:
        s (str): 可能包含前缀噪点('.', '·')的数字字符串

    返回:
        str: 格式化后的百分数字符串（如"12%" 或 "12.3%"）
    """
    # 清理开头的噪点字符
    cleaned = s.lstrip('.·')

    # 如果清理后为空，返回0%
    if not cleaned:
        return "0%"

    # 使用正则匹配数字模式（整数或带一位小数）
    match = re.match(r'^(\d{1,2})(\.\d)?', cleaned)
    if not match:
        return "0%"

    # 提取匹配到的数字部分
    num_str = match.group(0)

    # 处理整数情况
    if '.' not in num_str:
        try:
            value = int(num_str)
            if value <= 50:
                return f"{value}%"
            # 超过50%按0%处理
            return "0%"
        except ValueError:
            return "0%"

    # 处理小数情况
    try:
        value = float(num_str)
        if value <= 50.0:
            # 保留一位小数格式化
            return f"{value:.1f}%"
        # 超过50.0%按0%处理
        return "0%"
    except ValueError:
        return "0%"
