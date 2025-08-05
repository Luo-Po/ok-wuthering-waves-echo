import re

from ok import Box

from src.Echo import Echo
from src.data import cost_list
from src.echo_scorer import sum_cost_scores, sum_count_sub_scores

cases = {
    "攻击": "攻击",
    "生命": "生命",
    "防御": "防御",
    "共鸣效率": "共鸣效率",
    "普攻伤害加成": "普攻伤害",
    "重击伤害加成": "重击伤害",
    "共鸣技能伤害加成": "技能伤害",
    "共鸣解放伤害加成": "解放伤害",
    "暴击伤害": "暴伤",
    "暴击": "暴击",
    "治疗效果加成": "治疗",
    "衍射伤害加成": "属伤",
    "气动伤害加成": "属伤",
    "热熔伤害加成": "属伤",
    "冷凝伤害加成": "属伤",
    "湮灭伤害加成": "属伤",
    "导电伤害加成": "属伤",
}

box_list = {
    "echo_change": {
        "name": Box(1880, 195, to_x=2426, to_y=240),
        # "cost": Box(1894, 233, to_x=2051, to_y=285),
        "level": Box(1880, 278, to_x=1968, to_y=311),
        "main": Box(1940, 317, to_x=2426, to_y=407),
        "sub": Box(1940, 421, to_x=2426, to_y=633)
    },
    "echo_upgrade": {
        "name": Box(251, 152, to_x=635, to_y=201),
        "level": Box(230, 229, to_x=325, to_y=290),
        "main": Box(297, 322, to_x=908, to_y=362),
        "sub": Box(287, 422, to_x=918, to_y=704)
    }
}

match_list = {
    "cost": re.compile(
        r'^COST [134]$'),
    "level": re.compile(
        r'^\+([0-9]|1[0-9]|2[0-5])$'),
    "main": re.compile(
        r'^((\d{1,3}(?:\.\d%)?)|(暴击|暴击伤害|攻击|生命|防御|共鸣效率|治疗效果加成|((衍射|气动|热熔|冷凝|湮灭|导电)伤害加成)))$'),
    "sub": re.compile(
        r'^((\d{1,3}(?:\.\d%)?)|(暴击|暴击伤害|攻击|生命|防御|共鸣效率|((普攻|重击|共鸣技能|共鸣解放)伤害加成)))$')
}


def ocr_echo(task, page) -> Echo:
    echo = Echo()

    name_boxs = task.ocr(box=box_list[page]["name"])
    level_boxs = task.ocr(match=match_list["level"], box=box_list[page]["level"])
    main_attr_boxs = task.ocr(match=match_list["main"], box=box_list[page]["main"])
    sub_boxs = task.ocr(match=match_list["sub"], box=box_list[page]["sub"])

    name = name_boxs[0].name

    main_attr = cases[main_attr_boxs[0].name] + main_attr_boxs[1].name
    a = True
    for sub in sub_boxs:
        if a:
            property = sub.name
            a = False
        else:
            if property == "生命":
                if sub.name.endswith("%"):
                    property = "大生命"
                else:
                    property = "小生命"
            elif property == "防御":
                if sub.name.endswith("%"):
                    property = "大防御"
                else:
                    property = "小防御"
            elif property == "攻击":
                if sub.name.endswith("%"):
                    property = "大攻击"
                else:
                    property = "小攻击"
            elif property in cases:
                property = cases[property]
            else:
                task.log_error(f'未扫描到{property}的属性')
            if sub.name in cases:
                task.log_error(f'未扫描到{property}的数值')
                property = cases[sub.name]
            echo.add_property(property, sub.name)
            a = True

    try:
        level = level_boxs[0].name
    except IndexError:
        level = len(echo.property_list) * 5

    type = ""
    for b in cost_list:
        if b["name"] == name:
            type = b["type"]

    echo.name = name
    echo.cost = type
    echo.level = level
    echo.main_attr = main_attr

    role = task.role
    sub_score = sum_count_sub_scores(echo.property_list, role)
    echo.score = sum_cost_scores(echo, role)
    echo.sub_score = sub_score
    return echo
