import copy
import shutil
import string
from collections import deque
from Graph import Chessboard
from HashTable import HashTable
from InferenceEngine import InferenceEngine
from User import User

INFINITY = float('inf')
NEG_INFINITY = float('-inf')


class Interfejs:
    def __init__(self):
        self.velicina_table = 0
        self.trenutni_igrac = ''
        self.tabla = None
        self.igraci = {'X': 'Čovek', 'O': 'Računar'}
        # da se pametne trenutna stanja
        self.trenutno_stanje = HashTable(1)
        self.pozicija_polja = ''
        self.smer_pomeranja = ''
        self.mesto_na_steku = 0
        self.user1 = None
        self.user2 = None
        self.potezi = deque()
        self.matrica= []
        self.vrednost_stanja = 0
        self.inference_engine = InferenceEngine()

        self.inference_engine.add_rule(self.pravilo_broj_stekova, self.pravilo_broj_stekova_action)
        self.inference_engine.add_rule(self.pravilo_vrednost_stekova, self.pravilo_vrednost_stekova_action)



    def pravilo_broj_stekova(self, facts):
        #da moze da odigra da ima bar jednu figuru koju moze da pomeri
        return "BrojStekova" in facts and int(facts["BrojStekova"]) >= 1

    def pravilo_broj_stekova_action(self, facts):
        #kad je na true znaci da je pravilo da ima bar jednu figuricu ispunjeno i mozed da se igra
        facts["IgracImaViseStekova"] = True

    def pravilo_vrednost_stekova(self, facts):
        return "VrednostStekova" in facts and int(facts["VrednostStekova"]) >= 1

    def pravilo_vrednost_stekova_action(self, facts):
        facts["IgracImaVisokuVrednostStekova"] = True

    def dodaj_stanje(self, broj, stek):
        self.trenutno_stanje.set_val(broj, stek)

    def vrati_stanje(self, broj):
        return self.trenutno_stanje.get_val(broj)

    def obrisi_stanje(self, broj):
        self.trenutno_stanje.delete_val(broj)

    def vrati_korisnike(self):
        return [self.user1, self.user2]

    def vrati_tablu(self):
        return self.tabla

    def izaberi_ko_prvi_igra(self):
        while True:
            izbor = input("Ko će igrati prvi? Unesite 'C' za Čoveka  ili 'R' za Računar: ").upper()
            if izbor == 'C' or izbor == 'R':
                self.user1 = User(True, 'X')
                self.user2 = User(False, 'O')
                # Postavite prvog igrača prema izboru korisnika
                if izbor == 'C':
                    self.trenutni_igrac = self.user1.oznaka

                elif izbor == 'R':
                    self.trenutni_igrac = self.user2.oznaka

                print(f"self.trenutni_igrac: {self.trenutni_igrac}")

                return self.user1, self.user2
            else:
                print("Pogrešan izbor. Molimo unesite 'C' ili 'R'.")

    def unesi_velicinu_table(self):
        while True:
            try:
                velicina = int(input("Unesite veličinu table (parni broj): "))
                if velicina % 2 == 0:
                    self.trenutno_stanje = HashTable(velicina * velicina)
                    return velicina
                else:
                    print("Veličina table mora biti paran broj.")
            except ValueError:
                print("Pogrešan unos. Molimo unesite ispravan broj.")

    def zapocni_igru(self):
        self.velicina_table = self.unesi_velicinu_table()
        self.tabla = [[' ' for _ in range(self.velicina_table)] for _ in range(self.velicina_table)]
        self.izaberi_ko_prvi_igra()
        return self.velicina_table

    def number_to_letter(self, number):
        ascii_value = ord('a') + number - 1
        letter = chr(ascii_value)
        return letter

    def je_validno_polje(self, polje):
        if polje[0] in string.ascii_uppercase and polje[1:].isdigit():
            return True
        return False

    def je_validno_polje2(self, polje):
        if polje[0] in string.ascii_uppercase and polje[1:].isdigit():
            if self.je_prazno_polje(polje):
                if self.ima_vise_nepraznih_suseda(polje):
                    return False
            return True
        return False

    def je_validna_pozicija_steka(self, pozicija, og):
        p = self.vrati_vrednost(self.letter_to_number(og[0]), int(og[1]))
        if p[8 - int(pozicija)] == self.trenutni_igrac or p[8 - int(pozicija)] == '.':
            if pozicija.isdigit() and 0 <= int(pozicija) <= 7:
                   return True
            else:
                   return False
        else:
            print("To nije vasa figura i ne mozete je pomeriti! Izaberite drugu!")
            return False

    def je_validan_smer(self, smer, pozicija_polja):
        if (smer.upper() in {'GL', 'DL', 'GD', 'DD'}):
            if (self.pozicija_polja.startswith('A')):
                if (smer == 'GL' or smer == 'GD'):
                    return False
            if (self.pozicija_polja.startswith(self.number_to_letter(self.velicina_table))):
                if (smer == 'DL' or smer == 'DD'):
                    return False
            if (self.pozicija_polja.__contains__('1')):
                if (smer == 'GL' or smer == 'DL'):
                    return False
            if (self.pozicija_polja.__contains__(str(self.velicina_table))):
                if (smer == 'GD' or smer == 'DD'):
                    return False
            return True
        else:
            return False

    def je_validan_potez(self, polje, pozicija_steka, smer):
        if not self.je_validno_polje(polje):
            print('Unesli ste neispravno polje.')
            return False
        if not self.je_validna_pozicija_steka(pozicija_steka, polje):
            return False
        if not self.je_validan_smer(smer, polje):
            print("Smer nije validan.")
            return False

    def letter_to_number(self, letter):
        if letter.isalpha() and letter.isupper():
            return ord(letter) - ord('A') + 1
        else:
            return None  # Or handle

    def proveri_susedna_polja(self, pozicija):
        # pozcija je oblika ABCDH 1234
        # to je zapravo u matrici
        i = self.letter_to_number(pozicija[0])
        j = int(pozicija[1])
        element = self.vrati_stanje(i * 10 + j)
        if 0 <= i <= self.velicina_table and 0 <= j <= self.velicina_table:
            dijagonalni_elementi = []
            if i > 0 and j > 0:
                dijagonalni_elementi.append([self.vrati_stanje((i - 1) * 10 + (j - 1)), "GL", ((i - 1) * 10 + (j - 1))])
            if i > 0 and j < self.velicina_table:
                dijagonalni_elementi.append([self.vrati_stanje((i - 1) * 10 + (j + 1)), "GD", ((i - 1) * 10 + (j + 1))])
            if i < self.velicina_table and j > 0:
                dijagonalni_elementi.append([self.vrati_stanje((i + 1) * 10 + (j - 1)), "DL", ((i + 1) * 10 + (j - 1))])
            if i < self.velicina_table and j < self.velicina_table:
                dijagonalni_elementi.append([self.vrati_stanje((i + 1) * 10 + (j + 1)), "DD", ((i + 1) * 10 + (j + 1))])

        list = []
        lista_punih = []
        for polje in dijagonalni_elementi:
            if (polje[0] == "PRAZNO" or polje[0] == deque(['.'] * 9)):
                list.append(polje[1])
            else:
                lista_punih.append(polje)
        return [list, lista_punih]

    def ima_vise_nepraznih_suseda(self, pozicija):
        susedna_polja = self.proveri_susedna_polja(pozicija)
        neprazna_susedna_polja = [sused for sused in susedna_polja[1] if sused[0] != "PRAZNO" and sused[0] != "."]
        if len(neprazna_susedna_polja) + 1 > 0:
            return True
        else:
            return False

    def vrati_pozicije_igraca(self):
        pozicije_i_stekovi_igraca = []

        for i in range(1, self.velicina_table + 1):
            for j in range(1, self.velicina_table + 1):
                pozicija = self.number_to_letter(i) + str(j)
                vrednost_steka = self.vrati_stanje(i * 10 + j)

                if vrednost_steka != "PRAZNO" and self.trenutni_igrac in vrednost_steka:
                    mesto_na_steku = self.nadji_mesto_na_steku(vrednost_steka)
                    pozicije_i_stekovi_igraca.append((pozicija, mesto_na_steku))

        return pozicije_i_stekovi_igraca

    def nadji_mesto_na_steku(self, figura):
        for i, element in enumerate(figura):
            if element == self.trenutni_igrac:
                return i
    def unos_poteza(self):
        self.pozicija_polja = input("Unesite poziciju polja:").upper()
        if self.pozicija_polja=="DALJE":
            return 1
       # print("Ovo su svi moguci potezi, koje mozete odigrati")

      #  pozicije_igraca = self.vrati_pozicije_igraca()

       # for pozicija in pozicije_igraca:
       #   self.potezi.append(self.moguci_potezi_igraca(self.vrati_tablu(), pozicija[0],pozicija[1]))
       # svi = self.pronadji() ovo je ona funkcija visak, sad se sve proverava u sva_moguca_stanja

        moguca_stanja = self.sva_moguca_stanja()



        self.mesto_na_steku = input("Unesite mesto figure na steku:")
        self.smer_pomeranja = input("Unesite smer pomeranja figure:").upper()
        return self.je_validan_potez(self.pozicija_polja, self.mesto_na_steku, self.smer_pomeranja)

    def hashumatricu(self, tabela, matrix_size):
        matrix = [[''] * (matrix_size + 1) for _ in range(matrix_size + 1)]

        for i in range(0, matrix_size + 1):
            for j in range(0, matrix_size + 1):
                value = tabela.get_val(i * 10 + j)
                # Primena deepcopy na vrednost pre nego što je postavite u matricu
                matrix[i][j] = copy.deepcopy(value)


        return matrix
    def print_stack_matrix(self, stack):
        matrix1 = [[0] * 3 for _ in range(3)]
        stack_list = list(stack)
        k = 0;
        for i in range(3):
            for j in range(3):
                if k < len(stack_list):
                    matrix1[i][j] = stack_list[k]
                    k += 1
                else:
                    break
        indeks = len(stack_list) - 1
        if (matrix1[2][2] != 0):
            if stack_list[indeks] not in {'O', 'X', '.'}:
                for _ in range(8):
                    print(' ', end=' ')
                print(matrix1[2][2], end=' ')

            else:
                for row in matrix1:
                    print(' '.join(map(str, row)), end=' ')
        else:
            for _ in range(9):
                print(' ', end=' ')

    def najblizi_element(self):
        i = self.letter_to_number((self.pozicija_polja[0:1]).upper())
        j = int(self.pozicija_polja[1])
        element = self.vrati_stanje(i * 10 + j)
        # u element se nalazi polje koje zelimo da pomerim
        # treba da nadjemo gde je najblizi stek ako su nam pozicije sussedne prazne
        # na onsovu i j izracunamo
        # na primer imam i i j
        listaIpozitivno = []
        for k in range(i +1, self.velicina_table + 1):
            listaIpozitivno.append(k)
        listaInegativno = []
        for k in range(1, i):
            listaInegativno.append(k)
        listaJnegativno = []
        for k in range(1, j):
            listaJnegativno.append(k)
        listaJpozitivno = []
        for k in range(j +1, self.velicina_table + 1):
            listaJpozitivno.append(k)
        listaInegativno = list(reversed(listaInegativno))
        listaJnegativno = list(reversed(listaJnegativno))
        fleg = False
        p = 0
        k = 0
        while (fleg == False):
            najblizi_element = []
            '''          
            if(p == 0):
              element1 = self.vrati_stanje(listaInegativno[p]*10 + listaJnegativno[p])
              element2 = self.vrati_stanje(listaInegativno[p]*10 + listaJpozitivno[p])
              element3 = self.vrati_stanje(listaIpozitivno[p]*10 + listaJpozitivno[p])
              element4 = self.vrati_stanje(listaIpozitivno[p]*10 + listaJnegativno[p])
            '''
            if (p > 0):
                if (len(listaInegativno) < p or len(listaInegativno) == p):
                    indeks2 = 1
                else:
                    indeks2 = listaInegativno[p]
                if (len(listaIpozitivno) < p or len(listaIpozitivno) == p):
                    indeks3 = self.velicina_table
                else:
                    indeks3 = listaIpozitivno[p]

                if (p < len(listaJpozitivno)):
                    for o in range(indeks2, indeks3 + 1):
                        indeks = o * 10 + listaJpozitivno[p]
                        #print(indeks)
                        element = self.vrati_stanje(indeks)
                        if (element != "PRAZNO" and element != deque(['.'] * 9) ):
                            najblizi_element.append([element, indeks, p])
                            fleg = True
                        #print(element)

                if (p < len(listaJnegativno)):
                    for o in range(indeks2, indeks3 + 1):
                        indeks = o * 10 + listaJnegativno[p]
                        element = self.vrati_stanje(indeks)
                        if (element != "PRAZNO" and element != deque(['.'] * 9)):
                            najblizi_element.append([element, indeks, p])
                            fleg = True
                        #print(element)
                        #print(indeks)
                if (len(listaJnegativno) < p or len(listaJnegativno) == p):
                    indeks2 = 1
                else:
                    indeks2 = listaJnegativno[p]
                if (len(listaJpozitivno) < p or len(listaJpozitivno) == p):
                    indeks3 = self.velicina_table
                else:
                    indeks3 = listaJpozitivno[p]

                if (p < len(listaInegativno)):
                    for o in range(indeks2 + 1, indeks3):
                        indeks = listaInegativno[p] * 10 + o
                        element = self.vrati_stanje(indeks)
                        if (element != "PRAZNO" and element != deque(['.'] * 9)):
                            najblizi_element.append([element, indeks, p])
                            fleg = True
                        #print(element)
                        #print(indeks)

                if (p < len(listaIpozitivno)):
                    for o in range(indeks2 + 1, indeks3):
                        indeks = listaIpozitivno[p] * 10 + o
                        element = self.vrati_stanje(indeks)
                        if (element != "PRAZNO" and  element != deque(['.'] * 9)):
                            najblizi_element.append([element, indeks, p])
                            fleg = True
                        #print(element)
                        #print(indeks)
            p = p + 1
        #print(najblizi_element)
        return najblizi_element

    def kreiraj_tablu(self, velicina_table, graf):
        for row in range(1, velicina_table + 1):
            for col in range(1, velicina_table + 1):
                square = f"{chr(96 + col)}{row}"
                graf.add_square(square, self.vrati_stanje(col * 10 + row), square)

    def najkraci_put(self):

        tabla = Chessboard()
        self.kreiraj_tablu(self.velicina_table, tabla)
        tabla.add_diagonal_edges(self.velicina_table)
        #tabla.print_graph()


        start_key = self.pozicija_polja.lower()
        #niz najblizih elemeneata treba da oprodjemo kroz taj
        niz_najblizih = self.najblizi_element()
        listaValidnih = []
        for element in niz_najblizih:
           end_key = element[1]
           slovo = self.number_to_letter(end_key // 10)
           end_key = f"{slovo}{end_key % 10}"
            # vraca mi veci broj obicno je prvi taj koji je dobar
           shortest_paths = tabla.bfs_shortest_paths(start_key, end_key)

           #print(f"Najkraći putevi između {start_key} i {end_key}:")

           for path in shortest_paths:
               listaValidnih.append(path[1])
               #print(path[1])
               #print(" -> ".join(path))
        #print(listaValidnih)
        return  listaValidnih

    def spajanje_praznog_steka(self, polje1, polje2, indeks1, indeks2):
        if polje1.count('.') == 9:
            while '.' in polje2:
                polje2.remove('.')
            while '.' in polje1:
                polje1.remove('.')


            for i in range(int(self.mesto_na_steku), (len(polje2))):
                polje1.appendleft(polje2[i])

            indeks = int(self.mesto_na_steku)

            elementi_od_pocetka_do_mesta = (list(polje1)[indeks:])
            polje1.rotate(-int(self.mesto_na_steku))
            for _ in range(0, len(elementi_od_pocetka_do_mesta)):
                polje2.popleft()



            duzinaPolja1 = len(polje1)
            if (duzinaPolja1 < 9):
                for i in range(0, 9 - duzinaPolja1):
                    polje1.appendleft('.')
            duzinaPolja2 = len(polje2)
            if (duzinaPolja2 < 9):
                for i in range(0, 9 - duzinaPolja2):
                    polje2.appendleft('.')

            self.menjaj_stanje_igre(indeks1, polje1, indeks2, polje2)

    def spajanje_stekova(self, polje1, polje2, indeks1, indeks2):

        kopijaPolja1 =copy.deepcopy(polje1)
        kopijaPolja2 = copy.deepcopy(polje2)
        while '.' in polje1:
            polje1.remove('.')
        while '.' in polje2:
            polje2.remove('.')
        visina_drugog_steka = len(polje2)

        indeks = int(self.mesto_na_steku)
        # pajton koristi indeksiranje od 0
        elementi_od_pocetka_do_mesta = (list(polje1)[indeks:])
        visina_steka_za_premestanje = len(elementi_od_pocetka_do_mesta)
        if (visina_drugog_steka + visina_steka_za_premestanje > 8):
            print("Rezultujuci stek ima vise od 8 elemenata potez nije validan")
        else:
            if (visina_drugog_steka > int(self.mesto_na_steku)):
                for element in reversed(elementi_od_pocetka_do_mesta):
                    polje2.appendleft(element)
                duzinaPolja2 = len(polje2)
                if (duzinaPolja2 < 9):
                    for i in range(0, 9 - duzinaPolja2):
                        polje2.appendleft('.')

                polje1.rotate(-int(self.mesto_na_steku))
                for _ in range(0, len(elementi_od_pocetka_do_mesta)):
                    polje1.popleft()
                duzinaPolja1 = len(polje1)
                if (duzinaPolja1 < 9):
                    for i in range(0, 9 - duzinaPolja1):
                        polje1.appendleft('.')

                self.menjaj_stanje_igre(indeks1, polje1, indeks2, polje2)
                return True
            else:
                polje1 = copy.deepcopy(kopijaPolja1)
                polje2 = copy.deepcopy(kopijaPolja2)
                self.menjaj_stanje_igre(indeks1, polje1, indeks2, polje2)

                return False

    def menjaj_stanje_igre(self, pozicija1, stek1, pozicija2, stek2):
        self.obrisi_stanje(pozicija1)
        self.obrisi_stanje(pozicija2)
        self.dodaj_stanje(pozicija1, stek1)
        self.dodaj_stanje(pozicija2, stek2)

    def nacrtaj_pocetno_stanje(self):
        n = self.velicina_table + 1
        m = self.velicina_table
        self.trenutno_stanje = HashTable(m * m)
        matrix = [[deque(['.'] * 8) for _ in range(n)] for _ in range(n)]
        for j in range(1, n):
            matrix[0][j].append(str(j))
        for i, letter in enumerate(string.ascii_uppercase[:n - 1]):
            matrix[i + 1][0].append(letter)
        for i in range(1, n):
            for j in range(1, n):
                if (i == 1 and j % 2 != 0) or (i == m and j % 2 == 0):
                    matrix[i][j] = deque(['.'] * 9)
                    self.dodaj_stanje(i*10+j, deque(['.'] * 9))
                elif i % 2 == 0 and j % 2 == 0:
                    matrix[i][j].append('X')
                    # user1.dodaj_stanje((i * 10 + j), matrix[i][j])
                    self.dodaj_stanje((i * 10 + j), matrix[i][j])
                elif i % 2 != 0 and j % 2 != 0:
                    matrix[i][j].append('O')
                    # user2.dodaj_stanje((i * 10 + j), matrix[i][j])
                    self.dodaj_stanje((i * 10 + j), matrix[i][j])
        for i in range(n):
            for j in range(n):
                self.print_stack_matrix(matrix[i][j])
            print('\n')
        self.tabla = matrix

    def nacrtaj_trenutno_stanje(self):
        n = self.velicina_table + 1
        matrix = [[deque(['.'] * 8) for _ in range(n)] for _ in range(n)]
        for j in range(1, n):
            matrix[0][j].append(str(j))
        for i, letter in enumerate(string.ascii_uppercase[:n - 1]):
            matrix[i + 1][0].append(letter)
        for i in range(1, n):
            for j in range(1, n):
                if (i + j) % 2 == 0:
                    que1 = self.vrati_stanje(i * 10 + j)
                    if que1 == "PRAZNO" or que1.count('.') == 1 or que1.count('.') == 9:
                        matrix[i][j] = deque(['.'] * 9)
                        self.dodaj_stanje(i*10+j, deque(['.'] * 9))
                    else:
                        matrix[i][j] = que1
        self.tabla = matrix
        for i in range(n):
            for j in range(n):
                self.print_stack_matrix(matrix[i][j])

            print('\n')

    def proveri_kraj_igre(self, user1, user2, polje):  # funkciju pozivamo nakon svakog poteza
        dimenzija = self.velicina_table
        broj_figura = (dimenzija - 2) * dimenzija / 2
        broj_pobednickih_stekova = broj_figura // 8
        # broj stekova koje je svaki igrač složio
        broj_stekova_user1 = user1.broj_slozenih_stekova(polje)
        broj_stekova_user2 = user2.broj_slozenih_stekova(polje)
        if broj_pobednickih_stekova % 2 != 0:
            if broj_stekova_user1 > broj_pobednickih_stekova // 2:
                print("Čestitamo! Pobedio je korisnik 'X'!")
                return True
            if broj_stekova_user2 > broj_pobednickih_stekova // 2:
                print("Čestitamo! Pobedio je korisnik 'Y'!")
                return True

        return False

    def is_tabla_puna(self):
        for i in range(1, self.velicina_table + 1):
            for j in range(1, self.velicina_table + 1):
                if self.matrix[i - 1][j][0] == '.':
                    return False
        return True

    def odigraj_potez(self):
        if self.trenutni_igrac == 'X':
            potez = self.unos_poteza()
            if potez != False:  # Provera da li je unos validan
              if potez != 1:
                susedna_polja = self.proveri_susedna_polja(self.pozicija_polja)
                if len(susedna_polja[0]) == 4 or ((int(self.pozicija_polja[1])) == 8 and len(susedna_polja[0]) == 2):
                    listaValidnih = self.najkraci_put()
                    i = self.letter_to_number(self.pozicija_polja[0])
                    j = int(self.pozicija_polja[1])
                    if self.smer_pomeranja[0] == 'D':
                       i =  i+1
                    else:
                       i =  i-1
                    if self.smer_pomeranja[1] == 'D':
                        j = j+1
                    else:
                       j =  j-1

                    novaPozicija = self.number_to_letter(i) + str(j)
                    if novaPozicija in listaValidnih:
                        slovo, broj = self.pozicija_polja[0].upper(), int(self.pozicija_polja[1:])
                        broj_slova = self.letter_to_number(slovo)
                        indeks1 = broj_slova * 10 + broj
                        indeks2 = self.letter_to_number(novaPozicija[0].upper())*10 + int(novaPozicija[1])
                        vrednsot_steka1 = self.vrati_stanje(indeks1)
                        vrednost_steka2 = self.vrati_stanje(indeks2)
                        if vrednsot_steka1 == deque(['.'] * 9):
                             self.spajanje_praznog_steka(vrednsot_steka1, vrednost_steka2, indeks1, indeks2)
                        else:
                             self.spajanje_praznog_steka(vrednost_steka2, vrednsot_steka1, indeks2, indeks1)

                    else:
                        print("potez nije validan, validna polja da se odigra potez su" + str(listaValidnih))

                else:
                    zauzeta_polja = susedna_polja[1]
                    for polje in zauzeta_polja:
                        if polje[1] == self.smer_pomeranja:
                            slovo, broj = self.pozicija_polja[0].upper(), int(self.pozicija_polja[1:])
                            broj_slova = self.letter_to_number(slovo)
                            indeks1 = broj_slova * 10 + broj
                            indeks2 = polje[2]
                            vrednsot_steka1 = self.vrati_stanje(indeks1)
                            vrednost_steka2 = self.vrati_stanje(indeks2)
                            rezultat = self.spajanje_stekova(vrednsot_steka1, vrednost_steka2, indeks1, indeks2)
                            if rezultat is False:
                                print("Odigrajte novi potez")
                                self.odigraj_potez()
                                return
                            self.trenutni_igrac = 'X' if self.trenutni_igrac == 'O' else 'O'

                            #self.prikazi_stanje_igre()
                            return
              else:
                  self.trenutni_igrac = 'X' if self.trenutni_igrac == 'O' else 'O'
                  return

            else:
                print("Molimo unesite ispravan potez")
                self.odigraj_potez()
        else:
            stanje = copy.deepcopy(self.trenutno_stanje)
            self.matrica = self.hashumatricu(stanje, self.velicina_table)
            potez_racunara = self.odaberi_najbolji_potez('O', stanje)
            polje_odakle=potez_racunara[2]
            polje_gde=potez_racunara[0]

            slovo, broj = polje_odakle[0].upper(), int(polje_odakle[1:])
            broj_slova = self.letter_to_number(slovo)
            indeks1 = broj_slova * 10 + broj

            slovo, broj = polje_gde[0].upper(), int(polje_gde[1:])
            broj_slova = self.letter_to_number(slovo)
            indeks2 = broj_slova * 10 + broj
            vrednsot_steka1 = self.vrati_stanje(indeks1)
            vrednost_steka2 = self.vrati_stanje(indeks2)
            self.spajanje_stekova(vrednost_steka2 , vrednsot_steka1, indeks2, indeks1)
            self.trenutni_igrac = 'X' if self.trenutni_igrac == 'O' else 'O'
            #self.prikazi_stanje_igre()
            return
    '''
    def evaluate_board(self, board, player):
        # Broj stekova u vlasništvu igrača
        broj_stekova_igraca = 0
        for row in board:
            for cell in row:
                if cell == player:
                    broj_stekova_igraca += 1

        # Ukupna vrednost stekova igrača
        vrednost_stekova_igraca = 0
        for row in board:
            for cell in row:
                if cell == player:
                    vrednost_stekova_igraca += len(row) - row.index(cell)  # Vrednost figure na steku

        return broj_stekova_igraca * 10 + vrednost_stekova_igraca  # Ponderisana vrednost
    '''

    def evaluate_board(self, board, player):
        # Inicijalizacija činjenica koje opisuju trenutno stanje igre
        facts = {
            "BrojStekova": 0,
            "VrednostStekova": 0,
            "IgracImaViseStekova": False,
            "IgracImaVisokuVrednostStekova": False
        }

        # Prolazak kroz tablu i računanje broja figurica i ukupne vrednosti stekova igrača
        for row in board:
            for cell in row:
                for x in cell:
                   if x == player:
                      facts["BrojStekova"] += 1
                      facts["VrednostStekova"] += len(row) - row.index(cell)

        # Izvršavanje mehanizma zaključivanja
        self.inference_engine.infer(facts)

        # Proučavanje zaključaka i ažuriranje vrednosti stanja prema potrebi
        self.vrednost_stanja = facts["BrojStekova"] * 10 + facts["VrednostStekova"]

        if facts["IgracImaViseStekova"]:
            # Dodajte odgovarajući uticaj na vrednost stanja
            self.vrednost_stanja += 3 # Prilagodite NEKA_VREDNOST1 prema vašim potrebama

        if facts["IgracImaVisokuVrednostStekova"]:
            # Dodajte odgovarajući uticaj na vrednost stanja
            self.vrednost_stanja += 4  # Prilagodite NEKA_VREDNOST2 prema vašim potrebama

        # Vraćanje ažurirane vrednosti stanja
        return self.vrednost_stanja

    def pravilo_broj_stekova(self, facts):
        if "BrojStekova" in facts:
            broj_stekova = int(facts["BrojStekova"])
            return broj_stekova >= 1
        return False

    def pravilo_vrednost_stekova(self, facts):
        if "VrednostStekova" in facts:
            vrednost_stekova = int(facts["VrednostStekova"])
            return vrednost_stekova >= 3
        return False

    def odaberi_najbolji_potez(self, igrac, tabla):
        najbolji_potez = None
        vrednost_najboljeg_poteza = float('-inf') if igrac == 'O' else float('inf')

        # Generisi dubinu pretraživanja na osnovu veličine table
        dubina = self.generisi_dubinu_pretrazivanja()

        pozicije_igraca = self.vrati_pozicije_igraca()

        for pozicija in pozicije_igraca:
            moguci_potezi = self.moguci_potezi_igraca(self.vrati_tablu(), pozicija[0], pozicija[1])
            for potez in moguci_potezi:
                # Ispravljen poziv funkcije:
                self.pozicija_polja=potez[2]
                novo_stanje = self.novo_stanje_na_osnovu_poteza( potez[0])
                vrednost_poteza = self.minimax_alphabeta(novo_stanje, dubina - 1, not igrac == 'O', float('-inf'),float('inf'))

                if igrac == 'O' and vrednost_poteza > vrednost_najboljeg_poteza:
                    vrednost_najboljeg_poteza = vrednost_poteza
                    najbolji_potez = potez
                elif igrac == 'X' and vrednost_poteza < vrednost_najboljeg_poteza:
                    vrednost_najboljeg_poteza = vrednost_poteza
                    najbolji_potez = potez

        return najbolji_potez

    def minimax_alphabeta(self, node, depth, maximizing_player, alpha, beta):
        if depth == 0:
            return self.evaluate_board(node, 'O')

        pozicije_igraca = self.vrati_pozicije_igraca()

        for pozicija in pozicije_igraca:
            moguci_potezi = self.moguci_potezi_igraca(node, pozicija[0], pozicija[1])

            if maximizing_player:
                max_eval = float('-inf')
                for child_state in moguci_potezi:
                    self.pozicija_polja = child_state[2]
                    novo_stanje = self.novo_stanje_na_osnovu_poteza(child_state[0])
                    eval = self.minimax_alphabeta(novo_stanje, depth - 1, False, alpha, beta)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return max_eval
            else:
                min_eval = float('inf')
                for child_state in moguci_potezi:
                    self.pozicija_polja = child_state[2]
                    novo_stanje = self.novo_stanje_na_osnovu_poteza(child_state[0])
                    eval = self.minimax_alphabeta(novo_stanje, depth - 1, True, alpha, beta)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval

    def generisi_dubinu_pretrazivanja(self):
        if self.velicina_table <= 8:
            return 4
        elif self.velicina_table <= 10:
            return 3
        else:
            return 2

    def prikazi_stanje_igre(self):
        print("Trenutno stanje igre:")
        self.nacrtaj_trenutno_stanje()
        print(f"Na potezu je {self.igraci[self.trenutni_igrac]}")

    def moguci_potezi_igraca(self, tabla, lokacijaIgraca,stek):
        moguci_potezi = []
        i = self.letter_to_number(lokacijaIgraca[0].upper())
        j = int(lokacijaIgraca[1])
        potezi_za_poziciju = self.pronadji_moguce_poteze(tabla, (i, j),stek)
        moguci_potezi.extend([(lokacijaIgraca, 0, potez[0] + str(potez[1])) for potez in potezi_za_poziciju])
      #  for potez in moguci_potezi:
        #    print(potez)
        return moguci_potezi

    def vrati_vrednost(self, i, j):
        cell_value = self.vrati_stanje(i * 10 + j)
        if cell_value == "PRAZNO":
            return ['.'] * 9
        else:
            return cell_value

    #ovde treba da dodamo poteze kad su svi susedi prazni
    def pronadji_moguce_poteze(self, tabla, pozicija, stek):
        #ovo treba da se promeni kad su svi susedi prazni sta se onda radi
        moguci_potezi = []
        x, y = pozicija
        if pozicija is not None:
            susedi = []
            for sused in self.pronadji_susede(tabla, pozicija,stek):
               susedi.append(sused)
               if sused is not None:
                  sused_x, sused_y = sused
                  moguci_potezi.append((self.number_to_letter(sused_x).upper(), sused_y))

            if all(element is None for element in susedi):

               self.pozicija_polja=self.number_to_letter(pozicija[0])+str(pozicija[1])
               Putevi=self.najkraci_put()
               for mesto in Putevi:
                 moguci_potezi.append((mesto[0],mesto[1]))

            return moguci_potezi
        else:
            return moguci_potezi

    def pronadji_susede(self, tabla, pozicija, stek):
        susedi = []
        a, b = pozicija
        x = int(a)
        y = int(b)

        koraci = [(-1, -1, "gl"), (-1, 1, "gd"), (1, -1, "dl"), (1, 1, "dd")]

        if x >= self.velicina_table:
            koraci = [k for k in koraci if "d" not in k[2]]

        if x <= 1:
            koraci = [k for k in koraci if "g" not in k[2]]

        if y <= 1:
            koraci = [k for k in koraci if
                      "l" not in k[2]]

        if y >= self.velicina_table:
            koraci = [k for k in koraci if
                      "d" not in k[2]]

        # Dijagonalna kretanja
        for korak in koraci:
            sused_x, sused_y = x + korak[0], y + korak[1]
            pozicija_sused = self.number_to_letter(sused_x).upper() + str(sused_y)
            p = self.vrati_vrednost(sused_x, sused_y)
            broj_figura_zaprenos = self.broj_nepraznih_polja(x, y, stek)
            broj_tacaka = p.count('.')
            og = self.number_to_letter(x).upper() + str(y)
            if self.validan_sused(pozicija_sused, str(broj_tacaka - 1), korak[2], og, broj_figura_zaprenos):
                susedi.append((sused_x, sused_y))

        return susedi

    def broj_nepraznih_polja(self, x, y, stek):
        count_nepraznih = 0
        m = self.vrati_vrednost(x, y)
        for i in range(stek, -1, -1):
            if m[i] != ".":
                count_nepraznih += 1

        return count_nepraznih

    def postavi_moguce_stanje(self,  pozicija_postavljanja):
        slovo, broj = self.pozicija_polja[0].upper(), int(self.pozicija_polja[1:])
        broj_slova = self.letter_to_number(slovo)
        indeks1 = broj_slova * 10 + broj
        slovo, broj = pozicija_postavljanja[0].upper(), int(pozicija_postavljanja[1:])
        broj_slova = self.letter_to_number(slovo)
        broj_slova = self.letter_to_number(slovo)
        indeks2 = broj_slova * 10 + broj
        vrednost_steka1 = copy.deepcopy(self.vrati_stanje(indeks1))
        vrednost_steka2 = copy.deepcopy(self.vrati_stanje(indeks2))
        matrica = self.spajanje_stekova3( vrednost_steka1, vrednost_steka2, indeks1, indeks2)

        return matrica



    def spajanje_stekova3(self, polje1, polje2, indeks1, indeks2):
        while '.' in polje1:
            polje1.remove('.')
        while '.' in polje2:
            polje2.remove('.')
        visina_drugog_steka = len(polje2)

        indeks = int(self.mesto_na_steku)
        # pajton koristi indeksiranje od 0
        elementi_od_pocetka_do_mesta = (list(polje1)[indeks:])
        visina_steka_za_premestanje = len(elementi_od_pocetka_do_mesta)
        if (visina_drugog_steka + visina_steka_za_premestanje > 8):
            print("Rezultujuci stek ima vise od 8 elemenata potez nije validan")
        else:
            if (visina_drugog_steka > int(self.mesto_na_steku)):
                for element in reversed(elementi_od_pocetka_do_mesta):
                    polje2.appendleft(element)
                duzinaPolja2 = len(polje2)
                if (duzinaPolja2 < 9):
                    for i in range(0, 9 - duzinaPolja2):
                        polje2.appendleft('.')

                polje1.rotate(-int(self.mesto_na_steku))
                for _ in range(0, len(elementi_od_pocetka_do_mesta)):
                    polje1.popleft()
                duzinaPolja1 = len(polje1)
                if (duzinaPolja1 < 9):
                    for i in range(0, 9 - duzinaPolja1):
                        polje1.appendleft('.')

                trenutno_stanje1 = self.menjaj_stanje_igre2(indeks1, polje1, indeks2, polje2)

                return trenutno_stanje1
            else:
                 print("Potez ne moze da se odigra, nije validan")
                 return None
    def novo_stanje_na_osnovu_poteza(self, pozicija_postavljanja):

        novo_stanje = self.postavi_moguce_stanje(  pozicija_postavljanja)

        return novo_stanje

    def sva_moguca_stanja(self):
        nova_stanja = []
        stanje = copy.deepcopy(self.trenutno_stanje)
        for potezi_za_poziciju in self.potezi:
            for potez in potezi_za_poziciju:
                self.matrica = self.hashumatricu(stanje,self.velicina_table)
                novo_stanje = self.novo_stanje_na_osnovu_poteza( potez[2])
                #print('------------------------------------------------------------------------------------------OPCIJA-------------------------------------------------------------------------')
                #self.odstampaj_moguce_stanje(novo_stanje)
                nova_stanja.append(novo_stanje)


        return nova_stanja

    def je_prazno_polje(self, pozicija):
        p = self.vrati_vrednost(self.letter_to_number(pozicija[0]), int(pozicija[1]))
        count = p.count('.')
        if count == 9:
            return True
        else:
            return False

    def validan_sused(self, polje_gde, pozicija_gde, smer,polje_odakle,koliko_prenos):
        if not self.je_validno_polje2(polje_gde):
            return False
        if not self.je_validna_pozicija_steka2(polje_gde,pozicija_gde,koliko_prenos):
            return False
        if not self.je_validan_smer(smer, polje_odakle):
            return False
        return True

    # funkcije za prikaz mogucih stanja
    def je_validna_pozicija_steka2(self,polje_gde,pozicija_gde,koliko_prenos):
        p = self.vrati_vrednost(self.letter_to_number(polje_gde[0]), int(polje_gde[1]))
        if p[int(pozicija_gde)] == '.':
            if pozicija_gde.isdigit() and 0 <= int(pozicija_gde) <= 7:
                if p.count('.')-1 >= int(koliko_prenos):
                    return True
            else:
                return False
        else:
            return False

    def vrati_stanje2(self, broj, trenutno_stanje):
        return trenutno_stanje[broj//10][broj%10]

    def obrisi_stanje2(self, broj, trenutno_stanje):
        #nije hash nego je matrica
        return trenutno_stanje[broj[0]][broj[1]]
        #trenutno_stanje.delete_val(broj)

    def vrati_tablu2(self, trenutno_stanje):
        return trenutno_stanje

    def dodaj_stanje2(self, broj, stek, trenutno_stanje):
        trenutno_stanje.set_val(broj, stek)
        return trenutno_stanje

    def update_stanje(self, broj, vrednost):
         self.matrica[broj//10][broj%10] = vrednost
         return self.matrica

    def set_val(self, broj, stek, trenutno_stanje):
        matrix_size = len(trenutno_stanje)
        row = broj // matrix_size
        col = broj % matrix_size
        trenutno_stanje[row][col] = stek

    def delete_val(self, broj, trenutno_stanje):
        matrix_size = len(trenutno_stanje)  # Assuming trenutno_stanje is a matrix
        row = broj // matrix_size
        col = broj % matrix_size
        trenutno_stanje[row][col] = ''
    def menjaj_stanje_igre2(self, pozicija1, stek1, pozicija2, stek2):
        self.update_stanje(pozicija1, stek1)
        self.update_stanje(pozicija2, stek2)
        return self.matrica

    def pronadji(self):

        svi = []
        for i in range(0, self.velicina_table + 1):
            for j in range(0, self.velicina_table + 1):
                if (i + j) % 2 == 0:
                    vrednost = self.vrati_stanje(i * 10 + j)
                    br = 0
                    for l in vrednost:
                        if l == self.trenutni_igrac:
                            mesto = {
                                'red': i,
                                'kolona': j,
                                'pozicija_u_steku': 8 - br
                            }
                            svi.append(mesto)
                        br = br + 1
        return svi

    def odstampaj_moguce_stanje(self,matrica):


        n = self.velicina_table + 1

        matrix = [[deque(['.'] * 8) for _ in range(n)] for _ in range(n)]

        for j in range(1, n):
            matrix[0][j].append(str(j))
        for i, letter in enumerate(string.ascii_uppercase[:n - 1]):
            matrix[i + 1][0].append(letter)

        for i in range(1, n):
            for j in range(1, n):
                if (i + j) % 2 == 0:
                     que1 =matrica[i][j]
                     if que1.count('.') == 1:
                        self.update_stanje(i*10+j , deque([]))
                        matrix[i][j] = deque(['.'] * 9)
                     elif que1 == "PRAZNO" or que1 == deque([]):
                         matrix[i][j] = deque(['.'] * 9)
                     else:
                        matrix[i][j] = que1
        self.tabla = matrix
        for i in range(n):
            for j in range(n):
                self.print_stack_matrix(matrix[i][j])

            print('\n')