import util
import os
import sys
sys.setrecursionlimit(10000)
class TransportationMDP(object):
    def __init__(self, N):
        self.N = N
    def startState(self):
        return 1
    def isEnd(self, state):
        return state == self.N
    def actions(self, state):
        result = []
        if state + 1 <= self.N:
            result.append('walk')
        if state * 2 <= self.N:
            result.append('tram')
        return result
    def succProbReward(self, state, action):
        result = []
        if action == 'walk':
            result.append((state + 1, 1., -1.))
        elif action == 'tram':
            failProb = 0.5
            result.append((state * 2, 1 - failProb, -2.))
            result.append((state, failProb, -2.))
        return result
    def discount(self):
        return 1.
    def states(self):
        return range(1, self.N + 1)

# doing value iteration

def valueIteration(mdp):
    cache = {}

    v = {}
    for state in mdp.states():
        v[state] = 0.

    def Q(state, action):
        return sum(prob * (reward + mdp.discount() * v[newState]) \
                for newState, prob, reward in mdp.succProbReward(state, action))

    reversed_states = list(mdp.states())[::-1]
    for state in reversed_states:
        if mdp.isEnd(state):
            v[state] = 0.
        else:
            print(mdp.actions(state))
            v[state] = max(Q(state, action) for action in mdp.actions(state))

    os.system('clear')
    print('{:15} {:15}'.format('s', 'V(s)', 'pi(s)'))
    for state in mdp.states():
        print('{:15} {:15}'.format(state, v[state]))
    input()
mdp = TransportationMDP(N=100)
valueIteration(mdp)