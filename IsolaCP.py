import tkinter
import random
from itertools import product
import winsound
import logging
import argparse
import threading


VELIKOST_POLJA = 70
GLOBINA = 1
VELJAVNO = "v"
IGRALEC_1 = 1
IGRALEC_2 = 2
UNICENO = 0
ZACETNI_IGRALEC = IGRALEC_1
NEODLOCENO = None
PREMIK = True
UNICENJE = False

NAPIS_IGRALEC1_PREMIK = "Na potezi je MODRI igralec. Cas je da se premaknes."
NAPIS_IGRALEC2_PREMIK = "Na potezi je ZELENI igralec. Cas je da se premaknes."
NAPIS_IGRALEC1_UNICENJE = "Na potezi je MODRI igralec. Cas je da unicis polje."
NAPIS_IGRALEC2_UNICENJE = "Na potezi je ZELENI igralec. Cas je da unicis polje."

NAVODILA = """just kiding \n hahahah \n \n
Na polju 7*7 igralca postavita svojo figurico
na sredino nasprotnih robov. Igralca si izmenjujeta
poteze. V vsaki potezi se igralec najprej premakne
za eno polje(kot kralj pri šahu), nato odstrani
eno polje. Na polja, ki so že bila odstranjena
se ni dovoljeno premakniti. Cilj igre je odstraniti
ploščice tako, da se nasprotnik ne more več premakniti."""


def nasprotnik(igralec):
    #določi nasprotnika

    if igralec == IGRALEC_1:
        return IGRALEC_2
    else:
        return IGRALEC_1


######################################################    class Igra      #############################


class Igra():
    '''napisana je logika igre '''

    def __init__(self):
        self.polje = list([VELJAVNO]*7 for _ in range(7)) #mreza za shranjevanje veljavnih polj
        self.polje[0][3] = IGRALEC_1
        self.polje[6][3] = IGRALEC_2
        self.na_potezi = ZACETNI_IGRALEC
        self.del_poteze = PREMIK
        self.pozicija_1 = (0, 3)
        self.pozicija_2 = (6, 3)                #zacetna pozicija obeh igralcev

        self.zgodovina = []


    def shrani_pozicijo(self):
        pol = [self.polje[i][:] for i in range(7)]
        self.zgodovina.append((pol, self.na_potezi, self.del_poteze, self.pozicija_1, self.pozicija_2))


    def razveljavi(self):

        (self.polje, self.na_potezi, self.del_poteze, self.pozicija_1, self.pozicija_2) = self.zgodovina.pop()


    def kopija(self):
        """Vrni kopijo te igre, brez zgodovine."""
        # Kopijo igre naredimo, ko poženemo na njej algoritem.
        # Če bi algoritem poganjali kar na glavni igri, ki jo
        # uporablja GUI, potem bi GUI mislil, da se menja stanje
        # igre (kdo je na potezi, kdo je zmagal) medtem, ko bi
        # algoritem vlekel poteze
        k = Igra()
        k.polje = [self.polje[i][:] for i in range(7)]
        k.na_potezi = self.na_potezi
        k.pozicija_1 = self.pozicija_1
        k.pozicija_2 = self.pozicija_2
        k.del_poteze = self.del_poteze
        # k.zgodovina = self.zgodovina
        return k


    def je_veljavna(self, i, j):
        return (self.polje[i][j] == VELJAVNO)

    def je_konec(self):
        if self.porazenec() != None:
            return True
        else:
            return False

    def pozicija_na_potezi(self):
        ''' vrne par koordinate igralca na potezi'''

        if self.na_potezi == IGRALEC_1:
            return self.pozicija_1
        else:
            return self.pozicija_2

    def pozicija_nasprotnik(self):
        if self.na_potezi == IGRALEC_2:
            return self.pozicija_1
        else:
            return self.pozicija_2

    def veljavne_poteze(self, nasprotnik = False):
        if self.del_poteze:
            return self.veljavne_poteze_premik(nasprotnik)
        else:
            return self.veljavne_poteze_unici()


    def veljavne_poteze_premik(self, nasprotnik = False ):
        ''' preveri vsa polja okoli igralca na potezi in vrne seznam polj na katere se lahko premakne'''

        poteze = []
        if not nasprotnik:
            (a, b) = self.pozicija_na_potezi()
        else:
            (a, b) = self.pozicija_nasprotnik()
        for i in range(3):
            for j in range(3):
                c = a - 1 + i
                d = b - 1 + j
                if c >= 0 and c <= 6 and d >= 0 and d <= 6 and self.je_veljavna(c, d):
                    poteze.append((c, d))
        return poteze

    def veljavne_poteze_unici(self):
        '''vrne seznam vseh polj, ki jih lahko uničimo'''
        poteze = []
        for i in range(7):
            for j in range(7):
                if self.je_veljavna(i, j):
                    poteze.append((i, j))
        return poteze

    def naredi_pravo_potezo(self, i, j):
        if self.del_poteze == PREMIK:
            self.premik(i, j)
        else:
            self.unici(i, j)


    def premik(self, i, j):
        '''premaknemo se na veljavno polje, staro polje naredimo spet veljavno, zapišemo pozicijo igralca, zamenjamo del poteze'''

        if (i, j) in self.veljavne_poteze_premik():
            #print("naredimo premik na polje", i, j)
            self.shrani_pozicijo()
            self.polje[i][j] = self.na_potezi
            (c, d) = self.pozicija_na_potezi()
            self.polje[c][d] = VELJAVNO
            if self.na_potezi == IGRALEC_1:
                self.pozicija_1 = (i, j)
            else:
                self.pozicija_2 = (i, j)
            self.del_poteze = UNICENJE
        else:
            print(self.na_potezi, "klice premik na nedovoljenem polju", i, j)

    def unici(self, i, j):
        '''uniči veljavno polje, spremeni del poteze, zamenja igralca'''

        if (i, j) in self.veljavne_poteze_unici():
           # print("naredimo uničenje na polju", i, j)
            self.shrani_pozicijo()
            self.polje[i][j] = UNICENO
            self.del_poteze = PREMIK

            self.na_potezi = nasprotnik(self.na_potezi)

        else:
            print(self.na_potezi, "klice unici na nedovoljenem polju")

    def zmagovalec(self):
        pass

    def porazenec(self):
        if len(self.veljavne_poteze_premik()) == 0:
            return self.na_potezi


