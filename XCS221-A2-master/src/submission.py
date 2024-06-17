import shell
import util
import wordsegUtil

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        pass
        # ### START CODE HERE ###
        return 0
        # ### END CODE HERE ###

    def isEnd(self, state):
        pass
        # ### START CODE HERE ###
        return state == len(self.query)

        # ### END CODE HERE ###

    def succAndCost(self, state):
        pass
        # ### START CODE HERE ###
        words = []
        for i in range(state + 1, len(self.query) + 1):
            word = self.query[state:i]
            newState = i
            cost = self.unigramCost(word)
            action = word
            tup = action, newState, cost
            words.append(tup)
        return words
        # ### END CODE HERE ###

def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # ### START CODE HERE ###
    words = ucs.actions
    return ' '.join(words)
    # ### END CODE HERE ###

############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        pass
        # ### START CODE HERE ###
        return (wordsegUtil.SENTENCE_BEGIN, 0)
        # ### END CODE HERE ###

    def isEnd(self, state):
        pass
        # ### START CODE HERE ###
        return state[1] == len(self.queryWords)
        # ### END CODE HERE ###

    def succAndCost(self, state):
        pass
        # ### START CODE HERE ###
        words = []
        reconstruction = self.possibleFills(self.queryWords[state[1]])
        if len(reconstruction) == 0:
            other_tup = self.queryWords[state[1]],(self.queryWords[state[1]], state[1] + 1), self.bigramCost(state[0], self.queryWords[state[1]])
            words.append(other_tup)
        else:
            for reconstructed_word in reconstruction:
                newState = (reconstructed_word, state[1] + 1)
                cost = self.bigramCost(state[0], reconstructed_word)
                action = reconstructed_word
                tup = action, newState, cost
                words.append(tup)
        return words
        # ### END CODE HERE ###

def insertVowels(queryWords, bigramCost, possibleFills):
    pass
    # ### START CODE HERE ###
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(VowelInsertionProblem(queryWords, bigramCost, possibleFills))

    final = ucs.actions
    return ' '.join(final)
    # ### END CODE HERE ###

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        pass
        # ### START CODE HERE ###
        return (wordsegUtil.SENTENCE_BEGIN, 0)
        # ### END CODE HERE ###

    def isEnd(self, state):
        pass
        # ### START CODE HERE ###
        return state[1] == len(self.query)
        # ### END CODE HERE ###

    def succAndCost(self, state):
        pass
        # ### START CODE HERE ###
        words = []
        for i in range(state[1] + 1, len(self.query) + 1):
            word = self.query[state[1]:i]
            reconstruction = self.possibleFills(word)
            for reconstructed_word in reconstruction:
                newState = (reconstructed_word, state[1] + len(word))
                cost = self.bigramCost(state[0], reconstructed_word)
                action = reconstructed_word
                tup = action, newState, cost
                words.append(tup)
        return words
        # ### END CODE HERE ###

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    # ### START CODE HERE ###
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost, possibleFills))

    final = ucs.actions
    return ' '.join(final)
    # ### END CODE HERE ###

############################################################

if __name__ == '__main__':
    shell.main()
