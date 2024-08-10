import os


def average_code_similarity(report_path):
    all_score = {}
    with open(report_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        generator = line.split(", ")[0].split(":")[1]
        task = line.split(", ")[1].split(":")[1]
        score = line.split(", ")[2].split(":")[1]
        if generator not in all_score:
            all_score[generator] = {}
            all_score[generator][task] = score
        else:
            all_score[generator][task] = score
    average_score = {}
    print(f"\n\nReport path: {report_path}")
    for generator in all_score:
        average_score[generator] = sum(float(score) for score in all_score[generator].values()) / len(all_score[generator])
        # print(f"{generator}:\n{all_score[generator]}\nAverage score: {average_score[generator]}")
        print(f"{generator}: {average_score[generator]}")

    return average_score



if __name__ == '__main__':
    code_path = os.path.join(os.path.dirname(__file__), '..', 'code_similarity_report.txt')
    result_path = os.path.join(os.path.dirname(__file__), '..', 'result_similarity_report.txt')
    average_code_similarity(code_path)
    average_code_similarity(result_path)
