# 鸣潮声骸评分系统
# 版本: 1.0
# 描述: 用于计算鸣潮游戏中声骸的评分系统，基于角色属性、伤害乘区和极限积点数据


from src.Echo import Echo, EchoAttr
from src.data import role_list, rule_list, role_sum_property, main_attr_map

base_attr_map = {
    1: EchoAttr("小生命", "2280"),
    3: EchoAttr("小攻击", "100"),
    4: EchoAttr("小攻击", "150"),
}

"""
    鸣潮声骸评分器类
    提供声骸属性评分计算功能，支持不同角色类型和属性类型的权重计算
    """


def getIdByName(name):
    for role in role_list:
        if role["name"] == name:
            return role["id"]
    return None


def check_ming_config(role_id, role_sum_property):
    """校验角色是否配置了命座权重参数"""
    for item in role_sum_property:
        if item["id"] == role_id:
            if "mzProperty" in item:
                return True
    return False


def sum_scores(echo: Echo, role):
    """计算声骸总得分"""
    if not echo or not role:
        return 0.0

    main_attr_score = count_main_attr(echo, role)
    echo.set_main_score(main_attr_score)

    sub_scores = sum_sub_scores(echo, role)
    echo.set_sub_score(sub_scores)

    return round(main_attr_score + sub_scores, 2)


def sum_sub_scores(echo: Echo, role) -> float:
    rel = 0.0
    for echoAttr in echo.get_sub_attr_list():
        rel += sum_sub_score(echoAttr, role)
    echo.set_sub_score(rel)
    return round(rel, 2)


def sum_sub_score(echo_attr: EchoAttr, role) -> float:
    """计算词条分数"""
    if role is None or echo_attr is None:
        print("异常：数据关联角色失败。")
        return 0.0

    try:
        # 获取基础规则
        rule_type = role_list[role["roleListId"] - 1]
        cur_rule = rule_list[rule_type["rule"]]

        # 检查命座配置
        if check_ming_config(role["roleListId"], role_sum_property):
            if "ming" in role and int(role["ming"]) > 0:
                ming_idx = int(role["ming"]) - 1
                # 获取命座特殊规则
                for rsp in role_sum_property:
                    if rsp["id"] == role["roleListId"]:
                        rule_type = rsp["mzProperty"][ming_idx]
                        cur_rule = rsp["mzRule"][ming_idx]
                        break

        # 确定词条系数
        xs_map = {
            "暴击": cur_rule["crit"],
            "暴伤": cur_rule["critDamage"],
            "大攻击": cur_rule["attack01"],
            "小攻击": cur_rule["attack02"],
            "大生命": cur_rule["health01"],
            "小生命": cur_rule["health02"],
            "大防御": cur_rule["defense01"],
            "小防御": cur_rule["defense02"],
            "属伤": cur_rule["property"],
            "治疗": cur_rule["treat"],
            "共鸣效率": cur_rule["efficiency01"],
            "普攻伤害": cur_rule["unike"] * float(rule_type["normal"]),
            "重击伤害": cur_rule["unike"] * float(rule_type["heavy"]),
            "技能伤害": cur_rule["unike"] * float(rule_type["skill"]),
            "解放伤害": cur_rule["unike"] * float(rule_type["liberate"]),
        }
        xs = xs_map.get(echo_attr.get_attr(), 0.0)
        # 处理百分号
        value_str = echo_attr.get_value().replace("%", "")
        value = float(value_str)
        # 计算分数
        score = value * xs * 100 / float(rule_type["maxscore"])
        return round(score, 2)

    except KeyError as e:
        print(f"计算分数时缺少关键字段: {e}")
        return 0.0


def count_main_attr2(echo: Echo, role):
    """仅计算基础属性分数"""
    base_attr = base_attr_map.get(echo.get_cost(), None)
    if base_attr:
        return sum_sub_score(base_attr, role)
    return 0.0


def count_main_attr(echo: Echo, role):
    """计算主属性分数（含基础属性）"""
    # 计算基础属性分数
    base_score = count_main_attr2(echo, role)

    # 计算主属性分数
    main_attr = main_attr_map.get(echo.get_main_attr(), None)
    main_score = sum_sub_score(
        main_attr, role
    ) if main_attr else 0.0

    echo.set_main_score(main_score)
    return round(base_score + main_score, 2)
