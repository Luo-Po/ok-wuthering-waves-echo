import re

from ok import Box

from src.Echo import Echo, EchoAttr
from src.data import cost_list
from src.echo_scorer import sum_scores, sum_sub_scores

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
    "行射伤害加成": "属伤",
    "气动伤害加成": "属伤",
    "热熔伤害加成": "属伤",
    "冷凝伤害加成": "属伤",
    "灭伤害加成": "属伤",
    "湮灭伤害加成": "属伤",
    "导电伤害加成": "属伤",
}

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
        "main": Box(1827, 566, to_x=2450, to_y=677),
        "sub": Box(1827, 681, to_x=2450, to_y=960)
    }

}

match_list = {
    "cost": re.compile(
        r'^COST [134]$'),
    "level": re.compile(
        r'^\+([0-9]|1[0-9]|2[0-5])$'),
    "main": re.compile(
        r'^((\d{1,3}(?:\.\d%)?)|暴击|暴击伤害|攻击|生命|防御|共鸣效率|治疗效果加成|((([衍行])射|气动|热熔|冷凝|(湮灭|灭)|导电)伤害加成))$'),
    "sub": re.compile(
        r'^((\d{1,3}(?:\.\d%)?)|(暴击|暴击伤害|攻击|生命|防御|共鸣效率|((普攻|重击|共鸣技能|共鸣解放)伤害加成)))$'),
    "page": re.compile(
        r'^(属性详情|武器|技能|共鸣链|档案|数据坞|声骸图鉴|合鸣图鉴|数据融合|数据重构|声骸强化|声骸调谐|COST|((武器|声骸|补给|资源|素材|任务|特殊)|\d{1,4}/[123]000))$')
}

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
    return page == which_page(task)


def which_page(task) -> str:
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
    task.sleep(0.2)
    echo = Echo()
    try:
        name_boxs = task.ocr(box=box_list[page]["name"])
        level_boxs = task.ocr(match=match_list["level"], box=box_list[page]["level"])
        main_attr_boxs = task.ocr(match=match_list["main"], box=box_list[page]["main"])
        sub_boxs = task.ocr(match=match_list["sub"], box=box_list[page]["sub"])

        name = name_boxs[0].name
        main_attr = EchoAttr(cases[main_attr_boxs[0].name], main_attr_boxs[1].name)
        a = True
        attr = ""
        for sub in sub_boxs:
            if a:
                attr = sub.name
                a = False
            else:
                if attr == "生命":
                    if sub.name.endswith("%"):
                        attr = "大生命"
                    else:
                        attr = "小生命"
                elif attr == "防御":
                    if sub.name.endswith("%"):
                        attr = "大防御"
                    else:
                        attr = "小防御"
                elif attr == "攻击":
                    if sub.name.endswith("%"):
                        attr = "大攻击"
                    else:
                        attr = "小攻击"
                elif attr in cases:
                    attr = cases[attr]
                else:
                    task.log_error(f'未扫描到{attr}的属性')
                if sub.name in cases:
                    task.log_error(f'未扫描到{attr}的数值')
                    attr = cases[sub.name]
                echo.add_sub_attr(attr, sub.name)
                a = True

        try:
            level = int(level_boxs[0].name)
        except IndexError:
            level = len(echo.get_sub_attr_list()) * 5
        if level == 0:
            level = len(echo.get_sub_attr_list()) * 5

        cost = ""
        for b in cost_list:
            if b["name"] == name:
                cost = b["type"]

        echo.set_name(name)
        echo.set_cost(cost)
        echo.set_level(level)
        echo.set_main(main_attr)
        try:
            role = task.role
            score = sum_scores(echo, role)
            main_score = sum_scores(echo, role)
            sub_score = sum_sub_scores(echo, role)
        except:
            score = 0
            main_score = 0
            sub_score = 0

        echo.set_score(score)
        echo.set_main_score(main_score)
        echo.set_sub_score(sub_score)
    except ImportError:
        echo = ocr_echo(task, page)
    except IndexError:
        echo = ocr_echo(task, page)
    return echo
