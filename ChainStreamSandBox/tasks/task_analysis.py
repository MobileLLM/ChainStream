from ChainStreamSandBox.tasks import TASKS_WITH_DATA
import matplotlib
from matplotlib import pyplot as plt
import tqdm
from ChainStreamSandBox.tasks.task_tag import Domain_Task_tag, Difficulty_Task_tag, Modality_Task_tag

# matplotlib.use('Agg')


def draw_task_tag():
    "画直方图"

    domain_task_statistics = {tag.value: 0 for tag in Domain_Task_tag}
    difficulty_task_statistics = {tag.value: 0 for tag in Difficulty_Task_tag}
    modality_task_statistics = {tag.value: 0 for tag in Modality_Task_tag}

    for _, task in tqdm.tqdm(TASKS_WITH_DATA.items()):
        task = task()
        domain_task_statistics[task.task_tag.domain] = domain_task_statistics.get(task.task_tag.domain, 0) + 1
        difficulty_task_statistics[task.task_tag.difficulty] = difficulty_task_statistics.get(task.task_tag.difficulty, 0) + 1
        modality_task_statistics[task.task_tag.modality] = modality_task_statistics.get(task.task_tag.modality, 0) + 1

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.bar(domain_task_statistics.keys(), domain_task_statistics.values())
    plt.title('Domain')
    plt.subplot(1, 3, 2)
    plt.bar(difficulty_task_statistics.keys(), difficulty_task_statistics.values())
    plt.title('Difficulty')
    plt.subplot(1, 3, 3)
    plt.bar(modality_task_statistics.keys(), modality_task_statistics.values())
    plt.title('Modality')
    # plt.savefig('task_tag.png')
    plt.show()


if __name__ == '__main__':
    draw_task_tag()