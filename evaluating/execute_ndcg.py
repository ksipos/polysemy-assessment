from rank_metrics import ndcg_at_k
from os import listdir
from operator import itemgetter
import random

def assing_value(index, ranked_dict):
    scores = [0] * len(index)
    # max_score = max(ranked_dict.values())
    # for k, v in ranked_dict.items():
    #     ranked_dict[k] = float(v)/float(max_score)
    # norm = sum(ranked_dict.values())
    norm = float(max(ranked_dict.values()))
    for k, v in ranked_dict.items():
        if k in index:
            scores[index.index(k)] = v
    return scores, norm

def ndcg(input_ranking_file, ground_truth_index, method, normalize_layers=1):
    with open(input_ranking_file, 'r') as f:
        data = [line.replace("\n", "").split(",") for line in f]
        data = {data_tuple[0]: float(data_tuple[1])/normalize_layers for data_tuple in data}
        scores, norm = assing_value(ground_truth_index, data)
        return ndcg_at_k(scores, len(ground_truth_index) + 1, norm, method=method)

def compare_against_baseline(ground_truth_file, wordlist, pyramid_path, method):
    result_scores = {}
    with open(ground_truth_file, 'r') as f:
        ground_truth = [line.replace("\n", "").split(",") for line in f]
        ground_truth = {",".join(gt_tuple[:-1]): float(gt_tuple[-1]) for gt_tuple in ground_truth}
        index = [pair[0] for pair in sorted(ground_truth.items(), key=itemgetter(1), reverse=True) if pair[0] in wordlist]

    ############################ Wikipedia ############################

    result_scores['wikipedia'] = ndcg('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/wikipedia_disambiguation_rank.txt', index, method)

    ############################ Random ############################

    random_dict = {}
    total_average = 0
    for j in range(10): # Execute for 10 random files
        random_pyramid_file = '/data/home/cxypolop/Projects/openpaas_elmo/clustering/pyramid_output2/' + random.choice(listdir('/data/home/cxypolop/Projects/openpaas_elmo/clustering/pyramid_output2'))
        with open(random_pyramid_file, 'r') as f:
            pyramid_rank = [line.replace("\n", "").split(",") for line in f]
            pyramid_rank = {pyramid_tuple[0]: float(pyramid_tuple[1]) for pyramid_tuple in pyramid_rank}

        pyramid_keys = list(pyramid_rank.keys())
        random_iterations = 1000 # Shuffle the ordering # times
        random_scores = []
        shuffled_keys = pyramid_keys.copy()
        for i in range(random_iterations):
            random.shuffle(shuffled_keys)
            ra_scores, ra_norm = assing_value(index, {k: pyramid_rank[k] for k in shuffled_keys})
            random_scores.append(ndcg_at_k(ra_scores, len(index) + 1, ra_norm, method=method))
        # print(ndcg_at_k(wi_scores, len(index) + 1, wi_norm, method=1))
        random_dict[random_pyramid_file] = random_scores
        total_average += (sum(random_scores)/len(random_scores))
    result_scores['random'] = total_average/len(random_dict)


    ############################# WordNet #############################

    result_scores['wordnet_original'] = ndcg('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/wordnet_original.txt', index, method)
    result_scores['wordnet_restricted'] = ndcg('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/wordnet_restricted.txt', index, method)

    ############################# Lexicon #############################

    result_scores['google'] = ndcg('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/google_list.txt', index, method)

    ############################# Frequency #############################

    result_scores['frequency'] = ndcg('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/frequency_ranking.txt', index, method)

    ############################# OntoNotes #############################

    result_scores['ontonotes'] = ndcg('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/ontonotes_ranking.txt', index, method)

    ############################# WN-Domains #############################

    result_scores['wn-domains'] = ndcg('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/wndomains_ranking.txt', index, method)

    ############################# Pyramid #############################

    for pyramid_name in listdir(pyramid_path):
        pyramid_file = pyramid_path + "/" + pyramid_name
        number_of_layers = int(pyramid_file.split("_")[-1][1:])
        result_scores['pyramid_' + pyramid_name] = ndcg(pyramid_file, index, method, number_of_layers)

    result_scores = sorted(result_scores.items(), key=itemgetter(1), reverse=True)

    with open('ndcg_results/gt-' + ground_truth_file.split("/")[-1][:-4] + '.txt', 'w') as f:
        f.write("\n".join([r[0] + ": " + str(r[1]) for r in result_scores]))

    return result_scores


method = 1
pyramid_path = '/data/home/cxypolop/Projects/openpaas_elmo/clustering/pyramid_output2'
ground_truth_file='/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/wikipedia_disambiguation_rank.txt'

baselines = ['results/' + name for name in listdir('results') if '.txt' in name]
with open('wordlist.txt', 'r') as f:
    wordlist = [line.replace("\n", "") for line in f]
total_scores = {}
for baseline in baselines:
    result_scores = compare_against_baseline(baseline, wordlist, pyramid_path, method)
    for pair in result_scores:
        k, v = pair
        total_scores[k] = total_scores.get(k, 0) + v

for k, v in total_scores.items():
    total_scores[k] = float(v)/float(len(baselines))

total_scores = sorted(total_scores.items(), key=itemgetter(1), reverse=True)
with open('ndcg_results/total_average_score.txt', 'w') as f:
    f.write("\n".join([r[0] + ": " + str(r[1]) for r in total_scores]))

with open('ndcg_results/total_average_pyramid_score.txt', 'w') as f:
    f.write("\n".join([r[0] + ": " + str(r[1]) for r in total_scores if 'pyramid' in r[0]]))