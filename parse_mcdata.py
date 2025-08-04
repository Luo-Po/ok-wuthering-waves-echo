import json
import sys
from src.Echo import Echo

def parse_mcdata(role_name):
    # 读取mcdata.json文件
    with open('e:\\project\\ok-script-boilerplate\\assets\\mcdata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 查找指定角色
    target_role = None
    for role in data.get('role', []):
        if role.get('name') == role_name:
            target_role = role
            break

    if not target_role:
        print(f"未找到角色: {role_name}")
        return []

    # 提取声骸数据并转换为Echo对象
    echo_list = []
    for cost in target_role.get('costList', []):
        # 提取消耗点数
        cost_type = cost.get('type', '')
        cost_value = int(cost_type.replace('Echo', '')) if cost_type.startswith('Echo') else 0

        # 提取主属性
        main_attr = cost.get('mainAtrri', {})
        main_stat = main_attr.get('property', '')
        main_value_str = main_attr.get('value', '0%')
        # 去除百分号并转换为浮点数
        main_value = float(main_value_str.replace('%', '')) if '%' in main_value_str else float(main_value_str)

        # 提取副属性
        sub_stats = {}
        for prop in cost.get('propertyList', []):
            prop_name = prop.get('property', '')
            prop_value_str = prop.get('value', '0%')
            # 去除百分号并转换为浮点数
            prop_value = float(prop_value_str.replace('%', '')) if '%' in prop_value_str else float(prop_value_str)
            sub_stats[prop_name] = prop_value

        # 创建Echo对象
        echo = Echo(
            name=cost.get('name', ''),
            cost=cost_value,
            main_stat=main_stat,
            main_value=main_value,
            sub_stats=sub_stats,
            character=role_name
        )
        echo_list.append(echo)

    return echo_list

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("用法: python parse_mcdata.py <角色名> [输出文件路径]")
        sys.exit(1)

    role_name = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else None

    echo_array = parse_mcdata(role_name)
    if not echo_array:
        sys.exit(1)

    # 转换为字典列表
    echo_dicts = [echo.to_dict() for echo in echo_array]

    # 输出结果
    json_result = json.dumps(echo_dicts, ensure_ascii=False, indent=4)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_result)
        print(f"结果已保存到: {output_file}")
    else:
        print(json_result)