# 弗洛洛声骸分数计算测试脚本
# 描述: 用于计算弗洛洛声骸的分数，验证用户提供的数据

from echo_scorer import EchoScorer

def calculate_fuluolo_score():
    """
    计算弗洛洛声骸的分数
    :return: 分数
    """
    # 初始化评分器
    scorer = EchoScorer()
    
    # 弗洛洛的声骸属性
    fuluolo_attributes = {
        '暴伤': 17.4,
        '大防御': 9.0,
        '暴击': 8.7,
        '小生命': 430,
        '专伤': 7.9  # 技伤属于专伤
    }
    
    # 计算分数
    score = scorer.calculate_score('弗洛洛', fuluolo_attributes)
    
    # 打印详细信息
    print("弗洛洛声骸评分计算详情:")
    print(f"- 暴伤 17.4%: {17.4 * 0.9} 积点")
    print(f"- 大防御 9.0%: 0 积点 (生防属性权重为0)")
    print(f"- 暴击 8.7%: {8.7 * 1.8} 积点")
    print(f"- 小生命 430: 0 积点 (生防属性权重为0)")
    print(f"- 技伤 7.9%: {7.9 * 1.0 * 0.40} 积点 (技能占比40%)")
    print(f"总积点: {17.4*0.9 + 8.7*1.8 + 7.9*1.0*0.40}")
    print(f"弗洛洛极限积点: {scorer.character_max_points['弗洛洛']}")
    print(f"最终分数: {score}分")
    
    return score

if __name__ == "__main__":
    calculate_fuluolo_score()