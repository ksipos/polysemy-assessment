from rank_metrics import ndcg_at_k, dcg_at_k
from os import listdir
from operator import itemgetter
import random
    
def ndcg(input_ranking_file, ground_truth_index, method, normalize_layers=1):
    with open(input_ranking_file, 'r') as f:
        data = [line.replace("\n", "").split(",") for line in f]
    ranking = {data_tuple[0]: float(data_tuple[1])/normalize_layers for data_tuple in data}
    values_dict = {pair[0]:pair[1] for pair in ground_truth_index}

    # Reorder ground-truth's scores using provided rankings' order
    scores = [values_dict[pair[0]] for pair in sorted(ranking.items(), key=itemgetter(1), reverse=True) if pair[0] in values_dict]

    norm = float(max(values_dict.values()))
    norm = 1.0
    return dcg_at_k([s/norm for s in scores], method=method)/dcg_at_k([pair[1]/norm for pair in ground_truth_index], method=method)

def compare_against_baseline(ground_truth_file, wordlist, pyramid_path, method):
    result_scores = {}
    with open(ground_truth_file, 'r') as f:
        ground_truth = [line.replace("\n", "").split(",") for line in f]
        ground_truth = {",".join(gt_tuple[:-1]): float(gt_tuple[-1]) for gt_tuple in ground_truth}
        index = [pair for pair in sorted(ground_truth.items(), key=itemgetter(1), reverse=True) if pair[0] in wordlist]

    ############################ Wikipedia ############################

    result_scores['wikipedia'] = ndcg('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/wikipedia_disambiguation_rank.txt', index, method)

    ############################ Random ############################

    result_scores['random'] = ndcg('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/random_ranking.txt', index, method)

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

    result_scores['wndomains'] = ndcg('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/wndomains_ranking.txt', index, method)

    ############################# Pyramid #############################

    for pyramid_name in listdir(pyramid_path):
        pyramid_file = pyramid_path + "/" + pyramid_name
        number_of_layers = int(pyramid_file.split("_")[-1][1:])
        # number_of_layers = 1
        result_scores['pyramid_' + pyramid_name] = ndcg(pyramid_file, index, method, number_of_layers)

    result_scores = sorted(result_scores.items(), key=itemgetter(1), reverse=True)

    with open('ndcg_results/gt-' + ground_truth_file.split("/")[-1][:-4] + '.txt', 'w') as f:
        f.write("\n".join([r[0] + ": " + str(round(r[1], 3)) for r in result_scores]))

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

# Normalizing over number of baselines
for k, v in total_scores.items():
    total_scores[k] = float(v)/float(len(baselines))

# Sort and write to disk
total_scores = sorted(total_scores.items(), key=itemgetter(1), reverse=True)
with open('ndcg_results/total_average_score.txt', 'w') as f:
    f.write("\n".join([r[0] + ": " + str(round(r[1], 3)) for r in total_scores]))

with open('ndcg_results/total_average_pyramid_score.txt', 'w') as f:
    f.write("\n".join([r[0] + ": " + str(round(r[1], 3)) for r in total_scores if 'pyramid' in r[0]]))
