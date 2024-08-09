import matplotlib.pyplot as plt
import pandas as pd

data = []
with open('result_similarity_report.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(', ')
        generator = parts[0].split(': ')[1]
        task = parts[1].split(': ')[1]
        score = float(parts[2].split(': ')[1])
        data.append((task, generator, score))

df = pd.DataFrame(data, columns=['task', 'generator', 'score'])

df['task'] = pd.Categorical(df['task'], ordered=True)
df = df.sort_values('task')

plt.figure(figsize=(10, 5))
for generator in df['generator'].unique():
    subset = df[df['generator'] == generator].sort_values('task')
    plt.plot(subset['task'], subset['score'], marker='o', label=generator)

plt.title('Task Scores by Generator')
plt.xlabel('Task')
plt.ylabel('Score')
plt.legend(title='Generator')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
df.boxplot(column='score', by='generator')
plt.title('Boxplot of Scores by Generator')
plt.suptitle('')
plt.xlabel('Generator')
plt.ylabel('Score')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
