import random
import copy
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from src.wuwa_echo_data import Echo, EchoSet, Character, calculate_echo_score

@dataclass
class OptimizationConfig:
    """优化配置"""
    population_size: int = 50
    generations: int = 100
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    elite_ratio: float = 0.1
    target_stats: List[str] = None
    character: Optional[Character] = None
    preferred_sets: List[str] = None

class EchoCombination:
    """回音组合"""
    
    def __init__(self, echoes: List[Echo]):
        self.echoes = echoes[:5]  # 最多5个回音
        self.fitness = 0.0
        self.set_bonuses = {}
    
    def calculate_fitness(self, config: OptimizationConfig) -> float:
        """计算适应度"""
        if not self.echoes:
            return 0.0
        
        total_score = 0.0
        
        # 1. 基础属性评分
        for echo in self.echoes:
            if config.target_stats:
                total_score += calculate_echo_score(echo, config.target_stats)
        
        # 2. 套装效果评分
        set_counts = self._count_sets()
        set_bonus_score = self._calculate_set_bonus_score(set_counts, config)
        total_score += set_bonus_score
        
        # 3. 回音消耗限制 (总消耗不能超过12)
        total_cost = sum(echo.cost for echo in self.echoes)
        if total_cost > 12:
            total_score *= 0.5  # 超出消耗限制的惩罚
        
        # 4. 位置限制 (每个位置只能装备一个回音)
        positions = [echo.position for echo in self.echoes]
        if len(set(positions)) != len(positions):
            total_score *= 0.3  # 位置冲突的惩罚
        
        self.fitness = total_score
        return total_score
    
    def _count_sets(self) -> Dict[str, int]:
        """统计套装数量"""
        set_counts = {}
        for echo in self.echoes:
            if echo.set_name:
                set_counts[echo.set_name] = set_counts.get(echo.set_name, 0) + 1
        return set_counts
    
    def _calculate_set_bonus_score(self, set_counts: Dict[str, int], config: OptimizationConfig) -> float:
        """计算套装加成评分"""
        bonus_score = 0.0
        
        for set_name, count in set_counts.items():
            # 2件套加成
            if count >= 2:
                bonus_score += 50
                if config.preferred_sets and set_name in config.preferred_sets:
                    bonus_score += 25  # 偏好套装额外加分
            
            # 5件套加成
            if count >= 5:
                bonus_score += 150
                if config.preferred_sets and set_name in config.preferred_sets:
                    bonus_score += 75  # 偏好套装额外加分
        
        return bonus_score
    
    def get_total_stats(self) -> Dict[str, float]:
        """获取总属性"""
        total_stats = {}
        
        for echo in self.echoes:
            # 主词条
            main_stat = echo.main_stat
            if main_stat.stat_type not in total_stats:
                total_stats[main_stat.stat_type] = 0
            total_stats[main_stat.stat_type] += main_stat.value
            
            # 副词条
            for sub_stat in echo.sub_stats:
                if sub_stat.stat_type not in total_stats:
                    total_stats[sub_stat.stat_type] = 0
                total_stats[sub_stat.stat_type] += sub_stat.value
        
        return total_stats

