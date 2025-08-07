import yaml
from ok import TriggerTask

from src.utils.wuwa_controller_utils import click_echo_box, scroll_echo_list
from src.utils.wuwa_scanner_utils import is_page, ocr_echo


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
        self.processed_echo_coords = set()  # 记录已处理的声骸格子坐标，避免重复扫描

    def run(self):
        if not is_page(self, "bag_echos"):
            self.log_info("不在声骸背包页面，尝试进入...")

        while not is_page(self, "bag_echos"):  # 等待玩家进入声骸背包
            self.sleep(1)

        self.log_info(f"开始扫描声骸，已扫描 {self.scanned_count}/{self.config.get('scan_limit')}")

        level = 1
        x = 1
        y = 1
        page = 1
        click_echo_box(self, x, y)  # 点击声骸
        while level > 0:

            self.sleep(0.15)
            # 检查这个格子是否已经处理过
            # 使用格子中心点作为唯一标识
            slot_center_coord = (x, y)
            if slot_center_coord in self.processed_echo_coords:
                continue

            self.log_info(f"点击第 {self.scanned_count + 1} 个声骸格子: {x}, {y}")
            click_echo_box(self, x, y)  # 点击声骸
            echo = ocr_echo(self, "bag_echos")  # 提取声骸信息

            if echo.get_level() == 0:
                level = 0
                continue
            elif len(echo.get_sub_attr_list()) == 0:
                level = 0
                continue

            self.scanned_echoes.append(echo)
            self.scanned_count += 1
            self.processed_echo_coords.add(slot_center_coord)
            self.log_info(f"成功扫描声骸: {echo.get_name()}, 已扫描 {self.scanned_count}")

            if x < 6:
                x += 1
            elif y < 4:
                x = 1
                y += 1
            else:
                if page == 1:
                    scroll_echo_list(self, "down", 63)
                else:
                    scroll_echo_list(self, "down", 31)
                x = 1
                y = 1
                self.processed_echo_coords = set()  # 记录已处理的声骸格子坐标，避免重复扫描
            page += 1
        self._save_echo_data()

    def _save_echo_data(self):
        """将scanned_echoes保存到yaml文件"""
        save_path = self.config.get('save_path')
        # 将Echo对象转换为字典以便保存
        serializable_echoes = []
        for echo in self.scanned_echoes:
            serializable_echo = echo.to_dict()
            serializable_echoes.append(serializable_echo)

        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(serializable_echoes, f, allow_unicode=True, sort_keys=False)
        self.log_info(f"声骸数据已保存到 {save_path}")

    def on_stop(self):
        """任务停止时调用，确保数据保存"""
        if self.scanned_echoes:
            self._save_echo_data()
        self.log_info("鸣潮声骸扫描器已停止。")
