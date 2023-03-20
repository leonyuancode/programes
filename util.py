import json
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import random

random.seed(2023)


def get_num_in_string(chars, value):
    count = 0
    for c in chars:
        count += value.count(c)
    return count


def find_str_num_in_string(chars, file, minnum, all_data):
    lst = []
    indexs = []
    with open(file, "r", encoding='utf-8') as f:
        references_data = json.load(f)
        f.close()
    i = 0
    for key, value in references_data.items():
        if i not in all_data:
            i += 1
            continue
        count = get_num_in_string(chars, value)
        if count >= minnum:
            lst.append(key)
            indexs.append(i)
        i += 1

    return lst, indexs


def mask_rel_and_mid():
    compat_s_expression = dict()
    keys_words = ["(AND", "(JOIN", "(ARGMAX", "(R", "(ARGMIN", "(COUNT", "(lt", "(le", "(gt", "(ge"]
    end_rd = ")"
    with open("./data/train_s_expression.json", "r", encoding='utf-8') as f:
        references_data = json.load(f)
    print(len(references_data))
    for key, data in references_data.items():
        strs = data.split()
        new_str_lst = []
        for s in strs:
            if s in keys_words:
                new_str_lst.append(s)
            elif s.find(end_rd) == -1:
                new_str_lst.append(" ")
            else:
                new_str_lst.append(s[s.find(end_rd):len(s)])
        new_str = " ".join(new_str_lst)
        if new_str not in compat_s_expression:
            compat_s_expression[new_str] = ([key])
        else:
            compat_s_expression[new_str].append(key)

    print(len(compat_s_expression))
    # g = open("compat_s_expression.json", "w", encoding='utf-8')
    # json.dump(compat_s_expression, g, indent=2)
    # g.close()
    return compat_s_expression


