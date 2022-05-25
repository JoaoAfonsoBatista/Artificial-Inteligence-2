# 89629 Joao Afonso Batista; 89640 Tomas Freire; grupo 094

import random

# LearningAgent to implement
# no knowledeg about the environment can be used
# the code should work even with another environment
class LearningAgent:

    # init
    # nS maximum number of states
    # nA maximum number of action per state
    def __init__(self,nS,nA):

            # define this function
            self.nS = nS
            self.nA = nA
            self.visitados = [False] * nS
            self.vezes_testado = [0] * nS
            self.vezes_testado_acao = [[0 for i in range(nA)] for j in range(nS)]
            
            #em cada posição, tem uma lista com 1-quantas vezes esta ação foi realizada e depois triplos
            #a dizer "fui para aqui estas vezes, logo tenho esta probablidade de ir para este sitio"
            self.modelo_transicao =  [[[0] for i in range(nA)] for j in range(nS)]
            
            #em cada lista, tem os numeros dos precessores dele
            self.precessores = [[] for j in range(nS)]
            #em cada lista, tem os numeros dos sucessores dele
            self.sucessores = [[] for j in range(nS)]
            self.recompensas = [0] * nS
            self.utilidades = [0 for j in range(nS)]
          
    
    # Select one action, used when learning  
    # st - is the current state        
    # aa - is the set of possible actions
    # for a given state they are always given in the same order
    # returns
    # a - the index to the action in aa
    def selectactiontolearn(self,st,aa):
        b = min([self.vezes_testado_acao[st][j] for j in range(len(aa))])
        
        
        for i in range(len(aa)):
            if self.vezes_testado_acao[st][i] == b:
                return i
        


    # Select one action, used when evaluating
    # st - is the current state        
    # aa - is the set of possible actions
    # for a given state they are always given in the same order
    # returns
    # a - the index to the action in aa
    def selectactiontoexecute(self,st,aa):
        util = -1000
        j = 0
        for i in aa:
            if self.utilidades[i] > util:
                util = self.utilidades[i]
                j = i
        return aa.index(j)
            


    # this function is called after every action
    # st - original state
    # nst - next state
    # a - the index to the action taken
    # r - reward obtained
    def learn(self,ost,nst,a,r):
        def f(u,n):
            if n < 1:
                return 1
            else:
                return u
        
        
        
        self.vezes_testado[ost] += 1
        
        self.vezes_testado_acao[ost][a] += 1
        
        #atualização do modelo de transação
        w = False
        for i in range(len(self.modelo_transicao[ost][a])):
            if i == 0:
                self.modelo_transicao[ost][a][i] += 1
            else:
                if self.modelo_transicao[ost][a][i][0] == nst:
                    self.modelo_transicao[ost][a][i][1] += 1
                    self.modelo_transicao[ost][a][i][2] = self.modelo_transicao[ost][a][i][1]/self.modelo_transicao[ost][a][0]
                    w = True
                else:
                    self.modelo_transicao[ost][a][i][2] = self.modelo_transicao[ost][a][i][1]/self.modelo_transicao[ost][a][0]
                    
        if not w:
            self.modelo_transicao[ost][a] = self.modelo_transicao[ost][a] + [[nst,1,1/self.modelo_transicao[ost][a][0]]]
          
        if not(nst in self.sucessores[ost]):
            self.sucessores[ost] += [nst]
        if not(ost in self.precessores[nst]):
            self.precessores[nst] += [ost]    
            

               
        self.recompensas[ost] = r
        self.visitados[ost] = True
             
        
        util = -1000
        for j in self.modelo_transicao[ost][1:]:
            e = 0
            visto = False
            for n in j[1:]:
                visto = True
                
                d = self.utilidades[n[0]] * n[2]
                
                e = e + d
            if util < e and visto:
                util = e
        if util == -1000:
            self.utilidades[ost] = r
        else:
            self.utilidades[ost] = r + util
                        
        b = self.precessores[ost]
        

        while b != []:
            c = b[0]

                
                
            if self.sucessores[c] != []:
                util_sucessor_max = -1000
                for j in self.modelo_transicao[c]:
                    e = 0
                    visto = False
                    for n in j[1:]:
                        visto = True 
                        
                        d = self.utilidades[n[0]] * n[2]
                        
                        e = e + d
                    if util_sucessor_max < e and visto:
                        util_sucessor_max = e
                        
                self.utilidades[c] = self.recompensas[c] + util_sucessor_max
            
            
            
            b = b[1:]



    
