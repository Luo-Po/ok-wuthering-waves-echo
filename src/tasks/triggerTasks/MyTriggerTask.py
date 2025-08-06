from ok import TriggerTask

from src.utils.windows_utils import is_window_topmost, get_active_window, set_window_topmost


class MyTriggerTask(TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "置顶当前窗口"
        self.description = "开启后可以保持当前窗口一直显示在屏幕上"
        self.trigger_count = 0

    def run(self):
        self.trigger_count += 1
        self.log_debug(f'MyTriggerTask run {self.trigger_count}')
        if is_window_topmost(get_active_window()):
            set_window_topmost(get_active_window())
            print("置顶")

    def enable(self):
        """
        启用触发任务。
        """
        set_window_topmost(get_active_window(), True)

    def disable(self):
        """
        禁用触发任务。
        """
        set_window_topmost(get_active_window(), False)
