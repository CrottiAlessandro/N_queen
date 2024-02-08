#Author: Alessandro Crotti  885846
#Project: Assignment 1, Informatica 2 mod 1, Engineering Physics Ca' Foscari
import numpy as np
import time as time
import csv
import random
import matplotlib.pyplot as plt
import tracemalloc as trm

class nqueen():
    def __init__(self, n, shape):
        '''
        la classe prenderà in input la dimensione della scacchiera n e con quanti step suddividere il vettore che ci definisce la temperatura
        100000 sembra essere un buon valore.
        inizializziamo una scacchiera casuale di dimensione n con numeri da 0 a n senza ripetizioni; cosi da avere le righe e le colonne 
        prive di attacchi e dovremo controllare solo le diagonali.
        self.fitness la inizializziamo già chiamando la funzione attack che come vedremo dopo, conta tutti gli attacchi tra le regine
        la funzione della temperatura è costituita da un vettore che parte da 100 e scende a zero ed è costituito da 100000 step.
        gli altri valori inizializzati a zero, servono per tener conto di tutte le iterazione, in cui accettiamo un caso ottimale, negativo e totali.
        la lista self.fit raccoglie tutti i valori di fitness accettati e può essere utile per vedere gli andamenti della fitness al variare del tempo.
        '''
        self.n = n
        self.chess = np.random.choice(range(self.n), self.n, replace=False)
        self.fitness = self.attack(self.chess)
        self.T=np.linspace(100, 0, shape)
        self.negaccetpt = 0
        self.fit =[]
        self.iteration=0
        self.optimal=0

    def attack(self,state):
        '''
        La funzione controlla quante regine si stanno attaccando, quando ne incontra due che si attaccano, toglie un valore dalla fitness che viene
        inizializzata a N.
        La funzione è composta da 2 cicli for cosi ogni elemento del vettore può essere confrontato con ogni altro elemento dello stesso.
        Eliminiamo subito gli i e j uguali cosi non confrontiamo una data regina con se stessa e controlliamo subito la riga col primo if.
        in seguito esploriamo tutta la scacchiera "astratta" nel seguente modo:
        dato un valore di i(indica della colonna dov'è posizionata la regina) la confrontiamo con le altre j colonne. 
        x[i] è la riga in cui è posizionata la regina nella colonna i quindi se j indica la colonna successavia, sappiamo che la regina non dovrà trovarsi in 
        x[i] (quindi nella stessa riga) ne in x[i]+j e x[i]-j (quindi nelle due diagonali)
        e cosi riusciamo a controllare tutte le colonne della scacchiera tranne quelle per j==0 che le esploriamo a parte sapendo che 
        la regina posizionata nella colonna i, è distante i posizioni dalla prima colonna; quindi, x[i]+i e x[i]-i ci danno le diagonali riferite solo alla prima colonna
        tutto questo è effettuato sotto le condizioni di dimensione della scacchiera percui i valori devono essere compresi tra  0 e N 
        '''
        x = state
        fitness = self.n
        for i in range(len(x)):
                for j in range(len(x)):
                    if i!=j:
                        if x[j]==x[i]:
                            fitness-=1
                            break
                        elif j==0:
                            if(x[i]+i <= self.n and x[j] == x[i]+i) or (x[i]-i >= 0 and x[j] == x[i]-i):
                                fitness-=1
                                break
                        elif(x[i]+(i-j) <= self.n and x[j] == x[i]+(i-j)) or (x[i]-(i-j) >= 0 and x[j] == x[i]-(i-j)):
                            fitness-=1
                            break
        return fitness  
    
    def goal(self):
        '''
        questa funzione ci permetterà di uscire dal ciclo while qual'ora la fitness dovesse essere pari al valore di N
        la fitness ci conta quante regine non si stanno attaccando.
        '''
        if self.n == self.fitness:
            #print(self.chess)
            #print(self.fitness)
            return False
        else:
            return True


    def solve(self):
        '''
        finche lo stato non è ottimale, generiamo due numeri casuali da 0 a n e se i due valori non sono uguali, procediamo con invertire le colonne.
        per fare questo semplicemente copiamo gli elementi delle due colonne su due variabili ausiliarie e in seguito le ricopiamo sugli elementi del
        vettore ma invertite. quindi ricalcoliamo la fitness del nuovo stato e se è migliore o uguale diventera la nuova fitness mentre se è peggiore,
        genereremo un numero casuale tra 0 e 1000 e sè minore della funzione espressa sotto, allora accettiamo lo stato negativo.
        La probabilità media stimata è pari allo 0.1% e dagli studi fatti ed esplicitati nella relazione sembra essere tra i più vantaggiosi.
        '''
        i=0
        while self.goal():
          i+=1
          one = random.randint(0, self.n-1)
          two = random.randint(0, self.n-1)
          if one!=two:
            new_state = self.chess.copy()
            y = new_state[one]
            z = new_state[two]
            new_state[two]=y
            new_state[one]=z
            new_fitness = self.attack(new_state)
            if new_fitness>= self.fitness:
                self.chess=new_state
                self.fitness = new_fitness
                self.fit.append( self.fitness)
                self.optimal+=1
            elif np.random.uniform(0,1000)< np.exp(-(new_fitness - self.fitness)/self.T[i]):
                self.negaccetpt += 1
                self.chess=new_state
                self.fitness = new_fitness
                self.fit.append( self.fitness)
        self.iteration=i
        return True

if __name__ == "__main__":  
    queen = nqueen(35, 100000)
    queen.solve()
    print(queen.chess)
    
       
                
