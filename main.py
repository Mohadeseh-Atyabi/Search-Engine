import hazm
import math
import json
import matplotlib.pyplot as plt
import pandas


def zipf_calc(dictionary):
    zipf_dict = {}
    for word in dictionary:
        freq = 0
        for doc in dictionary[word]:
            freq += dictionary[word][doc]['frequency']
        zipf_dict.update({word: freq})
    zipf_dict = dict(sorted(zipf_dict.items(), key=lambda item: item[1], reverse=True))
    print(zipf_dict)
    name = list(zipf_dict.keys())[:10]
    values = list(zipf_dict.values())[:10]
    print(values)
    plt.plot(name, values)
    plt.show()


def preprocessing(data):
    file = open("stopwords.dat", encoding='utf-8')
    stop_list = file.read()
    stop_list = [word for word in stop_list.split()]
    data = hazm.Normalizer().normalize(data)
    data = hazm.word_tokenize(data)
    stemmer = hazm.Stemmer()
    words = []
    for word in data:
        if word not in stop_list:
            words.append(stemmer.stem(word))
    return words


# {word: {docID: {freq, weight, position: []}}
def indexer(dictionary, data, doc_id):
    for i in range(len(data)):
        position = [i]
        if data[i] not in dictionary:
            dictionary.update({data[i]: {doc_id: {"frequency": 1, "weight": 0, "position": position}}})
        else:
            if doc_id not in dictionary[data[i]]:
                dictionary[data[i]].update({doc_id: {"frequency": 1, "weight": 0, "position": position}})
            else:
                dictionary[data[i]][doc_id]["frequency"] += 1
                dictionary[data[i]][doc_id]["position"].append(i)
    return dictionary


# {word: {docID: weight}}
def champions_list(dictionary):
    champions = {}
    for word in dictionary:
        for doc in dictionary[word]:
            if word not in champions:
                champions.update({word: {doc: dictionary[word][doc]['weight']}})
            else:
                champions[word].update({doc: dictionary[word][doc]['weight']})
    for word in champions:
        champions[word] = dict(sorted(champions[word].items(), key=lambda item: item[1], reverse=True)[:10])
    return champions


def tf_idf(dictionary, doc_num):
    docs = []
    for word in dictionary:
        idf = math.log10(doc_num / len(dictionary[word]))
        for doc in dictionary[word]:
            dictionary[word][doc]["weight"] = idf * (1 + math.log10(dictionary[word][doc]["frequency"]))
    print("tf-idf done!")
    for i in range(doc_num):
        words = []
        for word in dictionary:
            if dictionary[word].get(i + 1) is not None:
                words.append(word)
        docs.append(words)
    print("docs appended!")
    for i in range(doc_num):
        norm = 0
        for word in docs[i]:
            norm += math.pow(dictionary[word][i + 1]['weight'], 2)
        norm = math.sqrt(norm)
        for word in docs[i]:
            dictionary[word][i + 1]['weight'] /= norm
    print("normalizing done!")


def cos_similarity(list, dictionary, doc_num):
    dict_list = {}
    score_list = {}
    for word in list:
        if dictionary.get(word) is None:
            continue
        if word not in dict_list:
            dict_list.update({word: 1})
        else:
            dict_list[word] += 1
    for word in dict_list:
        dict_list[word] = math.log10(doc_num / len(dictionary[word])) * (1 + math.log10(dict_list[word]))
    norm = 0
    for word in dict_list:
        norm += math.pow(dict_list[word], 2)
    norm = math.sqrt(norm)
    for word in dict_list:
        dict_list[word] /= norm
    for word in dict_list:
        for doc in dictionary[word]:
            if doc not in score_list:
                score_list.update({doc: dict_list[word] * dictionary[word][doc]['weight']})
            else:
                score_list[doc] += dict_list[word] * dictionary[word][doc]['weight']
    return score_list


