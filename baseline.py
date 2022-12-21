"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""
from collections import defaultdict

def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words). E.g.,  [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words). E.g.,  [[word1, word2], [word3, word4]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    tagCount = defaultdict(int)
    wordTagCount = defaultdict(dict)
    result = []
    for sentence in train:
        for input in sentence:
            word, tag = input
            if tag not in wordTagCount[word]:
                wordTagCount[word][tag] = 1
            else:
                wordTagCount[word][tag] += 1
            tagCount[tag] += 1

    commonTag = max(tagCount, key=tagCount.get)
    for sentence in test:
        tags = []
        for word in sentence:
            if word in wordTagCount:
                tag = max(wordTagCount[word], key=wordTagCount[word].get)
                tags.append((word, tag))
            else:
                tags.append(
                    (word, commonTag))
        result.append(tags)

    return result