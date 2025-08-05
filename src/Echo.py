class Echo:
    def __init__(self, name="", costType="", main_attr="", level="", score="", sub_score="", property_list=None):
        if property_list is None:
            property_list = []
        self.name = name  # 名称 (字符串)
        self.cost = costType  # 类型 (字符串)
        self.main_attr = main_attr  # 主属性 (字符串)
        self.level = level  # 等级 (字符串或整数)
        self.score = score  # 评分 (字符串或浮点数)
        self.sub_score = sub_score
        self.property_list = property_list  # 属性列表 (字典列表)

    @classmethod
    def from_dict(cls, data):
        """从字典创建echo对象"""
        return cls(
            name=data.get("name", ""),
            costType=data.get("type", ""),
            main_attr=data.get("main_attr", ""),  # 注意原始键名拼写
            level=data.get("level", "0"),
            score=data.get("score", "0.00"),
            property_list=data.get("property_list", [])
        )

    def to_dict(self):
        """将对象转换为字典格式"""
        return {
            "name": self.name,
            "type": self.cost,
            "main_attr": self.main_attr,  # 保持原始键名拼写
            "level": self.level,
            "score": self.score,
            "property_list": self.property_list
        }

    def __repr__(self):
        """对象的官方字符串表示"""
        return (
            f"Echo(name={self.name!r}, type={self.cost!r}, "
            f"main_attr={self.main_attr!r}, level={self.level!r}, "
            f"score={self.score!r}, properties={self.property_list})"
        )

    # ===== 新增的修改方法 =====

    def update_name(self, new_name):
        """更新名称"""
        self.name = new_name
        return self

    def update_type(self, new_type):
        """更新类型"""
        self.cost = new_type
        return self

    def update_main_attr(self, new_main_attr):
        """更新主属性"""
        self.main_attr = new_main_attr
        return self

    def update_level(self, new_level):
        """更新等级"""
        self.level = str(new_level)  # 确保转换为字符串
        return self

    def update_score(self, new_score):
        """更新评分"""
        self.score = str(new_score)  # 确保转换为字符串
        return self

    def add_property(self, property_name, property_value):
        """添加新属性"""
        self.property_list.append({
            "property": property_name,
            "value": property_value
        })
        return self

    def update_property(self, index, new_name=None, new_value=None):
        """
        更新指定索引处的属性
        可单独更新名称或值，或同时更新两者
        """
        if index < 0 or index >= len(self.property_list):
            raise IndexError("属性索引超出范围")

        prop = self.property_list[index]
        if new_name is not None:
            prop["property"] = new_name
        if new_value is not None:
            prop["value"] = new_value

        return self

    def remove_property(self, index):
        """删除指定索引处的属性"""
        if index < 0 or index >= len(self.property_list):
            raise IndexError("属性索引超出范围")

        del self.property_list[index]
        return self

    def find_properties(self, property_name):
        """查找特定名称的所有属性"""
        return [prop for prop in self.property_list if prop["property"] == property_name]

    def upgrade_level(self, levels=1):
        """提升等级"""
        try:
            current_level = int(self.level)
            self.level = str(current_level + levels)
        except ValueError:
            raise ValueError("等级不是有效的整数")
        return self

    def recalc_score(self, formula):
        """
        使用自定义公式重新计算评分
        formula: 函数，接受property_list并返回分数
        """
        try:
            self.score = str(formula(self.property_list))
        except Exception as e:
            raise ValueError(f"评分计算失败: {str(e)}")
        return self


def contrast_echo(a: Echo, b: Echo) -> bool:
    if not a.cost == b.cost:
        return False
    elif not a.name == b.name:
        return False
    elif not a.main_attr == b.main_attr:
        return False
    elif not len(a.property_list) == len(b.property_list):
        return False
    for i, p in enumerate(a.property_list):
        if not p == b.property_list[i]:
            return False
    return True


# 使用示例
if __name__ == "__main__":
    # 创建初始对象
    cost_item = Echo(
        name="飞廉之猩",
        costType="Cost4",
        main_attr="暴击22.0%",
        level="25",
        score="16.62",
        property_list=[
            {"property": "暴击", "value": "10.5%"},
            {"property": "大生命", "value": "7.9%"},
            {"property": "共鸣效率", "value": "10.8%"},
            {"property": "重击伤害", "value": "6.4%"},
            {"property": "小生命", "value": "390"}
        ]
    )

    print("初始状态:")
    print(cost_item.to_dict())

    # 使用修改方法
    (cost_item.update_name("风暴之怒")
     .update_type("Cost5")
     .update_level(30)
     .add_property("防御力", "5.8%")
     .update_property(1, new_value="9.2%")  # 更新大生命值
     .remove_property(4)  # 删除小生命
     .upgrade_level(5))

    print("\n修改后状态:")
    print(cost_item.to_dict())

    # 查找属性
    print("\n查找'暴击'属性:")
    print(cost_item.find_properties("暴击"))


    # 重新计算评分（示例公式）
    def simple_score_formula(properties):
        """简单的评分公式示例"""
        score = 0
        for prop in properties:
            if "暴击" in prop["property"]:
                score += float(prop["value"].rstrip('%'))
            elif "伤害" in prop["property"]:
                score += float(prop["value"].rstrip('%')) * 0.8
        return round(score, 2)


    cost_item.recalc_score(simple_score_formula)
    print("\n重新计算评分后:")
    print(f"新评分: {cost_item.score}")
