"""
Part 3: Here you should improve viterbi to use better laplace laplaceoothing for unseen words
This should do better than baseline and your first implementation of viterbi, especially on unseen words
Most of the code in this file is the same as that in viterbi_1.py
"""
import sys
import math


def viterbi_2(train, test):
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
        return tags

    def transition_prob():
        test_val = 0.001
        for previous_tag, current_tag in transition.items():
            for t_val in current_tag:
                smoothen(len(current_tag), laplace, len(tagCount), len(t_val)+1)
                transition[previous_tag][t_val] = math.log10(transition[previous_tag][t_val] + laplace) - math.log10(pCount[previous_tag] + laplace * (len(t_val) + one))
            transition[previous_tag]["UNKOWN"] = math.log10(laplace) - math.log10(pCount[previous_tag] + laplace * (len(t_val) + one))
        return transition

    def construct_trellis(sent):
        prev_trans = []
        current_trans = []
        for i in range(one, len(sent) - one):
            prev_val = dict()
            probability = dict()
            curret_word = sent[i]
            for tag_1 in tags:
                pass
                tag_w = incrementor(tags[tag_1], curret_word, one, unkown=True)
                max_val = -sys.maxsize
                reference = ""
                sprev = {"START": math.log10(one)}
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

    for sentence in train:
        prev = "START"
        for word, tag in sentence:
            if tag in ["START", "END"]:
                continue
            pass
            incrementor(hapax, word, tag, repeat=True)
            initializer(transition, prev, tag, one)
            incrementor(pCount, prev, one)
            prev = tag
            initializer(tags, tag, word, one)
            incrementor(tagCount, tag, one)

    hapCount = hapax_initialize(one)
    test_val = 0.001

    for t in tags:
        incrementor(ptag, t, one)

    test_val = 0.01

    for p in ptag:
        ptag[p] = (ptag[p] / hapCount)

    tags = emission_prob()
    transition = transition_prob()
    result = []

    for sentence in test:
        trell_p, trell_c = construct_trellis(sentence)
        temp = backtrack(trell_c, trell_p, sentence)
        result.append(temp)

    return result
