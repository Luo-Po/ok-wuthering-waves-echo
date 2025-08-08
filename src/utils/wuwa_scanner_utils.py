#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import List

from ok import Box

from src.Echo import Echo, EchoAttr
from src.data import cost_list
from src.echo_scorer import sum_sub_scores, sum_main_score

# 属性映射字典，将游戏中显示的属性名称映射为内部使用的属性名称
cost_tran = {
    "呼咻咻": "呼咻咻",
    "咔嚓嚓": "咔嚓嚓",
    "阿嗞嗞": "阿嗞嗞",
    "阿磁磁": "阿嗞嗞",
    "呜咔咔": "呜咔咔",
    "冰墩墩": "冰墩墩",
    "咕咕河豚": "咕咕河豚",
    "啾啾河豚": "啾啾河豚",
    "遁地鼠": "遁地鼠",
    "绿熔蜥（稚形）": "绿熔蜥（稚形）",
    "碎獠猪": "碎獠猪",
    "火鬃狼": "火鬃狼",
    "晶螯蝎": "晶螯蝎",
    "游弋蝶": "游弋蝶",
    "寒霜陆龟": "寒霜陆龟",
    "幼猿": "幼猿",
    "融火虫": "融火虫",
    "侏侏鸵": "侏侏鸵",
    "青羽鹭": "青羽鹭",
    "紫羽鹭": "紫羽鹭",
    "绿熔蜥": "绿熔蜥",
    "箭簇熊": "箭簇熊",
    "暗鬃狼": "暗鬃狼",
    "戏猿": "戏猿",
    "雪鬃狼": "雪鬃狼",
    "踏光兽": "踏光兽",
    "飞廉之猩": "飞廉之猩",
    "无常凶鹭": "无常凶鹭",
    "哀声鸷": "哀声鸷",
    "哀声": "哀声鸷",
    "无冠者": "无冠者",
    "无妄者": "无妄者",
    "鸣钟之龟": "鸣钟之龟",
    "冷凝棱镜": "冷凝棱镜",
    "热熔棱镜": "热熔棱镜",
    "湮灭棱镜": "湮灭棱镜",
    "衍射棱镜": "衍射棱镜",
    "辉萤军势": "辉萤军势",
    "车刃镰": "车刃镰",
    "聚械机偶": "聚械机偶",
    "刺玫菇（稚形）": "刺玫菇（稚形）",
    "先锋幼岩": "先锋幼岩",
    "裂变幼岩": "裂变幼岩",
    "刺玫菇": "刺玫菇",
    "坚岩斗士": "坚岩斗士",
    "惊蛰猎手": "惊蛰猎手",
    "破霜猎手": "破霜猎手",
    "巡徊猎手": "巡徊猎手",
    "鸣泣战士": "鸣泣战士",
    "审判战士": "审判战士",
    "振铎乐师": "振铎乐师",
    "奏谕乐师": "奏谕乐师",
    "冥渊守卫": "冥渊守卫",
    "磐石守卫": "磐石守卫",
    "朔雷之鳞": "朔雷之鳞",
    "云闪之鳞": "云闪之鳞",
    "燎照之骑": "燎照之骑",
    "通行灯偶": "通行灯偶",
    "巡哨机傀": "巡哨机傀",
    "游鳞机枢": "游鳞机枢",
    "角": "角",
    "无归的谬误": "无归的谬误",
    "雷鬃狼": "雷鬃狼",
    "霜鬃狼": "霜鬃狼",
    "风鬃狼": "风鬃狼",
    "梦魇·飞廉之猩": "梦魇·飞廉之猩",
    "梦魇·无常凶鹭": "梦魇·无常凶鹭",
    "梦魇·哀声鸷": "梦魇·哀声鸷",
    "梦魇·哀声莺": "梦魇·哀声鸷",
    "梦魇·无冠者": "梦魇·无冠者",
    "叹息古龙": "叹息古龙",
    "浮灵偶·海德": "浮灵偶·海德",
    "浮灵偶·蕾弗": "浮灵偶·蕾弗",
    "浮灵偶·莱特": "浮灵偶·莱特",
    "幽翎火": "幽翎火",
    "云海妖精": "云海妖精",
    "魔术先生": "魔术先生",
    "寂寞小姐": "寂寞小姐",
    "工头布偶": "工头布偶",
    "欺诈奇藏": "欺诈奇藏",
    "浮灵偶": "浮灵偶",
    "巨布偶": "巨布偶",
    "巡游骑士": "巡游骑士",
    "幻昼骑士": "幻昼骑士",
    "暗夜骑士": "暗夜骑士",
    "毒冠贵族": "毒冠贵族",
    "持刃贵族": "持刃贵族",
    "凝水贵族": "凝水贵族",
    "琉璃刀伶": "琉璃刀伶",
    "梦魇·朔雷之鳞": "梦魇·朔雷之鳞",
    "梦魇·云闪之鳞": "梦魇·云闪之鳞",
    "梦魇·燎照之骑": "梦魇·燎照之骑",
    "罗蕾莱": "罗蕾莱",
    "异构武装": "异构武装",
    "赫卡忒": "赫卡忒",
    "重塑雕像的拳砾": "重塑雕像的拳砾",
    "飓力熊": "飓力熊",
    "气动棱镜": "气动棱镜",
    "愚金幼岩": "愚金幼岩",
    "釉变幼岩": "釉变幼岩",
    "梦魇·辉萤军势": "梦魇·辉萤军势",
    "共鸣回响·芙露德莉斯": "共鸣回响·芙露德莉斯",
    "共鸣回响·": "共鸣回响·芙露德莉斯",
    "共鸣回响": "共鸣回响·芙露德莉斯",
    "慈悲节使": "慈悲节使",
    "赦罪节使": "赦罪节使",
    "卫冕节使": "卫冕节使",
    "小翼龙·气动": "小翼龙·气动",
    "小翼龙·导电": "小翼龙·导电",
    "小翼龙·冷凝": "小翼龙·冷凝",
    "荣光节使": "荣光节使",
    "梦魇·凯尔匹": "梦魇·凯尔匹",
    "荣耀狮像": "荣耀狮像",
    "角鳄": "角鳄",
    "传道者的遗形": "传道者的遗形",
    "小翼龙·衍射": "小翼龙·衍射",
    "小翼龙·热熔": "小翼龙·热熔",
    "小翼龙·湮灭": "小翼龙·湮灭",
    "苦信者的作俑": "苦信者的作俑",
    "梦魇·破霜猎手": "梦魇·破霜猎手",
    "梦魇·审判战士": "梦魇·审判战士",
    "梦·审判战士": "梦魇·审判战士",
    "梦魇·振铎乐师": "梦魇·振铎乐师",
    "共鸣回响·芬莱克": "共鸣回响·芬莱克",
    "梦魇·赫卡忒": "梦魇·赫卡忒"}
