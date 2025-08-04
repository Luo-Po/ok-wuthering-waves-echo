import re

from ok import BaseTask, Box

from echo_scorer import sum_cost_scores, getIdByName, cost_list, sum_count_sub_scores
from parse_mcdata import parse_mcdata
from src.Echo import Echo, contrast_echo
from src.tasks.MyBaseTask import MyBaseTask
from src.wuwa_screen_utils import WuWaScreenUtils


class EchoUpgradeAssistTask(BaseTask):

    boxList = {
        "name": Box(1880, 195,to_x= 2426,to_y=240),
        "type": Box(1894,233,to_x=2051,to_y=285),
        "level": Box(1880,278,to_x=1968,to_y=311),
        "main": Box(1940,317,to_x=2426,to_y=407),
        "sub": Box(1940,421,to_x=2426,to_y=633)


    }
    matchList = {
        "type" : re.compile(r'^COST [134]$', re.IGNORECASE),
        "level" : re.compile(r'^\+([0-9]|1[0-9]|2[0-5])$'),
        "sub" : re.compile(r'^((\d{1,3}(?:\.\d%)?)|(暴击|暴击伤害|攻击|生命|防御|共鸣效率|((普攻|重击|共鸣技能|共鸣解放)伤害加成)))$')
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
                                        'options': ['光主-男','光主-女','暗主-男','暗主-女','风主-男','风主-女',
                                                    '弗洛洛', '卡提希娅', '露帕', '夏空', '赞妮', '坎特蕾拉',
                                                    '布兰特', '菲比', '洛可可', '珂莱塔', '椿', '灯灯',
                                                    '守岸人', '釉瑚', '折枝', '相里要', '长离', '今汐', '吟霖', '忌炎',
                                                    '鉴心', '卡卡罗', '安可', '维里奈', '凌阳',
                                                    '桃祈', '白芷', '炽霞', '散华',
                                                    '秋水', '丹瑾', '莫特斐', '渊武', '桃祈']}

    def run(self):
        self.echos = []
        cases = self.cases
        echo = Echo()
        self.role = {
            "roleListId": getIdByName(self.config.get("选择角色")),
            "ming": 1
        }
        role = self.role
        for box in self.ocr(box = Box(65,49,to_x=169,to_y=86)):
            if box.name == "COST":
                self.identifyExistingEcho()
        a = True
        self.log_info("可以开始强化声骸了")
        while True:
            self.sleep(1)
            box = self.ocr(box = Box(142,71,to_x=290,to_y=116))

            if len(box) == 0:
                a = True
                continue
            if not a:
                continue
            for b in box:
                if b.name == "声骸强化":
                    a = False
                    name = self.ocr(box=Box(251, 152, to_x=635,to_y=201))
                    echo.name = name
                    level = int(self.ocr(match=self.matchList["level"],box=Box(230, 229, to_x=325, to_y=290))[0].name.replace("+",""))
                    echo.level = level
                    type = ""
                    for b in cost_list:
                        if b["name"] == name:
                            type = b["type"]
                    echo.type = type
                    boxb = self.ocr(box = Box(297,322,to_x=908,to_y=362))

                    echo.mainAttr = cases[boxb[0].name]+boxb[1].name


                    box = self.ocr(match = self.matchList["sub"],box = Box(297,432,to_x=908,to_y=694))
                    for i in range(0,int(level/5)):
                        echo.add_property(cases[box[i*2].name],box[i*2+1].name)
                    echo.subScore = sum_count_sub_scores(echo.propertyList,role)
                    avgSubScore = echo.subScore/len(echo.propertyList)
                    low = 0
                    if type == "COST1":
                        low = avgSubScore - self.c1
                    elif type == "COST3":
                        low = avgSubScore - self.c3
                    elif type == "COST4":
                        low = avgSubScore - self.c4
                    self.log_info(f'该声骸副词条平均分为{avgSubScore},{"低" if low<0 else "高"}于已装备同类{-low if low<0 else low}',True)






    def identifyExistingEcho(self):
        echos = self.echos
        self.click_box(box=Box(500,700,to_x=501,to_y=701))
        previous = self.ocr_echo()
        self.c1 = None
        self.c3 = None
        self.c4 = None
        self.click_box(box=Box(53,217,to_x=183,to_y=348))
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
        name = self.ocr(box = boxList["name"])[0].name
        echo.name = name
        type = ""
        for b in cost_list:
            if b["name"] == name:
                type = b["type"]
        echo.type = type
        for a in self.ocr(match = self.matchList["level"],box = boxList["level"]):
            echo.level = a.name

        main = self.ocr(box = boxList["main"])

        echo.mainAttr = cases[main[0].name] + main[1].name
        subs = self.ocr(match = self.matchList["sub"] ,box = boxList["sub"])
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
        subScore = sum_count_sub_scores(echo.propertyList, role)
        echo.subScore = subScore
        if type=="COST1":
            if self.c1 == None:
                self.c1 = 20
            self.c1= min(self.c1,subScore)
        elif type=="COST3":
            if self.c3 == None:
                self.c3 = 20
            self.c3= min(self.c3,subScore)
        elif type=="COST4":
            if self.c4 == None:
                self.c4 = 20
            self.c4= min(self.c4,subScore)
        return echo


