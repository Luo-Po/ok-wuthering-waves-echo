import re

from ok import BaseTask, Box

from src.tasks.MyBaseTask import MyBaseTask
from src.wuwa_screen_utils import WuWaScreenUtils


class EchoUpgradeAssistTask(BaseTask):



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wuwa_screen = WuWaScreenUtils(self)
        self.name = "声骸升级辅助"
        self.description = "请在声骸替换页面点击开始"
        self.default_config.update({
            '选择角色': "第一",
        })
        self.config_type["选择角色"] = {'type': "drop_down",
                                            'options': ['弗洛洛', '卡提希娅', '瑞莉', '夏空', '赞妮', '坎特蕾拉', '漂泊者-气动', '布兰特长', '菲比', '洛可可', '珂莱塔', '椿', '灯灯', '守岸人', '柚蝴', '折枝', '相里要', '长离', '今汐', '吟霖', '总炎', '鉴心', '卡卡罗', '安可', '维里奈', '凌阳', '漂泊者-衍射', '漂泊者-淬火', '漂泊者-湮灭', '桃桠', '白芷', '炽黄', '韶华', '秋水', '丹星', '莫特斐', '澜贰', '槐祈']}

    def run(self):
        rel = self.ocr(match="(COST)",box=Box(65,50,105,36))
        if len(rel) == 0:
            self.identifyExistingEcho()
            return
        if rel[0].name == "COST":
            self.identifyExistingEcho()

    def identifyExistingEcho(self):
        self.log_info("identifyExistingEcho")
        self.find_feature("echo_space",box = "left")
        sub_stat_boxes = self.ocr(box=Box(1940,317,to_x=2430,to_y=590))
        for box in sub_stat_boxes:
            self.log_info("box: "+box.name)
