import math
import nltk
import time
import sys

# Constants to be used by you when you fill the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

class Pd():
    counter = 0
    
    @staticmethod
    def printdot():
        if Pd.counter % 5000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
        Pd.counter += 1


def log2(num):
    Pd.printdot()
    return math.log(num,2)

def calc_prob(ngrams):
    total = float(len(ngrams)) - ngrams.count((START_SYMBOL,)) #- ngrams.count((STOP_SYMBOL,))
    counts = {}
    logs = {}
    
    for token in ngrams:
        x = counts.get(token, 0)
        counts[token] = x + 1
        Pd.printdot()
        
    print("\nCalculating log probabilities")
    for key in counts.keys():
        logs[key] = log2(counts[key]/total)

    return logs, counts

def calc_prob_bi(bgrams, ugrams):
    counts = {}
    logs = {}
    
    for token in bgrams:
        x = counts.get(token, 0)
        counts[token] = x + 1
        Pd.printdot()
        
    print("\nCalculating log probabilities")
    for key in counts.keys():
        subkey = key[:-1]
        try:
            logs[key] = log2(float(counts[key])/ugrams[subkey])
        except:
            print("Damnit, it broke...")
            print(key)
            print(counts[key])
            print(subkey)
            print(ugrams[subkey])
            

    return logs, counts


def make_tok(sentence):
    tokens = sentence.split()
    tokens.insert(0, START_SYMBOL)
    tokens.append(STOP_SYMBOL)
    return tokens

# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):
    
    counter = 0
    
    unigram_tuples = []
    bigram_tuples = []
    trigram_tuples = []
    print("Processing sentences")
    for sentence in training_corpus:
#        tokens = make_tok(sentence)
#        unigram_tuples.extend(list([(x,) for x in tokens]))
#        bigram_tuples.extend(list(nltk.bigrams(tokens)))
#        trigram_tuples.extend(list(nltk.trigrams(tokens)))
        unigram_tuples.extend(make_ngrams(sentence, 1))
        bigram_tuples.extend(make_ngrams(sentence, 2))
        trigram_tuples.extend(make_ngrams(sentence, 3))


        Pd.printdot()

    print("\nProcessing unigrams")
    #unigram_p = {item : log2(unigram_tuples.count(item)/ucount) for item in set(unigram_tuples)}
    unigram_p, unigram_counts = calc_prob(unigram_tuples)
    unigram_counts[(START_SYMBOL,)] = len(training_corpus) 
    
    print("\nProcessing bigrams")
    #bigram_p =  {item : log2(bigram_tuples.count(item)/bcount) for item in set(bigram_tuples)}
    bigram_p, bigram_counts = calc_prob_bi(bigram_tuples, unigram_counts)
    bigram_counts[(START_SYMBOL,START_SYMBOL)] = len(training_corpus) 
    
    print("\nProcessing trigrams")
    #trigram_p = {item : log2(trigram_tuples.count(item)/tcount) for item in set(trigram_tuples)}
    trigram_p, trigram_counts = calc_prob_bi(trigram_tuples, bigram_counts)

    return unigram_p, bigram_p, trigram_p

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys = sorted(unigrams_keys)
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys = sorted(bigrams_keys)
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys = sorted(trigrams_keys)    
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, corpus):
    
    scores = []
    
    for sentence in corpus:
        ngrams = make_ngrams(sentence, n)
        score = sum([ ngram_p.get(x, -1000) for x in ngrams])
        scores.append(max(score, -1000))
        
    return scores

def make_ngrams(sentence, n):
    
    tokens = sentence.split()
    tokens.append(STOP_SYMBOL)
    
    grams = []
    if n == 1:
        grams = list([(x,) for x in tokens])
    elif n == 2:
        tokens.insert(0, START_SYMBOL)
        grams = list(nltk.bigrams(tokens))
    elif n == 3:
        tokens.insert(0, START_SYMBOL)
        tokens.insert(0, START_SYMBOL)
        grams = list(nltk.trigrams(tokens))  
    
    return grams

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    scores = []
    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# DO NOT MODIFY THE MAIN FUNCTION
def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print("Part A time: " + str(time.clock()) + ' sec')

if __name__ == "__main__": main()
