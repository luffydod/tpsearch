from typing import Type, List, Tuple, Callable, Any, Optional, Union
import time
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from hillclimbing import HillClimbing, EightPuzzleHillClimbing, QueenHillClimbing
from simannealing import SimulatedAnnealing

class AlgorithmEvaluator:
   """算法评估器"""
   
   def __init__(self, 
                problem_generator: Callable[[], Any],
                num_trials: Optional[Union[int, List[int]]]):
       """
       初始化评估器
       
       参数：
       problem_generator: 生成问题实例的函数
       num_trials: 评估试验次数
       """
       self.problem_generator = problem_generator
       self.num_trials = num_trials
       self.results = defaultdict(list)
       
   def evaluate_algorithm(self, 
                        trial: int,
                        algorithm: Callable,
                        algorithm_name: str,
                        **kwargs) -> dict:
       """
       评估单个算法的性能
       
       参数：
       algorithm: 要评估的算法函数
       algorithm_name: 算法名称
       **kwargs: 算法的其他参数
       
       返回：
       包含评估指标的字典
       """
       success_count = 0
       steps_list = []
       times_list = []
       final_scores = []
       
       for _ in range(trial):
           initial_state = self.problem_generator()
           
           # 记录开始时间
           start_time = time.time()
           
           # 运行算法
           final_state, scores = algorithm(initial_state, **kwargs)
           
           # 记录结束时间
           end_time = time.time()
           
           # 收集数据
           steps = len(scores)
           run_time = end_time - start_time
           final_score = scores[-1]
           
           # 判断是否成功找到解
           if final_state.is_goal():
               success_count += 1
               
           steps_list.append(steps)
           times_list.append(run_time)
           final_scores.append(final_score)
           
       # 计算统计指标
       results = {
           'success_rate': success_count / trial,
           'avg_steps': np.mean(steps_list),
           'std_steps': np.std(steps_list),
           'avg_time': np.mean(times_list),
           'std_time': np.std(times_list),
           'avg_score': np.mean(final_scores),
           'std_score': np.std(final_scores)
       }
       
       self.results[algorithm_name] = results
       return results
   
   def compare_algorithms(self, algorithms: List[Tuple[Callable, str, dict]]):
       """
       比较多个算法的性能
       
       参数：
       algorithms: 算法列表，每个元素为 (算法函数, 算法名称, 参数字典)
       """
       if isinstance(self.num_trials, int):
           num_trials = [self.num_trials] * len(algorithms)
       else:
           num_trials = self.num_trials
       for i, (algorithm, name, kwargs) in enumerate(algorithms):
           print(f"\n评估算法: {name}")
           results = self.evaluate_algorithm(num_trials[i], algorithm, name, **kwargs)
           self._print_results(results)
           
   def plot_comparisons(self):
       """绘制算法比较图表"""
       # 设置中文字体
       plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
       plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
       
       metrics = ['success_rate', 'avg_steps', 'avg_time', 'avg_score']
       fig, axes = plt.subplots(2, 2, figsize=(15, 10))
       fig.suptitle('算法性能比较')
       
       for idx, metric in enumerate(metrics):
           ax = axes[idx // 2, idx % 2]
           values = [self.results[alg][metric] for alg in self.results]
           
           if metric == 'success_rate':
               errors = None
           else:
               errors = [self.results[alg][f'std_{metric.split("_")[1]}'] 
                        for alg in self.results]
           
           if errors is None:
               ax.bar(self.results.keys(), values)
           else:
               ax.bar(self.results.keys(), values, yerr=errors)
               
           ax.set_title(metric)
           ax.tick_params(axis='x', rotation=45)
           
       plt.tight_layout()
       plt.show()
       
   @staticmethod
   def _print_results(results: dict):
       """打印评估结果"""
       print(f"成功率: {results['success_rate']:.2%}")
       print(f"平均步数: {results['avg_steps']:.2f} ± {results['std_steps']:.2f}")
       print(f"平均时间: {results['avg_time']:.4f}s ± {results['std_time']:.4f}s")
       print(f"平均得分: {results['avg_score']:.2f} ± {results['std_score']:.2f}")
# 使用示例
if __name__ == '__main__':
   
   # 评估八数码问题
   print("评估八数码问题的算法性能：")
   evaluator = AlgorithmEvaluator(
       EightPuzzleHillClimbing.generate_random_state,
       num_trials=[50, 50, 10, 5]
   )
   
   algorithms = [
       (HillClimbing.steepest_ascent, "最陡上升法", {}),
       (HillClimbing.first_choice, "首选爬山法", {}),
       (HillClimbing.random_restart, "随机重启爬山法", {'max_restarts': 1000}),
       (SimulatedAnnealing.anneal, "模拟退火法", {
           'initial_temp': 100,
           'cooling_rate': 0.95
       })
   ]
   
   evaluator.compare_algorithms(algorithms)
#    evaluator.plot_comparisons()
   
   # 评估八皇后问题
#    print("\n评估八皇后问题的算法性能：")
#    evaluator = AlgorithmEvaluator(
#        QueenHillClimbing.generate_random_state,
#        num_trials=3
#    )
   
#    evaluator.compare_algorithms(algorithms)
#    evaluator.plot_comparisons()