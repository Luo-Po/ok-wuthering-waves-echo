from ok import BaseTask, Box

from src.Echo import contrast_echo
from src.echo_scorer import getIdByName
from src.utils.windows_utils import set_window_topmost, get_active_window
from src.wuwa_scanner_utils import ocr_echo, is_page


class EchoUpgradeAssistTask(BaseTask):
    role = {}
    echos = []
    lost_cost = {
        1: None,
        3: None,
        4: None,
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        set_window_topmost(get_active_window())
        if is_page(self, "echo_change"):
            self.identifyExistingEcho()
            for echo in self.echos:
                self.log_info(
                    f'声骸: {echo.get_name()}\n评分: {echo.get_score()}\n主词条评分: {echo.get_main_score()}\n副词条评分: {echo.get_sub_score()}')
                cost = echo.get_cost()
                sub_score = echo.get_sub_score()
                if self.lost_cost[cost] is None:
                    self.lost_cost[cost] = sub_score / len(echo.get_sub_attr_list())
                else:
                    self.lost_cost[cost] = min(self.lost_cost[cost], sub_score / len(echo.get_sub_attr_list()))
            for c, s in self.lost_cost:
                self.notification(
                    f's',
                    f'COST{c} 最低副词条平均分'
                )

            self.log_info("可以开始强化声骸了")

        a = True
        while True:
            self.sleep(1)

            if is_page(self, "echo_upgrade"):
                if a:
                    a = not self.upgrade_assist()
            elif is_page(self, "role_echo"):
                self.log_info("任务结束，已自动退出")
                break
            else:
                a = True

    def upgrade_assist(self) -> bool:
        echo = ocr_echo(self, "echo_upgrade")

        count = len(echo.get_sub_attr_list())
        avg_sub_score = 0.0
        if count > 1:
            avg_sub_score = echo.get_sub_score() / count

        msg = f'声骸副词条平均分{avg_sub_score},{echo.get_score()}'
        self.log_info(msg)
        return True

    def identifyExistingEcho(self):
        echos = self.echos
        # self.sleep(0.5)
        # self.click_box(box=Box(500, 700, to_x=501, to_y=701))
        # previous = ocr_echo(self, "echo_change")

        self.click_box(box=Box(53, 217, to_x=183, to_y=348))
        this = ocr_echo(self, "echo_change")
        # if not contrast_echo(previous, this):
        previous = this

        self.click_box(box=Box(66, 437, to_x=169, to_y=542))
        this = ocr_echo(self, "echo_change")
        if not contrast_echo(previous, this):
            echos.append(previous)
            echos.append(this)
            previous = this

        self.click_box(box=Box(66, 581, to_x=169, to_y=586))
        this = ocr_echo(self, "echo_change")
        if not contrast_echo(previous, this):
            echos.append(this)
            previous = this

        self.click_box(box=Box(66, 725, to_x=169, to_y=830))
        this = ocr_echo(self, "echo_change")
        if not contrast_echo(previous, this):
            echos.append(this)
            previous = this

        self.click_box(box=Box(66, 869, to_x=169, to_y=974))
        this = ocr_echo(self, "echo_change")
        if not contrast_echo(previous, this):
            echos.append(this)

        self.echos = echos
