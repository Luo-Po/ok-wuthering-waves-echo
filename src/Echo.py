from typing import List


class EchoAttr:
    """回音属性"""
    __attr: str
    __value: float

    def __init__(self, attr, value):
        self.__attr = attr
        self.__value = value

    def get_attr(self):
        return self.__attr

    def set_attr(self, attr):
        self.__attr = attr

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def to_dict(self):
        return {"attr": self.__attr, "value": self.__value}


class Echo:
    __name: str
    __cost: int
    __level: int
    __main_attr: EchoAttr
    __sub_attr_list: List[EchoAttr]
    __score: float
    __mian_score: float
    __sub_score: float

    def __init__(self, __name="", __cost=0, __main=EchoAttr("", 0.0), __level=0, __sub_list=None, ):
        if __sub_list is None:
            __sub_list = []
        self.__name = __name  # 名称 (字符串)
        self.__cost = __cost  # 类型 (字符串)
        self.__main_attr = __main  # 主属性 (Echo)
        self.__level = __level  # 等级 (字符串或整数)
        self.__sub_attr_list = __sub_list  # 属性列表 (Echo列表)
        self.__score = 0.0
        self.__main_score = 0.0
        self.__sub_score = 0.0

    @classmethod
    def from_dict(cls, data):
        """从字典创建echo对象"""
        return cls(
            __name=data.get("name", ""),
            __cost=data.get("cost", ""),  # 注意原始键名拼写
            __level=data.get("level", "0"),
            __sub_list=data.get("property_list", [])
        )

    def to_dict(self):
        """将对象转换为字典格式"""
        return {
            "name": self.__name,
            "cost": self.__cost,  # 保持原始键名拼写
            "level": self.__level,
            "score": self.__score,
            "property_list": [prop.to_dict() for prop in self.__sub_attr_list]
        }

    # ===== 新增的修改方法 =====
    def get_name(self) -> str:
        """获取名称"""
        return self.__name

    def set_name(self, new):
        """设置名称"""
        self.__name = new
        return self

    def get_cost(self) -> int:
        """获取花费"""
        return self.__cost

    def set_cost(self, new):
        """设置花费"""
        self.__cost = new
        return self

    def get_level(self) -> int:
        """获取等级"""
        return self.__level

    def set_level(self, new: int):
        """设置等级"""
        self.__level = new
        return self

    def get_main_attr(self) -> EchoAttr:
        """获取主属性"""
        return self.__main_attr

    def set_main_attr(self, attr, value):
        """设置主属性"""
        self.__main_attr = EchoAttr(attr, value)  # 确保转换为字符串
        return self

    def set_main(self, echo_attr):
        """设置主属性"""
        self.__main_attr = echo_attr  # 确保转换为字符串
        return self

    def get_sub_attr_list(self) -> List[EchoAttr]:
        """获取所有副属性"""
        return self.__sub_attr_list

    def get_sub_attr(self, index) -> EchoAttr:
        """获取副属性"""
        if index >= len(self.__sub_attr_list):
            raise Exception(f'DEBUG{self.__name},index out of range')

        return self.__sub_attr_list[index]

    def add_sub_attr(self, property___name, property_value):
        """添加新属性到末尾"""
        if len(self.__sub_attr_list) > 5:
            raise IndexError("属性索引超出范围")
        self.__sub_attr_list.append(EchoAttr(property___name, property_value))
        return self

    def set_sub_attr(self, index, new_attr=None, new_value=None):
        """
        更新指定索引处的属性
        可单独更新名称或值，或同时更新两者
        """
        if index < 0 or index >= len(self.__sub_attr_list):
            raise IndexError("属性索引超出范围")
        self.__sub_attr_list[index] = EchoAttr(new_attr, new_value)
        return self

    def del_sub_attr(self, index):
        """删除指定索引处的属性"""
        if index < 0 or index >= len(self.__sub_attr_list):
            raise IndexError("属性索引超出范围")
        del self.__sub_attr_list[index]
        return self

    def find_sub_attrs(self, property___name):
        """查找特定名称的所有属性"""
        return [prop for prop in self.__sub_attr_list if prop == property___name]

    def get_score(self):
        """获取得分"""
        return self.__score

    def set_score(self, new):
        """设置得分"""
        self.__score = new
        return self

    def get_main_score(self):
        """获取主词条得分"""
        return self.__main_score

    def set_main_score(self, new):
        """设置主词条得分"""
        self.__main_score = new
        return self

    def get_sub_score(self):
        """获取副词条得分"""
        return self.__sub_score

    def set_sub_score(self, new):
        """设置副词条得分"""
        self.__sub_score = new
        return self


def contrast_echo(a: Echo, b: Echo) -> bool:
    if not a.get_cost() == b.get_cost():
        return False
    elif not a.get_name == b.get_name:
        return False
    elif not a.get_cost == b.get_cost:
        return False
    elif not len(a.get_sub_attr_list()) == len(b.get_sub_attr_list()):
        return False
    for i, p in enumerate(a.get_sub_attr_list()):
        if not p == b.get_sub_attr_list()[i]:
            return False
    return True
