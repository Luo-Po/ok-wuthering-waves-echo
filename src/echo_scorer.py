# 鸣潮声骸评分系统
# 版本: 1.0
# 描述: 用于计算鸣潮游戏中声骸的评分系统，基于角色属性、伤害乘区和极限积点数据


from src.Echo import Echo
from src.data import role_list, rule_list, role_sum_property

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


def sum_cost_scores(cost: Echo, role):
    print(cost.to_dict(), role)
    """计算声骸总得分"""
    if not cost or not role:
        return 0.0

    main_attr_score = count_main_attr(
        cost,  # 占位值
        role)

    sub_scores = 0.0
    if cost.property_list:
        for prop in cost.property_list:
            sub_scores += count_scores(prop, role)
            print(count_scores(prop, role))

    return round(main_attr_score + sub_scores, 2)


def sum_count_sub_scores(cts, role) -> float:
    rel = 0.0
    for ct in cts:
        rel += count_scores(ct, role)
    return round(rel, 2)


def count_scores(ct, role) -> float:
    """计算词条分数"""
    if role is None or ct is None:
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
        xs = xs_map.get(ct["property"], 0.0)
        # 处理百分号
        value_str = ct["value"].replace("%", "")
        value = float(value_str)
        # 计算分数
        score = value * xs * 100 / float(rule_type["maxscore"])
        return round(score, 2)

    except KeyError as e:
        print(f"计算分数时缺少关键字段: {e}")
        return 0.0


def count_main_attr2(current_cost: Echo, cur_role):
    """仅计算基础属性分数"""
    base_attr_map = {
        "Cost1": {"property": "生命", "value": "2280"},
        "Cost3": {"property": "小攻击", "value": "100"},
        "Cost4": {"property": "小攻击", "value": "150"},
    }

    base_attr = base_attr_map.get(current_cost.cost, None)
    if base_attr:
        return count_scores(base_attr, cur_role)
    return 0.0


def count_main_attr(current_cost: Echo, cur_role):
    """计算主属性分数（含基础属性）"""
    # 基础属性映射
    base_attr_map = {
        "Cost1": {"property": "生命", "value": "2280"},
        "Cost3": {"property": "小攻击", "value": "100"},
        "Cost4": {"property": "小攻击", "value": "150"},
    }

    # 主属性转换
    main_attr_map = {
        "暴击22%": {"property": "暴击", "value": "22%"},
        "暴击22.0%": {"property": "暴击", "value": "22%"},
        "暴伤44%": {"property": "暴伤", "value": "44%"},
        "暴伤44.0%": {"property": "暴伤", "value": "44%"},
        "生命33%": {"property": "大生命", "value": "33%"},
        "攻击力33%": {"property": "大攻击", "value": "33%"},
        "防御41.8%": {"property": "大防御", "value": "41.8%"},
        "治疗26.4%": {"property": "治疗", "value": "26.4%"},
        "攻击力30%": {"property": "大攻击", "value": "30%"},
        "属伤30%": {"property": "属伤", "value": "30%"},
        "生命30%": {"property": "大生命", "value": "30%"},
        "共鸣效率32%": {"property": "共鸣效率", "value": "32%"},
        "防御38%": {"property": "大防御", "value": "38%"},
        "攻击力18%": {"property": "大攻击", "value": "18%"},
        "攻击18%": {"property": "大攻击", "value": "18%"},
        "生命22.8%": {"property": "大生命", "value": "22.8%"},
        "防御18%": {"property": "大防御", "value": "18%"},
    }

    # 计算基础属性分数
    base_attr = base_attr_map.get(current_cost.cost, None)
    base_score = count_scores(
        base_attr, cur_role
    ) if base_attr else 0.0

    # 计算主属性分数
    main_attr = main_attr_map.get(current_cost.main_attr, None)
    main_score = count_scores(
        main_attr, cur_role
    ) if main_attr else 0.0

    return round(base_score + main_score, 2)


def __init__():
    """
        初始化评分器，加载角色数据和权重配置
        """


def main():
    role = {
        "roleListId": 38,
        "ming": 0  # 0命
    }

    # 测试声骸对象 (4号位)
    cost = Echo(
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
    # # 测试中文数字转换
    # print("中文数字测试:")
    # print(f"123 -> {num_to_chinese(123)}")  # 一百二十三
    # print(f"10086 -> {num_to_chinese(10086)}")  # 一万零八十六
    # print()

    # # 测试缓存功能
    # print("缓存功能测试:")
    # test_data = {"test": "data"}
    # save_data_to_cache(test_data)
    # cached = get_data_from_cache("mcData")
    # print(f"缓存内容: {cached}")
    # print()

    # 测试词条分数计算
    print("词条分数计算测试:")
    print("命座规则测试:")
    ming_role = {"roleListId": 38, "ming": 1}
    for crit_entry in cost.property_list:
        crit_score = count_scores(crit_entry, role)
        # print(f"{crit_entry["property"]}{crit_entry["value"]} 分数: {crit_score}")
        ming_crit_score = count_scores(crit_entry, ming_role)
        print(f"1命{crit_entry["property"]}{crit_entry["value"]} 分数: {ming_crit_score} (对比0命: {crit_score})")
    print()

    # 测试声骸总分计算
    print("声骸总分计算测试:")
    total_score = sum_cost_scores(cost, role)
    # 计算1命下的声骸总分
    ming_total_score = sum_cost_scores(cost, ming_role)
    print(f"1命声骸总分: {ming_total_score} (对比0命: {total_score})")
    print()

    # 测试主属性计算
    print("主属性计算测试:")
    main_attr_score = count_main_attr(cost, role)
    print(f"主属性+基础属性分数: {main_attr_score}")

    base_attr_score = count_main_attr2(cost, role)
    print(f"仅基础属性分数: {base_attr_score}")
    print()

    # 测试命座规则
    print("命座规则测试:")
    ming_role = {"roleListId": 1, "ming": 1}  # 1命今汐

    # 计算1命下的声骸总分
    ming_total_score = sum_cost_scores(cost, ming_role)
    print(f"1命声骸总分: {ming_total_score} (对比0命: {total_score})")


if __name__ == '__main__':
    main()
