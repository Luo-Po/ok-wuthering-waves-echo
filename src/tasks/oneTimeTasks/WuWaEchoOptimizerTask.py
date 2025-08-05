import random
import re

import yaml
from ok import BaseTask


class WuWaEchoOptimizerTask(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "鸣潮回音优化器"
        self.description = "基于扫描的回音数据进行优化计算"
        self.default_config.update({
            'echo_data_path': 'echoes.yaml',  # 回音数据文件路径
            'optimization_target': '攻击力',  # 优化目标
            'population_size': 50,  # 遗传算法种群大小
            'generations': 100,  # 遗传算法代数
            'mutation_rate': 0.1,  # 变异率
        })

    def run(self):
        self.log_info("开始回音优化计算...")

        # 读取回音数据
        echo_data = self._load_echo_data()
        if not echo_data:
            self.log_error("未找到回音数据，请先运行回音扫描器")
            return

        self.log_info(f"加载了 {len(echo_data)} 个回音数据")

        # 执行优化算法
        best_combination = self._optimize_echoes(echo_data)

        # 输出结果
        self._display_results(best_combination)

        self.log_info("回音优化计算完成！")

    def _load_echo_data(self):
        """加载回音数据"""
        try:
            with open(self.config.get('echo_data_path'), 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.log_error(f"回音数据文件 {self.config.get('echo_data_path')} 不存在")
            return None
        except Exception as e:
            self.log_error(f"加载回音数据失败: {e}")
            return None

    def _optimize_echoes(self, echo_data):
        """简化的遗传算法优化回音组合"""
        population_size = self.config.get('population_size')
        generations = self.config.get('generations')
        mutation_rate = self.config.get('mutation_rate')

        # 初始化种群 (每个个体是5个回音的组合)
        population = []
        for _ in range(population_size):
            individual = random.sample(echo_data, min(5, len(echo_data)))
            population.append(individual)

        best_individual = None
        best_fitness = -1

        for generation in range(generations):
            # 计算适应度
            fitness_scores = []
            for individual in population:
                fitness = self._calculate_fitness(individual)
                fitness_scores.append(fitness)

                if fitness > best_fitness:
                    best_fitness = fitness
                    best_individual = individual.copy()

            # 选择、交叉、变异 (简化实现)
            new_population = []

            # 保留最优个体
            new_population.append(best_individual.copy())

            # 生成新个体
            while len(new_population) < population_size:
                # 简单的轮盘赌选择
                parent1 = self._roulette_selection(population, fitness_scores)
                parent2 = self._roulette_selection(population, fitness_scores)

                # 简单交叉
                child = self._crossover(parent1, parent2, echo_data)

                # 变异
                if random.random() < mutation_rate:
                    child = self._mutate(child, echo_data)

                new_population.append(child)

            population = new_population

            if generation % 20 == 0:
                self.log_info(f"第 {generation} 代，最佳适应度: {best_fitness:.2f}")

        self.log_info(f"优化完成，最终适应度: {best_fitness:.2f}")
        return best_individual

    def _calculate_fitness(self, echo_combination):
        """计算回音组合的适应度 (简化版本)"""
        # 这里应该根据鸣潮的实际计算公式来评估回音组合的强度
        # 目前只是一个简化的示例
        total_score = 0
        target = self.config.get('optimization_target')

        for echo in echo_combination:
            # 主词条评分
            if target in echo.get('main_stat', ''):
                total_score += 100

            # 副词条评分
            for sub_stat in echo.get('sub_stats', []):
                if target in sub_stat:
                    # 简单的数值提取和评分
                    numbers = re.findall(r'\d+', sub_stat)
                    if numbers:
                        total_score += int(numbers[0])

        return total_score

    def _roulette_selection(self, population, fitness_scores):
        """轮盘赌选择"""
        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            return random.choice(population)

        pick = random.uniform(0, total_fitness)
        current = 0
        for i, fitness in enumerate(fitness_scores):
            current += fitness
            if current > pick:
                return population[i]
        return population[-1]

    def _crossover(self, parent1, parent2, echo_data):
        """交叉操作"""
        # 简单的单点交叉
        crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]

        # 确保不超过5个回音
        if len(child) > 5:
            child = child[:5]

        return child

    def _mutate(self, individual, echo_data):
        """变异操作"""
        if len(individual) > 0 and len(echo_data) > len(individual):
            # 随机替换一个回音
            index = random.randint(0, len(individual) - 1)
            new_echo = random.choice(echo_data)
            individual[index] = new_echo

        return individual

    def _display_results(self, best_combination):
        """显示优化结果"""
        if not best_combination:
            self.log_error("未找到最优组合")
            return

        self.log_info("=== 最优回音组合 ===")
        for i, echo in enumerate(best_combination, 1):
            self.log_info(f"回音 {i}: {echo.get('name', '未知')}")
            self.log_info(f"  主词条: {echo.get('main_stat', '未知')}")
            self.log_info(f"  副词条: {', '.join(echo.get('sub_stats', []))}")
            self.log_info("")

        # 计算总体评分
        total_fitness = self._calculate_fitness(best_combination)
        self.log_info(f"组合总评分: {total_fitness:.2f}")

        # 保存结果到文件
        result_file = "optimization_result.yaml"
        with open(result_file, 'w', encoding='utf-8') as f:
            yaml.dump({
                'best_combination': best_combination,
                'fitness_score': total_fitness,
                'optimization_target': self.config.get('optimization_target')
            }, f, allow_unicode=True)

        self.log_info(f"优化结果已保存到 {result_file}")
