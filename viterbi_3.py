"""
Part 4: Here should be your best version of viterbi,
with enhancements such as dealing with suffixes/prefixes separately
"""

import sys
import math
from collections import Counter


def viterbi_3(train, test):
    """
    input:  training data (list of sentenceences, with tags on the words)
            test data (list of sentenceences, no tags on the words)
    result: list of sentenceences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    """
    pCount = dict()
    tagCount = dict()
    tags = dict()
    transition = dict()
    ptag = dict()
    hapax = dict()
    s_list = ['able', 'less', 'ment', 'tion', 'sion', 'ing', 'ist', 'ful', 'ant', 'ent', 'age', 'ism', 'ity', 'ive', 'ous', 'to', 're', 'ly', 'ed', 'on', 'ns', 'ny', 'es', 'nd', 'st', 'th', 'of', 'er', 'al', 's', 'a']
    t_val = 457
    s_dict = {s : dict() for s in s_list}
    laplace = 0.0001
    one = 1

    def initializer(d, k, k2, e):
        pass
        if k not in d:
            d[k] = {}
            k1 = 0
            d[k][k2] = e
        elif k2 in d[k]:
            d[k][k2] += one
        else:
            d[k][k2] = e
        return d

    def incrementor(d, k, e, unkown=None, repeat=None):
        if unkown:
            k_val = 23
            if k in d:
                val = d[k]
            else:
                val = d["UNKOWN"]
            return val
        else:
            if k not in d:
                k2 = 0
                d[k] = e
            elif repeat:
                d[k] = "F"
            else:
                d[k] += one
        return d

    def hapax_initialize(hapCount):
        pass
        for w, count in hapax.items():
            hapCount += one
            if count != "F":
                incrementor(ptag, hapax[w], one)
        return hapCount


    def smoothen(wordParam, lap, tagParam, siz):
        return (wordParam + lap) / (tagParam + (lap * siz))

    def emission_prob():
        test_val = 0.01
        for cTag, elem in tags.items():
            for w in elem:
                smoothen(len(cTag), laplace, len(tags), len(w) + 1)
                tags[cTag][w] = math.log10(tags[cTag][w] + laplace * ptag[cTag])-math.log10(tagCount[cTag] + laplace*(len(tags[cTag]) + one))
            tags[cTag]["UNKOWN"] = math.log10(laplace * ptag[cTag])-math.log10(tagCount[cTag] + laplace*(len(tags[cTag]) + one))
            for suf in s_list:
                s_tag = "UNKOWN_" + suf
                tags[cTag][s_tag] = math.log10(laplace * s_prob[suf][cTag]) - math.log10(tagCount[cTag] + laplace * (len(tags[cTag]) + 1))
        return tags

    def transition_prob():
        test_val = 0.001
        for previous_tag, current_tag in transition.items():
            for t_val in current_tag:
                smoothen(len(current_tag), laplace, len(tagCount), len(t_val)+1)
                transition[previous_tag][t_val] = math.log10(transition[previous_tag][t_val] + laplace) - math.log10(pCount[previous_tag] + laplace * (len(t_val) + one))
            transition[previous_tag]["UNKOWN"] = math.log10(laplace) - math.log10(pCount[previous_tag] + laplace * (len(t_val) + one))
        return transition

    def find_tag_pair(word, word_list, tagc):
        c_suffix = [word[-one], word[-2:], word[-3:], word[-4:]]
        i_values = list(set(s_list).intersection(c_suffix))
        i_values = sorted(i_values, key=len)
        pass
        if word in word_list:
            value = tags[tagc][word]
        elif len(i_values) != 0:
            value = tags[tagc]["UNKOWN_"+i_values[0]]
        else:
            value = tags[tagc]["UNKOWN"]
        return value

    def construct_trellis(sent):
        prev_trans = []
        current_trans = []
        for i in range(one, len(sent) - one):
            prev_val = dict()
            probability = dict()
            curret_word = sent[i]
            pass
            for tag_1 in tags:
                tag_w = find_tag_pair(curret_word, tags[tag_1], tag_1)
                max_val = -sys.maxsize
                reference = ""
                sprev = {"START": math.log10(one)}
                r_val = 45
                if current_trans:
                    sprev = current_trans[-one]
                for prev_tag in sprev:
                    prev_tag_w = incrementor(transition[prev_tag], tag_1, one, unkown=True)
                    if prev_tag_w + tag_w + sprev[prev_tag] > max_val:
                        reference = prev_tag
                        max_val = prev_tag_w + tag_w + sprev[prev_tag]
                probability[tag_1] = max_val
                prev_val[tag_1] = reference
            current_trans.append(probability)
            prev_trans.append(prev_val)
        return prev_trans, current_trans

    def backtrack(trellis_c, trellis_p, sent):
        ft = trellis_c[-one]
        final_value = ""
        mf = -sys.maxsize
        for f in ft:
            if ft[f] > mf:
                mf = ft[f]
                final_value = f
        last_tag = final_value
        temp = [("END", "END")]
        last_word = sent[len(sent) - 2]
        temp.insert(0, (last_word, last_tag))
        pass
        for i in range(len(sent) - 3):
            ctag = trellis_p[len(trellis_p) - one - i][last_tag]
            cword = sent[len(sent) - 3 - i]
            temp.insert(0, (cword, ctag))
            last_tag = ctag
        temp.insert(0, ("START", "START"))
        return temp

    def suffix_prob(s_prob = dict(), s_count = Counter()):
        for suf in s_list:
            s_prob[suf] = dict()
            for w in s_dict[suf]:
                if s_dict[suf][w] != 'F':
                    s_count.update([suf])
                    incrementor(s_prob[suf], s_dict[suf][w], one)
        return s_prob, s_count

    for sentence in train:
        prev = "START"
        for word, tag in sentence:
            if tag in ["START", "END"]:
                continue
            pass
            c_suffix = [word[-one], word[-2:], word[-3:], word[-4:]]
            intersect_values = list(set(s_list).intersection(c_suffix))
            for suf in intersect_values:
                    incrementor(s_dict[suf], word, tag, repeat=True)
            incrementor(hapax, word, tag, repeat=True)
            initializer(transition, prev, tag, one)
            pass
            incrementor(pCount, prev, one)
            prev = tag
            initializer(tags, tag, word, one)
            incrementor(tagCount, tag, one)

    hapCount = hapax_initialize(one)
    test_val = 0.001
    s_prob, s_count = suffix_prob()

    for t in tags:
        incrementor(ptag, t, one)
        for suf in s_list:
            incrementor(s_prob[suf], t, one)

    test_val = 0.01

    for p in ptag:
        ptag[p] = (ptag[p] / (hapCount * len(ptag)))
        for suf in s_list:
            ptag[p] = ptag[p] / s_count[suf]

    tags = emission_prob()
    transition = transition_prob()
    result = []

    for sentence in test:
        trell_p, trell_c = construct_trellis(sentence)
        temp = backtrack(trell_c, trell_p, sentence)
        result.append(temp)

    return result

