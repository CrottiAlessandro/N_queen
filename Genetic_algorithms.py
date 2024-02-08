#Author: Alessandro Crotti  885846
#Project: Assignment 1, Informatica 2 mod 1, Engineering Physics Ca' Foscari
'''
generiamo lo stato successivo partendo dalla combinazione di due stati
creiamo k stati random e gli stati sono rappresentati da una stringa di elementi finiti
(potrebbe essere utile creare un vettore con le regine dove l'indice e la colonna, e il numero è la riga)
Poi si valutano gli stati attraverso una fitness function
e in modo casuale un punto a caso della matrice può mutare.

1. generiamo k stati [1. 3. 0. 4. 2.] 
2. calcoliamo la fitness e li ordiniamo secondo questa.
3. prendiamo i primi due stati, li estraiamo dalla lista e ed effetuiamo un crossover
    ogni tanto avverrà una mutazione in un riga a caso di una colonna a caso di uno stato a caso quindi vanno estratti 3 numeri random 
    più il numero che ci definisce la prob.
4. li metto in nuova lista e vado avanti cosi finchè lo stato non è buono

FITNESS definito dalle regine che non sono sotto attacco(numero naturale)
CROSSOVER presi due stati più probabili, i vettori che li descrivono vengono tagliati e reincollati in un punto casuale
            [1. 3. 0. 4. 2.] [0. 2. 1. 3. 4.] [3. 2. 0. 1. 4.] [1. 4. 0. 2. 3.]
                          \    /
             [1. 3. 1. 3. 4.][0. 2. 0. 4. 2.]

MUTAZIONE  calcolo una probabilità di mutazione per lo stato generato e se la probabilità è superiore a tot genero due numeri random che mi identificano la collona 
            da mutare e il valore della riga che andremo a cambiare


   [1,3,0,4,2]     (fitness == 2)                   [0,2,4,3,1]   (fitness == 2)            
      |   |                                            |   |
      v   v                                            v   v
[[^. ^. w. ^. ^.]   questo stato non va         [[w. ^. ^. ^. ^.]   combianimao questi stati
 [w. ^. ^. ^. ^.]   bene perchè nelle            [^. ^. ^. ^. w.]   prendendo quello con la fitness   
 [^. ^. ^. ^. w.]   diagonali alcune regine      [^. w. ^. ^. ^.]   più alta e tagliamo dove c'è la 
 [^. w. ^. ^. ^.]   si attaccano                 [^. ^. ^. w. ^.]   colonna errata e rimuoviamo la 
 [^. ^. ^. w. ^.]]  ha 2 regine sbagliate        [^. ^. w. ^. ^.]]  minore se è in centro potremmo 
  x     x  x                                      x     x  x        provarle entrambe



funzioni che mi servono
-generare un vettore random                  numpy.random.randint(low=0, high=n, size=n, dtype=int)
-splittare un vettore in due parti           numpy.split(ary, indices_or_sections, axis=0)[source]
-creare un vettore partendo da due parti     numpy.concatenate((arr, arr1))   
-controllo delle regine

'''

import numpy as np
import time as time
import random
import tracemalloc as trm
import csv


