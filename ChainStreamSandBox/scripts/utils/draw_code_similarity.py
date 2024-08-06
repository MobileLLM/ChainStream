import matplotlib.pyplot as plt
import pandas as pd

# 从文件中读取数据
data = []
with open('code_similarity2.txt', 'r') as file:
    for line in file:
        # 解析每一行的数据
        parts = line.strip().split(', ')
        task = parts[0].split(" in ")[0].split(': ')[1]
        generator = parts[0].split(" in ")[1]
        score = float(parts[1].split(': ')[1])
        data.append((task, generator, score))

# 创建 DataFrame
df = pd.DataFrame(data, columns=['task', 'generator', 'score'])

# 对任务名称进行排序
df['task'] = pd.Categorical(df['task'], ordered=True)
df = df.sort_values('task')

# 第一张图：以 task 为横轴，以分数为纵轴的折线图
plt.figure(figsize=(10, 5))
for generator in df['generator'].unique():
    subset = df[df['generator'] == generator].sort_values('task')  # 根据task名称排序
    plt.plot(subset['task'], subset['score'], marker='o', label=generator)

plt.title('Task Scores by Generator')
plt.xlabel('Task')
plt.ylabel('Score')
plt.legend(title='Generator')
plt.xticks(rotation=30)  # 将横轴的标识旋转30度
plt.tight_layout()
plt.show()

# 第二张图：以 generator 为横轴，以分数为纵轴的箱线图
plt.figure(figsize=(8, 6))
df.boxplot(column='score', by='generator')
plt.title('Boxplot of Scores by Generator')
plt.suptitle('')
plt.xlabel('Generator')
plt.ylabel('Score')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
