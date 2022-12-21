# Hidden_Markov_Model_POS_Tagging

https://courses.grainger.illinois.edu/cs440/fa2022/MPs/mp4/assignment4.html

The code reads data from two files. Tagging function will be given the training data with tags and the test data without tags. Tagger will use the training data to estimate the probabilities it requires, and then use this model to infer tags for the test input. The main function will compare these against the correct tags and report accuracy.

The data is divided into sentences. Tagger will process each sentence independently.

There are two tagging functions:

1. Baseline
2. Viterbi: HMM tagger (in three versions)

To run the code on the Brown corpus data we need to tell it where the data is and which algorithm to run, either baseline, viterbi_1, viterbi_2, or viterbi_3:

```python3 mp4.py --train data/brown-training.txt --test data/brown-dev.txt --algorithm [baseline, viterbi_1, viterbi_2, viterbi_3]```
The program will run the algorithm and report three accuracy numbers:
- overall accuracy
- accuracy on words that have been seen with multiple different tags
- accuracy on unseen words

Viterbi_3 provides overall accuracy above 96%


## I hereby state that I shall not be held responsible for any misuse of my work or any academic integrity violations. ##
## DO NOT COPY. Only for reference ##
