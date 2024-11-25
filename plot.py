import matplotlib.pyplot as plt
from typing import List, Optional


def plot_comparison(scores_list: List[List[float]], labels: List[str], best_score: Optional[int] = None, title: str = "爬山算法性能比较"):
   """
   绘制多个算法的评估分数变化对比图
   
   参数:
   scores_list: 多个算法的评估分数列表
   labels: 对应每个算法的标签名称
   best_score: 最优解对应的评估分数
   title: 图表标题
   """
   # 设置中文字体
   plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
   plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
   
   plt.figure(figsize=(12, 6))
   
   # 找出最长的序列长度
   max_length = max(len(scores) for scores in scores_list)
   
   # 定义颜色列表
   colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
   
   # 绘制每个算法的评估分数曲线
   for i, (scores, label) in enumerate(zip(scores_list, labels)):
       # 补齐序列长度
       extended_scores = scores.copy()
       if len(scores) < max_length:
           extended_scores.extend([scores[-1]] * (max_length - len(scores)))
           
       plt.plot(extended_scores, 
                color=colors[i % len(colors)], 
                label=label, 
                linewidth=2)
   if best_score is not None:
       # 绘制最优分数线
       plt.axhline(y=best_score, 
               color='red', 
               linestyle='--', 
               label='目标分数')
   
   plt.xlabel('迭代次数')
   plt.ylabel('评估分数')
   plt.title(title)
   plt.legend()
   plt.grid(True)
   plt.show()


if __name__ == '__main__':
    # 测试代码
    scores_list = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7]]
    labels = ["算法1", "算法2", "算法3"]
    plot_comparison(scores_list, labels, best_score=7)
