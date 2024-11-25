from abc import ABC, abstractmethod
from typing import TypeVar, List, Optional, Tuple
import random
from eightpuzzle import EightPuzzleState
from eightqueen import QueenState
from plot import plot_comparison

T = TypeVar('T')  # 状态类型

class HillClimbingProblem(ABC):
    """爬山算法问题的抽象基类"""
    
    @abstractmethod
    def get_neighbors(self) -> List[T]:
        """获取当前状态的所有邻居状态"""
        pass
    
    @abstractmethod
    def evaluate(self) -> float:
        """评估函数，返回当前状态的评分（越大越好）"""
        pass
    
    @abstractmethod
    def is_goal(self) -> bool:
        """判断是否达到目标状态"""
        pass

class HillClimbing:
    """爬山算法实现"""
    
    @staticmethod
    def steepest_ascent(initial_state: T, max_steps: int = 1000) -> Tuple[T, List[float]]:
        """最陡上升爬山法"""
        current = initial_state
        scores = [current.evaluate()]
        
        for _ in range(max_steps):
            neighbors = current.get_neighbors()
            if not neighbors:
                break
                
            # 评估所有邻居
            neighbor_scores = [(n, n.evaluate()) for n in neighbors]
            best_neighbor, best_score = max(neighbor_scores, key=lambda x: x[1])
            
            # 如果没有更好的邻居则停止
            if best_score <= current.evaluate():
                break
            # 选择使评估函数最大（最好）的邻居（后继状态）进行行动
            current = best_neighbor
            scores.append(best_score)
            
            # 如果达到目标状态则停止
            if current.is_goal():
                break
                
        return current, scores

    @staticmethod
    def first_choice(initial_state: T, max_steps: int = 1000) -> Tuple[T, List[float]]:
        """首选爬山法"""
        current = initial_state
        scores = [current.evaluate()]
        
        for _ in range(max_steps):
            neighbors = current.get_neighbors()
            if not neighbors:
                break
                
            # 随机打乱邻居顺序
            random.shuffle(neighbors)
            found_better = False
            
            # 选择第一个更好的邻居或相同评估函数值的邻居
            for neighbor in neighbors:
                neighbor_score = neighbor.evaluate()
                if neighbor_score >= current.evaluate():
                    current = neighbor
                    scores.append(neighbor_score)
                    found_better = True
                    break
                    
            if not found_better:
                break
                
            if current.is_goal():
                break
                
        return current, scores
    
    @staticmethod
    def random_restart(initial_state: T, max_restarts: int = 1000) -> Tuple[T, List[float]]:
        """随机重启爬山法"""
        best_state = initial_state
        best_score = initial_state.evaluate()
        all_scores = [best_score]
        
        for _ in range(max_restarts):
            # 使用最陡上升法进行一次爬山
            current_state, current_scores = HillClimbing.steepest_ascent(initial_state)
            current_score = current_state.evaluate()
            
            # 更新最佳状态
            if current_score > best_score:
                best_state = current_state
                best_score = current_score
                
            all_scores.extend(current_scores)
            
            # 如果找到目标状态则提前结束
            if current_state.is_goal():
                break
                
            # 随机生成新的初始状态
            if isinstance(initial_state, EightPuzzleHillClimbing):
                initial_state = EightPuzzleHillClimbing.generate_random_state()
            elif isinstance(initial_state, QueenHillClimbing):
                initial_state = QueenHillClimbing.generate_random_state()
                
        return best_state, all_scores
    

class EightPuzzleHillClimbing(EightPuzzleState, HillClimbingProblem):
    """八数码问题的爬山算法实现"""
    def __init__(self, board: List[List[int]], goal: EightPuzzleState):
        super().__init__(board)
        self.goal = goal

    def get_neighbors(self) -> List['EightPuzzleHillClimbing']:
        """获取所有可能的邻居状态"""
        return [
            EightPuzzleHillClimbing(new_state.board, self.goal)
            for m in self.get_possible_moves()
            if (new_state := self.move(m)) is not None
        ]
    
    def evaluate(self) -> float:
        """
        评估函数：计算当前状态与目标状态的曼哈顿距离的负值
        （负值是因为爬山算法寻找最大值，而我们要最小化距离）
        """
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    # 找到当前数字在目标状态中的位置
                    for gi in range(self.size):
                        for gj in range(self.size):
                            if self.goal.board[gi][gj] == self.board[i][j]:
                                distance += abs(i - gi) + abs(j - gj)
        return 100 - distance
    
    def is_goal(self) -> bool:
        """判断是否达到目标状态"""
        return self.evaluate() == 100

    @classmethod
    def generate_random_state(cls):
        """重写父类的方法，确保返回 EightPuzzleHillClimbing 对象"""
        state = EightPuzzleState.generate_random_puzzle()
        # goal = EightPuzzleState.generate_random_puzzle()
        goal = EightPuzzleState([[0,1,2],[3,4,5],[6,7,8]])
        return cls(state.board, goal)


