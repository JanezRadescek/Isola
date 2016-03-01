import tkinter
import random

IGRALEC_1
IGRALEC_2

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



    def shrani_pozicijo(self):
        p = [self.polje[i][:] for i in range(7)]
        self.zgodovina.append((p, self.na_potezi))

    def razveljavi(self):
        (self.polje, self.na_potezi) = self.zgodovina.pop()

    def je_veljavna(self, i, j):
        return (self.polje[i][j] is None)

    def je_konec(self):
        pass


