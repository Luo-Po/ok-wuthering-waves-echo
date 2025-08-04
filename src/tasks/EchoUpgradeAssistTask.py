import re

from ok import BaseTask, Box

from parse_mcdata import parse_mcdata
from src.tasks.MyBaseTask import MyBaseTask
from src.wuwa_screen_utils import WuWaScreenUtils
from echo_scorer import EchoScorer


class EchoUpgradeAssistTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wuwa_screen = WuWaScreenUtils(self)
        self.name = "声骸升级辅助"
        self.description = "请在声骸替换页面点击开始"
        self.default_config.update({
            '选择角色': "漂泊者-衍射",
        })
        self.config_type["选择角色"] = {'type': "drop_down",
                                        'options': ['弗洛洛', '卡提希娅', '露帕', '夏空', '赞妮', '坎特蕾拉',
                                                    '漂泊者-气动', '布兰特', '菲比', '洛可可', '珂莱塔', '椿', '灯灯',
                                                    '守岸人', '釉瑚', '折枝', '相里要', '长离', '今汐', '吟霖', '忌炎',
                                                    '鉴心', '卡卡罗', '安可', '维里奈', '凌阳', '漂泊者-衍射',
                                                    '漂泊者-湮灭', '桃祈', '白芷', '炽霞', '散华',
                                                    '秋水', '丹瑾', '莫特斐', '渊武', '桃祈']}

    def run(self):
        self.identifyExistingEcho()

    def identifyExistingEcho(self):
        # 初始化声骸评分器
        scorer = EchoScorer()
        
        # 获取选择的角色
        character_name = self.config.get('选择角色', "漂泊者-衍射")
        
        # 解析声骸数据
        echos = parse_mcdata(character_name)
        
        # 为每个声骸计算评分
        for echo in echos:
            # 假设echo是一个字典，包含声骸的属性
            # 提取声骸属性
            attributes = {
                '暴击': echo.get('暴击', 0.0),
                '暴伤': echo.get('暴伤', 0.0),
                '大攻击': echo.get('大攻击', 0.0),
                '小攻击': echo.get('小攻击', 0.0),
                '属伤': echo.get('属伤', 0.0),
                '专伤': echo.get('专伤', 0.0),
                '共鸣效率<40%': echo.get('共鸣效率', 0.0) if echo.get('共鸣效率', 0.0) < 40 else 0.0,
                '共鸣效率>40%': echo.get('共鸣效率', 0.0) if echo.get('共鸣效率', 0.0) >= 40 else 0.0
            }
            
            # 计算评分
            score = scorer.calculate_score(character_name, attributes)
            
            # 打印声骸信息和评分
            self.log_info(f"声骸: {echo.get('name', '未知')} - 评分: {score}分")
            print(f"声骸: {echo.get('name', '未知')} - 评分: {score}分")
