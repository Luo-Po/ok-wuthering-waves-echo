import re
from typing import List, Optional, Dict

from ok import Box


class WuWaScreenUtils:
    """鸣潮游戏屏幕交互辅助工具"""

    def __init__(self, task_instance):
        """
        初始化屏幕工具
        
        Args:
            task_instance: ok-script的Task实例，用于调用OCR和点击等方法
        """
        self.task = task_instance

        # 定义屏幕区域 (相对坐标，0-1之间)
        self.screen_regions = {
            'echo_list': Box(x=278, y=166, width=1303, height=1056),  # 声骸列表区域
            'echo_detail': Box(x=1747, y=152, width=744, height=1094),  # 声骸详情区域
            'echo_name': Box(x=1747, y=170, width=703, height=50),  # 声骸名称
            'main_stat': Box(x=1747, y=567, width=703, height=112),  # 主词条
            'sub_stats': Box(x=1747, y=679, width=703, height=280),  # 副词条区域
            'echo_level': Box(x=2360, y=330, width=80, height=48),  # 声骸等级
            # 'echo_rarity': Box(x=0.7*2560, y=0.2*1440, width=0.05*2560, height=0.03*1440),  # 声骸稀有度
        }

    def is_in_echo_page(self) -> bool:
        """检查是否在声骸背包页面"""
        # 通过OCR识别特定文字来判断
        echo_indicators = ["声骸", "Echo", "背包"]

        for indicator in echo_indicators:
            if self.task.ocr(match=indicator, box="top_left"):
                return True

        return False

    def navigate_to_echo_page(self) -> bool:
        """导航到声骸背包页面"""
        # 这里需要根据实际游戏界面来实现
        # 可能需要按B键打开背包，然后点击声骸标签

        # 按B键打开背包
        if not self.task.send_key('b', 0.3, 0.3, 0.3):
            return False
        self.task.sleep(1)

        # 查找并点击声骸标签
        try:
            # 假设声骸标签在固定位置，这需要根据实际游戏界面调整
            echo_tab_coord = Box(x=50, y=350, width=100, height=150)  # 示例坐标，需要实际测试
            self.task.click_box(echo_tab_coord)
            self.task.sleep(1)
            if self.is_in_echo_page():
                return True
        except Exception as e:
            self.task.log_debug(f"固定坐标点击失败: {e}")

        self.task.log_error("无法导航到声骸页面，请手动进入声骸背包页面")
        return False

    def get_echo_list_items(self) -> List[Box]:
        """获取声骸列表中的所有声骸项"""
        # 在声骸列表区域查找所有可点击的声骸项
        echo_items = self.task.find_feature('echo_item', box=self.screen_regions['echo_list'])
        return echo_items

    def click_echo_item(self, echo_box: Box) -> bool:
        """点击声骸项以查看详情"""
        self.task.click_box(echo_box)
        self.task.sleep(0.5)  # 等待详情加载
        return True

    def extract_echo_name(self) -> Optional[str]:
        """提取声骸名称"""
        name_boxes = self.task.ocr(box=self.screen_regions['echo_name'])
        if name_boxes:
            self.task.log_info("声骸名称: " + name_boxes[0].name.strip())
            return name_boxes[0].name.strip()
        return None

    def extract_echo_level(self) -> Optional[int]:
        """提取声骸等级"""
        level_boxes = self.task.ocr(box=self.screen_regions['echo_level'])
        if level_boxes:
            level_text = level_boxes[0].name
            # 提取数字
            level_match = re.search(r'(\d+)', level_text)
            if level_match:
                self.task.log_info("声骸等级: " + level_match.group(1))
                return int(level_match.group(1))
        return None

    def extract_echo_rarity(self) -> Optional[int]:
        """提取声骸稀有度（星级）"""
        # 可以通过OCR识别星级，或者通过图像特征识别
        rarity_boxes = self.task.ocr(box=self.screen_regions['echo_rarity'])
        if rarity_boxes:
            rarity_text = rarity_boxes[0].name
            # 计算星号数量
            star_count = rarity_text.count('★') or rarity_text.count('*')
            if star_count > 0:
                return star_count

        # 如果OCR失败，尝试通过特征匹配
        for rarity in range(1, 6):
            if self.task.find_one(f'star_{rarity}', box=self.screen_regions['echo_rarity']):
                return rarity

        return None

    def extract_main_stat(self) -> Optional[Dict[str, any]]:
        """提取主词条"""
        main_stat_boxes = self.task.ocr(box=self.screen_regions['main_stat'])
        if main_stat_boxes:
            main_stat_text = main_stat_boxes[0].name.strip()
            self.task.log_info("主词条: " + main_stat_text)
            return self._parse_stat_text(main_stat_text)
        return None

    def extract_sub_stats(self) -> List[Dict[str, any]]:
        """提取副词条"""
        sub_stats = []
        sub_stat_boxes = self.task.ocr(box=self.screen_regions['sub_stats'])

        for box in sub_stat_boxes:
            stat_text = box.name.strip()
            box.name.strip()
            parsed_stat = self._parse_stat_text(stat_text)
            if parsed_stat:
                sub_stats.append(parsed_stat)
            self.task.log_info("副词条: " + stat_text)
        return sub_stats

    def _parse_stat_text(self, text: str) -> Optional[Dict[str, any]]:
        """解析属性文本"""
        if not text:
            return None

        # 匹配百分比属性 (例如: "攻击力+15.5%")
        percent_pattern = r'(.+?)\+(\d+(?:\.\d+)?)%'
        percent_match = re.search(percent_pattern, text)
        if percent_match:
            return {
                'name': percent_match.group(1).strip(),
                'value': float(percent_match.group(2)),
                'is_percentage': True
            }

        # 匹配固定数值属性 (例如: "攻击力+150")
        fixed_pattern = r'(.+?)\+(\d+(?:\.\d+)?)'
        fixed_match = re.search(fixed_pattern, text)
        if fixed_match:
            return {
                'name': fixed_match.group(1).strip(),
                'value': float(fixed_match.group(2)),
                'is_percentage': False
            }

        # 如果都不匹配，返回原始文本
        return {
            'name': text,
            'value': 0,
            'is_percentage': False
        }

    def extract_echo_set(self) -> Optional[str]:
        """提取声骸套装名称"""
        # 套装名称通常在声骸详情的特定位置
        set_region = Box(x=0.55, y=0.65, width=0.35, height=0.05)
        set_boxes = self.task.ocr(box=set_region)

        if set_boxes:
            set_text = set_boxes[0].name.strip()
            # 过滤掉一些无关文字，提取套装名称
            known_sets = [
                "破浪踏潮", "熔山裂谷", "彻空冥雷", "啸谷长风",
                "沉日劫明", "凝夜白霜", "隐世回光", "不绝余音"
            ]

            for set_name in known_sets:
                if set_name in set_text:
                    self.task.log_info(set_name)
                    return set_name

        return None

    def scroll_echo_list(self, direction: str = "down", amount: int = 33) -> bool:
        """滚动声骸列表"""
        if direction == "down":
            for _ in range(amount):
                self.task.scroll(929, 1222, -1)
                self.task.sleep(0.2)
        elif direction == "up":
            for _ in range(amount):
                self.task.scroll(929, 166, 1)
                self.task.sleep(0.2)

        return True

    def extract_complete_echo_data(self) -> Optional[Dict]:
        """提取完整的声骸数据"""
        echo_data = {}

        # 提取基本信息
        echo_data['name'] = self.extract_echo_name()
        echo_data['level'] = self.extract_echo_level()
        # echo_data['rarity'] = self.extract_echo_rarity()

        # echo_data['set_name'] = self.extract_echo_set()

        # 提取属性
        echo_data['main_stat'] = self.extract_main_stat()
        echo_data['sub_stats'] = self.extract_sub_stats()

        # 检查是否成功提取到关键信息
        if echo_data['name'] and echo_data['main_stat']:
            return echo_data

        return None

    def wait_for_page_load(self, timeout: float = 3.0) -> bool:
        """等待页面加载完成"""
        import time
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.is_in_echo_page():
                return True
            self.task.sleep(0.1)

        return False

    def get_echo_position_from_ui(self) -> Optional[int]:
        """从UI中获取声骸装备位置"""
        # 这需要根据实际游戏界面来实现
        # 可能需要识别装备槽位的图标或文字
        position_region = Box(x=0.55, y=0.7, width=0.1, height=0.05)
        position_boxes = self.task.ocr(box=position_region)

        if position_boxes:
            position_text = position_boxes[0].name
            # 提取位置数字
            position_match = re.search(r'(\d+)', position_text)
            if position_match:
                return int(position_match.group(1))

        # 默认返回1
        return 1

    def estimate_echo_cost(self, rarity: int, echo_type: str = None) -> int:
        """估算声骸消耗"""
        # 根据稀有度和类型估算消耗
        cost_map = {
            1: 1,  # 1星
            2: 1,  # 2星
            3: 1,  # 3星
            4: 3,  # 4星
            5: 4,  # 5星
        }

        base_cost = cost_map.get(rarity, 1)

        # 某些特殊类型的声骸可能有不同的消耗
        if echo_type and "霸主" in echo_type:
            base_cost = 4
        elif echo_type and "精英" in echo_type:
            base_cost = 3

        return base_cost

    def get_echo_slot_boxes(self):
        return [
            Box(278, 166, 192, 234),
            Box(500, 166, 192, 234),
            Box(722, 166, 192, 234),
            Box(944, 166, 192, 234),
            Box(1166, 166, 192, 234),
            Box(1388, 166, 192, 234),

            Box(278, 440, 192, 234),
            Box(500, 440, 192, 234),
            Box(722, 440, 192, 234),
            Box(944, 440, 192, 234),
            Box(1166, 440, 192, 234),
            Box(1388, 440, 192, 234),

            Box(278, 714, 192, 234),
            Box(500, 714, 192, 234),
            Box(722, 714, 192, 234),
            Box(944, 714, 192, 234),
            Box(1166, 714, 192, 234),
            Box(1388, 714, 192, 234),

            Box(278, 988, 192, 234),
            Box(500, 988, 192, 234),
            Box(722, 988, 192, 234),
            Box(944, 988, 192, 234),
            Box(1166, 988, 192, 234),
            Box(1388, 988, 192, 234),
        ]
