from typing import List, Optional, Set, Tuple
import random

class QueenState:
    def __init__(self, size: int = 8):
       self.size = size
       # 使用列表存储每行皇后的列位置，索引为行号
       self.queen_cols = [-1] * size
   
    def place_queen(self, row: int, col: int) -> bool:
        """在指定位置放置皇后"""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        
        self.queen_cols[row] = col
        return True
    
    def get_queen_position(self, row: int) -> Optional[int]:
        """获取指定行皇后的列位置"""
        col = self.queen_cols[row]
        return col if col != -1 else None
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """检查在指定位置放置皇后是否有效"""
        for other_row in range(self.size):
            other_col = self.queen_cols[other_row]
            if other_col == -1 or other_row == row:
                continue
            if (col == other_col or  # 同列
                abs(row - other_row) == abs(col - other_col)):  # 对角线
                return False
        return True
    
    @classmethod
    def generate_random_state(cls) -> 'QueenState':
        """生成随机的初始状态"""
        state = cls()
        for row in range(state.size):
            col = random.randint(0, state.size - 1)
            state.place_queen(row, col)
        return state
    
    def get_board(self) -> List[List[str]]:
        """获取棋盘的字符表示"""
        board = [['.' for _ in range(self.size)] for _ in range(self.size)]
        for row, col in enumerate(self.queen_cols):
            if col != -1:
                board[row][col] = 'Q'
        return board
    
    def __str__(self) -> str:
        board = self.get_board()
        return '\n'.join([' '.join(row) for row in board])
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QueenState):
            return False
        return self.queen_cols == other.queen_cols


if __name__ == '__main__':
   # 测试随机生成
   random_state = QueenState.generate_random_state()
   print("随机生成的八皇后状态：")
   print(random_state)
   
   # 测试放置皇后是否有效
   print("\n在指定位置放置皇后：")
   new_state = QueenState()
   new_state.queen_cols = random_state.queen_cols.copy()
   if new_state.is_valid_position(0, 0):
       new_state.place_queen(0, 0)
   print(f"在(0,0)位置放置皇后：{'成功' if new_state.is_valid_position(0, 0) else '失败'}")
   if new_state.is_valid_position(1, 2):
       new_state.place_queen(1, 2)
   print(f"在(1,2)位置放置皇后：{'成功' if new_state.is_valid_position(1, 2) else '失败'}")
   if new_state.is_valid_position(2, 4):
       new_state.place_queen(2, 4)
   print(f"在(2,4)位置放置皇后：{'成功' if new_state.is_valid_position(2, 4) else '失败'}")
   print(new_state)
