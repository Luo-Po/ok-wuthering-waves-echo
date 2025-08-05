from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional

from Echo import Echo, EchoAttr


class EchoRarity(Enum):
    """回音稀有度"""
    COMMON = 1  # 1星
    UNCOMMON = 2  # 2星
    RARE = 3  # 3星
    EPIC = 4  # 4星
    LEGENDARY = 5  # 5星


class EchoType(Enum):
    """回音类型"""
    CALAMITY = "Calamity"  # 灾变
    OVERLORD = "Overlord"  # 霸主
    ELITE = "Elite"  # 精英
    COMMON_CLASS = "Common Class"  # 通用


class StatType(Enum):
    """属性类型"""
    ATK = "攻击力"
    ATK_PERCENT = "攻击力%"
    HP = "生命值"
    HP_PERCENT = "生命值%"
    DEF = "防御力"
    DEF_PERCENT = "防御力%"
    CRIT_RATE = "暴击率"
    CRIT_DMG = "暴击伤害"
    ENERGY_REGEN = "共鸣效率"
    ELEMENTAL_DMG = "属性伤害加成"
    HEALING_BONUS = "治疗效果加成"


@dataclass
class EchoSet:
    """回音套装"""
    name: str  # 套装名称
    two_piece_effect: str  # 2件套效果
    five_piece_effect: str  # 5件套效果


@dataclass
class Character:
    """角色数据"""
    name: str  # 角色名称
    element: str  # 属性
    weapon_type: str  # 武器类型
    base_stats: Dict[str, float]  # 基础属性


class EchoDatabase:
    """回音数据库"""

    def __init__(self):
        self.echo_sets = self._initialize_echo_sets()
        self.characters = self._initialize_characters()

    def _initialize_echo_sets(self) -> Dict[str, EchoSet]:
        """初始化回音套装数据"""
        return {
            "破浪踏潮": EchoSet(
                name="破浪踏潮",
                two_piece_effect="水属性伤害加成+10%",
                five_piece_effect="施放共鸣技能后，下一个共鸣技能造成的伤害提升22%，持续15秒"
            ),
            "熔山裂谷": EchoSet(
                name="熔山裂谷",
                two_piece_effect="熔化属性伤害加成+10%",
                five_piece_effect="施放共鸣技能后，攻击力提升22%，持续15秒"
            ),
            "彻空冥雷": EchoSet(
                name="彻空冥雷",
                two_piece_effect="导电属性伤害加成+10%",
                five_piece_effect="施放共鸣技能后，攻击力提升22%，持续15秒"
            ),
            "啸谷长风": EchoSet(
                name="啸谷长风",
                two_piece_effect="气动属性伤害加成+10%",
                five_piece_effect="施放共鸣技能后，攻击力提升22%，持续15秒"
            ),
            "沉日劫明": EchoSet(
                name="沉日劫明",
                two_piece_effect="湮灭属性伤害加成+10%",
                five_piece_effect="施放共鸣技能后，攻击力提升22%，持续15秒"
            ),
            "凝夜白霜": EchoSet(
                name="凝夜白霜",
                two_piece_effect="凝结属性伤害加成+10%",
                five_piece_effect="施放共鸣技能后，攻击力提升22%，持续15秒"
            ),
            "隐世回光": EchoSet(
                name="隐世回光",
                two_piece_effect="治疗效果加成+10%",
                five_piece_effect="施放共鸣技能后，为队伍中生命值最低的角色恢复生命值"
            ),
            "不绝余音": EchoSet(
                name="不绝余音",
                two_piece_effect="攻击力+10%",
                five_piece_effect="施放共鸣技能后，队伍中所有角色攻击力提升20%，持续20秒"
            )
        }

    def _initialize_characters(self) -> Dict[str, Character]:
        """初始化角色数据"""
        return {
            "漂泊者": Character(
                name="漂泊者",
                element="光谱",
                weapon_type="剑",
                base_stats={"攻击力": 344, "生命值": 12405, "防御力": 1165}
            ),
            "秧秧": Character(
                name="秧秧",
                element="导电",
                weapon_type="矩阵",
                base_stats={"攻击力": 267, "生命值": 13348, "防御力": 1606}
            ),
            "白芷": Character(
                name="白芷",
                element="凝结",
                weapon_type="矩阵",
                base_stats={"攻击力": 274, "生命值": 15552, "防御力": 1485}
            ),
            # 可以继续添加更多角色
        }


def parse_stat_from_text(text: str) -> Optional[EchoAttr]:
    """从文本解析属性"""
    import re

    # 匹配百分比属性
    percent_match = re.search(r'(.+?)\+(\d+(?:\.\d+)?)%', text)
    if percent_match:
        stat_name = percent_match.group(1).strip()
        value = float(percent_match.group(2))
        return EchoAttr(attr=stat_name, value=value)

    # 匹配固定数值属性
    fixed_match = re.search(r'(.+?)\+(\d+(?:\.\d+)?)', text)
    if fixed_match:
        stat_name = fixed_match.group(1).strip()
        value = float(fixed_match.group(2))
        return EchoAttr(attr=stat_name, value=value)

    return None


def calculate_echo_score(echo: Echo, target_stats: List[str]) -> float:
    """计算回音评分"""
    score = 0.0

    # 主词条评分
    if echo.get_main_attr().attr in target_stats:
        score += 100  # 主词条权重较高

    # 副词条评分
    for sub_stat in echo.get_sub_attr_list():
        if sub_stat.stat_type in target_stats:
            # 根据数值和是否为百分比属性给分
            if sub_stat.is_percentage:
                score += sub_stat.value * 2  # 百分比属性权重更高
            else:
                score += sub_stat.value * 0.1  # 固定数值属性权重较低

    return score
