import re

from src.tasks.MyBaseTask import MyBaseTask
from src.utils.wuwa_scanner_utils import box_list, match_list


class MyOneTimeTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "点击触发运行任务"
        self.description = "用户点击时调用run方法"
        self.default_config.update({
            '下拉菜单选项': "第一",
            '是否选项默认支持': False,
            'int选项': 1,
            '文字框选项': "默认文字",
            '长文字框选项': "默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字",
            'list选项': ['第一', '第二', '第3'],
        })
        self.config_type["下拉菜单选项"] = {'type': "drop_down",
                                            'options': ['第一', '第二', '第3']}

    def run(self):
        while True:
            self.sleep(1)
            self.ocr(match=match_list["level"], box=box_list["echo_change"]["level"])

    def find_some_text_on_bottom_right(self):
        return self.ocr(box="bottom_right", match="商城", log=True)  # 指定box以提高ocr速度

    def find_some_text_with_relative_box(self):
        return self.ocr(0.5, 0.5, 1, 1, match=re.compile("招"), log=True)  # 指定box以提高ocr速度

    def test_find_one_feature(self):
        return self.find_one('box_battle_1')

    def test_find_feature_list(self):
        return self.find_feature('box_battle_1')

    def run_for_5(self):
        self.operate(lambda: self.do_run_for_5())

    def do_run_for_5(self):
        self.do_send_key_down('w')
        self.sleep(0.1)
        self.do_mouse_down(key='right')
        self.sleep(0.1)
        self.do_mouse_up(key='right')
        self.sleep(5)
        self.do_send_key_up('w')
