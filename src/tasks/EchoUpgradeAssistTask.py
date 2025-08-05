import re

from ok import BaseTask, Box

from src.Echo import Echo, contrast_echo
from src.data import cost_list
from src.echo_scorer import sum_cost_scores, getIdByName, sum_count_sub_scores
from src.wuwa_screen_utils import WuWaScreenUtils


class EchoUpgradeAssistTask(BaseTask):
    boxList = {
        "name": Box(1880, 195, to_x=2426, to_y=240),
        "cost": Box(1894, 233, to_x=2051, to_y=285),
        "level": Box(1880, 278, to_x=1968, to_y=311),
        "main": Box(1940, 317, to_x=2426, to_y=407),
        "sub": Box(1940, 421, to_x=2426, to_y=633)

    }
    matchList = {
        "cost": re.compile(r'^COST [134]$', re.IGNORECASE),
        "level": re.compile(r'^\+([0-9]|1[0-9]|2[0-5])$'),

        "main": re.compile(
            r'^((\d{1,3}(?:\.\d%)?)|(暴击|暴击伤害|攻击|生命|防御|共鸣效率|治疗效果加成|((衍射|气动|热熔|冷凝|湮灭|导电)伤害加成)))$'),
        "sub": re.compile(
            r'^((\d{1,3}(?:\.\d%)?)|(暴击|暴击伤害|攻击|生命|防御|共鸣效率|((普攻|重击|共鸣技能|共鸣解放)伤害加成)))$')
    }
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
    c1 = None
    c3 = None
    c4 = None
    role = {}
    echos = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wuwa_screen = WuWaScreenUtils(self)
        self.name = "声骸升级辅助"
        self.description = "请在声骸替换页面点击开始"
        self.default_config.update({
            '选择角色': "光主-男",
            '选择命座': 0
        })
        self.config_type["选择角色"] = {'type': "drop_down",
                                        'options': ['光主-男', '光主-女', '暗主-男', '暗主-女', '风主-男', '风主-女',
                                                    '弗洛洛', '卡提希娅', '露帕', '夏空', '赞妮', '坎特蕾拉',
                                                    '布兰特', '菲比', '洛可可', '珂莱塔', '椿', '灯灯',
                                                    '守岸人', '釉瑚', '折枝', '相里要', '长离', '今汐', '吟霖', '忌炎',
                                                    '鉴心', '卡卡罗', '安可', '维里奈', '凌阳',
                                                    '桃祈', '白芷', '炽霞', '散华',
                                                    '秋水', '丹瑾', '莫特斐', '渊武', '桃祈']}

    def run(self):
        self.echos = []
        self.role = {
            "roleListId": getIdByName(self.config.get("选择角色")),
            "ming": 1
        }

        page_boxs = self.ocr(match="COST", box=Box(65, 49, to_x=169, to_y=86))

        for box in page_boxs:
            if box.name == "COST":
                self.identifyExistingEcho()
                self.log_info("可以开始强化声骸了")

        a = True
        while True:
            self.sleep(1)

            page_boxs = self.ocr(box=Box(142, 71, to_x=290, to_y=116))

            if len(page_boxs) == 0:
                a = True
                continue
            if not a:
                continue
            for box in page_boxs:
                if box.name == "声骸强化":
                    a = not self.upgrade_assist()

    def upgrade_assist(self) -> bool:
        cases = self.cases
        role = self.role
        echo = Echo()
        try:
            name_boxs = self.ocr(box=Box(251, 152, to_x=635, to_y=201))
            level_boxs = self.ocr(match=self.matchList["level"], box=Box(230, 229, to_x=325, to_y=290))
            main_attr_boxs = self.ocr(match=self.matchList["main"], box=Box(297, 322, to_x=908, to_y=362))
            property_boxs = self.ocr(match=self.matchList["sub"], box=Box(287, 422, to_x=918, to_y=704))
        except Exception as e:
            return False

        try:
            name = name_boxs[0].name
            level = int(
                level_boxs[0].name.replace("+", ""))
            cost = ""
            for cost in cost_list:
                if cost["name"] == name:
                    cost = cost["type"]
        except Exception as e:
            return False

        echo.name = name
        echo.level = level
        echo.cost = cost
        echo.main_attr = cases[main_attr_boxs[0].name] + main_attr_boxs[1].name
        count_critical = 0

        for i in range(0, int(level / 5)):
            attr = cases[property_boxs[i * 2].name]
            echo.add_property(attr, property_boxs[i * 2 + 1].name)
            if attr == "暴击" or attr == "爆伤":
                count_critical += 1
        echo.sub_score = sum_count_sub_scores(echo.property_list, role)

        count = len(echo.property_list)
        avg_sub_score = echo.sub_score / count

        if count == 1:
            if count_critical == 1:
                msg = "建议：这不强化留着干什么？"
            elif 0.0 < avg_sub_score:
                msg = "建议：可以强化的兄弟。"
            else:
                msg = "建议：再来一发试试水？"
        elif count == 2:
            if 0.0 < avg_sub_score < 1.0:
                msg = "建议：可以强化的兄弟。"
            elif avg_sub_score > 1.0 == count_critical:
                msg = "建议：这不强化留着干什么？"
            elif avg_sub_score > 1.0 and count_critical == 0:
                msg = "建议：虽然没出双爆但是都有效哎！"
            elif count_critical == 2:
                msg = "建议：双爆！这不冲？"
            else:
                msg = "建议：这还要？"
        elif count == 5:
            if 0.0 < avg_sub_score < 1.0 and count_critical == 2:
                msg = "建议：看你实力决定去留。"
            elif 0.0 < avg_sub_score < 1.0 and count_critical != 1:
                msg = "建议：这就别要了吧。"
            elif 1.0 < avg_sub_score < 2.0:
                if count_critical == 0:
                    msg = "建议：不太建议。"
                elif count_critical == 1:
                    msg = "建议：看你实力决定去留。"
                else:
                    msg = "建议：看你实力决定去留。"
            else:
                if count_critical == 0:
                    msg = "建议：这可能吗？"
                elif count_critical == 1:
                    msg = "建议：可惜了。"
                else:
                    msg = "建议：这还不留着？"
        else:
            if 0.0 < avg_sub_score < 1.0:
                msg = "建议：其实不太建议强化，你看着来。"
            elif 1.0 < avg_sub_score:
                msg = "建议：这不强化留着干什么？"
            else:
                msg = "建议：这还能要？"
        msg += f'\n声骸副词条平均分{avg_sub_score}'
        self.log_info(msg)
        return True



    def identifyExistingEcho(self):
        echos = self.echos
        self.sleep(0.5)
        self.click_box(box=Box(500, 700, to_x=501, to_y=701))
        previous = self.ocr_echo()
        self.c1 = None
        self.c3 = None
        self.c4 = None

        self.click_box(box=Box(53, 217, to_x=183, to_y=348))
        this = self.ocr_echo()
        if not contrast_echo(previous, this):
            previous = this
            echos.append(this)

        self.click_box(box=Box(66, 437, to_x=169, to_y=542))
        this = self.ocr_echo()
        if not contrast_echo(previous, this):
            previous = this
            echos.append(this)

        self.click_box(box=Box(66, 581, to_x=169, to_y=586))
        this = self.ocr_echo()
        if not contrast_echo(previous, this):
            previous = this
            echos.append(this)

        self.click_box(box=Box(66, 725, to_x=169, to_y=830))
        this = self.ocr_echo()
        if not contrast_echo(previous, this):
            previous = this
            echos.append(this)

        self.click_box(box=Box(66, 869, to_x=169, to_y=974))
        this = self.ocr_echo()
        if not contrast_echo(previous, this):
            previous = this
            echos.append(this)

        self.echos = echos

    def ocr_echo(self) -> Echo:
        echo = Echo()
        cases = self.cases
        boxList = self.boxList
        name = self.ocr(box=boxList["name"])[0].name
        echo.name = name
        type = ""
        for b in cost_list:
            if b["name"] == name:
                type = b["type"]
        echo.cost = type
        for a in self.ocr(match=self.matchList["level"], box=boxList["level"]):
            echo.level = a.name

        main = self.ocr(box=boxList["main"])

        echo.main_attr = cases[main[0].name] + main[1].name
        subs = self.ocr(match=self.matchList["sub"], box=boxList["sub"])
        a = False
        for sub in subs:
            if a:
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
                    break
                echo.add_property(property, sub.name)
                a = False
            else:
                property = sub.name
                a = True
        role = self.role
        echo.score = sum_cost_scores(echo, role)
        sub_score = sum_count_sub_scores(echo.property_list, role)
        echo.sub_score = sub_score
        if type == "COST1":
            if self.c1 is None:
                self.c1 = 20
            self.c1 = min(self.c1, sub_score)
        elif type == "COST3":
            if self.c3 is None:
                self.c3 = 20
            self.c3 = min(self.c3, sub_score)
        elif type == "COST4":
            if self.c4 is None:
                self.c4 = 20
            self.c4 = min(self.c4, sub_score)
        return echo