class QueenHillClimbing(QueenState, HillClimbingProblem):
   """八皇后问题的爬山算法实现"""
   
   def get_neighbors(self) -> List['QueenHillClimbing']:
       """
       获取邻居状态：通过移动一个皇后到同一行的不同位置
       返回所有可能的邻居状态列表
       """
       neighbors = []
       
       for row in range(self.size):
           current_col = self.queen_cols[row]
           # 尝试将当前行的皇后移动到其他列
           for new_col in range(self.size):
               if new_col != current_col:
                   new_state = QueenHillClimbing(self.size)
                   # 复制当前状态的皇后位置
                   new_state.queen_cols = self.queen_cols.copy()
                   # 移动当前行的皇后
                   new_state.queen_cols[row] = new_col
                   neighbors.append(new_state)
                   
       return neighbors
   
   def evaluate(self) -> float:
       """
       评估函数：计算不受攻击的皇后对数
       返回值为负的冲突数（越大越好）
       """
       conflicts = 0
       for i in range(self.size):
           for j in range(i + 1, self.size):
               # 获取两个皇后的位置
               col1 = self.queen_cols[i]
               col2 = self.queen_cols[j]
               
               # 检查是否有冲突：同列或对角线
               if (col1 == col2 or  # 同列
                   abs(i - j) == abs(col1 - col2)):  # 对角线
                   conflicts += 1
                   
       return 100 - conflicts  # 返回负值，因为爬山算法寻找最大值
   
   def is_goal(self) -> bool:
       """
       判断是否达到目标状态
       当评估函数为100（没有冲突）时表示找到解
       """
       return self.evaluate() == 100
   
   @classmethod
   def generate_random_state(cls):
       """重写父类的方法，确保返回 QueenHillClimbing 对象"""
       state = super().generate_random_state()
       # 创建新的 QueenHillClimbing 实例并复制状态
       new_state = cls(state.size)
       new_state.queen_cols = state.queen_cols.copy()
       return new_state

if __name__ == '__main__':
    # # 八数码问题示例
    # initial_puzzle = EightPuzzleHillClimbing.generate_random_state()

    # print("八数码初始状态：")
    # print(initial_puzzle)
    # print("目标状态：")
    # print(initial_puzzle.goal)
    # scores_list = []

    # # 使用最陡上升法求解
    # print("使用最陡上升法求解：")
    # final_state, scores = HillClimbing.steepest_ascent(initial_puzzle)
    # print("\n最终状态：")
    # print(final_state)
    # print(f"评估分数变化：{scores}")
    # scores_list.append(scores)

    # # 使用首选爬山法求解
    # print("使用首选爬山法求解：")
    # final_state, scores = HillClimbing.first_choice(initial_puzzle)
    # print("\n最终状态：")
    # print(final_state)
    # print(f"评估分数变化：{scores}")
    # scores_list.append(scores)

    # # 使用随机重启爬山法求解
    # print("使用随机重启爬山法求解：")
    # final_state, scores = HillClimbing.random_restart(initial_puzzle)
    # print("\n最终状态：")
    # print(final_state)
    # print(f"评估分数变化：{scores}")
    # scores_list.append(scores)

    # plot_comparison(scores_list, ["最陡上升法", "首选爬山法", "随机重启爬山法"], best_score=100)

    # 八皇后问题示例
    initial_queens = QueenHillClimbing.generate_random_state()
    print("\n八皇后初始状态：")
    print(initial_queens)
    scores_list = []

    # 使用最陡上升法求解
    print("使用最陡上升法求解：")
    final_state, scores = HillClimbing.steepest_ascent(initial_queens)
    print("\n最终状态：")
    print(final_state)
    print(f"评估分数变化：{scores}")
    scores_list.append(scores)

    # 使用首选爬山法求解
    print("使用首选爬山法求解：")
    final_state, scores = HillClimbing.first_choice(initial_queens)
    print("\n最终状态：")
    print(final_state)
    print(f"评估分数变化：{scores}")
    scores_list.append(scores)

    # 使用随机重启爬山法求解
    print("使用随机重启爬山法求解：")
    final_state, scores = HillClimbing.random_restart(initial_queens)
    print("\n最终状态：")
    print(final_state)
    print(f"评估分数变化：{scores}")
    scores_list.append(scores)

    plot_comparison(scores_list, ["最陡上升法", "首选爬山法", "随机重启爬山法"], best_score=100)
