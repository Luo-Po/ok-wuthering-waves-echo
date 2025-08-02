import re
import time
from ok import TriggerTask, Box

class WuWaEchoScannerTask(TriggerTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "鸣潮声骸扫描器"
        self.description = "扫描游戏中的声骸数据并保存"
        self.default_config.update({
            'scan_count': 10,  # 默认扫描声骸数量
            'scan_delay': 0.5, # 默认扫描延迟
            'save_path': 'echoes.yaml', # 声骸数据保存路径
        })
        self.scanned_echoes = []
        self.current_scan_count = 0

    def run(self):
        # 检查是否在声骸背包页面
        # 假设通过OCR识别“声骸”字样来判断是否在声骸页面
        # 实际应用中可能需要更精确的特征匹配
        if not self.ocr(match="声骸", box="top_left"):
            self.log_info("不在声骸背包页面，等待进入...")
            return

        self.log_info(f"开始扫描声骸，已扫描 {self.current_scan_count}/{self.config.get('scan_count')}")

        # 模拟扫描一个声骸的逻辑
        # 实际中需要根据游戏界面布局，精确OCR声骸名称、主词条、副词条等
        # 这里仅为示例，假设每次run扫描一个声骸
        if self.current_scan_count < self.config.get('scan_count'):
            # 模拟识别声骸名称
            echo_name_box = self.ocr(box=Box(x=0.1, y=0.2, width=0.2, height=0.05)) # 示例坐标
            echo_name = echo_name_box[0].name if echo_name_box else f"未知声骸_{self.current_scan_count}"

            # 模拟识别主词条
            main_stat_box = self.ocr(box=Box(x=0.1, y=0.3, width=0.2, height=0.05)) # 示例坐标
            main_stat = main_stat_box[0].name if main_stat_box else "未知主词条"

            # 模拟识别副词条 (需要多次OCR或更复杂的逻辑)
            sub_stats = []
            for i in range(4): # 假设有4个副词条
                sub_stat_box = self.ocr(box=Box(x=0.1, y=0.4 + i * 0.05, width=0.2, height=0.05)) # 示例坐标
                if sub_stat_box: 
                    sub_stats.append(sub_stat_box[0].name)
                else:
                    sub_stats.append(f"未知副词条_{i}")

            echo_data = {
                "name": echo_name,
                "main_stat": main_stat,
                "sub_stats": sub_stats,
                "scanned_time": time.time()
            }
            self.scanned_echoes.append(echo_data)
            self.current_scan_count += 1
            self.log_info(f"扫描到声骸: {echo_name}")

            # 模拟滚动到下一个声骸
            self.scroll("down") # 示例操作，实际可能需要更精确的滚动或点击下一页
            self.sleep(self.config.get('scan_delay'))
        else:
            self.log_info("声骸扫描完成，保存数据...")
            self._save_echo_data()
            self.log_info("扫描任务结束，请手动停止触发器。")
            # 实际中可能需要一个机制来自动停止TriggerTask，或者通知用户停止
            # self.stop() # 如果有stop方法可以调用

    def _save_echo_data(self):
        # 将scanned_echoes保存到yaml文件
        import yaml
        save_path = self.config.get('save_path')
        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.scanned_echoes, f, allow_unicode=True)
        self.log_info(f"声骸数据已保存到 {save_path}")

    def on_stop(self):
        # 任务停止时调用，确保数据保存
        if self.scanned_echoes:
            self._save_echo_data()
        self.log_info("鸣潮声骸扫描器已停止。")


