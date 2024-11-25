from typing import List, Optional, Tuple
import random
import copy

class EightPuzzleState:
    """八数码问题的状态类"""
    
    def __init__(self, board: List[List[int]]):
        """
        board: 初始状态，3x3的二维数组，0表示空格
        """
        self.board = board
        self.size = 3
        self.blank_pos = self._find_blank()
    
    def _find_blank(self) -> tuple[int, int]:
        """找到空格(0)的位置"""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        raise ValueError("无效的八数码状态：没有找到空格")
    
    def get_possible_moves(self) -> List[str]:
        """获取当前状态下所有可能的移动方向"""
        moves = []
        x, y = self.blank_pos
        
        if x > 0: moves.append("上")
        if x < 2: moves.append("下")
        if y > 0: moves.append("左")
        if y < 2: moves.append("右")
        
        return moves
    
    def move(self, direction: str) -> Optional['EightPuzzleState']:
        """
        根据给定方向移动空格，返回新的状态
        如果移动无效则返回None
        """
        moves = {
            "上": (-1, 0),
            "下": (1, 0),
            "左": (0, -1),
            "右": (0, 1)
        }
        
        if direction not in moves:
            return None
            
        dx, dy = moves[direction]
        new_x, new_y = self.blank_pos[0] + dx, self.blank_pos[1] + dy
        
        if 0 <= new_x < self.size and 0 <= new_y < self.size:
            new_board = copy.deepcopy(self.board)
            new_board[self.blank_pos[0]][self.blank_pos[1]] = new_board[new_x][new_y]
            new_board[new_x][new_y] = 0
            return EightPuzzleState(new_board)
        return None

    @classmethod
    def generate_random_puzzle(cls) -> 'EightPuzzleState':
        """生成随机的初始状态和目标状态"""
        # 生成0-8的随机排列
        numbers = list(range(9))
        random.shuffle(numbers)
        initial_board = [numbers[i:i+3] for i in range(0, 9, 3)]
        
        return cls(initial_board)
    
    def __str__(self) -> str:
        """打印状态"""
        return "\n".join([" ".join(map(str, row)) for row in self.board])


if __name__ == '__main__':
    # 创建随机状态
    puzzle = EightPuzzleState.generate_random_puzzle()
    print("生成的八数码状态：")
    print(puzzle)

    # 获取可能的移动方向
    print("\n可能的移动方向：", puzzle.get_possible_moves())
