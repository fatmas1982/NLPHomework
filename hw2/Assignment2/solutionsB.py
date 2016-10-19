import sys
import nltk
import math
import time
import re

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000

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


# TODO: IMPLEMENT THIS FUNCTION
# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train):
    brown_words = []
    brown_tags = []
    #first = True  
    
    for sentence in brown_train:
        words = []
        tags = []
        words.append(START_SYMBOL)
        tags.append(START_SYMBOL)
        words.append(START_SYMBOL)
        tags.append(START_SYMBOL)
        for str in sentence.split():
            m = re.search("^(.+)[/]([^/]+)$", str)
            words.append(m.group(1))
            tags.append(m.group(2))
        words.append(STOP_SYMBOL)
        tags.append(STOP_SYMBOL)
        
        #if first:
        #    print(words)
        #    first = False
        
        brown_words.append(words)
        brown_tags.append(tags)

    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags):
    tcounts = {}
    bcounts = {}
    logs = {}
    tgrams = []
    bgrams = []
    logs = {}
    
    for tokens in brown_tags:
        bgrams.extend(list(nltk.bigrams(tokens)))
        #tokens.insert(0, START_SYMBOL) 
        tgrams.extend(list(nltk.trigrams(tokens)))
        
    
    print("\nCalculating ngram counts")    
    for token in tgrams:
        x = tcounts.get(token, 0)
        tcounts[token] = x + 1
        Pd.printdot()

    for token in bgrams:
        x = bcounts.get(token, 0)
        bcounts[token] = x + 1
        Pd.printdot()        
    #bcounts[(START_SYMBOL, START_SYMBOL)] = len(brown_tags) 
        
    print("\nCalculating log probabilities")
    for key in tcounts.keys():
        subkey = key[:-1]
        try:
            logs[key] = log2(float(tcounts[key])/bcounts[subkey])
        except:
            print("Damnit, it broke...")
            print(key)
            print(tcounts[key])
            print(subkey)
            print(bcounts[subkey])
            
    return logs

# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()  
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
    known_words = set([])
    
    counts = {}
    print("\nCalculating known words")
    for words in brown_words:
        for token in words:
            x = counts.get(token, 0)
            counts[token] = x + 1
            Pd.printdot()
    
    for key in counts.keys():
        if counts[key] > RARE_WORD_MAX_FREQ:
            known_words.add(key)
    
    return known_words

# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words, known_words):
    brown_words_rare = []
    
    #first = True
    
    print("\nReplacing words")
    for words in brown_words:
        new_words = []
        #if first:
        #    print(words)
        #    first = False
        for token in words:
            if token in known_words:
                new_words.append(token)
            else:
                new_words.append(RARE_SYMBOL)
            Pd.printdot()
        brown_words_rare.append(new_words)
    
    return brown_words_rare

# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(brown_words_rare, brown_tags):
    e_values = {}
    taglist = set([])
    
    for tokens in brown_tags:
        for tag in tokens:
            taglist.add(tag)
    
    #print taglist
    print("\nCalculating emission probabilities")
    
    #group words by tag
    tag_words = {}
    for tag in taglist:
        tag_words[tag] = []
        
    #this is messy with indexes but whatever...
    for i in range(len(brown_words_rare)):
        words = brown_words_rare[i]
        for j in range(len(words)):
            tag = brown_tags[i][j]
            word = brown_words_rare[i][j]
            tag_words[tag].append(word)
            Pd.printdot()
    
    tw_tuple_counts = {}
    #get word counts by tag
    for tag in tag_words.keys():
        words = tag_words[tag]
        for word in words:
            tw_tuple = (word, tag)
            x = tw_tuple_counts.get(tw_tuple, 0)
            tw_tuple_counts[tw_tuple] = x + 1
            Pd.printdot()
    
    #calculate divisor for each tag (dict comprehention blew up...)
    tw_word_counts = {}
    for tag in tag_words.keys():
        tw_word_counts[tag] = len(tag_words[tag])
        Pd.printdot()
    
    #get log probs of words by tag 
    for tw_tuple in tw_tuple_counts.keys():
        e_values[tw_tuple] = log2(float(tw_tuple_counts[tw_tuple]) / tw_word_counts[tw_tuple[1]])
    
    return e_values, taglist

# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()  
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words
# q_values is from the return of calc_trigrams()
# e_values is from the return of calc_emissions()
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    tagged = []
    return tagged

# This function takes the output of viterbi() and outputs it to file
def q5_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# This function uses nltk to create the taggers described in question 6
# brown_words and brown_tags is the data to be used in training
# brown_dev_words is the data that should be tagged
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. 
def nltk_tagger(brown_words, brown_tags, brown_dev_words):
    # Hint: use the following line to format data to what NLTK expects for training
    training = [ zip(brown_words[i],brown_tags[i]) for i in xrange(len(brown_words)) ]

    # IMPLEMENT THE REST OF THE FUNCTION HERE
    tagged = []
    return tagged

# This function takes the output of nltk_tagger() and outputs it to file
def q6_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    # start timer
    time.clock()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)

    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    # delete unneceessary data
    del brown_train
    del brown_words_rare

    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    # format Brown development data here
    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])

    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)

    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')

    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)

    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')

    # print total time to run Part B
    print "Part B time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
