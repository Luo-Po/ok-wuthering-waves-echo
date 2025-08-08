from ok import TriggerTask

from src.globals import Globals


class Telemetry(TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "遥测"
        self.description = """
        目前仅针对强化流程这一功能
        并且由于作者只是个菜鸡本功能仅是将部分数据记录到一个名为Telemetry的文件中并无上传功能
        """
        self.trigger_count = 0

    def enable(self):
        """
        启用触发任务。
        """
        Globals(exit_event=None).set_telemetry(True)

    def disable(self):
        """
        禁用触发任务。
        """
        Globals(exit_event=None).set_telemetry(False)
