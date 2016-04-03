import tkinter
import random
from itertools import product
import winsound
import logging
import argparse
import threading


VELIKOST_POLJA = 70
GLOBINA = 4
VELJAVNO = None
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

NAVODILA = """
Na polju 7*7 igralca postavita svojo figurico
na sredino nasprotnih robov. Igralca si izmenjujeta
poteze. V vsaki potezi se igralec najprej premakne
za eno polje(kot kralj pri šahu), nato odstrani
eno polje. Na polja, ki so že bila odstranjena,
se ni dovoljeno premakniti. Cilj igre je odstraniti
polja tako, da se nasprotnik ne more več premakniti."""


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

    def prekini(self):
        pass


#########################################################     racunalnik    #############################

class Racunalnik():
    '''Igralec, ki ga upravlja racunalnik'''

    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem
        self.mislec = None

    def igraj(self):
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))

        self.mislec.start()

        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, ali je algoritem že izračunal potezo."""
        if self.algoritem.poteza is not None:
            # Algoritem je našel potezo, povleci jo, če ni bilo prekinitve
            i, j = self.algoritem.poteza
            self.gui.povleci_potezo(i, j)
            # Vzporedno vlakno ni več aktivno, zato ga "pozabimo"
            self.mislec = None
        else:
            # Algoritem še ni našel poteze, preveri še enkrat čez 100ms
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        if self.mislec != None:
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

        (poteza, vrednost) = self.albe(self.globina, True)
        print("Najdena poteza je", poteza)

        self.jaz = None
        self.igra_kopija = None

        if not self.prekinitev:
            if self.poteza_konec == None:
                self.poteza = poteza
            else:
                self.poteza = self.poteza_konec


    def vrednost_pozicije(self, i, j, zap_potez):
    #Ocenjujemo stanje plošče ne pa zadnjo potezo !!.
        vsota = 1000    #nova ničla
        vsota1 = 0
        vsota2 = 0

        for _ in self.igra_kopija.veljavne_poteze_premik():
            vsota1 += 100
        for _ in self.igra_kopija.veljavne_poteze_premik(True):
            vsota2 += 100

        if self.jaz == self.igra_kopija.na_potezi:
            vsota2 *= -1
        else:
            vsota1 *= -1

        vsota += vsota1 + vsota2

        return vsota


    def albe(self, globina, maksimiziramo, na_ze_na_vrednost = NESKONCNO, zap_potez = []):
        ##rabmo sam še eno ker so že poteze premiki brisanje sami vejo kaj pa kako
        if self.prekinitev:
             # Sporočili so nam, da moramo prekiniti
             logging.debug ("Minimax prekinja, globina = {0}".format(globina))
             return (None, 0)


        if globina == 0:
            (i, j) = zap_potez[-1]

            if len(zap_potez) != GLOBINA:
                print("globina in GLOBINA se ne ujemata")
            return ((i,j), self.vrednost_pozicije(i, j, zap_potez))

        else:
            if maksimiziramo:
                if self.igra_kopija.del_poteze == PREMIK:
                    return self.albe_max_pre(globina, na_ze_na_vrednost, zap_potez)
                else:
                    return self.albe_max_uni(globina, na_ze_na_vrednost, zap_potez)

            else:
                if self.igra_kopija.del_poteze == PREMIK:
                    return self.albe_min_pre(globina, na_ze_na_vrednost, zap_potez)
                else:
                    return self.albe_min_uni(globina, na_ze_na_vrednost, zap_potez)


    def albe_max_pre(self, globina, na_ze_na_vrednost, zap_potez):

        najboljsa_poteza = None
        vrednost_najboljse = -self.NESKONCNO

        c = self.igra_kopija.veljavne_poteze()
        if len(c) == 0:
            return (zap_potez[0], -self.NESKONCNO)


        random.shuffle(c)

        for (a, b) in c:

            self.igra_kopija.naredi_pravo_potezo(a, b)

            zap_potez.append((a, b))
            if najboljsa_poteza == None:                    #če kličemo prvič nimammo še ničesar s čimer bi primerjali
                alba_vrednost = self.NESKONCNO
            else:
                alba_vrednost = vrednost_najboljse

            (p,vrednost) = self.albe(globina-1, True, alba_vrednost, zap_potez)

            self.igra_kopija.razveljavi()
            zap_potez.pop()


            if (vrednost >= self.NESKONCNO) and (self.poteza_konec == None):         ##našli smo zmagovalno potezo
                self.poteza_konec = zap_potez[0]


            if vrednost >= na_ze_na_vrednost:        ## alba-max kliče alba-min. se pravi če lahko nasprotnik naredi boljšo
                                                            ## kot jo je alba_min že našel potem je ta "veja zanič" in vrne takoj vrne
                                                            ##  neskončno, da je alba-min ne uporabi

                return (None, na_ze_na_vrednost)

            if vrednost >= vrednost_najboljse:
                vrednost_najboljse = vrednost
                najboljsa_poteza = (a, b)

        return (najboljsa_poteza, vrednost_najboljse)


    def albe_max_uni(self, globina, na_ze_na_vrednost, zap_potez):
    #tu ne moremo uporabiti alba rezanja saj smo še vedno mi napotezi.

        najboljsa_poteza = None
        vrednost_najboljse = -self.NESKONCNO
        c = self.igra_kopija.veljavne_poteze()
        random.shuffle(c)
        if len(c) == 0:
            print("max_uni nima veljavnih potez")

        for (a, b) in c:

            self.igra_kopija.naredi_pravo_potezo(a, b)
            zap_potez.append((a, b))

            if najboljsa_poteza == None:                    #če kličemo prvič nimammo še ničesar s čimer bi primerjali
                alba_vrednost = -self.NESKONCNO
            else:
                alba_vrednost = vrednost_najboljse


            (p,vrednost) = self.albe(globina-1, False, alba_vrednost, zap_potez)

            self.igra_kopija.razveljavi()
            zap_potez.pop()

            if (vrednost >= self.NESKONCNO) and (self.poteza_konec == None):         ##našli smo zmagovalno potezo
                self.poteza_konec = zap_potez[0]
                return (self.poteza_konec, self.NESKONCNO)



            if vrednost >= vrednost_najboljse:
                vrednost_najboljse = vrednost
                najboljsa_poteza = (a, b)

        return (najboljsa_poteza, vrednost_najboljse)


    def albe_min_pre(self, globina, na_ze_na_vrednost, zap_potez):

        najboljsa_poteza = None
        vrednost_najboljse = self.NESKONCNO

        c = self.igra_kopija.veljavne_poteze()
        random.shuffle(c)

        if len(c) == 0:
            self.poteza_konec = zap_potez[0]
            return (zap_potez[0],self.NESKONCNO)

        for (a, b) in c:

            self.igra_kopija.naredi_pravo_potezo(a, b)
            zap_potez.append((a, b))


            if najboljsa_poteza == None:                    #če kličemo prvič nimammo še ničesar s čimer bi primerjali
                alba_vrednost = -self.NESKONCNO
            else:
                alba_vrednost = vrednost_najboljse


            (p,vrednost) = self.albe(globina-1, False, alba_vrednost, zap_potez)

            self.igra_kopija.razveljavi()
            zap_potez.pop()


            if vrednost <= na_ze_na_vrednost:
                return (None, na_ze_na_vrednost)


            if vrednost <= vrednost_najboljse:
                vrednost_najboljse = vrednost
                najboljsa_poteza = (a, b)

        return (najboljsa_poteza, vrednost_najboljse)


    def albe_min_uni(self, globina, na_ze_na_vrednost, zap_potez):
        #ne režemo


        najboljsa_poteza = None
        vrednost_najboljse = self.NESKONCNO
        c = self.igra_kopija.veljavne_poteze()
        random.shuffle(c)

        if len(c) == 0:
            print("min_uni nima veljavnih potez")

        for (a, b) in c:

            self.igra_kopija.naredi_pravo_potezo(a, b)
            zap_potez.append((a,b))


            if najboljsa_poteza == None:                    #če kličemo prvič nimammo še ničesar s čimer bi primerjali
                alba_vrednost = self.NESKONCNO
            else:
                alba_vrednost = vrednost_najboljse


            (p,vrednost) = self.albe(globina-1, True, alba_vrednost, zap_potez)

            self.igra_kopija.razveljavi()
            zap_potez.pop()


            if vrednost <= vrednost_najboljse:
                vrednost_najboljse = vrednost
                najboljsa_poteza = (a, b)

        return (najboljsa_poteza, vrednost_najboljse)







#########################################################     class Gui     ################################

class Gui():
    '''graficni vmesnik'''

    def __init__(self, master, velikost, globina = GLOBINA, igralci=["racunalnik","racunalnik"]):
        self.igralci = igralci
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
        self.konec = False

    def unici(self):
        if self.igralec_1 != None:
            self.igralec_1.prekini()
        if self.igralec_2 != None:
            self.igralec_2.prekini()
        self.igralec_1 = None
        self.igralec_2 = None
        self.konec = True
        self.plosca.destroy()



    def izbira_igralcev(self):
        if self.igralci == ["igralec", "igralec"]:
            self.igralec_1 = Clovek(self)
            self.igralec_2 = Clovek(self)
        elif self.igralci == ["igralec", "racunalnik"]:
            self.igralec_1 = Clovek(self)
            self.igralec_2 = Racunalnik(self, Alfabeta(GLOBINA))
        elif self.igralci == ["racunalnik", "igralec"]:
            self.igralec_1 = Racunalnik(self, Alfabeta(GLOBINA))
            self.igralec_2 = Clovek(self)
        elif self.igralci == ["racunalnik","racunalnik"]:
            self.igralec_1 = Racunalnik(self, Alfabeta(GLOBINA))
            self.igralec_2 = Racunalnik(self, Alfabeta(GLOBINA))
        else:
            print("napacni igralci")
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

    def povleci_potezo(self, i, j):
        '''celoten potek poteze'''
        if self.konec:
            self.koncaj_igro()
            return None

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
                self.igralec_1.igraj()
            else:
                self.igralec_2.igraj()




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
        self.igralec1 = "igralec"
        self.igralec2 = "igralec"

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
        self.aplication2 = None
        self.play()


    def play(self, event = None):
        if self.aplication2 != None:
            self.aplication2.unici()

        self.aplication2 = Gui(root, self.velikost_polja, GLOBINA, [self.igralec1, self.igralec2])

    def options(self):
        #self.plosca.delete("all")

        def izbira_igralcev_pvp():
            self.igralec1 = "igralec"
            self.igralec2 = "igralec"
            self.play()

        def izbira_igralcev_eve():
            self.igralec1 = "racunalnik"
            self.igralec2 = "racunalnik"
            self.play()

        def izbira_igralcev_pve():
            self.igralec1 = "igralec"
            self.igralec2 = "racunalnik"
            self.play()

        def izbira_igralcev_evp():
            self.igralec1 = "racunalnik"
            self.igralec2 = "igralec"
            self.play()


        if self.aplication2 != None:
            self.aplication2.unici()

        napis_options = "NASTAVITVE"

        self.aplication2.spremeni_napis(napis_options)
        self.gumb1 = tkinter.Button(self.master, text="PvP", command=izbira_igralcev_pvp, height=(4), width=(10))
        self.gumb1.grid(row=0, column=0, columnspan=2)
        self.gumb2 = tkinter.Button(self.master, text="EvE", command=izbira_igralcev_eve, height=(4), width=(10))
        self.gumb2.grid(row=0, column=1, columnspan=2)
        self.gumb3 = tkinter.Button(self.master, text="PvE", command=izbira_igralcev_pve, height=(4), width=(10))
        self.gumb3.grid(row=1, column=0, columnspan=2)
        self.gumb4 = tkinter.Button(self.master, text="EvP", command=izbira_igralcev_evp, height=(4), width=(10))
        self.gumb4.grid(row=1, column=1, columnspan=2)
        self.plosca.delete("all")



        print("options")


    def help(self):
        if self.aplication2 != None:
            self.aplication2.unici()

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
