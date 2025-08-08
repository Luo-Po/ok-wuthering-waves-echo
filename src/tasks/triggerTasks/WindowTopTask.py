from ok import TriggerTask

from src.utils.windows_utils import get_active_window, set_window_topmost


class WindowTopTask(TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "窗口置顶"
        self.description = "开启后可以保持当前窗口一直显示在屏幕上"
        self.trigger_count = 0

    def run(self):
        {}

    def enable(self):
        """
        启用触发任务。
        """
        set_window_topmost(get_active_window(), True)
        print(self.get_status())

    def disable(self):
        """
        禁用触发任务。
        """
        set_window_topmost(get_active_window(), False)
        print(self.get_status())
