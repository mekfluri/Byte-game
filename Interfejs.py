import copy
import string
from collections import deque
from Graph import Chessboard
from HashTable import HashTable
from User import User

INFINITY = float('inf')
NEG_INFINITY = float('-inf')


class Interfejs:
    def __init__(self):
        self.velicina_table = 0
        self.trenutni_igrac = ''
        self.tabla = None
        self.igraci = {'X': 'Čovek 1', 'O': 'Čovek 2'}
        # da se pametne trenutna stanja
        self.trenutno_stanje = HashTable(1)
        self.pozicija_polja = ''
        self.smer_pomeranja = ''
        self.mesto_na_steku = 0
        self.user1 = None
        self.user2 = None
        self.potezi = deque()
        self.matrica= []

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
            izbor = input("Ko će igrati prvi? Unesite 'C1' za Čoveka 1 ili 'C2' za Čoveka 2: ").upper()
            if izbor == 'C1' or izbor == 'C2':
                self.user1 = User(True, 'X')
                self.user2 = User(False, 'O')
                # Postavite prvog igrača prema izboru korisnika
                if izbor == 'C1':
                    self.trenutni_igrac = self.user1.oznaka

                elif izbor == 'C2':
                    self.trenutni_igrac = self.user2.oznaka

                print(f"self.trenutni_igrac: {self.trenutni_igrac}")

                return self.user1, self.user2
            else:
                print("Pogrešan izbor. Molimo unesite 'C1' ili 'C2'.")

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
        if p[int(pozicija)] == self.trenutni_igrac or p[int(pozicija)] == '.':
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
            if (polje[0] == "PRAZNO"):
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

    def unos_poteza(self):
        self.pozicija_polja = input("Unesite poziciju polja:").upper()
        print("Ovo su svi moguci potezi, koje mozete odigrati")
        self.potezi = self.moguci_potezi_igraca(self.vrati_tablu(), self.pozicija_polja)

        moguca_stanja = self.sva_moguca_stanja()
        for stanje in moguca_stanja:
            self.odstampaj_moguce_stanje(stanje)
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
                print(f'Tabela[{i * 10 + j}] = {value}')

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
        i = self.letter_to_number(self.pozicija_polja[0])
        j = int(self.pozicija_polja[1])
        element = self.vrati_stanje(i * 10 + j)
        # u element se nalazi polje koje zelimo da pomerim
        # treba da nadjemo gde je najblizi stek ako su nam pozicije sussedne prazne
        # na onsovu i j izracunamo
        # na primer imam i i j
        listaIpozitivno = []
        for k in range(i + 1, self.velicina_table + 1):
            listaIpozitivno.append(k)
        listaInegativno = []
        for k in range(1, i):
            listaInegativno.append(k)
        listaJnegativno = []
        for k in range(1, j):
            listaJnegativno.append(k)
        listaJpozitivno = []
        for k in range(j + 1, self.velicina_table + 1):
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
                        print(indeks)
                        element = self.vrati_stanje(indeks)
                        if (element != "PRAZNO"):
                            najblizi_element.append([element, indeks, p])
                            fleg = True
                        print(element)

                if (p < len(listaJnegativno)):
                    for o in range(indeks2, indeks3 + 1):
                        indeks = o * 10 + listaJnegativno[p]
                        element = self.vrati_stanje(indeks)
                        if (element != "PRAZNO"):
                            najblizi_element.append([element, indeks, p])
                            fleg = True
                        print(element)
                        print(indeks)
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
                        if (element != "PRAZNO"):
                            najblizi_element.append([element, indeks, p])
                            fleg = True
                        print(element)
                        print(indeks)

                if (p < len(listaIpozitivno)):
                    for o in range(indeks2 + 1, indeks3):
                        indeks = listaIpozitivno[p] * 10 + o
                        element = self.vrati_stanje(indeks)
                        if (element != "PRAZNO"):
                            najblizi_element.append([element, indeks, p])
                            fleg = True
                        print(element)
                        print(indeks)
            p = p + 1
        print(najblizi_element)
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
        tabla.print_graph()
        self.unos_poteza()
        start_key = self.pozicija_polja.lower()
        niz_najblizih = self.najblizi_element()
        end_key = niz_najblizih[0][1]
        slovo = self.number_to_letter(end_key // 10)
        end_key = f"{slovo}{end_key % 10}"
        # vraca mi veci broj obicno je prvi taj koji je dobar
        shortest_paths = tabla.bfs_shortest_paths(start_key, end_key)

        print(f"Najkraći putevi između {start_key} i {end_key}:")
        for path in shortest_paths:
            print(" -> ".join(path))

    def spajanje_stekova(self, polje1, polje2, indeks1, indeks2):
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
                print(polje2)
                polje1.rotate(-int(self.mesto_na_steku))
                for _ in range(0, len(elementi_od_pocetka_do_mesta)):
                    polje1.popleft()
                duzinaPolja1 = len(polje1)
                if (duzinaPolja1 < 9):
                    for i in range(0, 9 - duzinaPolja1):
                        polje1.appendleft('.')
                print(polje1)
                self.menjaj_stanje_igre(indeks1, polje1, indeks2, polje2)
            else:
                print("Potez ne moze da se odigra, nije validan")

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
                    if que1 == "PRAZNO":
                        matrix[i][j] = deque(['.'] * 9)
                    else:
                        matrix[i][j] = que1
        #self.tabla = matrix
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
        if (self.unos_poteza() != False):  # Provera da li je unos validan
            susedna_polja = self.proveri_susedna_polja(self.pozicija_polja)
            if len(susedna_polja[0]) == 4:
                print("Sva polja susedna su prazna")
            else:
                zauzeta_polja = susedna_polja[1]
                for polje in zauzeta_polja:
                    if polje[1] == self.smer_pomeranja:
                        print("Potez je validan")
                        slovo, broj = self.pozicija_polja[0].upper(), int(self.pozicija_polja[1:])
                        broj_slova = self.letter_to_number(slovo)
                        indeks1 = broj_slova * 10 + broj
                        indeks2 = polje[2]
                        vrednsot_steka1 = self.vrati_stanje2(indeks1)
                        vrednost_steka2 = self.vrati_stanje2(indeks2)
                        self.spajanje_stekova(vrednsot_steka1, vrednost_steka2, indeks1, indeks2)
                        self.trenutni_igrac = 'X' if self.trenutni_igrac == 'O' else 'O'
                        self.prikazi_stanje_igre()
                        return
        else:
            print("Molimo unesite ispravan potez")
            self.odigraj_potez()

    def prikazi_stanje_igre(self):
        print("Trenutno stanje igre:")
        self.nacrtaj_trenutno_stanje()
        print(f"Na potezu je {self.igraci[self.trenutni_igrac]}")

    def moguci_potezi_igraca(self, tabla, lokacijaIgraca):
        moguci_potezi = []
        i = self.letter_to_number(lokacijaIgraca[0])
        j = lokacijaIgraca[1]
        potezi_za_poziciju = self.pronadji_moguce_poteze(tabla, (i, j))
        moguci_potezi.extend([(lokacijaIgraca, 0, potez[0] + str(potez[1])) for potez in potezi_za_poziciju])
        for potez in moguci_potezi:
            print(potez)
        return moguci_potezi

    def vrati_vrednost(self, i, j):
        cell_value = self.vrati_stanje(i * 10 + j)
        if cell_value == "PRAZNO":
            return ['.'] * 9
        else:
            return cell_value

    def pronadji_moguce_poteze(self, tabla, pozicija):
        moguci_potezi = []
        x, y = pozicija
        for sused in self.pronadji_susede(tabla, pozicija):
            sused_x, sused_y = sused
            moguci_potezi.append((self.number_to_letter(sused_x).upper(), sused_y))
        return moguci_potezi

    def pronadji_susede(self, tabla, pozicija):
        susedi = []
        a, b = pozicija
        x = int(a)
        y = int(b)
        koraci = [(-1, -1, "gl"), (-1, 1, "gd"), (1, -1, "dl"), (1, 1, "dd")]  # Dijagonalna kretanja sa smerom
        # Dijagonalna kretanja
        for korak in koraci:
            sused_x, sused_y = x + korak[0], y + korak[1]
            pozicija = self.number_to_letter(sused_x).upper() + str(sused_y)
            p = self.vrati_vrednost(sused_x, sused_y)
            broj_tacaka = p.count('.')
            og = self.number_to_letter(x).upper() + str(y)
            if self.validan_sused(pozicija, str(broj_tacaka - 2), korak[2], og):
                susedi.append((sused_x, sused_y))
        return susedi

    def postavi_moguce_stanje(self, mesto_na_steku, pozicija_postavljanja):
        slovo, broj = self.pozicija_polja[0].upper(), int(self.pozicija_polja[1:])
        broj_slova = self.letter_to_number(slovo)
        indeks1 = broj_slova * 10 + broj
        slovo, broj = pozicija_postavljanja[0].upper(), int(pozicija_postavljanja[1:])
        broj_slova = self.letter_to_number(slovo)
        indeks2 = broj_slova * 10 + broj
        vrednost_steka1 = copy.deepcopy(self.vrati_stanje(indeks1))
        vrednost_steka2 = copy.deepcopy(self.vrati_stanje(indeks2))
        matrica = self.spajanje_stekova3( vrednost_steka1, vrednost_steka2, indeks1, indeks2)
        print("postavi moguce stanje")
        self.nacrtaj_trenutno_stanje()
        return matrica

    def spajanje_stekova2(self, polje1, polje2, indeks1, indeks2, trenutno_stanje):
        matrix_size = len(trenutno_stanje)  # Assuming trenutno_stanje is a matrix
        row1, col1 = indeks1 // matrix_size, indeks1 % matrix_size
        row2, col2 = indeks2 // matrix_size, indeks2 % matrix_size

        while '.' in polje1:
            polje1.remove('.')
        while '.' in polje2:
            polje2.remove('.')

        visina_drugog_steka = len(polje2)
        indeks = int(self.mesto_na_steku)

        # Ensure indeks is an integer
        indeks = int(indeks)

        # Pajton koristi indeksiranje od 0
        elementi_od_pocetka_do_mesta = list(polje1)[indeks:]

        visina_steka_za_premestanje = len(elementi_od_pocetka_do_mesta)

        if (visina_drugog_steka + visina_steka_za_premestanje > 8):
            print("Rezultujuci stek ima vise od 8 elemenata potez nije validan")
        else:
            if (visina_drugog_steka > int(self.mesto_na_steku)):
                for i, element in enumerate(reversed(elementi_od_pocetka_do_mesta)):
                    row = row2 + i
                    trenutno_stanje[row][col2] = element

                duzinaPolja2 = len(polje2)
                if duzinaPolja2 < 8:
                    for i in range(0, 8 - duzinaPolja2):
                        new_row = row2 + i + len(elementi_od_pocetka_do_mesta)
                        if new_row < 8:  # Make sure not to exceed the valid row index
                            trenutno_stanje[new_row][col2] = '.'

                print(trenutno_stanje)

                for i in range(len(elementi_od_pocetka_do_mesta)):
                    row = row1 + i
                    trenutno_stanje[row][col1] = '.'

                duzinaPolja1 = len(polje1)
                if duzinaPolja1 < 8:  # Assuming the matrix has 8 rows
                    for i in range(0, 8 - duzinaPolja1):
                        new_row = row1 + i + len(elementi_od_pocetka_do_mesta)
                        if new_row < 8:
                            trenutno_stanje[new_row][col1] = '.'

                print(trenutno_stanje)

                return trenutno_stanje
            else:
                print("Potez ne moze da se odigra, nije validan")

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
                print(polje2)
                polje1.rotate(-int(self.mesto_na_steku))
                for _ in range(0, len(elementi_od_pocetka_do_mesta)):
                    polje1.popleft()
                duzinaPolja1 = len(polje1)
                if (duzinaPolja1 < 9):
                    for i in range(0, 9 - duzinaPolja1):
                        polje1.appendleft('.')
                print(polje1)
                trenutno_stanje1 = self.menjaj_stanje_igre2(indeks1, polje1, indeks2, polje2)
                print("spajanje stekova")
                self.nacrtaj_trenutno_stanje()
                return trenutno_stanje1
            else:
                 print("Potez ne moze da se odigra, nije validan")
                 return None
    def novo_stanje_na_osnovu_poteza(self, pozicija, mesto_na_steku, pozicija_postavljanja):

        novo_stanje = self.postavi_moguce_stanje( mesto_na_steku, pozicija_postavljanja)
        print("novo stanje")
        self.nacrtaj_trenutno_stanje()
        return novo_stanje

    def sva_moguca_stanja(self):
        nova_stanja = []
        stanje = copy.deepcopy(self.trenutno_stanje)
        for potez in self.potezi:
            self.matrica = self.hashumatricu(stanje,self.velicina_table)
            self.nacrtaj_trenutno_stanje()
            print("stampam matricu")
            for red in self.matrica:
                for element in red:
                  print(element, end=" ")  # Koristimo end=" " da bismo razdvojili elemente u istom redu
                print()  # Prelazi
            novo_stanje = self.novo_stanje_na_osnovu_poteza(potez[0], potez[1], potez[2])
            for red in novo_stanje:
                for element in red:
                    print(element, end=" ")  # Koristimo end=" " da bismo razdvojili elemente u istom redu
                print()  # Prelazi
            nova_stanja.append(novo_stanje)
            print("sva moguca stanja")
            self.nacrtaj_trenutno_stanje()

        return nova_stanja

    def je_prazno_polje(self, pozicija):
        p = self.vrati_vrednost(self.letter_to_number(pozicija[0]), int(pozicija[1]))
        count = p.count('.')
        if count == 9:
            return True
        else:
            return False

    def validan_sused(self, polje, pozicija_steka, smer, og):
        if not self.je_validno_polje2(polje):
            return False
        if not self.je_validna_pozicija_steka2(pozicija_steka, og):
            return False
        if not self.je_validan_smer(smer, og):
            return False
        return True

    # funkcije za prikaz mogucih stanja
    def je_validna_pozicija_steka2(self, pozicija, og):
        p = self.vrati_vrednost(self.letter_to_number(og[0]), int(og[1]))
        if p[int(pozicija)] == self.trenutni_igrac or p[int(pozicija)] == '.':
            if pozicija.isdigit() and 0 <= int(pozicija) <= 7:
                if 9 - p.count('.') <= int(pozicija):
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
        print("update")
        self.nacrtaj_trenutno_stanje()
        return self.matrica[broj//10][broj%10] == vrednost

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
        print("menjaj stanje")
        self.nacrtaj_trenutno_stanje()
        return self.matrica






    def odstampaj_moguce_stanje(self, matrica):
        print("EVO")
        print(matrica)