def cluster_and_select(references_data, num_clusters):
    corpus = [key for key in references_data.keys()]
    embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    corpus_embeddings = embedder.encode(corpus)
    clustering_model = KMeans(n_clusters=num_clusters, random_state=2023)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_
    dist = clustering_model.transform(corpus_embeddings)

    clustered_sentences = [[] for i in range(num_clusters)]
    clustered_dists = [[] for i in range(num_clusters)]
    clustered_idx = [[] for i in range(num_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(corpus[sentence_id])
        clustered_dists[cluster_id].append(dist[sentence_id][cluster_id])
        clustered_idx[cluster_id].append(sentence_id)

    min_dict_sentences = []
    for i in range(len(clustered_dists)):
        tmp = list(map(list, zip(range(len(clustered_dists[i])), clustered_dists[i])))
        top_min_dist = sorted(tmp, key=lambda x: x[1], reverse=False)
        min_idx = -1
        for j in range(len(top_min_dist)):
            idx = top_min_dist[j][0]
            compact_key = clustered_sentences[i][idx]
            count = get_num_in_string(["AND","JOIN", "ARGMAX", "ARGMIN", "COUNT", "lt", "le", "ge", "gt"], compact_key)
            if count > 3:
                continue
            else:
                min_idx = top_min_dist[j][0]
                break
        if min_idx == -1:
            min_idx = top_min_dist[0][0]
        min_dict_sentences.append(clustered_sentences[i][min_idx])
    result = []
    keys = []
    for i, cluster in enumerate(clustered_sentences):
        # print(cluster)
        # k = cluster[random.randint(0, len(cluster)) - 1] #随机选
        # print(k)
        # keys.append(k)
        k = min_dict_sentences[i]  # 最靠近中心点
        keys.append(k)
        lst = references_data[k]
        result.append(lst[random.randint(0, len(lst)) - 1])
    return keys, result


def select_sample(lst1, lst2):
    with open("./data/train_sp_name.json", "r", encoding='utf-8') as f:
        references_data = json.load(f)

    r1 = []
    r2 = []
    i = 1
    for qid, value in references_data.items():
        if i in lst1:
            r1.append(qid)
        if i in lst2:
            r2.append(qid)
        i += 1
    return r1, r2


def select_compact_example(source_file, target_file1, target_file2):
    with open(source_file, "r", encoding='utf-8') as f:
        datas = json.load(f)

    with open("./data/train_sp_name.json", "r", encoding='utf-8') as f:
        sexpr_lst = json.load(f)

    with open("./data/train_question.json", "r", encoding='utf-8') as f:
        question_lst = json.load(f)

    result_sexpr = {}
    result_question = {}
    for key, lst in datas.items():
        qid = lst[random.randint(0, len(lst) - 1)]
        result_sexpr[qid] = sexpr_lst[qid]
        result_question[qid] = question_lst[qid]
    g = open(target_file1, "w", encoding='utf-8')
    json.dump(result_sexpr, g, indent=2)
    g.close()
    g = open(target_file2, "w", encoding='utf-8')
    json.dump(result_question, g, indent=2)
    g.close()


def compact_sexpr_anlyse():
    with open("./result/compat_s_expression.json", "r", encoding='utf-8') as f:
        datas = json.load(f)
    keys = datas.keys()
    print(len(keys))
    corpus = []
    for key in keys:
        contain = False
        for canc in datas.keys():
            if key == canc:
                continue
            if key in canc:
                contain = True
                break
        if not contain:
            corpus.append(key)
    embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    corpus_embeddings = embedder.encode(corpus)
    clustering_model = KMeans(n_clusters=8, random_state=2023)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_
    clustered_sentences = [[] for i in range(8)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(corpus[sentence_id])
    result = []
    keys = []
    with open("./result/compat_s_expression.json", "r", encoding='utf-8') as f:
        references_data = json.load(f)
    for i, cluster in enumerate(clustered_sentences):
        # print(cluster)
        cluster = sorted(cluster, key=lambda x: len(x))
        k = cluster[0]
        keys.append(k)
        lst = references_data[k]
        result.append(lst[random.randint(0, len(lst)) - 1])
    print(keys)
    print(result)


def select_range_data():
    with open("./data/dev_sp_name.json", "r", encoding='utf-8') as f:
        spers = json.load(f)
    with open("./data/dev_question.json", "r", encoding='utf-8') as f:
        questions = json.load(f)
    result = {}
    i = 0
    for qid, sper in spers.items():
        if i < 100:
            i += 1
            continue
        if i >= 150:
            break
        result[qid] = {"sexpr": sper, "quest": questions[qid]}
        i += 1
    g = open("./result/analyse.json", "w", encoding='utf-8')
    json.dump(result, g, indent=2)
    g.close()


if __name__ == "__main__":
    # find_str_num_in_string("JOIN", "./data/dev_sp_name.json", 100)
    # mask_rel_and_mid()
    with open("./result/compat_s_expression.json", "r", encoding='utf-8') as f:
        references_data = json.load(f)
    keys, re = cluster_and_select(references_data, 8)
    print(keys)
    print(re)
    # random.seed(2023)
    # resultlist = random.sample(range(0, 44337), 8)
    # print(resultlist)
    # lst1 = random.sample(range(0, 44337), 8)
    # lst2 = random.sample(range(0, 44337), 8)
    # r1,r2=select_sample(lst1,lst2)
    # print(r1)
    # print(r2)
    # select_compact_example("./result/compat_s_expression.json","./data/compat_s_expression_example.json","./data/compat_question_example.json")
    # compact_sexpr_anlyse()
    # select_range_data()
    all_data = [i for i in range(1500)]
    _, complex_datas = find_str_num_in_string(["AND","JOIN", "ARGMAX", "ARGMIN", "COUNT", "lt", "le", "ge", "gt"],
                                              "./data/dev_sp_name.json",  11, all_data)
    print(len(complex_datas))
    #50 21 12 5 3 1 0
    #=2-->29  58%
    #=3-->9   18%
    #=4-->7   14%
    #=5-->2
    #=6-->2
    #=7-->2
    #1450 778 430 228 113 40 18 12 1
    #=1-->50   3.3%
    #=2-->672  44.8%
    #=3-->348  23.2%
    #=4-->102  6.8%
    #=5-->115  7.7%
    #=6-->73   4.9%
    #=7-->22
    #=8-->6
    #=9-->11
    #=10-->1
    pass