def quotation(quotations_final, docs, dictionary):
    docs = set(docs)
    temp_docs = []
    curr_docs = []
    for word in quotations_final:
        curr_docs.append(docs.union(set(dictionary[word].keys())))
    for i in range(len(curr_docs) - 1):
        for doc in curr_docs[i]:
            if dictionary.get(quotations_final[i]) is None or dictionary.get(quotations_final[i + 1]) is None:
                break
            if dictionary[quotations_final[i]].get(doc) is None or dictionary[quotations_final[i + 1]].get(
                    doc) is None:
                continue
            index = dictionary[quotations_final[i]][doc]['position']
            index2 = dictionary[quotations_final[i + 1]][doc]['position']
            for position in index:
                if position + 1 in index2:
                    temp_docs.append(doc)
    if len(temp_docs) == 0:
        temp_docs = set(temp_docs)
        temp_docs = temp_docs.union(set(dictionary[quotations_final[0]].keys()))
    return temp_docs


def not_in(nots_final, dictionary, docs):
    docs = set(docs)
    not_docs = set()
    for word in nots_final:
        if dictionary.get(word) is not None:
            not_docs = docs.intersection(set(dictionary[word].keys()))
    return not_docs


def query(data, dictionary):
    data = data.split()
    quotations = []
    quotations_final = []
    nots = []
    nots_final = []
    normals = []
    normals_final = []
    is_quotation = False
    is_not = False
    for word in data:
        if word.endswith('"'):
            word = word.replace('"', "")
            quotations.append(word)
            is_quotation = False
            continue
        if is_quotation:
            quotations.append(word)
            continue
        if word.startswith('"'):
            word = word.replace('"', "")
            quotations.append(word)
            is_quotation = True
            continue
        if word == '!':
            is_not = True
            continue
        if is_not:
            is_not = False
            nots.append(word)
            continue
        normals.append(word)

    stemmer = hazm.Stemmer()
    for phrase in quotations:
        phrase = hazm.Normalizer().normalize(phrase)
        quotations_final.append(stemmer.stem(phrase))

    for phrase in nots:
        phrase = hazm.Normalizer().normalize(phrase)
        nots_final.append(stemmer.stem(phrase))

    for phrase in normals:
        phrase = hazm.Normalizer().normalize(phrase)
        normals_final.append(stemmer.stem(phrase))

    docs = set()
    not_docs = set()
    if normals_final is not None:
        for normal in normals_final:
            if dictionary.get(normal) is not None:
                docs = docs.union(set(dictionary[normal].keys()))
    if nots_final is not None:
        for word in nots_final:
            if dictionary.get(word) is not None:
                not_docs = docs.intersection(set(dictionary[word].keys()))
                docs -= not_docs
    if len(quotations_final) != 0:
        temp_docs = quotation(quotations_final, docs, dictionary)
        docs = docs.union(set(temp_docs))

    dictionary_temp = {}
    for doc in docs:
        score = 0
        for word in normals_final:
            try:
                score += dictionary[word][doc]['frequency']
            except:
                pass
        dictionary_temp.update({doc: score})
    dictionary_temp = dict(sorted(dictionary_temp.items(), key=lambda item: item[1], reverse=True))
    sim = cos_similarity(normals_final + quotations, dictionary, len(dictionary))
    sim = dict(sorted(sim.items(), key=lambda item: item[1], reverse=True))
    print(sim)

    if len(quotations_final) != 0:
        temp_docs = quotation(quotations_final, sim, dictionary)
        sim = set(sim)
        sim = sim.intersection(set(temp_docs))
    if not_docs is not None:
        sim = set(sim)
        sim -= not_docs
    return sim


file = open('IR_data_news_12k.json')
data = json.load(file)
dictionary = {}
# heaps = []
for i in range(len(data.keys())):
    proc = preprocessing(data.get(str(i))['content'])
    dictionary = indexer(dictionary, proc, i)
    # if i == 500 or i == 1000 or i == 1500 or i == 2000:
    #     heap = 100 * pow(len(dictionary), 0.5)
    #     heaps.append(heap)
print("preprocess done!")
tf_idf(dictionary, i)
print("weighting done!")
# plt.plot([500, 1000, 1500, 2000], heaps)
# plt.show()
# zipf_calc(dictionary)
q = input("Enter query: ")
while q != 'خروج':
    docs = query(q, dictionary)
    d = []
    for doc in docs:
        if len(d) == 5:
            break
        url = data.get(str(doc))['url']
        title = data.get(str(doc))['title']
        d.append(title + " : " + url)
    print(d)
    q = input("Enter query: ")
