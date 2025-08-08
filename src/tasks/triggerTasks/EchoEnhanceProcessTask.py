from typing import List

from ok import TriggerTask

from src.Echo import EchoAttr
from src.utils.wuwa_scanner_utils import is_level_up, ocr_echo_level_up_attr, ocr_level_increase


class EchoEnhanceProcessTask(TriggerTask):
    arrange: List[str] = []
    msg = ""
    ttt = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "声骸强化流程"
        self.description = "建议开启窗口置顶"
        self.trigger_interval = True
        self.trigger_count = 0

    def run(self):
        self.trigger_count += 1
        # self.log_debug(f'MyTriggerTask run {self.trigger_count}')
        # self.log_debug("EchoEnhanceProcessTask:run")
        msg = self.msg
        archive = 0

        if not is_level_up(self):
            self.ttt = True
            return
        elif not self.ttt:
            return
        self.ttt = False
        increase_boxs = ocr_echo_level_up_attr(self)
        this_attrs = ""
        for box in increase_boxs:
            if box.get_attr() == "暴击":
                if this_attrs == 1:
                    this_attrs = 2
                else:
                    this_attrs = 0
            if box.get_attr() == "爆伤":
                if this_attrs == 0:
                    this_attrs = 2
                else:
                    this_attrs = 1
        this_attrs = "x"
        self.arrange.append(this_attrs)
        arrange = self.arrange
        if len(arrange) == 2:
            if arrange[0] == "x" and arrange[1] == "x":
                msg = "符合xx**，今日不宜梭哈，结束。"
        elif len(arrange) == 4:
            if arrange[0] == arrange[1] == arrange[2] == arrange[3] != "x":
                msg = "符合1111或0000，今日不宜梭哈，结束。"
            archive = 4
        else:

            if this_attrs == 2:
                if is_have_attr(increase_boxs, "大攻击") or is_have_attr(increase_boxs, "伤害"):
                    msg = "重启游戏，然后拉25级。"
                else:
                    msg = "拉25级，然后重启游戏。"
                archive = len(arrange)
            else:
                arrange = arrange[archive:]
                if len(arrange) < 3:
                    return
                aa = ""
                for a in arrange[-3:]:
                    aa += a
                if aa == "xxx":
                    msg = "停止梭哈今日运势不佳，明天再来。"
                elif len(arrange) < 7:
                    return
                else:
                    a7 = arrange[-7]
                    rel = True
                    for a in a7:
                        if a == 2:
                            rel = False
                    if rel:
                        msg = "重启游戏，然后升级刚刚出单爆的声骸。"

                    if len(increase_boxs) == 1 and this_attrs != "x":
                        _, after_level = ocr_level_increase(self)
                        if after_level == 25:
                            msg = "重启游戏，继续强化4孔"
        if msg != "":
            self.msg = msg
            self.notification(msg, "声骸强化助手")


def is_have_attr(attrs: List[EchoAttr], attr_name: str) -> bool:
    for attr in attrs:
        if attr.get_attr().endswith(attr_name):
            return True
    return False