class nqueen():
    def __init__(self, n, muterr=0.20):
        '''
        Inizializzazione dei parametri con i valori forniti 
        N - dimensione della scacchiera
        muterr - tolleranza alle mutazioni
        In seguito vengono create 2 liste
        self.chess conterrà tutte le scacchiere generate dalla funzione successiva
        self.fitness conterrà i valori di fitnesse per ogni scacchiera contenuta in self.chess e organizzate con lo stesso ordine
        self.pi
        '''
        self.n = n
        self.chess = []
        self.muterr = muterr
        self.fitness = []

    def generate_queen(self):
        '''
        uitlizza la funzione random.choise di numpy per generare N scacchiere random che identificano la posizione delle regine.
        nella generazione i numeri non possono ripetersi cosi che le righe e le colonne siano già prive di attacchi.
        le scacchiere vengono inserite nella list self.chess
        '''
        for i in range(self.n):
            self.chess.append(np.random.choice(range(self.n), self.n, replace=False))
        return

    def attack(self):
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
        for x in self.chess:
            fitness=self.n
            for i in range(len(x)):
                for j in range(len(x)):
                    if i!=j:
                        if x[j]==x[i]:
                            #print(x[j],x[i])
                            fitness-=1
                            break
                        elif j==0:
                            if(x[i]+i <= self.n and x[j] == x[i]+i) or (x[i]-i >= 0 and x[j] == x[i]-i):
                                #print("j==0", x[i]+i, x[i]-i,"la regine è nella colonna ",j,"e riga " ,x[j])
                                fitness-=1
                                break
                        elif(x[i]+(i-j) <= self.n and x[j] == x[i]+(i-j)) or (x[i]-(i-j) >= 0 and x[j] == x[i]-(i-j)):
                            #print(x[i]+(i-j), x[i]-(i-j),"la regine è nella colonna ",i,"e riga " ,x[i]," e la regina che della colonna che voglio controllare è in ", j , x[j])
                            fitness-=1
                            break
            self.fitness.append(fitness)   
      
    def crossover_mutation(self):
        '''
        questa funzion effettua sia la mutazione sia il crossover
        finche la lista degli stati non è vuota noi estraiamo il rettore relativo al valore di fitness più alto e lo facciamo accoppiare col secondo più alto
        estriamo ogni elemento sia dalla lista di vettori sia da quella delle fitness cosi da mantenere la corrispondenza degl'indici poi genergiamo un numero casuale
        che ci farà rientrare in 4 possibili casi in cui attaccheremo le quattro parti dei vettori in modi differenti. una volta attaccati proseguiamo con la mutazione
        che avverrà solo se il numero causale generato sarà minore della tolleranza che abbiamo definito. Se è minore procediamo con lo scambiare due colonne della matrice .
        Alla fine salviamo tutti i nuovi stati nella lista globale che sarà vuota.
        '''
        tmpchess = []
        while self.chess:
            index1 = np.argmax(self.fitness)                                    #prendo l'indice della fitness che ha il valore più alto
            cross1 = self.chess.pop(index1)                                     #uso il valore dell'indice per estrarre la suddetta scacchiera dalla lista di scacchiere
            fitness1 = self.fitness.pop(index1)                                 #rimuovo anche la fitness cosi da mantenere la corrispondenza degl'indici
            cut = np.random.randint(1,self.n-1)                                 #genero un numero casuale che indicherà dove effettuare il taglio del vettore
            arr1, arr2 =  np.split(cross1, indices_or_sections=[cut], axis=0)   #taglio il vettore

            try:                                                                #rifaccio la stessa cosa ma impongo un try except poi se la scacchiera è dispari 
                index2 = np.argmax(self.fitness)                                #mi darà un errore
                cross2 = self.chess.pop(index2)
                fitness2 = self.fitness.pop(index2)
                arr3, arr4 =  np.split(cross2, indices_or_sections=[cut], axis=0)
            except:
                son1= np.concatenate((arr1, arr2)) 
                tmpchess.append(son1)
                break
            prob = np.random.uniform(0,1)                                       #genero un numero casuale che mi permetterà di scegliere in che modo attaccare i due vettori
            #print(prob)
            if prob<0.25:
                son1= np.concatenate((arr1, arr4))
                son2= np.concatenate((arr3, arr2))  
            elif 0.25<=prob<0.50:
                son1= np.concatenate((arr2, arr3))
                son2= np.concatenate((arr4, arr1)) 
            elif 0.50<=prob<0.75:
                son1= np.concatenate((arr2, arr3))
                son2= np.concatenate((arr1, arr4)) 
            else:
                son1= np.concatenate((arr4, arr1))
                son2= np.concatenate((arr3, arr2)) 
            #mutazione
            if np.random.uniform(0,1) <= self.muterr:                           #applico la mutazione se il numero casuale è minore uguale al valore di tolleranza che abbiamo scelto
                one = random.randint(0, self.n-1)                               #genero due numeri casuali per indiduare quale colonne scambiare.
                two = random.randint(0, self.n-1)
                if one!=two:                                                    
                    y = son1[one]
                    z = son1[two]
                    son1[two]=y
                    son1[one]=z
                one = random.randint(0, self.n-1)                               #faccio lo stesso per l'altro vettore
                two = random.randint(0, self.n-1)
                if one!=two:
                    y = son2[one]
                    z = son2[two]
                    son2[two]=y
                    son2[one]=z
            tmpchess.append(son1)                                               #salvo i due valori in un lista temporanea e appena self.chess si svuota li sposterò
            tmpchess.append(son2)   
        self.chess = tmpchess

    def goal(self):
        '''
        questa funzione ci permetterà di uscire quando arriveremo ad una soluzione
        '''
        if self.n in self.fitness:
            index = self.fitness.index(self.n)
            print(self.chess[index])
            return True
        else:
            return False

    def solve(self):
        '''
        questa funzione chiama le altre funzioni in ordine per effettuare correttamente l'algoritmo
        '''
        while not self.goal():
            self.crossover_mutation()
            self.attack()
        return 

if __name__ == "__main__":

    queen = nqueen(5,0.05)
    queen.generate_queen()
    queen.attack()
    queen.solve()
    print()
      
    

         
    
    
