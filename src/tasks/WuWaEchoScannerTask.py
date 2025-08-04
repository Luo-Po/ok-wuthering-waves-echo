import time
import yaml
from ok import TriggerTask, Box
from src.wuwa_screen_utils import WuWaScreenUtils
from src.wuwa_echo_data import Echo, EchoRarity, EchoType, EchoStat, parse_stat_from_text


class WuWaEchoScannerTask(TriggerTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "鸣潮声骸扫描器"
        self.description = "扫描游戏中的声骸数据并保存"
        self.default_config.update({
            'scan_limit': 3000,  # 默认扫描声骸数量上限
            'scan_delay': 0.5,  # 每次点击后的等待时间
            'save_path': 'echoes.yaml',  # 声骸数据保存路径
        })
        self.scanned_echoes = []
        self.scanned_count = 0
        self.wuwa_screen = WuWaScreenUtils(self)  # 实例化屏幕工具
        self.processed_echo_coords = set()  # 记录已处理的声骸格子坐标，避免重复扫描

    def run(self):
        if not self.wuwa_screen.is_in_echo_page():
            self.log_info("不在声骸背包页面，尝试进入...")
            if not self.wuwa_screen.navigate_to_echo_page():
                self.log_error("无法进入声骸背包页面，请确保游戏运行且在正确界面。")
                return
            self.sleep(2)  # 等待页面完全加载

        self.log_info(f"开始扫描声骸，已扫描 {self.scanned_count}/{self.config.get('scan_limit')}")

        current_page_scanned = False

        level = 1
        i = 0
        slot_box = Box(278,166,192,234)

        while level > 0:


            # 检查这个格子是否已经处理过
            # 使用格子中心点作为唯一标识
            slot_center_coord = (slot_box.x + slot_box.width / 2, slot_box.y + slot_box.height / 2)
            if slot_center_coord in self.processed_echo_coords:
                continue

            self.log_info(f"点击第 {i + 1} 个声骸格子: {slot_box.x}, {slot_box.y}")
            self.wuwa_screen.click_echo_item(slot_box)  # 点击声骸
            self.sleep(self.config.get('scan_delay'))

            echo_data_dict = self.wuwa_screen.extract_complete_echo_data()  # 提取声骸信息
            if echo_data_dict:
                # 尝试将字典数据转换为Echo对象
                try:

                    if echo_data_dict['level'] == 0:
                        self._save_echo_data()
                        self.log_info("扫描任务结束，请手动停止触发器。")
                    else:
                        level = int(echo_data_dict['level'])

                    main_stat = EchoStat(
                        stat_type=echo_data_dict['main_stat']['name'],
                        value=echo_data_dict['main_stat']['value'],
                        is_percentage=echo_data_dict['main_stat']['is_percentage']
                    )
                    sub_stats = [
                        EchoStat(
                            stat_type=s['name'],
                            value=s['value'],
                            is_percentage=s['is_percentage']
                        ) for s in echo_data_dict['sub_stats']
                    ]

                    # 尝试从字符串解析EchoType和EchoRarity
                    echo_type_str = echo_data_dict.get('echo_type', 'COMMON_CLASS')  # 假设可以从UI提取
                    echo_type = EchoType[
                        echo_type_str.upper().replace(' ', '_')] if echo_type_str else EchoType.COMMON_CLASS

                    rarity_int = echo_data_dict.get('rarity', 1)
                    rarity = EchoRarity(rarity_int)

                    echo_obj = Echo(
                        name=echo_data_dict['name'],
                        rarity=rarity,
                        echo_type=echo_type,
                        level=echo_data_dict['level'],
                        main_stat=main_stat,
                        sub_stats=sub_stats,
                        # set_name=echo_data_dict['set_name'],
                        cost=self.wuwa_screen.estimate_echo_cost(rarity_int, echo_type_str),  # 估算消耗
                        position=self.wuwa_screen.get_echo_position_from_ui()  # 从UI获取位置
                    )
                    self.scanned_echoes.append(echo_obj)
                    self.scanned_count += 1
                    self.processed_echo_coords.add(slot_center_coord)
                    self.log_info(f"成功扫描声骸: {echo_obj.name}, 已扫描 {self.scanned_count}")
                    current_page_scanned = True
                except Exception as e:
                    self.log_error(f"解析声骸数据失败: {e}, 原始数据: {echo_data_dict}")
            else:
                self.log_info(f"未能在格子 {i + 1} 提取到声骸数据，可能为空或识别失败。")

            i = i + 1

            if slot_box.x != 1388:
                slot_box.x += 222
            else:
                slot_box.x = 278
                if slot_box.y != 988:
                    slot_box.y += 274
                else:

                    slot_box.x = 278
                    slot_box.y = 166
                    self.log_info("滚动页面以扫描更多声骸...")
                    # self.wuwa_screen.scroll_echo_list("down")
                    # self.sleep(1)  # 等待滚动和新内容加载
                    # self.processed_echo_coords = set()
                    return

            if self.scanned_count >= self.config.get('scan_limit'):
                self.log_info("达到扫描数量上限，停止扫描。")
                self._save_echo_data()
                self.log_info("扫描任务结束，请手动停止触发器。")
                return


    def _save_echo_data(self):
        """将scanned_echoes保存到yaml文件"""
        save_path = self.config.get('save_path')
        # 将Echo对象转换为字典以便保存
        serializable_echoes = []
        for echo in self.scanned_echoes:
            serializable_echo = {
                'name': echo.name,
                'rarity': echo.rarity.value,
                'echo_type': echo.echo_type.value,
                'level': echo.level,
                'main_stat': {'stat_type': echo.main_stat.stat_type, 'value': echo.main_stat.value,
                              'is_percentage': echo.main_stat.is_percentage},
                'sub_stats': [{'stat_type': s.stat_type, 'value': s.value, 'is_percentage': s.is_percentage} for s in
                              echo.sub_stats],
                'set_name': echo.set_name,
                'cost': echo.cost,
                'position': echo.position
            }
            serializable_echoes.append(serializable_echo)

        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(serializable_echoes, f, allow_unicode=True, sort_keys=False)
        self.log_info(f"声骸数据已保存到 {save_path}")

    def on_stop(self):
        """任务停止时调用，确保数据保存"""
        if self.scanned_echoes:
            self._save_echo_data()
        self.log_info("鸣潮声骸扫描器已停止。")