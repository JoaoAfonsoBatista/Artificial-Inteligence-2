import pickle
import random
import matplotlib.pyplot as plt
from teste6 import *

def runagent(A, T, R, I = 1, learningphase=True, nlearn = 1000, ntest = 100):

        J = 0
        if learningphase:
                n = nlearn
        else:
                n = ntest
                
        st = I
        for ii in range(1,n):
                aa = T[st][0]
                if learningphase:
                        a = A.selectactiontolearn(st,aa)
                else:
                        a = A.selectactiontoexecute(st,aa)
                try:
                        nst = T[st][0][a]
                except:
                        print(st,a)
                r = R[st]
                J += r
                #print(st,nst,a,r)
                #nst = aa[a]
                if learningphase:
                        A.learn(st,nst,a,r)
                else:
                        print(st,nst,a,r)
                        pass
                
                st = nst

                if not ii%15:
                        st = I
        return J/n
        

# due to the randomness in the learning process, we will run everythin NREP times
# the final grades is based on the average on all of them

NREP = 5
val = [0,0,0,0]
print("exemplo 1")
for nrep in range(0,NREP):       
        A = LearningAgent(114,15)
        # your solution will be tested with other environments    
        with open("mapasgraph2.pickle", "rb") as fp:   #Unpickling
            AA = pickle.load(fp)

        T = AA[0]
        R = [-1]*114
        R[72] = 0
        R[89] = 0
        R[112] = 2
#        Caminho otimal:
#        55 58 2 -1
#        58 72 1 -1
#        72 80 4 0
#        80 89 2 -1
#        89 111 4 0
#        111 112 3 -1
#        112 113 2 2
#        113 112 1 -1
#        112 113 2 2
#        average reward -0.1

        print("# learning phase")
        # in this phase your agent will learn about the world
        # after these steps the agent will be tested
        runagent(A, T, R, I = 55, learningphase=True, nlearn = 1000)
        print("# testing phase")
        # in this phase your agent will execute what it learned in the world
        # the total reward obtained needs to be the optimal
        Jn = runagent(A, T, R, I = 55, learningphase=False, ntest = 10)
        val[0] += Jn
        print("average reward",Jn)
        print("# 2nd learning phase")
        runagent(A, T, R, I = 55, learningphase=True, nlearn = 10000)
        print("# testing phase")
        Jn = runagent(A, T, R, I = 55, learningphase=False, ntest = 10)
        val[1] += Jn
        print("average reward",Jn)
print(".")
print(".")
print(".")    
print("exemplo 2")
print(".")
print(".")
print(".")
for nrep in range(0,NREP):
        
        A = LearningAgent(114,15)

        T = AA[0]
        R = [-1]*114
        R[72] = 0
        R[112] = 2
#        Caminho otimal:
#        55 58 2 -1
#        58 72 1 -1
#        72 80 4 0
#        80 89 2 -1
#        89 111 4 0
#        111 112 3 -1
#        112 113 2 2
#        113 112 1 -1
#        112 113 2 2
#        average reward -0.1


        print("# learning phase")
        # in this phase your agent will learn about the world
        # after these steps the agent will be tested
        runagent(A, T, R, I = 55, learningphase=True, nlearn = 1000)
        print("# testing phase")
        # in this phase your agent will execute what it learned in the world
        # the total reward obtained needs to be the optimal
        Jn = runagent(A, T, R, I = 55, learningphase=False, ntest = 10)
        val[2] += Jn
        print("average reward",Jn)
        print("# 2nd learning phase")
        runagent(A, T, R, I = 55, learningphase=True, nlearn = 10000)
        print("# testing phase")
        Jn = runagent(A, T, R, I = 55, learningphase=False, ntest = 10)
        val[3] += Jn
        print("average reward",Jn)        


val = list([ii/NREP for ii in val])
print(val)
cor = [(val[0]) >= -0.1, (val[1]) >= -0.1, (val[2]) >= -0.1, (val[3]) >= -0.1] #valores otimais
print(cor)

grade = 0
for correct,mark in zip(cor,[3,7,3,7]):
        if correct:
                grade += mark
print("Grade in these tests (the final will also include hidden tests) : ", grade)        
