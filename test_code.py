import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 创建一些数据点
x = [1, 2, 3, 4, 5]
y = [2, 3, 4, 5, 6]
z = [1, 2, 3, 4, 5]

# 绘制散点图
ax.scatter(x, y, z)

# 选择要注释的点
point_index = 2  # 选择第三个点（索引从0开始）

# 添加注释
print(x[point_index])
ax.text(x[point_index], y[point_index], z[point_index], f'Point {point_index+1}', color='red')

plt.show()
