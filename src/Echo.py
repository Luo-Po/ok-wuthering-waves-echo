class Echo:
    def __init__(self, name, costType, mainAttr, level, score, propertyList):
        self.name = name  # 名称 (字符串)
        self.type = costType  # 类型 (字符串)
        self.mainAttr = mainAttr  # 主属性 (字符串)
        self.level = level  # 等级 (字符串或整数)
        self.score = score  # 评分 (字符串或浮点数)
        self.propertyList = propertyList  # 属性列表 (字典列表)

    @classmethod
    def from_dict(cls, data):
        """从字典创建echo对象"""
        return cls(
            name=data.get("name", ""),
            costType=data.get("type", ""),
            mainAttr=data.get("mainAtrri", ""),  # 注意原始键名拼写
            level=data.get("level", "0"),
            score=data.get("score", "0.00"),
            propertyList=data.get("propertyList", [])
        )

    def to_dict(self):
        """将对象转换为字典格式"""
        return {
            "name": self.name,
            "type": self.type,
            "mainAtrri": self.mainAttr,  # 保持原始键名拼写
            "level": self.level,
            "score": self.score,
            "propertyList": self.propertyList
        }

    def __repr__(self):
        """对象的官方字符串表示"""
        return (
            f"Echo(name={self.name!r}, type={self.type!r}, "
            f"mainAttr={self.mainAttr!r}, level={self.level!r}, "
            f"score={self.score!r}, properties={self.propertyList})"
        )


# 使用示例
if __name__ == "__main__":
    # 原始数据
    data = {
        "name": "飞廉之猩",
        "type": "Cost4",
        "mainAtrri": "暴击22.0%",
        "level": "25",
        "score": "16.62",
        "propertyList": [
            {"property": "暴击", "value": "10.5%"},
            {"property": "大生命", "value": "7.9%"},
            {"property": "共鸣效率", "value": "10.8%"},
            {"property": "重击伤害", "value": "6.4%"},
            {"property": "小生命", "value": "390"}
        ]
    }

    # 从字典创建对象
    echo_item = Echo.from_dict(data)

    # 打印对象信息
    print("Object representation:")
    print(echo_item)

    # 转换回字典
    print("\nDictionary representation:")
    print(echo_item.to_dict())