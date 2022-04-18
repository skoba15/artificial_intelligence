# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.



""" int this case discount should be large and noise should be be small so
pacman won't get negative reward"""
def question2():
    answerDiscount = 0.9
    answerNoise = 0.0
    return answerDiscount, answerNoise



""" in this case discount is small and the reward is small too to reach the goal"""
def question3a():
    answerDiscount = 0.1
    answerNoise = 0.0
    answerLivingReward = -9.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


""" in this case noise is not zero, so there is a chance that pacman will get the 
negative reward and therefore tries to avoid it"""
def question3b():
    answerDiscount = 0.1
    answerNoise = 0.1
    answerLivingReward = -2.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'



"""in this case liwing reward is smaller than than in question3b(), so pacman 
continues his road to the farther terminal state"""
def question3c():
    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


""" the case is almost the same as for the nearest cliff, the noise is not zero compared
to previous case"""
def question3d():
    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = -0.001
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


""" in this case living reward is so high that pacman prefers not to terminate 
the game and get positive points infinitely"""
def question3e():
    answerDiscount = 0.00000001
    answerNoise = 0.0
    answerLivingReward = 100000
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'



def question6():
    answerEpsilon = None
    answerLearningRate = None
    # If not possible, return 'NOT POSSIBLE'
    """ this is not possible"""
    return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
