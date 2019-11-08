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
with open('/data/home/cxypolop/Projects/openpaas_elmo/clustering/pyramid_output2/pca4_L1', 'r') as f:
    vocabulary = [line.replace("\n", "").split(",")[0] for line in f]

############################ Wikipedia ############################

with open('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/wikipedia_disambiguation_rank.txt', 'r') as f:
    wikipedia = [line.replace("\n", "").split(",") for line in f]
    wikipedia = {wiki_tuple[0]: float(wiki_tuple[1]) for wiki_tuple in wikipedia}
    index = [pair[0] for pair in sorted(wikipedia.items(), key=itemgetter(1), reverse=True)]
    index = index + [word for word in vocabulary if word not in index]
    wi_scores, wi_norm = assing_value(index, wikipedia)
    # print(ndcg_at_k(wi_scores, len(index) + 1, wi_norm, method=1))
    result_scores['wikipedia'] = ndcg_at_k(wi_scores, len(index) + 1, wi_norm, method=method)


############################ Random ############################

random_dict = {}
total_average = 0
for j in range(10):
    random_pyramid_file = '/data/home/cxypolop/Projects/openpaas_elmo/clustering/pyramid_output2/' + random.choice(listdir('/data/home/cxypolop/Projects/openpaas_elmo/clustering/pyramid_output2'))
    with open(random_pyramid_file, 'r') as f:
        pyramid_rank = [line.replace("\n", "").split(",") for line in f]
        pyramid_rank = {pyramid_tuple[0]: float(pyramid_tuple[1]) for pyramid_tuple in pyramid_rank}

    pyramid_keys = list(pyramid_rank.keys())
    random_iterations = 1000
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

with open('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/wordnet_original.txt', 'r') as f:
    wordnet_original = [line.replace("\n", "").split(",") for line in f]
    wordnet_original = {wordnet_tuple[0]: float(wordnet_tuple[1]) for wordnet_tuple in wordnet_original}
    # wordnet_original = sorted(wordnet_original.items(), key=itemgetter(1), reverse=True)
    woo_scores, woo_norm = assing_value(index, wordnet_original)
    # print(ndcg_at_k(woo_scores, len(index) + 1, woo_norm, method=1))
    result_scores['wordnet_original'] = ndcg_at_k(woo_scores, len(index) + 1, woo_norm, method=1)

with open('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/wordnet_restricted.txt', 'r') as f:
    wordnet_restricted = [line.replace("\n", "").split(",") for line in f]
    wordnet_restricted = {wordnet_tuple[0]: float(wordnet_tuple[1]) for wordnet_tuple in wordnet_restricted}
    # wordnet_restricted = sorted(wordnet_restricted.items(), key=itemgetter(1), reverse=True)
    wor_scores, wor_norm = assing_value(index, wordnet_restricted)
    # print(ndcg_at_k(wor_scores, len(index) + 1, wor_norm, method=1))
    result_scores['wordnet_restricted'] = ndcg_at_k(wor_scores, len(index) + 1, wor_norm, method=method)

############################# Lexicon #############################

with open('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/google_list.txt', 'r') as f:
    google = [line.replace("\n", "").split(",") for line in f]
    google = {google_tuple[0]: float(google_tuple[1]) for google_tuple in google}
    go_scores, go_norm = assing_value(index, google)
    result_scores['google'] = ndcg_at_k(go_scores, len(index) + 1, go_norm, method=method)

############################# Frequency #############################

with open('/data/home/cxypolop/Projects/openpaas_elmo/clustering/results/frequency_list.txt', 'r') as f:
    frequency = [line.replace("\n", "").split(",") for line in f]
    frequency = {frequency_tuple[0]: float(frequency_tuple[1]) for frequency_tuple in frequency if frequency_tuple[0] in index}
    freq_scores, freq_norm = assing_value(index, frequency)
    result_scores['frequency'] = ndcg_at_k(freq_scores, len(index) + 1, freq_norm, method=method)

############################# Pyramid #############################

pyramid_path = '/data/home/cxypolop/Projects/openpaas_elmo/clustering/pyramid_output2'
for pyramid_name in listdir(pyramid_path):
    pyramid_file = pyramid_path + "/" + pyramid_name
    with open(pyramid_file, 'r') as f:
        pyramid_rank = [line.replace("\n", "").split(",") for line in f]
        pyramid_rank = {pyramid_tuple[0]: float(pyramid_tuple[1]) for pyramid_tuple in pyramid_rank}
        # pyramid_rank = sorted(pyramid_rank  .items(), key=itemgetter(1), reverse=True)
        pyr_scores, pyr_norm = assing_value(index, pyramid_rank)
        # print(ndcg_at_k(pyr_scores, len(index) + 1, pyr_norm, method=1))
        result_scores['pyramid_' + pyramid_name] = ndcg_at_k(pyr_scores, len(index) + 1, pyr_norm, method=method)


result_scores = sorted(result_scores.items(), key=itemgetter(1), reverse=True)
for r in result_scores:
    print(r[0] + ": " + str(r[1]))
