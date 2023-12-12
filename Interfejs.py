import string
from collections import deque

from Graph import Chessboard
from HashTable import HashTable

from User import User


class Interfejs:
    def __init__(self):
        self.velicina_table = 0
        self.trenutni_igrac = ''
        self.tabla = None
        self.igraci = {'X': 'Čovek', 'O': 'Računar'}
        #da se pametne trenutna stanja
        self.trenutno_stanje = HashTable(1)
        self.pozicija_polja = ''
        self.smer_pomeranja = ''
        self.mesto_na_steku = 0


    def dodaj_stanje(self, broj, stek):
        self.trenutno_stanje.set_val(broj, stek)

    def vrati_stanje(self, broj):
        return self.trenutno_stanje.get_val(broj)

    def obrisi_stanje(self, broj):
        self.trenutno_stanje.delete_val(broj)
    def izaberi_ko_prvi_igra(self):
        while True:
            izbor = input("Ko će igrati prvi? Unesite 'C' za Čoveka ili 'R' za Računar: ").upper()
            if izbor == 'C':
                return 'X', 'O'
            elif izbor == 'R':
                return 'O', 'X'
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
        prvi_igrac, drugi_igrac = self.izaberi_ko_prvi_igra()
        self.trenutni_igrac = prvi_igrac

        print(f"{self.igraci[self.trenutni_igrac]} igra prvi!")
        user1 = User(self.velicina_table * self.velicina_table)
        user2 = User(self.velicina_table * self.velicina_table)
        self.nacrtaj_pocetno_stanje()
        return self.velicina_table


    def number_to_letter(self, number):

        ascii_value = ord('a') + number - 1
        letter = chr(ascii_value)

        return letter

    def je_validno_polje(self, polje):
        if polje[0] in string.ascii_uppercase and polje[1:].isdigit():
            return True
        else:
            return False
    def je_validna_pozicija_steka(self, pozicija):
       if(pozicija.isdigit() and 1 <= int(pozicija) <= 8):
           return True
       else:
           return False

    def je_validan_smer(self, smer):
        if(smer.upper() in {'GL', 'DL', 'GD', 'DD'}):
            return True
        else:
            return False

    def je_validan_potez(self, polje , pozicija_steka, smer):


        if not self.je_validno_polje(polje):
            print('Unesli ste neispravno polje.')
            return False


        if not self.je_validna_pozicija_steka(pozicija_steka):
            print('Pozicija stek nije validna.')
            return False

        if not self.je_validan_smer(smer):
            print("Smer nije validna.")
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
        if 0 <= i < self.velicina_table and 0 <= j < self.velicina_table:
            dijagonalni_elementi = []

            if i > 0 and j > 0:
                dijagonalni_elementi.append([self.vrati_stanje((i - 1) * 10 + (j - 1)), "DL",((i - 1) * 10 + (j - 1))])
            if i > 0 and j < self.velicina_table - 1:
                dijagonalni_elementi.append([self.vrati_stanje((i - 1) * 10 + (j + 1)), "DD", ((i - 1) * 10 + (j + 1))])
            if i < self.velicina_table - 1 and j > 0:
                dijagonalni_elementi.append([self.vrati_stanje((i + 1) * 10 + (j - 1)), "GL", ((i + 1) * 10 + (j - 1))])
            if i < self.velicina_table - 1 and j < self.velicina_table - 1:
                dijagonalni_elementi.append([self.vrati_stanje((i + 1) * 10 + (j + 1)), "GD", ((i + 1) * 10 + (j + 1))])

        print(dijagonalni_elementi)
        list = []
        lista_punih = []
        for polje in dijagonalni_elementi:
            if(polje[0] == "PRAZNO"):
                print("Prazno polje" + " " + polje[1])
                list.append(polje[1])
            else:
                lista_punih.append(polje)
        return [list, lista_punih]



    def unos_poteza(self):

        self.pozicija_polja = input("Unesite poziciju polja").upper()
        self.mesto_na_steku = input("Unesite mesto figure na steku")
        self.smer_pomeranja = input("Unesite smer pomeranja figure").upper()

        self.proveri_susedna_polja(self.pozicija_polja)
        #   if self.je_validan_potez(self.pozicija_polja,mesto_na_steku,smer_pomeranja):
             #ovde implementiramo za izvrsavanje poteza, to je za drugu fazu




    def print_stack_matrix(self,stack):
        matrix1 = [[0] * 3 for _ in range(3)]
        stack_list = list(stack)

        k=0;
        for i in range(3):
            for j in range(3):
                if k < len(stack_list):
                    matrix1[i][j] = stack_list[k]
                    k += 1
                else:
                    break

        indeks = len(stack_list)-1
        if(matrix1[2][2] != 0):
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
        #u element se nalazi polje koje zelimo da pomerim
        #treba da nadjemo gde je najblizi stek ako su nam pozicije sussedne prazne

        #na onsovu i j izracunamo
        #na primer imam i i j
        listaIpozitivno = []
        for k in range(i+1, self.velicina_table+1):
            listaIpozitivno.append(k)
        listaInegativno = []
        for k in range(1, i):
            listaInegativno.append(k)
        listaJnegativno = []
        for k in range(1, j):
            listaJnegativno.append(k)
        listaJpozitivno = []
        for k in range(j+1, self.velicina_table+1):
            listaJpozitivno.append(k)

        listaInegativno = list(reversed(listaInegativno))
        listaJnegativno = list(reversed(listaJnegativno))

        fleg = False
        p = 0
        k = 0
        while ( fleg == False ):
           najblizi_element = []
           '''          
           if(p == 0):
             element1 = self.vrati_stanje(listaInegativno[p]*10 + listaJnegativno[p])
             element2 = self.vrati_stanje(listaInegativno[p]*10 + listaJpozitivno[p])
             element3 = self.vrati_stanje(listaIpozitivno[p]*10 + listaJpozitivno[p])
             element4 = self.vrati_stanje(listaIpozitivno[p]*10 + listaJnegativno[p])
           '''

           if(p > 0):
               if (len(listaInegativno) < p or len(listaInegativno) == p):
                   indeks2 = 1
               else:
                   indeks2 = listaInegativno[p]
               if (len(listaIpozitivno) < p or len(listaIpozitivno) == p):
                   indeks3 = self.velicina_table
               else:
                   indeks3 = listaIpozitivno[p]


               if( p < len(listaJpozitivno)):
                  for o in range(indeks2, indeks3+1):
                     indeks = o*10+listaJpozitivno[p]
                     print(indeks)
                     element = self.vrati_stanje(indeks)
                     if (element != "PRAZNO"):
                         najblizi_element.append([element, indeks, p])
                         fleg = True

                     print(element)


               if (p < len(listaJnegativno)):
                  for o in range(indeks2, indeks3+1):
                     indeks = o*10+listaJnegativno[p]
                     element = self.vrati_stanje(indeks)
                     if (element != "PRAZNO"):
                         najblizi_element.append([element, indeks, p])
                         fleg = True
                     print(element)
                     print(indeks)

               if( len(listaJnegativno) < p or len(listaJnegativno) == p ):
                   indeks2 = 1
               else:
                   indeks2 = listaJnegativno[p]
               if (len(listaJpozitivno) < p or len(listaJpozitivno) == p):
                   indeks3 = self.velicina_table
               else:
                   indeks3 = listaJpozitivno[p]


               if (p < len(listaInegativno)):
                  for o in range(indeks2+1, indeks3):
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
                     if(element != "PRAZNO"):
                         najblizi_element.append([element, indeks, p])
                         fleg = True
                     print(element)
                     print(indeks)
           p= p+1
        print(najblizi_element)
        return najblizi_element



    def kreiraj_tablu(self, velicina_table, graf):
        for row in range(1, velicina_table + 1):
            for col in range(1, velicina_table + 1):
                square = f"{chr(96 + col)}{row}"
                graf.add_square(square, self.vrati_stanje(col *10 + row), square)

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

        #vraca mi veci broj obicno je prvi taj koji je dobar
        shortest_paths = tabla.bfs_shortest_paths(start_key, end_key)


        print(f"Najkraći putevi između {start_key} i {end_key}:")
        for path in shortest_paths:
            print(" -> ".join(path))


    def validan_potez(self):
         self.unos_poteza()
         susedna_polja = self.proveri_susedna_polja(self.pozicija_polja)
         if(len(susedna_polja[0]) == 4):
             print("Sva polja susedna su prazna")
         else:
             zauzeta_polja = susedna_polja[1]

             for polje in zauzeta_polja:
                 if polje[1] == self.smer_pomeranja:
                     print("Potez je validan")
                     slovo, broj = self.pozicija_polja[0].upper(), int(self.pozicija_polja[1:])
                     broj_slova = self.letter_to_number(slovo)
                     rezultat = broj_slova * 10 + broj
                     vrednsot_steka1 = self.vrati_stanje(rezultat)
                     vrednost_steka2 = self.vrati_stanje(polje[2])
                     self.spajanje_stekova(vrednsot_steka1, vrednost_steka2)




    def spajanje_stekova(self, polje1, polje2):
        while '.' in polje1:
            polje1.remove('.')

        while '.' in polje2:
            polje2.remove('.')

        visina_drugog_steka = len(polje2)


        indeks = int(self.mesto_na_steku) +1
        elementi_od_pocetka_do_mesta = (list(polje1)[:indeks])
        visina_steka_za_premestanje = len(elementi_od_pocetka_do_mesta)

        if (visina_drugog_steka + visina_steka_za_premestanje > 8):
            print("Rezultujuci stek ima vise od 8 elemenata potez nije validan")

        else:
            if (visina_drugog_steka > int(self.mesto_na_steku)):
                for element in reversed(elementi_od_pocetka_do_mesta):
                    polje2.appendleft(element)
                print(polje2)
                polje1.rotate(-int(self.mesto_na_steku))
                for _ in range(int(self.mesto_na_steku) + 1):
                    polje1.popleft()
                print(polje1)
            else:
                print("Potez ne moze da se odigra, nije validan")

    def menjaj_stanje_igre(self, pozicija1, stek1, pozicija2, stek2):
        self.obrisi_stanje(pozicija1)
        self.obrisi_stanje(pozicija2)
        self.dodaj_stanje(pozicija1, stek1)
        self.dodaj_stanje(pozicija1, stek2)
        self.nacrtaj_trenutno_stanje()

    def odigravanje_partije(self):

        while( self.je_validan_smer() != True and self.je_validno_polje() != True and self.je_validna_pozicija_steka() != True ):
            print("Nije validan unos poteza")
            self.unos_poteza()


    def nacrtaj_pocetno_stanje(self):
        n = self.velicina_table +1
        m = self.velicina_table
        self.trenutno_stanje = HashTable(m*m)

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
                    #user1.dodaj_stanje((i * 10 + j), matrix[i][j])
                    self.dodaj_stanje((i * 10 + j), matrix[i][j])
                elif i % 2 != 0 and j % 2 != 0:
                    matrix[i][j].append('O')
                    #user2.dodaj_stanje((i * 10 + j), matrix[i][j])
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
              if(i+j) % 2 == 0:
                que1 =  self.vrati_stanje(i*10+j)
                if que1 == "PRAZNO":
                    matrix[i][j] = deque(['.'] * 9)
                else:
                    matrix[i][j] = que1
        for i in range(n):
            for j in range(n):

                self.print_stack_matrix(matrix[i][j])


            print('\n')

    def proveri_kraj_igre(user1, user2, polje): #funkciju pozivamo nakon svakog poteza
        # broj stekova koji je potreban za pobedu
        broj_pobednickih_stekova = len(user1.stanja) // 2

        # broj stekova koje je svaki igrač složio
        broj_stekova_user1 = user1.broj_slozenih_stekova()
        broj_stekova_user2 = user2.broj_slozenih_stekova()

        # provera da li je igra završena
        if broj_stekova_user1 > broj_pobednickih_stekova:
             print("Čestitamo! Igrač X je pobednik!")
             return True
        elif broj_stekova_user2 > broj_pobednickih_stekova:
             print("Čestitamo! Igrač O je pobednik!")
             return True

        # provera da li je tabla puna ili je nereseno
        elif polje.is_tabla_puna():
             print("Igra je završena nereseo.")
             return True

        return False




