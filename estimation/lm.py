from math import log, exp
from random import random
from collections import defaultdict, Counter
from zipfile import ZipFile
import re

kNEG_INF = -1e6

kSTART = "<s>"
kEND = "</s>"

kWORDS = re.compile("[a-z]{1,}")
kREP = set(["Bush", "GWBush", "Eisenhower", "Ford", "Nixon", "Reagan"])
kDEM = set(["Carter", "Clinton", "Truman", "Johnson", "Kennedy"])

class OutOfVocab(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def sentences_from_zipfile(zip_file, filter_presidents):
    """
    Given a zip file, yield an iterator over the lines in each file in the
    zip file.
    """
    with ZipFile(zip_file) as z:
        for ii in z.namelist():
            try:
                pres = ii.replace(".txt", "").replace("state_union/", "").split("-")[1]
            except IndexError:
                continue

            if pres in filter_presidents:
                for jj in z.read(ii).decode(errors='replace').split("\n")[3:]:
                    yield jj.lower()

def tokenize(sentence):
    """
    Given a sentence, return a list of all the words in the sentence.
    """

    return kWORDS.findall(sentence.lower())

def bigrams(sentence):
    """
    Given a sentence, generate all bigrams in the sentence.
    """

    for ii, ww in enumerate(sentence[:-1]):
        yield ww, sentence[ii + 1]



class BigramLanguageModel:

    def __init__(self):
        self._vocab = set([kSTART, kEND])
        self._bg_counter = Counter()
        self._ug_counter = Counter()
        self._vocab_final = False

    def train_seen(self, word):
        """
        Tells the language model that a word has been seen.  This
        will be used to build the final vocabulary.
        """
        assert not self._vocab_final, \
            "Trying to add new words to finalized vocab"

        self._vocab.add(word)

    def generate(self, context):
        """
        Given the previous word of a context, generate a next word from its
        conditional language model probability.
        """

        # Add your code here.  Make sure to the account for the case
        # of a context you haven't seen before and Don't forget the
        # smoothing "+1" term while sampling.

        bin = 0
        threshold = random()
        for word in self._vocab:
            bin += exp(self.laplace(context, word))
            if (bin > threshold):
                return word

    def sample(self, sample_size):
        """
        Generate an English-like string from a language model of a specified
        length (plus start and end tags).
        """

        # You should not need to modify this function
        yield kSTART
        next = kSTART
        for ii in range(sample_size):
            next = self.generate(next)
            if next == kEND:
                break
            else:
                yield next
        yield kEND

    def finalize(self):
        """
        Fixes the vocabulary as static, prevents keeping additional vocab from
        being added
        """

        # you should not need to modify this function

        self._vocab_final = True

    def tokenize_and_censor(self, sentence):
        """
        Given a sentence, yields a sentence suitable for training or testing.
        Prefix the sentence with <s>, generate the words in the
        sentence, and end the sentence with </s>.
        """

        # you should not need to modify this function

        yield kSTART
        for ii in tokenize(sentence):
            if ii not in self._vocab:
                raise OutOfVocab(ii)
            yield ii
        yield kEND

    def vocab(self):
        """
        Returns the language model's vocabulary
        """

        assert self._vocab_final, "Vocab not finalized"
        return list(sorted(self._vocab))

    def laplace(self, context, word):
        """
        Return the log probability (base e) of a word given its context
        """

        assert context in self._vocab, "%s not in vocab" % context
        assert word in self._vocab, "%s not in vocab" % word

        bg_count = self._bg_counter[(context, word)] # How many times the given bigram occured
        context_count = self._ug_counter[context] # How many times the context occured

        return log((bg_count + 1) / (len(self._vocab) + context_count))

    def add_train(self, sentence):
        """
        Add the counts associated with a sentence.
        """

        # You'll need to complete this function, but here's a line of code that
        # will hopefully get you started.
        tokenizedSentence = list(self.tokenize_and_censor(sentence))
        for context, word in bigrams(tokenizedSentence):
            assert word in self._vocab, "%s not in vocab" % word
            self._bg_counter.update({(context, word)})

        for word in tokenizedSentence:
            self._ug_counter.update([word])

    def log_likelihood(self, sentence):
        """
        Compute the log likelihood of a sentence, divided by the number of
        tokens in the sentence.
        """
        sentence = list(self.tokenize_and_censor(sentence))
        return sum(self.laplace(context, word) for context, word in bigrams(sentence)) / len(sentence)


if __name__ == "__main__":
    dem_lm = BigramLanguageModel()
    rep_lm = BigramLanguageModel()

    for target, pres, name in [(dem_lm, kDEM, "D"), (rep_lm, kREP, "R")]:
        for sent in sentences_from_zipfile("../data/state_union.zip", pres):
            for ww in tokenize(sent):
                target.train_seen(ww)

        print("Done looking at %s words, finalizing vocabulary" % name)
        target.finalize()

        for sent in sentences_from_zipfile("../data/state_union.zip", pres):
            target.add_train(sent)

        print("Trained language model for %s" % name)

    with open("../data/2016-obama.txt", encoding='utf8') as infile:
        print("REP\t\tDEM\t\tSentence\n" + "=" * 80)
        unused_words = set()
        unused_bg = set()
        for ii in infile:
            if len(ii) < 15: # Ignore short sentences
                continue
            try:
                for word in tokenize(ii):
                    if (word not in rep_lm._vocab) and (word not in dem_lm._vocab):
                        unused_words.add(word)

                for context, word in bigrams(list(rep_lm.tokenize_and_censor(ii))):
                    if (word not in rep_lm._bg_counter) and (word not in dem_lm._bg_counter):
                        unused_bg.add((context, word))

                #dem_score = dem_lm.log_likelihood(ii)
                #rep_score = rep_lm.log_likelihood(ii)

                #print("%f\t%f\t%s" % (dem_score, rep_score, ii.strip()))
            except OutOfVocab:
                None

        print(unused_words)
        print(unused_bg)
        print(' '.join(rep_lm.sample(10)))
        print(' '.join(dem_lm.sample(10)))