####################################################       človek        #####################


class Clovek():
    '''igralec, ki ga upravlja človek'''

    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        self.gui.plosca.bind('<Button-1>', self.klik)

    def klik(self, event):
        '''shrani koordinate polja kamor kliknemo'''

        i = int(event.x / self.gui.velikost_polja)
        j = int(event.y / self.gui.velikost_polja)
        self.gui.povleci_potezo(i, j)


#########################################################     racunalnik    #############################

class Racunalnik():
    '''Igralec, ki ga upravlja racunalnik'''

    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem
        self.mislec = None

    def igraj(self, n=None, m=None):
        if n == None:
            self.mislec = threading.Thread(
                target=lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))

            self.mislec.start()

            self.gui.plosca.after(100, self.preveri_potezo)
        else:
            self.gui.povleci_potezo(n, m)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, ali je algoritem že izračunal potezo."""
        if self.algoritem.poteza is not None:
            # Algoritem je našel potezo, povleci jo, če ni bilo prekinitve
            [(i, j), (n, m)] = self.algoritem.poteza
            #print("rač naredi potezo", i, j)
            self.gui.povleci_potezo(i, j, True, (n, m))
            #self.gui.povleci_potezo(n, m)
            # Vzporedno vlakno ni več aktivno, zato ga "pozabimo"
            self.mislec = None
        else:
            # Algoritem še ni našel poteze, preveri še enkrat čez 100ms
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        if self.mislec:
            logging.debug ("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporočimo, da mora nehati z razmišljanjem
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

    def klik(self):
        pass



##################################################      Algoritem Alfa-Beta     ####################


class Alfabeta():


    ZMAGA = 100000 # Mora biti vsaj 10^5
    NESKONCNO = ZMAGA + 1 # Več kot zmaga

    def __init__(self, globina = GLOBINA):
        self.globina = globina
        self.prekinitev = False
        self.igra_kopija = None
        self.jaz = None
        self.poteza = None
        self.poteza_konec = None

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra):

        self.igra_kopija = igra
        self.prekinitev = False
        self.jaz = self.igra_kopija.na_potezi
        self.poteza = None

        (poteza, vrednost) = self.albe(self.globina, True, 0, [])
        print("alba je našel", poteza)
        if len(poteza) < 2:
            print("to se ne bi smel zgodit")
        self.jaz = None
        self.igra_kopija = None

        if not self.prekinitev:
            if self.poteza_konec == None:
                self.poteza = poteza
            else:
                self.poteza = self.poteza_konec


    def vrednost_pozicije(self, i, j):
        #return 50
        return random.randrange(500)
        '''if not self.igra_kopija.del_poteze:  ####  mi se premaknemo na a,b toda sedaj je del poteze unici ceprav nas zanima premik
            return self.vrednost_pozicije_premik(i, j)
        else:                                  ### smo uničili sedaj je na potezi nasprotnik da se premakne
            return self.vrednost_pozicije_unici(i, j)'''


    def vrednost_pozicije_premik(self, i, j):
        return random.randrange(500)

    def vrednost_pozicije_premik1(self, i, j):
        vrednost = 0
        vre_prazno = 100
        for a in self.igra_kopija.veljavne_poteze_premik():
            vrednost += vre_prazno

        return vrednost

    def vrednost_pozicije_unici(self, i, j):
        return random.randrange(500)
        '''veljavne_poteze = self.igra_kopija.veljavne_poteze_premik()
        if len(veljavne_poteze) == 0:
            return self.NESKONCNO

        (n, m) = self.igra_kopija.pozicija_na_potezi()
        dobra_polja = []
        for a in range(7):
            for b in range(7):
                if (abs(a - n))**2 + (abs(b - m))**2 <= 2:
                    dobra_polja.append((a, b))

        vrednost = 0
        vre_ob_nasprotniku = 500
        if (i, j) in dobra_polja :
            print("jackpot")
            return 500
        else:
            return 10
'''
    def vrednost_pozicije_unici1(self, i, j):
        #print("unicujemo polje (i, j)")
#
        if len(self.igra_kopija.veljavne_poteze_premik()) == 0:
            return self.NESKONCNO

        vrednost = 0
        vre_ob_nasprotniku = 500

        (a, b) = self.igra_kopija.pozicija_na_potezi()

        razdalja = abs(a-i) + abs(b-j)
        if razdalja <=3:
            vrednost += (5-razdalja)*100

        def st_unicene(self):
            stevilo = 0
            for a in range(3):
                for b in range(3):
                    c = i - 1 + a
                    d = j - 1 + b
                    if c >= 0 and c <= 6 and d >= 0 and d <= 6 and (self.igra_kopija.polje[i][j] == UNICENO):
                        stevilo += 1
            return stevilo

        ste = st_unicene(self)
        if ste >= 3:
            return vrednost +10

        else:

            def polja_unicene(self):
                polja = []
                for a in range(3):
                    for b in range(3):
                        c = i - 1 + a
                        d = j - 1 + b
                        if c >= 0 and c <= 6 and d >= 0 and d <= 6 and (self.igra_kopija.polje[i][j] == UNICENO):
                            polja.append(a+b)
                return polja

            for a in polja_unicene():
                vrednost += (3-a)*100


            return vrednost



    def albe(self, globina, maksimiziramo, alba_vrednost = 0, zaporedje_potez = []):
        ##rabmo sam še eno ker so že poteze premiki brisanje sami vejo kaj pa kako

        if self.prekinitev:
             # Sporočili so nam, da moramo prekiniti
             logging.debug ("Minimax prekinja, globina = {0}".format(globina))
             return (None, 0)


        #print("izvajamo albe na globini", globina)
        #print("maks =", maksimiziramo)
        #print(zaporedje_potez)
        if globina == 0:
            poteza = (zaporedje_potez[-2], zaporedje_potez[-1])
            #print("ocenjujemo polje", poteza)
            return (poteza, self.vrednost_pozicije(poteza[1][0],poteza[1][1]))

        else:
            if maksimiziramo:
                return self.albe_max(globina, alba_vrednost, zaporedje_potez)

            else:
                return self.albe_min(globina, alba_vrednost, zaporedje_potez)


    def albe_max(self, globina, alba_vrednost = 0, zaporedje_potez = [], najboljsa_poteza = None, vrednost_najboljse = 0):
        #print("max")
        if zaporedje_potez == []:
            najboljsa_poteza = None
            vrednost_najboljse = 0
        #print("max število veljavnih potez je", len(self.igra_kopija.veljavne_poteze()))
        c = self.igra_kopija.veljavne_poteze()
        #print(c)
        if c == []:
            self.poteza_konec = (zaporedje_potez[0], zaporedje_potez [1])
            najboljsa_poteza = (zaporedje_potez[0], zaporedje_potez[1])
            #print(najboljsa_poteza, "c je prazen")

        for (a, b) in c:

            self.igra_kopija.naredi_pravo_potezo(a, b)
            zaporedje_potez.append((a, b))

            d = self.igra_kopija.veljavne_poteze()

            if d == []:
                self.poteza_konec = (zaporedje_potez[0], zaporedje_potez [1])
                najboljsa_poteza = (zaporedje_potez[0], zaporedje_potez[1])

            for (n, m) in d:
                #if self.igra_kopija.del_poteze != PREMIK:   ### še maksimiziramo
                     #   mak = (self.igra_kopija.del_poteze != PREMIK)
                self.igra_kopija.naredi_pravo_potezo(n, m)
                zaporedje_potez.append((n, m))
               # print(zaporedje_potez)
                if najboljsa_poteza == None:                    #če kličemo prvič nimammo še ničesar s čimer bi primerjali
                    alba_vrednost = 0
                else:
                    alba_vrednost = vrednost_najboljse
                '''else:                                       ### sedaj bomo mini
                    mak = (self.igra_kopija.del_poteze != PREMIK)
                    if najboljsa_poteza == None:
                        alba_vrednost = 0
                    else:
                        alba_vrednost = vrednost_najboljse'''


                (poteza,vrednost) = self.albe(globina-1, False, alba_vrednost, zaporedje_potez)


                self.igra_kopija.razveljavi()
                zaporedje_potez.pop()

                #print(a, b, "poteza, ki smo jo izvedli")
                #print(zaporedje_potez[-1])
                #if vrednost >= na_ze_na_vrednost:        ## alba-max kliče alba-min. se pravi če lahko nasprotnik naredi boljšo
                                                                ## kot jo je alba_min že našel potem je ta "veja zanič" in vrne takoj vrne
                                                                ##  neskončno, da je alba-min ne uporabi
                    #print("slaba veja")
                    #return (None, na_ze_na_vrednost)

                if vrednost > vrednost_najboljse:
                    vrednost_najboljse = vrednost
                    najboljsa_poteza = poteza

            self.igra_kopija.razveljavi()
            zaporedje_potez.pop()

        return (najboljsa_poteza, vrednost_najboljse)

    def albe_min(self, globina, alba_vrednost = 0, zaporedje_potez = [], najboljsa_poteza = None, vrednost_najboljse = 0):
        #print("min")
        if zaporedje_potez == []:
            najboljsa_poteza = None
            vrednost_najboljse = 0
        #print("min število veljavnih potez je", len(self.igra_kopija.veljavne_poteze()))
        c = self.igra_kopija.veljavne_poteze()
        #print(c)
        if c == []:
            self.poteza_konec = (zaporedje_potez[0], zaporedje_potez [1])
            najboljsa_poteza = (zaporedje_potez[0], zaporedje_potez[1])
            #print(najboljsa_poteza, "c je prazen")

       # print(zaporedje_potez)
        for (a, b) in c:

            #print(a,b)
            self.igra_kopija.naredi_pravo_potezo(a, b)
            zaporedje_potez.append((a, b))
            #print(zaporedje_potez)

            d = self.igra_kopija.veljavne_poteze()

            if d == []:
                self.poteza_konec = (zaporedje_potez[0], zaporedje_potez [1])
                najboljsa_poteza = (zaporedje_potez[0], zaporedje_potez[1])
            for (n, m) in d:
                #if self.igra_kopija.del_poteze != PREMIK:   ### še maksimiziramo
                 #   mak = (self.igra_kopija.del_poteze != PREMIK)
                self.igra_kopija.naredi_pravo_potezo(n, m)
                zaporedje_potez.append((n, m))

                if najboljsa_poteza == None:                    #če kličemo prvič nimammo še ničesar s čimer bi primerjali
                    alba_vrednost = 0
                else:
                    alba_vrednost = vrednost_najboljse
                '''if self.igra_kopija.del_poteze != PREMIK:         ###  še vedno minimiziramo
                mak = (self.igra_kopija.del_poteze == PREMIK)
                if najboljsa_poteza == None:
                    alba_vrednost = 0
                else:
                    alba_vrednost = vrednost_najboljse
            else:                                             ###  sedaj bomo maksimiziral
                mak = (self.igra_kopija.del_poteze == PREMIK)
                if najboljsa_poteza == None:
                    alba_vrednost = 0
                else:
                    alba_vrednost = vrednost_najboljse'''


                (poteza,vrednost) = self.albe(globina-1, True, alba_vrednost, zaporedje_potez)
                #vrednost = -vrednost

                self.igra_kopija.razveljavi()
                zaporedje_potez.pop()

            #print(a, b, "poteza, ki smo jo izvedli")
            #if vrednost <= na_ze_na_vrednost:
                #print("slaba veja")
                #return (None, na_ze_na_vrednost)


                if vrednost > vrednost_najboljse:
                    vrednost_najboljse = vrednost
                    najboljsa_poteza = poteza

            self.igra_kopija.razveljavi()
            zaporedje_potez.pop()

        return (najboljsa_poteza, vrednost_najboljse)







#########################################################     class Gui     ################################

class Gui():
    '''graficni vmesnik'''

    def __init__(self, master, velikost, globina = GLOBINA):
        self.napis = tkinter.StringVar()
        self.napis.set(NAPIS_IGRALEC1_PREMIK)
        #self.napis = tkinter.StringVar(master, value=NAPIS_IGRALEC1)
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=0, columnspan = 4)

        self.velikost_polja = velikost
        self.velikost_plosce = self.velikost_polja * 7          #dolocimo velikost celotnega polja in posameznih celic


        self.plosca = tkinter.Canvas(master, width=self.velikost_plosce, height=self.velikost_plosce)       #pripravimo platno
        self.plosca.grid(row=1, column=0, columnspan = 4)

        self.kvadratki = self.narisi_kvadratke()

        self.izbira_igralcev()
        self.globina = globina



    def izbira_igralcev(self):
        #self.igralec_1 = Clovek(self)
        self.igralec_1 = Racunalnik(self, Alfabeta(GLOBINA))
        #self.igralec_2 = Clovek(self)
        self.igralec_2 = Racunalnik(self, Alfabeta(GLOBINA))
        self.zacni_igro()

    def zacni_igro(self):
        '''Nastavi stanje igre na zacetek igre.'''

        self.igra = Igra()
        (a1, b1) = self.igra.pozicija_1
        (a2, b2) = self.igra.pozicija_2
        self.narisi_igralca(a1, b1, "blue")
        self.narisi_igralca(a2, b2, "green")
        self.igralec_1.igraj()              #sprement v random

    def koncaj_igro(self):
        '''Nastavi stanje igre na konec igre.'''

        print ("KONEC!")

    def povleci_potezo(self, i, j, racunalnik=False, unici=(None, None)):
        '''celoten potek poteze'''

        if (i, j) in self.igra.veljavne_poteze():
            self.narisi(i, j)
            self.igra.naredi_pravo_potezo(i, j)
            self.spremeni_napis()


        else:

            if self.igra.na_potezi == IGRALEC_1:
                self.igralec_1.igraj()
            else:
                self.igralec_2.igraj()


        if self.igra.je_konec():
                self.koncaj_igro()
        else:
            if self.igra.na_potezi == IGRALEC_1:
                self.igralec_1.igraj(unici[0],unici[1])
            else:
                self.igralec_2.igraj(unici[0],unici[1])



    def narisi(self, i, j):
        if self.igra.del_poteze:
            self.narisi_premik(i, j)
        else:
            self.narisi_uniceno(i, j)

    def narisi_uniceno(self, i, j):
        self.plosca.create_rectangle(i * self.velikost_polja, j * self.velikost_polja, (i + 1) * self.velikost_polja, (j + 1) * self.velikost_polja, fill="red", outline="black")


    def narisi_premik(self, i, j):
        '''premakne igralca, ki je na potezi na izbrano polje'''
        self.narisi_veljavno()
        self.narisi_igralca(i, j)

    def narisi_igralca(self, i, j, barva = None):
        '''na izbrano polje nariše igralca'''

        if barva == None:
            if self.igra.na_potezi == IGRALEC_1:
                barva = "blue"
            else:
                barva = "green"
        self.plosca.create_oval(i * self.velikost_polja, j * self.velikost_polja, (i + 1) * self.velikost_polja, (j + 1) * self.velikost_polja, fill=barva, outline="black")


    def narisi_veljavno(self, a = None, b = None):
        '''polje nariše spet veljavno, brez argumentov ga nariše kjer je igralec na potezi'''

        if a == None and b == None:
            (a,b) = self.igra.pozicija_na_potezi()
        self.plosca.create_rectangle(a * self.velikost_polja, b * self.velikost_polja, (a + 1) * self.velikost_polja, (b + 1) * self.velikost_polja, fill="white", outline="black")

    def narisi_kvadratke(self):
        '''narise polje ob zacetku igre'''

        for (i, j) in product(range(7), range(7)):
            coordX1 = (i * self.velikost_polja)
            coordY1 = (j * self.velikost_polja)
            coordX2 = coordX1 + self.velikost_polja
            coordY2 = coordY1 + self.velikost_polja
            color = "white" #if i%2 == j%2 else "black"
            self.plosca.create_rectangle(coordX1, coordY1, coordX2, coordY2, fill = color, outline = "black")


    def spremeni_napis(self, napis = None):
        if napis == None:

            if self.igra.na_potezi == IGRALEC_1:
                if self.igra.del_poteze:
                    self.napis.set(NAPIS_IGRALEC1_PREMIK)
                else:
                    self.napis.set(NAPIS_IGRALEC1_UNICENJE)
            else:
                if self.igra.del_poteze:
                    self.napis.set(NAPIS_IGRALEC2_PREMIK)
                else:
                    self.napis.set(NAPIS_IGRALEC2_UNICENJE)
        else:
            self.napis.set(napis)

#########################################################    class Meni    ##################################


class Meni():
    '''meni'''

    def __init__(self, master, velikost_polja):
        self.master = master
        self.velikost_polja = velikost_polja

        #winsound.PlaySound("files\\two.wav", winsound.SND_ASYNC|winsound.SND_LOOP)

        self.napis = tkinter.StringVar(master, value="Isola!")
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=0, columnspan = 4)

        #gumb play
        master.slika_play = slika_play = tkinter.PhotoImage(file="files\play.png")
        self.gumb_play = tkinter.Button(master, command = self.play, image = slika_play)
        self.gumb_play.grid(row=2, column=0)

        #gumb options
        master.slika_options = slika_options = tkinter.PhotoImage(file="files\options.png")
        self.gumb_options = tkinter.Button(master, command = self.options, image = slika_options)
        self.gumb_options.grid(row=2, column=1)

        #gumb help
        master.slika_help = slika_help = tkinter.PhotoImage(file="files\help.png")
        self.gumb_help = tkinter.Button(master, command = self.help, image = slika_help)
        self.gumb_help.grid(row=2, column=2)

        #gumb close
        master.slika_close = slika_close = tkinter.PhotoImage(file="files\close.png")
        self.gumb_close = tkinter.Button(master, command = self.close, image = slika_close)
        self.gumb_close.grid(row=2, column=3)

        #naredi igralno ploščo
        self.play()


    def play(self, event = None):
        self.aplication2 = Gui(root, self.velikost_polja, GLOBINA)
        #sam da vidm kva se zgodi pr manši globini

    def options(self):
        print("options")
        pass

    def help(self):
        napis_help = "NAVODILA"
        navodila = NAVODILA

        self.aplication2.spremeni_napis(napis_help)

        self.velikost_plosce = 7 * self.velikost_polja
        self.plosca = tkinter.Canvas(self.master, width=self.velikost_plosce, height=self.velikost_plosce)
        self.plosca.grid(row=1, column=0, columnspan = 4)
        self.plosca.create_text(self.velikost_plosce/2, self.velikost_polja*5, text = navodila)

        print("help")
        pass

    def close(self):
        root.destroy()

if __name__ == "__main__":
    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title("Isola")
    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplication1 = Meni(root, VELIKOST_POLJA)
    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
