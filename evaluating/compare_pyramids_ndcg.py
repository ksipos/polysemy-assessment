from rank_metrics import ndcg_at_k
from os import listdir
from operator import itemgetter
import random

def assing_value(index, ranked_dict):
    scores = [0] * len(index)
    max_score = max(ranked_dict.values())
    for k, v in ranked_dict.items():
        ranked_dict[k] = float(v)/float(max_score)
    norm = sum(ranked_dict.values())
    for k, v in ranked_dict.items():
        scores[index.index(k)] = v
    return scores, norm

result_scores = {}
method = 1
pyramid_path = '/data/home/cxypolop/Projects/openpaas_elmo/clustering/pyramid_output2'
with open(pyramid_path + '/pca4_L1', 'r') as f:
    vocabulary = [line.replace("\n", "").split(",")[0] for line in f]

############################ Wikipedia ############################

pyramids = [pyramid_path + "/" + fname for fname in listdir(pyramid_path)]
for index, pyramid in enumerate(pyramids):
    with open(pyramid, 'r') as f:
        ground_truth = [line.replace("\n", "").split(",") for line in f]
        ground_truth = {gt_tuple[0]: float(gt_tuple[1]) for gt_tuple in ground_truth}
        index = [pair[0] for pair in sorted(ground_truth.items(), key=itemgetter(1), reverse=True)]
        index = index + [word for word in vocabulary if word not in index]
        gt_scores, gt_norm = assing_value(index, ground_truth)
        # print(ndcg_at_k(wi_scores, len(index) + 1, wi_norm, method=1))
        result_scores['pyramid_' + pyramid.split("/")[-1]] = result_scores.get('pyramid_' + pyramid.split("/")[-1], [])  + [ndcg_at_k(gt_scores, len(index) + 1, gt_norm, method=method)]

    for pyramid_name in listdir(pyramid_path):
        pyramid_file = pyramid_path + "/" + pyramid_name
        with open(pyramid_file, 'r') as f:
            pyramid_rank = [line.replace("\n", "").split(",") for line in f]
            pyramid_rank = {pyramid_tuple[0]: float(pyramid_tuple[1]) for pyramid_tuple in pyramid_rank}
            # pyramid_rank = sorted(pyramid_rank  .items(), key=itemgetter(1), reverse=True)
            pyr_scores, pyr_norm = assing_value(index, pyramid_rank)
            # print(ndcg_at_k(pyr_scores, len(index) + 1, pyr_norm, method=1))
            result_scores['pyramid_' + pyramid_name] = result_scores.get('pyramid_' + pyramid_name, []) + [ndcg_at_k(pyr_scores, len(index) + 1, pyr_norm, method=method)]



average_scores = {k: float(sum(v))/len(v) for k, v in result_scores.items()}
average_scores = sorted(average_scores.items(), key=itemgetter(1), reverse=True)
for r in average_scores:
    print(r[0] + ": " + str(r[1]))
