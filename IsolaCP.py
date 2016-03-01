import tkinter
import random

#isue  shranjevanje poteze za premik in uničevanje posebej ne vem če vredu ??
PRAZNO = None
IGRALEC_1 = 1
IGRALEC_2 = 2
UNICENO = 0

NEODLOCENO = None

def nasprotnik(igralec):
    #določi nasprotnika
    if igralec == IGRALEC_1:
        return IGRALEC_2
    else:
        return IGRALEC_1

class Igra():
    def __init__(self):

        self.polje = list([0]*7 for i in range(7))
        self.polje[0][3] = 1
        self.polje[6][3] = 2
        self.na_potezi = IGRALEC_1
        self.zgodovina = []
        self.pozicija_1 = (0,3)
        self.pozicija_2 = (6,3)



    def shrani_pozicijo(self):
        p = [self.polje[i][:] for i in range(7)]
        self.zgodovina.append((p, self.na_potezi))

    def razveljavi(self):
        (self.polje, self.na_potezi) = self.zgodovina.pop()

    def je_veljavna(self, i, j):
        return (self.polje[i][j] is None)

    def je_konec(self):
        #treba še delat
        pass

    def pozicija_na_potezi(self):
        #vrne par koordinate igralca na potezi
        if self.na_potezi == IGRALEC_1:
            return self.pozicija_1
        else:
            return self.pozicija_2


    def veljavne_poteze_premik(self):
        #preveri vsa polja okoli igralca na potezi in vrne seznam polj na katere se lahko premakne
        poteze = []
        (a,b) = self.pozicija_na_potezi()
        for i in range(3):
            for j in range(3):
                c = a-1+i
                d = b-1+j
                if c>=0 and c<=6 and d>=0 and d<=6 and self.je_veljavna(c,d):
                    poteze.append((i,j))
        return poteze

    def veljavne_poteze_unici(self):
        #vrne seznam vseh polj, ki jih lahko uničimo
        poteze = []
        for i in range(7):
            for j in range(7):
                if self.je_veljavna(i, j):
                    poteze.append((i,j))
        return poteze



    def premik(self, i, j):
        #premaknemo se na veljavno polje in staro polje naredimo spet veljavno
        if (i,j) in self.veljavne_poteze_premik():
            self.shrani_pozicijo()
            self.polje[i][j] = self.na_potezi
            (c,d) = self.pozicija_na_potezi()
            self.polje[c][d] = None

    def unici(self, i, j):
        #uniči veljavno polje
        if (i,j) in self.veljavne_poteze_unici():
            self.shrani_pozicijo()
            self.polje[i][j] = UNICENO


