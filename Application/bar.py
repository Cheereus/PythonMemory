import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pyecharts.charts import Bar
from pyecharts import options as opts

"""plt方法"""
x = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
y = [0.55, 0.6, 0.45, 0.65, 0.55, 0.80, 0.4, 0.35, 0.35, 0.55, 0.45, 0.6]
fig = plt.figure()
plt.bar(x, y, 0.1, color=["red", "palegreen", "blue", "cyan", "orange", "purple"], align='center')
# plt.xlabel("x")
plt.ylabel("ACC")
plt.ylim([0, 1.1])
plt.title("title")
# plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3])
plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2])
plt.show()

"""pyecahrts方法生成html
bar = (
    Bar()
    .add_xaxis(["第一次试验", "第二次实验"])
    .add_yaxis("平均数1", [1, 1],gap="0%",category_gap="20%")
    .add_yaxis("平均数2", [2, 2],gap="0%",category_gap="20%")
    .add_yaxis("平均数3", [2, 2],gap="0%",category_gap="20%")
    .add_yaxis("平均数4", [2, 2],gap="0%",category_gap="20%")
    .add_yaxis("平均数5", [2, 2],gap="0%",category_gap="20%")
    .add_yaxis("平均数6", [2, 2],gap="0%",category_gap="20%")
    .set_global_opts(title_opts=opts.TitleOpts(title="This is title"))
)
bar.render()
"""
