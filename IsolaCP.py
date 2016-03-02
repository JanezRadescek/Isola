import tkinter
import random

#isue  shranjevanje poteze za premik in uničevanje posebej ne vem če vredu ??
VELJAVNO = None
IGRALEC_1 = 1
IGRALEC_2 = 2
UNICENO = 0
ZACETNI_IGRALEC = IGRALEC_1
NEODLOCENO = None
PREMIK = True
UNICENJE = False


def nasprotnik(igralec):
    #določi nasprotnika
    if igralec == IGRALEC_1:
        return IGRALEC_2
    else:
        return IGRALEC_1


class Igra():
    def __init__(self):
        self.polje = list([VELJAVNO]*7 for _ in range(7))
        self.polje[0][3] = 1
        self.polje[6][3] = 2
        self.na_potezi = ZACETNI_IGRALEC
        self.zgodovina = []
        self.pozicija_1 = (0, 3)
        self.pozicija_2 = (6, 3)
        self.del_poteze =

    def shrani_pozicijo(self):
        p = [self.polje[i][:] for i in range(7)]
        self.zgodovina.append((p, self.na_potezi))

    def razveljavi(self):
        (self.polje, self.na_potezi) = self.zgodovina.pop()

    def je_veljavna(self, i, j):
        return (self.polje[i][j] == VELJAVNO)

    def je_konec(self):
        #treba še delat
        pass

    def pozicija_na_potezi(self):
        # vrne par koordinate igralca na potezi
        if self.na_potezi == IGRALEC_1:
            return self.pozicija_1
        else:
            return self.pozicija_2

    def veljavne_poteze_premik(self):
        # preveri vsa polja okoli igralca na potezi in vrne seznam polj na katere se lahko premakne
        poteze = []
        (a, b) = self.pozicija_na_potezi()
        for i in range(3):
            for j in range(3):
                c = a - 1 + i
                d = b - 1 + j
                if c >= 0 and c <= 6 and d >= 0 and d <= 6 and self.je_veljavna(c, d):
                    poteze.append((i, j))
        return poteze

    def veljavne_poteze_unici(self):
        #vrne seznam vseh polj, ki jih lahko uničimo
        poteze = []
        for i in range(7):
            for j in range(7):
                if self.je_veljavna(i, j):
                    poteze.append((i, j))
        return poteze

    def povleci_potezo(self, i, j):
        if self.del_poteze == PREMIK:
            self.premik(i, j)
        else:
            self.unici(i, j)

    def premik(self, i, j):
        #premaknemo se na veljavno polje, staro polje naredimo spet veljavno, zapišemo pozicijo igralca
        if (i, j) in self.veljavne_poteze_premik():
            self.shrani_pozicijo()
            self.polje[i][j] = self.na_potezi
            (c, d) = self.pozicija_na_potezi()
            self.polje[c][d] = VELJAVNO
            if self.na_potezi == IGRALEC_1:
                self.pozicija_1 = (i, j)
            else:
                self.pozicija_2 = (i, j)
            self.del_poteze = UNICENJE

    def unici(self, i, j):
        #uniči veljavno polje
        if (i, j) in self.veljavne_poteze_unici():
            self.shrani_pozicijo()
            self.polje[i][j] = UNICENO
            self.del_poteze = PREMIK

    def zmagovalec(self):
        pass

    def porazenec(self):
        if len(self.veljavne_poteze_premik()) == 0:
            return self.na_potezi


#################################################### človek


class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        self.gui.plosca.bind('<Button-1>', self.klik)

    def klik(self, event):
        #
        i = int(event.x / self.gui.cellsize)
        j = int(event.y / self.gui.cellsize)
        self.gui.povleci_potezo(i, j)



#######################################################