class GeneticAlgorithmOptimizer:
    """遗传算法优化器"""
    
    def __init__(self, echo_pool: List[Echo], config: OptimizationConfig):
        self.echo_pool = echo_pool
        self.config = config
        self.population: List[EchoCombination] = []
        self.best_individual: Optional[EchoCombination] = None
        self.generation_stats = []
    
    def optimize(self) -> EchoCombination:
        """执行优化"""
        # 初始化种群
        self._initialize_population()
        
        for generation in range(self.config.generations):
            # 计算适应度
            self._evaluate_population()
            
            # 记录统计信息
            self._record_generation_stats(generation)
            
            # 选择、交叉、变异
            self._evolve_population()
        
        # 最终评估
        self._evaluate_population()
        return self.best_individual
    
    def _initialize_population(self):
        """初始化种群"""
        self.population = []
        
        for _ in range(self.config.population_size):
            # 随机选择回音组合
            combination_size = random.randint(3, 5)  # 3-5个回音
            selected_echoes = random.sample(self.echo_pool, 
                                          min(combination_size, len(self.echo_pool)))
            
            # 确保位置不冲突
            selected_echoes = self._ensure_unique_positions(selected_echoes)
            
            combination = EchoCombination(selected_echoes)
            self.population.append(combination)
    
    def _ensure_unique_positions(self, echoes: List[Echo]) -> List[Echo]:
        """确保回音位置不冲突"""
        used_positions = set()
        valid_echoes = []
        
        for echo in echoes:
            if echo.position not in used_positions:
                valid_echoes.append(echo)
                used_positions.add(echo.position)
        
        return valid_echoes
    
    def _evaluate_population(self):
        """评估种群适应度"""
        for individual in self.population:
            individual.calculate_fitness(self.config)
        
        # 排序并更新最佳个体
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        if not self.best_individual or self.population[0].fitness > self.best_individual.fitness:
            self.best_individual = copy.deepcopy(self.population[0])
    
    def _record_generation_stats(self, generation: int):
        """记录代数统计信息"""
        fitnesses = [ind.fitness for ind in self.population]
        stats = {
            'generation': generation,
            'best_fitness': max(fitnesses),
            'avg_fitness': sum(fitnesses) / len(fitnesses),
            'worst_fitness': min(fitnesses)
        }
        self.generation_stats.append(stats)
    
    def _evolve_population(self):
        """进化种群"""
        new_population = []
        
        # 精英保留
        elite_count = int(self.config.population_size * self.config.elite_ratio)
        new_population.extend(self.population[:elite_count])
        
        # 生成新个体
        while len(new_population) < self.config.population_size:
            # 选择父母
            parent1 = self._tournament_selection()
            parent2 = self._tournament_selection()
            
            # 交叉
            if random.random() < self.config.crossover_rate:
                child1, child2 = self._crossover(parent1, parent2)
            else:
                child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
            
            # 变异
            if random.random() < self.config.mutation_rate:
                child1 = self._mutate(child1)
            if random.random() < self.config.mutation_rate:
                child2 = self._mutate(child2)
            
            new_population.extend([child1, child2])
        
        # 截断到指定大小
        self.population = new_population[:self.config.population_size]
    
    def _tournament_selection(self, tournament_size: int = 3) -> EchoCombination:
        """锦标赛选择"""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda x: x.fitness)
    
    def _crossover(self, parent1: EchoCombination, parent2: EchoCombination) -> Tuple[EchoCombination, EchoCombination]:
        """交叉操作"""
        # 单点交叉
        all_echoes = parent1.echoes + parent2.echoes
        
        # 去重并随机选择
        unique_echoes = []
        seen_positions = set()
        
        for echo in all_echoes:
            if echo.position not in seen_positions:
                unique_echoes.append(echo)
                seen_positions.add(echo.position)
        
        # 创建两个子代
        child1_size = random.randint(3, min(5, len(unique_echoes)))
        child2_size = random.randint(3, min(5, len(unique_echoes)))
        
        child1_echoes = random.sample(unique_echoes, child1_size)
        child2_echoes = random.sample(unique_echoes, child2_size)
        
        return EchoCombination(child1_echoes), EchoCombination(child2_echoes)
    
    def _mutate(self, individual: EchoCombination) -> EchoCombination:
        """变异操作"""
        if not individual.echoes or not self.echo_pool:
            return individual
        
        mutation_type = random.choice(['replace', 'add', 'remove'])
        
        if mutation_type == 'replace' and individual.echoes:
            # 替换一个回音
            index = random.randint(0, len(individual.echoes) - 1)
            old_position = individual.echoes[index].position
            
            # 找到相同位置的其他回音
            candidates = [echo for echo in self.echo_pool 
                         if echo.position == old_position and echo not in individual.echoes]
            
            if candidates:
                individual.echoes[index] = random.choice(candidates)
        
        elif mutation_type == 'add' and len(individual.echoes) < 5:
            # 添加一个回音
            used_positions = {echo.position for echo in individual.echoes}
            candidates = [echo for echo in self.echo_pool 
                         if echo.position not in used_positions]
            
            if candidates:
                individual.echoes.append(random.choice(candidates))
        
        elif mutation_type == 'remove' and len(individual.echoes) > 1:
            # 移除一个回音
            index = random.randint(0, len(individual.echoes) - 1)
            individual.echoes.pop(index)
        
        return individual

def optimize_echo_combination(echo_pool: List[Echo], 
                            target_stats: List[str],
                            character: Optional[Character] = None,
                            preferred_sets: Optional[List[str]] = None,
                            **kwargs) -> Tuple[EchoCombination, List[Dict]]:
    """优化回音组合的便捷函数"""
    
    config = OptimizationConfig(
        target_stats=target_stats,
        character=character,
        preferred_sets=preferred_sets or [],
        **kwargs
    )
    
    optimizer = GeneticAlgorithmOptimizer(echo_pool, config)
    best_combination = optimizer.optimize()
    
    return best_combination, optimizer.generation_stats

