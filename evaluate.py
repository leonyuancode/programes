from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from rouge import Rouge
from util import *


def evaluate(references_file, candidates_file, limit_data):
    references_lst = []
    candidates_lst = []
    with open(references_file, "r", encoding='utf-8') as f:
        references_data = json.load(f)
        for key, value in references_data.items():
            references_lst.append(value)
    with open(candidates_file, "r", encoding='utf-8') as f:
        candidates_data = json.load(f)
        for key, value in candidates_data.items():
            # candidates.append(value.replace("(", "").replace(")", ""))
            candidates_lst.append(value.lower())
    # references = [references_lst[i] for i in limit_data if references_lst[i].startswith("wh")]
    # candidates = [candidates_lst[i] for i in limit_data if references_lst[i].startswith("wh")]
    references = [references_lst[i] for i in limit_data]
    candidates = [candidates_lst[i] for i in limit_data]
    length = len(references)
    print("length:-----------------", length)
    # bleu_score_1 = 0.0
    # bleu_score_2 = 0.0
    # bleu_score_3 = 0.0
    bleu_score_4 = 0.0
    # gleu_score = 0.0
    m_score = 0.0
    # rouge_score_1=0.0
    rouge_score_l = 0.0

    ref_l = []
    c_l = []
    for reference, candidate in zip(references, candidates):
        ref_list = [reference.split()]
        cand_list = candidate.split()
        ref_l.append(ref_list)
        c_l.append(cand_list)
        # glue = sentence_gleu(ref_list, cand_list)  # doctest: +ELLIPSIS
        # gleu_score += glue

        m_s = meteor_score(ref_list, cand_list)
        m_score += m_s
        # blue_1 = sentence_bleu(ref_list, cand_list, weights=(1, 0, 0, 0),
        #                        smoothing_function=SmoothingFunction().method2)
        # blue_2 = sentence_bleu(ref_list, cand_list, weights=(0.5, 0.5, 0, 0),
        #                        smoothing_function=SmoothingFunction().method2)
        # blue_3 = sentence_bleu(ref_list, cand_list, weights=(0.33, 0.33, 0.33, 0),
        #                        smoothing_function=SmoothingFunction().method2)
        blue_4 = sentence_bleu(ref_list, cand_list, weights=(0.25, 0.25, 0.25, 0.25),
                               smoothing_function=SmoothingFunction().method2)

        # bleu_score_1 += blue_1
        # bleu_score_2 += blue_2
        # bleu_score_3 += blue_3
        bleu_score_4 += blue_4

    # print("sentence_bleu_1:", bleu_score_1 / length)
    # print("sentence_bleu_2:", bleu_score_2 / length)
    # print("sentence_bleu_3:", bleu_score_3 / length)
    print("sentence_bleu_4:", bleu_score_4 / length * 100)
    # print("-------------------")
    # print("corpus_bleu_1:",
    #       corpus_bleu(ref_l, c_l, weights=(1, 0, 0, 0), smoothing_function=SmoothingFunction().method2))
    # print("corpus_bleu_2:",
    #       corpus_bleu(ref_l, c_l, weights=(0.5, 0.5, 0, 0), smoothing_function=SmoothingFunction().method2))
    # print("corpus_bleu_3:",
    #       corpus_bleu(ref_l, c_l, weights=(0.33, 0.33, 0.33, 0), smoothing_function=SmoothingFunction().method2))
    # print("corpus_bleu_4:",
    #       corpus_bleu(ref_l, c_l, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=SmoothingFunction().method2))
    # print("===================")
    # print("gleu_score:", gleu_score / length)
    print("meteor_score:", m_score / length * 100)

    rouge = Rouge()
    rouge_score = rouge.get_scores(candidates, references, avg=True)
    # print("rouge-1", rouge_score["rouge-1"]['f'])
    print("rouge-l", rouge_score["rouge-l"]['f'] * 100)


def data_join(references_data, candidates_data, save_file):
    d_dct = {}
    for data1, data2 in zip(references_data.items(), candidates_data.items()):
        qid1 = data1[0]
        qid2 = data2[0]
        if qid1 != qid2:
            print(data1)
            print(data2)
        q1 = data1[1]
        q2 = data2[1]
        d_dct[qid1] = [q1, q2]  #
    g = open(save_file, "w", encoding='utf-8')
    json.dump(d_dct, g, indent=2)
    g.close()


def data_analyse(file, limit_num):
    iid_data = []
    com_data = []
    zf_data = []
    i = 0
    with open(file, "r", encoding='utf-8') as f:
        references_data = json.load(f)
        for reference_data in references_data:
            if i >= limit_num:
                break
            for key, value in reference_data.items():
                if key != "level":
                    continue
                if value == "i.i.d.":
                    iid_data.append(i)
                elif value == "compositional":
                    com_data.append(i)
                else:
                    zf_data.append(i)
                i += 1
    return iid_data, com_data, zf_data


def get_min_score_question(references_file, candidates_files):
    candidates_data_lst = []
    for candidates_file in candidates_files:
        with open(candidates_file, "r", encoding='utf-8') as f:
            candidates_data_lst.append(json.load(f))
    with open(references_file, "r", encoding='utf-8') as f:
        references_data = json.load(f)

    result = {}

    for key, value in references_data.items():
        score = 0.0
        for candidates_data in candidates_data_lst:
            ref_list = [value.split()]
            cand_list = candidates_data[key].split()
            bleu_score = sentence_bleu(ref_list, cand_list, weights=(0.25, 0.25, 0.25, 0.25),
                                       smoothing_function=SmoothingFunction().method2)
            m_score = meteor_score(ref_list, cand_list)
            rouge = Rouge()
            rouge_score_l = rouge.get_scores([candidates_data[key]], [value],
                                             avg=True)["rouge-l"]['f']
            score += bleu_score + m_score + rouge_score_l
        result[key] = score
    sort_lst = sorted(result.items(), key=lambda x: x[1], reverse=False)
    sort_dct = {}
    for data in sort_lst:
        sort_dct[data[0]] = data[1]
    g = open("./uncertainty_test/dev_genarate_question_random_means_score.json", "w", encoding='utf-8')
    json.dump(sort_dct, g, indent=2)
    g.close()


if __name__ == '__main__':
    all_data = [i for i in range(500)]
    _, complex_datas = find_str_num_in_string(["JOIN", "ARGMAX", "ARGMIN", "COUNT", "lt", "le", "ge", "gt"],
                                              "./data/dev_sp_name.json", 5, all_data)
    references_file = "./data/dev_question.json"
    candidates_files = ["./result/dev_genarate_question_davinci_random_sub.json",
                            "./result/dev_genarate_question_davinci_kmeans_sub.json",
                            "./result/dev_genarate_question_davinci_kmeans_sub_short_first.json",
                               "./result/dev_genarate_question_davinci_kmeans_sub_short_first_ls.json" ]
    for candidates_file in candidates_files:
        print(candidates_file)
        evaluate(references_file, candidates_file, all_data)
    for candidates_file in candidates_files:
        print(candidates_file)
        evaluate(references_file, candidates_file, complex_datas)
    # get_min_score_question(references_file, ["./uncertainty_test/dev_genarate_question_random.json",
    #                                          "./uncertainty_test/dev_genarate_question_random2.json",
    #                                          "./uncertainty_test/dev_genarate_question_random3.json"])

    # 经过对比发现还是text-davinci-003更适合于根据s-expression生成问题
