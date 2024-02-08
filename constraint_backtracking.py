#Author: Alessandro Crotti  885846
#Project: Assignment 1, Informatica 2 mod 1, Engineering Physics Ca' Foscari
'''
Questo codice è finalizzato a risolvere il problema delle N-Regine attraverso il metodo Contrain-Backtracking
Ovvero quello di porre su una scacchiera NxN un numero N di regine, poste in modo tale da non attaccarsi tra di loro.

'''
from operator import truediv
from platform import java_ver
from site import venv
import numpy as np
import time as time
import tracemalloc as trm
import csv

class nqueens:
    def __init__(self,n):
        '''
        Questa classe prende come parametro il numero N di regine o del equivalente lato 
        ed inizializza una matrice di zeri della dimensione NxN
        '''
        self.n=n
        self.board = np.zeros((n,n))
    
    def propagate(self,i,j):      
            '''
            Questa funzione propaga gli attacchi della regina posizione alle cordinate i,j fornite.
            Nella matrice(scacchiera) verranno segnate con 
            0 le coordinate senza regina e in cui non è presente alcun attacco e nessuna regina
            1 le coordinate in cui e presente una regina 
            2 le coordinate sotto attacco dalla suddetta regina

            '''  
            if self.board[i,j]:
                return False
            idx=[]                                                    #qui salviamo le coordinate che andiamo a modificare su k           
            self.board[i,j] = 1                                       #inizializzo con 1 la coordinata in cui mettere la regina
            idx.append([i,j])                                         #aggiungo all'indice zero la coordinata della regina
            for k in range(self.n):                                   
                    #propago sulle colonne
                    if k!=j and self.board[i,k] == 0:                 #controllo che nella matrice che identifica la scacchiera, in [i,k] non ci sia un'altra regina
                        self.board[i,k] = 2                           #e con 2 segno quella coordinata come "sotto attacco"
                        idx.append([i,k])                             #aggiungo le propagazione nella lista
                    #propago sulle righe
                    if k!=i and self.board[k,j] ==0:                  #stessa cosa
                        self.board[k,j] = 2
                        idx.append([k,j])  
                    #propago nelle diagonali
                    if i+k < self.n and j+k < self.n and self.board[i+k,j+k] ==0:      #stessa cosa anche qui con i+k j+k mi muovo nel quadrante in basso a destra rispetto alla regina
                            self.board[i+k,j+k] = 2
                            idx.append([i+k,j+k]) 
                    if i-k >= 0 and j-k >= 0 and self.board[i-k,j-k] ==0:              #in basso a sinistra
                            self.board[i-k,j-k] = 2
                            idx.append([i-k,j-k])
                    if i+k < self.n and j-k >= 0 and self.board[i+k,j-k] ==0:          #in alto a sinistra
                            self.board[i+k,j-k] = 2
                            idx.append([i+k,j-k])
                    if i-k >= 0 and j+k < self.n and self.board[i-k,j+k]==0:           #in alto a destra
                            self.board[i-k,j+k] = 2
                            idx.append([i-k,j+k])                                      # e aggiungo ovviamente tutte queste componenti modificate alla lista che ci servirà dopo in caso di depropagazione
                    self.board[i,j] = 1                                                #qui rischio di modificare la denotazione della regina quindi la ribadisco
            return idx                                                                 #alla fine del ciclio ritorno la lista

    def parse(self,str):
        '''
        fornita una stringa con le posizioni delle regine in una colonna, questa funzione le aggiunge alla matrice
        '''
        assigments = str.split()
        if len(assigments)<(self.n*self.n):
            print("cannot parse string")
            return False
        for i in range(self.n):
            for j in range(self.n):
                c = assigments[i*self.n+j]
                if c == "1":
                    self.propagate(i,j)
        print(self.board)
        return True    

    def is_goal(self):                          
        '''
        La funzione ci dice se lo stato della matrice(scacchiera) è lo stato finale che vorremmo ottenere.
        Per fare cio cicla sulla scacchiera e conta quante regine abbiamo messo, 
        se ne abbiamo messo n allora torna True altrimenti restituisce False
        '''
        n=0                                         
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i,j] == 1:
                    n+=1
        if n==self.n:
            return True
        else:
            return False

    def remove_last_propagation(self, idx):
        '''
        Questa funzione pulisce la matrice(scacchiera) dall'ultima propagazione che vogliamo rimuovere e che forniamo attraverso la lista idx
        idx è una lista di lista del tipo [[i0,j0],[i1,j1],...,[im,jm]]
        '''
        for i,j in idx:
            self.board[i,j] = 0  
        return True  
 

    def first_idx(self,j,dict):
        '''
        Questa funzione prende come parametri j ovvero la colonna su cui siamo giunti che è ancora del tutto libera 
        e un dizionario che come chiavi le colonne e come valori una lista delle coordinate vietate
        in seguito si ciclia sulle righe della colonna e si identifica la prima coordinata libera che non sia contenuta della lista di coordiante vietate
        e si restituisce il mumero di riga se ne esiste uno libero altrimenti si torna None
        '''
        for k in range(self.n):
            if self.board[k,j]==0 and [k,j] not in dict[j]:
                return k

    def not_usefull(self):
        '''
        Questa funzione verifica se lo stato in cui siamo finiti è ancora utilizzabile.
        Per utilizzabile si intende se nella matrice(scacchiera) ci sono delle colonne con spazi liberi
        esempio 
            n==4
                i   j  0  1  2  3
                0    [[1. 2. 2. 2.]          nella colonna j=2 abbiamo una colonna intera di 2, 
                1     [2. 2. 2. 0.]          questo compromette il nostro stato e quindi lo escludiamo
                2     [2. 1. 2. 2.]
                3     [2. 2. 2. 2.]]

        nella funzione cicliamo sulle colonne e se una colonna ha un numero n di 2 allora torniamo True.
        Altrimenti False
        '''
        for i in range(self.n):
            if np.count_nonzero(self.board[:,i]==2)==self.n: 
                return True
        return False

    def get_j(self):
        '''
        Questa funzione ci restituisce il valore della prima colonna in cui dobbiamo ancora lavorare
        Presa la matrice(scacchiera) controlla le colonne -i che dovrebbe essere l'ultima su cui abbiamo lavorato ed in cui è presente una regina segnata col numero 1 
        e la colonna -i+1 e la successiva che se è uguale a 0 significa che è la colonna su cui dobbiamo lavorare.
        se questo ciclio non porta ad una soluzione significa che dobbiamo ancora partire o che siamo tornati indietro fino alla colonna 0
        '''
        for i in range(1,self.n+1): 
                if(np.count_nonzero(self.board[:,-i]==1)==1 and np.count_nonzero(self.board[:,-i+1]==1)==0):
                    return self.n-i+1
        return 0
    
    def clean_redflag(self,j,redflag):
        '''
        questa funzione pulisce il dizionario perchè quando depropraghiamo e ci spostiamo su un'altra coordinata, alcune coordinate vanno liberate
        
        1                       2                     3                     4
        [[1. 2. 2. 2.]        [[1. 2. 2. 2.]        [[1. 2. 2. 2.]        [[2. 2. 0. 0.]
         [2. 2. 2. 0.]         [2. 2. 0. 0.]         [2. 2. 1. 2.]         [1. 2. 2. 2.] 
         [2. 1. 2. 2.]         [2. 0. 2. 0.]         [2. 2. 2. 2.]         [2. 2. 0. 0.]
         [2. 2. 2. 2.]]        [2. 0. 0. 2.]]        [2. 1. 2. 2.]]        [2. 0. 2. 0.]]
        
        1. propaghiamo e otteniamo uno stato che non va bene poichè è presente una colonna di 2
        2. depropaghiamo e segnamo la coordinata [2,1] come vietata perchè non porta ad una soluzione e andiamo avanti   
                    redflag={0: [], 1: [[2,1]], 2: [], 3: []}    
        3. proseguiamo a ci ritroviamo in un altro stato che non va bene
                    redflag={0: [], 1: [[2,1]], 2: [[1,2]], 3: []} 
        4. depropaghiamo finche non troviamo uno stato utilizzabile e finisce che torniamo indietro e quindi i posti che abbiamo escluso prima ora devo diventare disponibili
           quindi quando depropaghiamo eliminiamo sempre gli stati vietati della colonna successiva 
                    redflag={0: [[0,0]], 1: [], 2: [], 3: []}

        '''
        for i in range(j+1,self.n):
            redflag[i] = []
        

    def initdict(self, dict):
        '''
        inizializzo il dizionario ponendo come chiavi il numero della colonna e valore un lista vuota in cui appenderemo gli stati vietati
        '''
        for i in range(self.n):
            dict.setdefault(i,[])

    def updatedict(self,j, dict, val):
        '''
        questa funzione aggiunge alla lista con chiave j, le coordinate vietate contenute in val
        '''
        for val in val:
            dict.setdefault(j,[]).append(val)

    def solve(self):           
            '''
            questa funzione è il corpo del risolutar, qui confluiscono tutte le funzioni definite in precedenza per la risoluzione del problema

            viene inizializzato il dizionario e creata la lista delle visite che conterrà tutte le coordinate che abbiamo propagato 
            e che verranno usare nella depropagazione se necessario
            '''
            redflag = dict()                            #dizionario che contiene come chiave le colonne e come valori le coordinate che etichettiamo come vietate poichè già provate e non ci hanno portato ad una soluzione
            self.initdict(redflag)                      #inizializzo il dizionario con n chiavi e una lista vuota come valori, vedi funzione 
            idx=[]                                      #vengono salvate tutte le propagazioni fatte in liste che avranno come prima componente il posto della regina mentre le altre sono le propagazioni della suddetta regina
            j=0
            while 0<=j<self.n:              
                i = self.first_idx(j,redflag)           #dato un valore di j(colonna) e il dizionario redflag che contiene gli stati vietati perchè gia provati, ci torna il primo valore di i(riga) disponbile
                self.clean_redflag(j,redflag)           #puliscie il dizionario 
                if i is None:                           #se i è None significa che non abbiamo trovato un indice disponibile e quindi non posso proseguire per questa strada
                    x=idx.pop()                         #prendo l'ultima propagazione fatta
                    if x[0] not in redflag[j-1]: self.updatedict(j-1,redflag,[x[0]])    #come primo elemento abbiamo le coordiante che vogliamo bandare e se non sono gia comprese nel dizionario, le aggiungiamo
                    self.remove_last_propagation(x)     #depropago l'ultima propagazione inserendo la lista che contiene le coordinate vietate perche sotto attacco dalla suddetta regina (vedi funzione)
                else:                           #se i è diverso da None e quindi è un numero
                    dx=self.propagate(i,j)      #propago la regina collocata in [i,j] e salvo in dx (lista temporanea) le coordinate modificate
                    idx.append(dx)              #salvo questa lista in idx che sarà quindi una lista di liste di liste [ [ [i0,j0], [i1,j1] ] , [ [i0,j0], [i1,j1], [i2,j2] ] ] dove [i0,j0] sono le posizioni delle regine
                    if self.not_usefull():                                              #se trovo una collona che non ha posti liberi perchè tutti sotto attacco, lo stato non è più utile e torno indietro mettendo l'ultima regina in redflag (vedi funzione)
                        x=idx.pop()                                                     #estraggo l'ultima propagazione
                        if x[0] not in redflag[j]: self.updatedict(j,redflag,[x[0]])    #aggiungo alla chiave j del dizionario redflag, una coordinata che escludiamo (vedi funzione)
                        self.remove_last_propagation(x)                                 #rimuoviamo la propagazione indesiderata fornendo la lista di punti da rimuovere
                if self.is_goal():        #se lo stato è quello desiderato (vedi funzione) abbiamo finito:)
                    return print(self.board)                      
                else:                                 #altrimenti prendiamo un nuovo j (vedi funzione)
                    j = self.get_j()
        


if __name__=="__main__":
  
  queen = nqueens(10)
  queen.solve()
  