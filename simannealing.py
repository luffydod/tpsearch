from typing import TypeVar, List, Optional, Tuple
import random
import math
from hillclimbing import EightPuzzleHillClimbing, QueenHillClimbing
from plot import plot_comparison
T = TypeVar('T')  # 状态类型


class SimulatedAnnealing:
   """模拟退火算法实现"""
   
   @staticmethod
   def anneal(initial_state: T, 
              initial_temp: float = 100.0,
              cooling_rate: float = 0.95,
              min_temp: float = 0.01,
              steps_per_temp: int = 100) -> Tuple[T, List[float]]:
       """
       模拟退火算法主体
       
       参数:
       initial_state: 初始状态
       initial_temp: 初始温度
       cooling_rate: 冷却率 (0-1之间)
       min_temp: 最小温度（终止条件）
       steps_per_temp: 每个温度下的迭代次数
       goal: 目标状态（可选）
       
       返回:
       (最终状态, 评分历史)
       """
       current = initial_state
       current_score = current.evaluate()
       best_state = current
       best_score = current_score
       
       temp = initial_temp
       scores = [current_score]
       
       while temp > min_temp:
           for _ in range(steps_per_temp):
               # 随机选择一个邻居
               neighbors = current.get_neighbors()
               if not neighbors:
                   break
               next_state = random.choice(neighbors)
               next_score = next_state.evaluate()
               
               # 计算评分差值
               delta = next_score - current_score
               
               # 如果是更好的解，或者以一定概率接受较差的解
               if (delta > 0 or 
                   random.random() < math.exp(delta / temp)):
                   current = next_state
                   current_score = next_score
                   scores.append(current_score)
                   
                   # 更新最佳解
                   if current_score > best_score:
                       best_state = current
                       best_score = current_score
               
               # 如果找到目标状态则提前结束
               if current.is_goal():
                   return current, scores
           
           # 降温
           temp *= cooling_rate
           
       return best_state, scores
   
   @staticmethod
   def random_restart_anneal(initial_state: T,
                           num_restarts: int = 10,
                           **kwargs) -> Tuple[T, List[float]]:
       """
       带随机重启的模拟退火算法
       
       参数:
       initial_state: 初始状态
       num_restarts: 重启次数
       goal: 目标状态（可选）
       **kwargs: 传递给anneal方法的其他参数
       
       返回:
       (最佳状态, 评分历史)
       """
       best_state = initial_state
       best_score = initial_state.evaluate()
       all_scores = []
       
       for _ in range(num_restarts):
           current_state, scores = SimulatedAnnealing.anneal(
               initial_state, **kwargs)
           current_score = current_state.evaluate()
           
           all_scores.extend(scores)
           
           if current_score > best_score:
               best_state = current_state
               best_score = current_score
           
           if current_state.is_goal():
               break
               
           # 随机生成新的初始状态
           if isinstance(initial_state, EightPuzzleHillClimbing):
               initial_state = EightPuzzleHillClimbing.generate_random_state()
           elif isinstance(initial_state, QueenHillClimbing):
               initial_state = QueenHillClimbing.generate_random_state()
               
       return best_state, all_scores
   

# 示例使用代码
if __name__ == '__main__':
   # 八数码问题示例
   initial_puzzle = EightPuzzleHillClimbing.generate_random_state()
   print("八数码初始状态：")
   print(initial_puzzle)
   print("目标状态：")
   print(initial_puzzle.goal)
   
   # 使用基本模拟退火算法
   print("\n使用基本模拟退火算法：")
   final_state, scores1 = SimulatedAnnealing.anneal(initial_puzzle)
   print("最终状态：")
   print(final_state)
   
   # 使用随机重启模拟退火算法
   print("\n使用随机重启模拟退火算法：")
   final_state, scores2 = SimulatedAnnealing.random_restart_anneal(initial_puzzle)
   print("最终状态：")
   print(final_state)
   
   # 绘制对比图
   plot_comparison(
       [scores1, scores2],
       ["基本模拟退火", "随机重启模拟退火"],
       best_score=100,
       title="八数码问题 - 模拟退火算法性能对比"
   )
   
   # 八皇后问题示例
   initial_queens = QueenHillClimbing.generate_random_state()
   print("\n八皇后初始状态：")
   print(initial_queens)
   
   # 使用基本模拟退火算法
   print("\n使用基本模拟退火算法：")
   final_state, scores1 = SimulatedAnnealing.anneal(initial_queens)
   print("最终状态：")
   print(final_state)
   
   # 使用随机重启模拟退火算法
   print("\n使用随机重启模拟退火算法：")
   final_state, scores2 = SimulatedAnnealing.random_restart_anneal(initial_queens)
   print("最终状态：")
   print(final_state)
   
   # 绘制对比图
   plot_comparison(
       [scores1, scores2],
       ["基本模拟退火", "随机重启模拟退火"],
       best_score=100,
       title="八皇后问题 - 模拟退火算法性能对比"
   )