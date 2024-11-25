from hillclimbing import HillClimbing, EightPuzzleHillClimbing, QueenHillClimbing
from plot import plot_comparison
from simannealing import SimulatedAnnealing

def solve_eight_puzzle():
    # 八数码问题示例
    initial_puzzle = EightPuzzleHillClimbing.generate_random_state()

    print("八数码初始状态：")
    print(initial_puzzle)
    print("目标状态：")
    print(initial_puzzle.goal)
    scores_list = []

    # 使用最陡上升法求解
    print("使用最陡上升法求解：")
    final_state, scores = HillClimbing.steepest_ascent(initial_puzzle)
    print("\n最终状态：")
    print(final_state)
    print(f"评估分数变化：{scores}")
    scores_list.append(scores)

    # 使用首选爬山法求解
    print("使用首选爬山法求解：")
    final_state, scores = HillClimbing.first_choice(initial_puzzle)
    print("\n最终状态：")
    print(final_state)
    print(f"评估分数变化：{scores}")
    scores_list.append(scores)

    plot_comparison(scores_list, 
                        ["最陡上升法", "首选爬山法"], 
                        best_score=100,
                        title="八数码问题算法性能比较")
    
    scores_list = []
    # 使用随机重启爬山法求解
    print("使用随机重启爬山法求解：")
    final_state, scores = HillClimbing.random_restart(initial_puzzle)
    print("\n最终状态：")
    print(final_state)
    print(f"评估分数变化：{scores}")
    scores_list.append(scores)

    # 使用模拟退火算法求解
    print("使用模拟退火算法：")
    final_state, scores = SimulatedAnnealing.anneal(initial_puzzle, steps_per_temp=80)
    print("\n最终状态：")
    print(final_state)
    print(f"评估分数变化：{scores}")
    scores_list.append(scores)

    plot_comparison(scores_list, 
                    ["随机重启爬山法", "模拟退火算法"], 
                    best_score=100,
                    title="八数码问题算法性能比较")


def solve_queens():
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

    plot_comparison(scores_list, ["最陡上升法", "首选爬山法"], best_score=100, title="八皇后问题算法性能比较")

    scores_list = []
    # 使用随机重启爬山法求解
    print("使用随机重启爬山法求解：")
    final_state, scores = HillClimbing.random_restart(initial_queens)
    print("\n最终状态：")
    print(final_state)
    print(f"评估分数变化：{scores}")
    scores_list.append(scores)

    # 使用模拟退火算法求解
    print("使用模拟退火算法：")
    final_state, scores = SimulatedAnnealing.anneal(initial_queens)
    print("\n最终状态：")
    print(final_state)
    print(f"评估分数变化：{scores}")
    scores_list.append(scores)

    plot_comparison(scores_list, ["随机重启爬山法", "模拟退火算法"], best_score=100, title="八皇后问题算法性能比较")
if __name__ == "__main__":
    # solve_eight_puzzle()
    solve_queens()
