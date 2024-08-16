import matplotlib.pyplot as plt
import pandas as pd

# Read data from file
data = []
with open('result_similarity_report.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(', ')
        generator = parts[0].split(': ')[1]
        task = parts[1].split(': ')[1]
        score = float(parts[2].split(': ')[1])
        data.append((task, generator, score))

# Create DataFrame
df = pd.DataFrame(data, columns=['task', 'generator', 'score'])

# Prepare data for plotting
tasks = df['task'].unique()
generators = df['generator'].unique()
task_indices = {task: idx for idx, task in enumerate(tasks)}

# Define a list of distinct colors
colors = plt.get_cmap('Set1').colors + plt.get_cmap('Paired').colors[:4]

# Set up the plot for bar chart
plt.figure(figsize=(20, 10))  # Increase figure size for better readability
num_generators = len(generators)
spacing = 1.5  # Distance between task groups

# Calculate the maximum possible width for each bar
max_width = spacing / num_generators

# Compute X positions for each task
task_positions = [task_indices[task] * spacing for task in tasks]

# Plot bars for each generator
for i, generator in enumerate(generators):
    subset = df[df['generator'] == generator]
    for j, task in enumerate(tasks):
        # Compute the center position of the task
        x_center = task_positions[j]

        # Compute the offset for this generator
        x_offset = x_center + (i - (num_generators - 1) / 2) * max_width

        # Plot each score for the generator
        plt.bar(x_offset,
                subset[subset['task'] == task]['score'],
                width=max_width,
                alpha=0.9,
                label=generator if j == 0 else "",  # Only show legend label once per generator
                color=colors[i % len(colors)])  # Cycle through colors if more than available

# Adding gridlines and labels for clarity
plt.title('Scores by Task and Generator')
plt.xlabel('Task')
plt.ylabel('Score')

# Set X ticks to be in the middle of each task group
plt.xticks(task_positions, tasks, rotation=90)

# Optionally add gridlines for better separation of groups
plt.grid(True, linestyle='--', alpha=0.7)

# Adding vertical lines to separate tasks, in the middle between tasks
for i in range(len(task_positions) - 1):
    mid_point = (task_positions[i] + task_positions[i + 1]) / 2
    plt.axvline(x=mid_point, color='gray', linestyle='--', linewidth=0.5)

plt.legend(title='Generator', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Set up the plot for boxplot
plt.figure(figsize=(12, 6))  # Adjust size if needed
ax = df.boxplot(column='score', by='generator', grid=False)
plt.title('Boxplot of Scores by Generator')
plt.suptitle('')  # Remove the default title
plt.xlabel('Generator')
plt.ylabel('Score')
plt.xticks(rotation=30)

# Adjust the layout to ensure proper spacing and alignment
plt.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.2)
plt.tight_layout()
plt.show()