cases = {
    "攻击": "大攻击",
    "生命": "大生命",
    "防御": "大防御",
    "共鸣效率": "共鸣效率",
    "艾鸣效率": "共鸣效率",
    "效率": "共鸣效率",
    "普攻伤害加成": "普攻伤害",
    "重击伤害加成": "重击伤害",
    "共鸣技能伤害加成": "技能伤害",
    "共鸣解放伤害加成": "解放伤害",
    "暴击伤害": "暴伤",
    "击伤害": "暴伤",
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
        "level": Box(230, 228, to_x=325, to_y=291),
        "main": Box(287, 312, to_x=918, to_y=372),
        "sub": Box(287, 422, to_x=918, to_y=704)
    },
    "level_up": {
        "is_level_up": Box(1176, 360, to_x=1382, to_y=427),
        "before": Box(909, 516, to_x=1093, to_y=605),
        "after": Box(1424, 516, to_x=1609, to_y=605),
        "main": Box(882, 658, to_x=1734, to_y=778),
        "sub": Box(882, 810, to_x=1734, to_y=1168)
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
        r'^((.*\d{1,3}(?:\.\d%)?)|暴击|暴击伤害|攻击|生命|防御|[共|艾]鸣效率|效率|((普攻|重击|共鸣技能|共鸣解放)伤害加成))$'),
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
    task.sleep(0.1)
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
        name = ocr_name(task, page)
        echo.set_name(name)
        task.log_info(f'name: {name}')
        # print(f'{name}')
        cost = ""
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

            score = round(main_score + sub_score, 2)
            echo.set_score(score)


    except ValueError as e:
        raise BaseException("识别声骸失败：" + e.__str__())
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
        task.sleep(0.1)
        name_boxs = task.ocr(box=box_list[page]["name"])
        if len(name_boxs) == 1:
            name = name_boxs[0].name
        else:
            name = name_boxs[0].name + name_boxs[1].name
        print(cost_tran["无妄者"])
        print(name)
        name = name.replace("梦魔", "梦魇").replace("一", "·").replace("~", "·").replace("异相·", "").replace("异相",
                                                                                                              "")
        print(name)
        if name in cost_tran:
            name = cost_tran[name]
        else:
            print("raise")
            raise
    except BaseException:
        if i == 4:
            raise BaseException("识别声骸名称错误")
        else:
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
            raise BaseException("识别声骸名称错误")
        else:
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
        task.sleep(0.1)
        level_boxs = task.ocr(match=match_list["level"], box=box_list[page]["level"])
        level = int(level_boxs[0].name.lstrip('+'))
    except BaseException:
        print(BaseException)
        if i == 4:
            raise BaseException("识别声骸等级错误")
        level = ocr_level(task, page, i + 1)
    return level

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
        task.sleep(0.1)
        main_attr_boxs = task.ocr(match=match_list["main"], box=box_list[page]["main"])
        # print(f'main_attr_boxs:{len(main_attr_boxs)},{[box for box in main_attr_boxs]}')
        main = EchoAttr(cases[main_attr_boxs[0].name], main_attr_boxs[1].name.replace("%", ""))
    except BaseException:
        if i == 4:
            raise BaseException("识别声骸主词条错误")
        main = ocr_main(task, page, i + 1)
    return main

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
        task.sleep(0.1)
        sub_boxs = task.ocr(match=match_list["sub"], box=box_list[page]["sub"])
        # print(f'sub_boxs:{len(sub_boxs)},{[box.name for box in sub_boxs]}')
        for sub in sub_boxs:

            if a:
                attr = sub.name
                a = False
            else:
                value = sub.name.lstrip('.·')
                if value.endswith("%"):
                    value = value.replace("%", "")
                    print(attr)
                    attr = cases[attr]
                else:
                    if attr == "生命":
                        attr = "小生命"
                    elif attr == "防御":
                        attr = "小防御"
                    elif attr == "攻击":
                        attr = "小攻击"

                    print(attr)
                print(f'attr:{attr},value:{value}')
                echo_attrs.append(EchoAttr(attr, value))
                a = True
    except Exception as e:
        if i == 4:
            raise BaseException("识别声骸副词条错误")
        echo_attrs = ocr_sub_attr(task, page, i + 1)
    return echo_attrs


def is_level_up(task) -> bool:
    task.sleep(0.1)
    boxs = task.ocr(match="调谐成功", box=box_list["level_up"]["is_level_up"])
    for box in boxs:
        return True
    return False


def ocr_level_increase(task):
    before_level = 0
    after_level = 0
    try:
        task.sleep(0.1)
        before_level_boxs = task.ocr(match=match_list["level"], box=box_list["level_up"]["before"])
        before_level = before_level_boxs[0].name.lstrip('+')
    except BaseException as e:
        task.error(f'声骸强化成功界面升级前等级识别错误')
    try:
        task.sleep(0.1)
        after_level_boxs = task.ocr(match=match_list["level"], box=box_list["level_up"]["after"])
        after_level = after_level_boxs[0].name.lstrip('+')
    except BaseException as e:
        task.error(f'声骸强化成功界面升级后等级识别错误')
    return int(before_level), int(after_level)


def ocr_echo_level_up_attr(task) -> List[EchoAttr]:
    before_level, after_level = ocr_level_increase(task)
    increase = int(after_level / 5) - int(before_level / 5)
    if increase > 0:
        return ocr_sub_attr(task, "level_up")
    return None
