import Levenshtein
from nltk.translate.bleu_score import sentence_bleu
from codebleu import calc_codebleu


# def average_code_similarity(report_path):
#     all_score = {}
#     with open(report_path, 'r') as f:
#         lines = f.readlines()
#     for line in lines:
#         generator = line.split(", ")[0].split(":")[1]
#         task = line.split(", ")[1].split(":")[1]
#         score = line.split(", ")[2].split(":")[1]
#         if generator not in all_score:
#             all_score[generator] = {}
#             all_score[generator][task] = score
#         else:
#             all_score[generator][task] = score
#     average_score = {}
#     print(f"\n\nReport path: {report_path}")
#     for generator in all_score:
#         average_score[generator] = sum(float(score) for score in all_score[generator].values()) / len(
#             all_score[generator])
#         # print(f"{generator}:\n{all_score[generator]}\nAverage score: {average_score[generator]}")
#         print(f"{generator}: {average_score[generator]}")
#
#     return average_score


def cal_str_bleu_similarity(reference: str, candidate: str):
    reference = reference.split()
    candidate = candidate.split()
    return sentence_bleu([reference], candidate)


def cal_code_bleu_similarity(reference: str, candidate: str):
    result = calc_codebleu([reference], [candidate], lang='python')
    return result['codebleu']


def cal_code_bleu_similarity_huggingface(reference: str, candidate: str):
    import evaluate
    metric = evaluate.load("dvitel/codebleu")

    # prediction = "def add ( a , b ) :\n return a + b"
    # reference = "def sum ( first , second ) :\n return second + first"

    result = metric.compute([reference], [candidate], lang="python")
    return result['codebleu']


def cal_str_edit_distance_similarity(s1, s2):
    return Levenshtein.ratio(s1, s2)


def cal_item_similarity(dict1, dict2, fields, similarity_func=None, hard_fields=False):
    final_score = 0.0
    for field in fields:
        if field not in dict1:
            raise ValueError(f"Field {field} not in dict")
        if field not in dict2:
            if hard_fields:
                return 0
        else:
            if similarity_func == "bleu":
                final_score += cal_str_bleu_similarity(dict1[field], dict2[field])
            elif similarity_func == "ed":
                final_score += cal_str_edit_distance_similarity(dict1[field], dict2[field])
            elif similarity_func == "llm":
                raise NotImplementedError("LLM not implemented yet")
            else:
                raise ValueError(f"Invalid similarity function: {similarity_func}")
    return final_score / len(fields)


def cal_list_similarity(list1, list2, fields, list_mode=None, similarity_func=None, hard_fields=False):
    if list_mode == "dict":
        len1, len2 = len(list1), len(list2)
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            for j in range(len2 + 1):
                tmp_sum = dp[i - 1][j - 1] + cal_item_similarity(
                    list1[i - 1],
                    list2[j - 1],
                    fields,
                    similarity_func,
                    hard_fields
                ) if i > 0 and j > 0 else 0
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1], tmp_sum)

        return dp[len1][len2] / len1
    elif list_mode == "str":
        if similarity_func == "bleu":
            return cal_str_bleu_similarity(str(list1), str(list2))
        elif similarity_func == "ed":
            return cal_str_edit_distance_similarity(str(list1), str(list2))
        else:
            raise ValueError(f"Invalid similarity function: {similarity_func}")
    else:
        raise ValueError(f"Invalid list function: {list_mode}")


def cal_multi_stream_similarity(stream_list1, stream_list2, list_mode=None, similarity_func=None, hard_fields=False,
                                len_weight=False):
    total_score = 0.0
    len_weight_total_score = 0.0
    stream_similarity = {}
    for stream_name, output1 in stream_list1.items():
        output2 = stream_list2.get(stream_name, None)
        if output2 is None:
            continue
        fields = output1[0].keys()
        tmp_score = cal_list_similarity(output1, output2, fields, list_mode=list_mode, similarity_func=similarity_func,
                                        hard_fields=hard_fields)
        stream_similarity[stream_name] = tmp_score
        total_score += tmp_score
        len_weight_total_score += tmp_score * len(output1)
    if not len_weight:
        avg_stream_score = total_score / len(stream_list1)
    else:
        avg_stream_score = len_weight_total_score / sum(len(output) for output in stream_list1.values())
    return avg_stream_score, stream_similarity


if __name__ == '__main__':
    import evaluate

    metric = evaluate.load("dvitel/codebleu")

    prediction = "def add ( a , b ) :\n return a + b"
    reference = "def sum ( first , second ) :\n return second + first"

    result = metric.compute([reference], [prediction], lang="python", weights=(0.25, 0.25, 0.25, 0.25))
