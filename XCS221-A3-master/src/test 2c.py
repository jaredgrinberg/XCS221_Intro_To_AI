import util
import sys
import os
sys.setrecursionlimit(10000)
class TransportationMDP(object):
    def __init__(self, N):
        self.N = N
    def startState(self):
        return 0
    def isEnd(self, state):
        return state == -self.N or state == self.N
    def actions(self, state):
        return [-1, 1]
    def succProbReward(self, state, action):
        result = []
        if action == -1:
            failProb = .35
            s1 = state - 1
            s2 = state + 1
            if s1 != -2:
                result.append((state - 1, 1 - failProb, -5.))
            else:
                result.append((state - 1, 1 - failProb, 20.))
            if s2 != 2:
                result.append((state + 1, failProb, -5.))
            else:
                result.append((state + 1, failProb, 100.))
        elif action == 1:
            failProb = .6
            s1 = state - 1
            s2 = state + 1
            if s1 != -2:
                result.append((state - 1, failProb, -5.))
            else:
                result.append((state - 1, failProb, 20.))
            if s2 != 2:
                result.append((state + 1, 1 - failProb, -5.))
            else:
                result.append((state + 1, 1 - failProb, 100.))
        return result
    def discount(self):
        return 1.
    def states(self):
        return range(-self.N, self.N + 1)

# doing value iteration

def valueIteration(mdp):
    v = {}
    for state in mdp.states():
        v[state] = 0.

    def Q(state, action):
        return sum(prob * (reward + mdp.discount() * v[newState]) for newState, prob, reward in mdp.succProbReward(state, action))

    while True:
        #get new values from old values
        newv = {}
        for state in mdp.states():
            blah = mdp.actions(state)
            if mdp.isEnd(state):
                newv[state] = 0.
            else:
                newv[state] = max(Q(state, action) for action in mdp.actions(state))
        # check for convergence
        if max(abs(v[state] - newv[state]) for state in mdp.states()) < 1e-10:
            break
        v = newv

        #read policy
        pi = {}
        for state in mdp.states():
            if mdp.isEnd(state):
                pi[state] = 'none'
            else:
                pi[state] = max((Q(state, action), action) for action in mdp.actions(state))[1]

        os.system('clear')
        print('{:15} {:15}'.format('s', 'V(s)', 'pi(s)'))
        for state in mdp.states():
            print('{:15} {:15} {:15}'.format(state, v[state], pi[state]))
        #input()
mdp = TransportationMDP(N=2)
valueIteration(mdp)