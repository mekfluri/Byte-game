import string
from collections import deque




class Interfejs:
    def __init__(self):
        self.velicina_table = 0
        self.trenutni_igrac = ''
        self.tabla = None
        self.igraci = {'X': 'Čovek', 'O': 'Računar'}

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
        return self.velicina_table

    def kreiraj_tablu(self, velicina_table, graf):
        for row in range(1, velicina_table + 1):
            for col in range(1, velicina_table + 1):
                square = f"{chr(96 + col)}{row}"  # Pretvara broj u slovo (1->a, 2->b, ..., 8->h)
                graf.add_square(square, deque(['.'] * 8), square)

    def number_to_letter(self, number):

        ascii_value = ord('a') + number - 1
        letter = chr(ascii_value)

        return letter

    #graf
    def trenutni_prikaz_table(self, graf, velicina_table, user1, user2):
        matrix = [['' for _ in range(velicina_table + 1)] for _ in range(velicina_table + 1)]
        visited = []
        matrix = graf.dfs_trenutno("a1", visited, matrix, velicina_table, user1, user2)

        for i in range(velicina_table + 1):
            for j in range(velicina_table + 1):
                if j == 0:
                    matrix[i][j] = deque(['.'] * 8)
                    matrix[i][j].append(self.number_to_letter(i))

                if i == 0:
                    matrix[i][j] = deque(['.'] * 8)
                    matrix[i][j].append(j)
                if (matrix[i][j] == ''):
                    matrix[i][j] = deque(['.'] * 8)
                    matrix[i][j].append(0)


                self.print_stack_matrix(matrix[i][j])


            print('\n')



    #graf
    def inicijalni_prikaz_table(self, graf, velicina_table, user1, user2):
        matrix = [['' for _ in range(velicina_table+1)] for _ in range(velicina_table+1)]
        visited = []
        matrix = graf.dfs("a1", visited, matrix, velicina_table, user1, user2)
        for i in range(len(matrix)):
          for j in range(len(matrix[i])):
            print(f"matrica[{i}][{j}] = {matrix[i][j]}")

        for i in range(velicina_table + 1):
            for j in range(velicina_table +1):
                if j == 0:
                    matrix[i][j] = deque(['.'] * 8)
                    matrix[i][j].append(self.number_to_letter(i))

                if i == 0:
                    matrix[i][j] = deque(['.'] * 8)
                    matrix[i][j].append(j)
                if (matrix[i][j] == ''):
                    matrix[i][j] = deque(['.'] * 8)
                    matrix[i][j].append(0)


                self.print_stack_matrix(matrix[i][j])


            print('\n')


    def je_validno_polje(self,polje):
        return polje[0] in string.ascii.lowercase and polje[1:].isdigit()

    def je_validna_pozicija_steka(self, pozicija):
        return pozicija.isdigit() and 1 <= int(pozicija) <= 8

    def je_validan_smer(self, smer):
        return smer.upper() in {'GORE', 'DOLJE', 'LEVO', 'DESNO'}

    def je_validan_potez(self, polje , pozicija_steka, smer):

        #da li je polje validno
        if not self.je_validno_polje(polje):
            print('Unesli ste neispravno polje.')
            return False

        #da li je pozicija steka validna
        if not self.je_validna_pozicija_steka(pozicija_steka):
            print('Pozicija stek nije validna.')
            return False

        #da li je smer validan
        if not self.je_validan_smer(smer):
            print("Smer nije validna.")
            return False

    def unos_poteza(self):
      while True:
        pozicija_polja = input("Unesite poziciju polja").upper()
        mesto_na_steku = input("Unesite mesto figure na steku")
        smer_pomeranja = input("Unesite smer pomeranja figure").upper()

        if self.je_validan_potez(pozicija_polja,mesto_na_steku,smer_pomeranja):
             #ovde implementiramo za izvrsavanje poteza, to je za drugu fazu
              break



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




    #matrica
    def nacrtaj_pocetno_stanje(self, user1, user2):
        n = self.velicina_table +1
        m = self.velicina_table

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
                    user1.dodaj_stanje((i * 10 + j), matrix[i][j])
                elif i % 2 != 0 and j % 2 != 0:
                    matrix[i][j].append('O')
                    user2.dodaj_stanje((i * 10 + j), matrix[i][j])

        for i in range(n):
            for j in range(n):


                self.print_stack_matrix(matrix[i][j])


            print('\n')






    #matrica

    def nacrtaj_trenutno_stanje(self, user1, user2):
        n = self.velicina_table + 1
        m = self.velicina_table
        matrix = [[deque(['.'] * 8) for _ in range(n)] for _ in range(n)]

        for j in range(1, n):
            matrix[0][j].append(str(j))
        for i, letter in enumerate(string.ascii_uppercase[:n - 1]):
            matrix[i + 1][0].append(letter)


        user2.prikazi_stanje()
        for i in range(1, n):
            for j in range(1, n):
              if(i+j) % 2 == 0:
                que1 =  user1.vrati_stanje(i*10+j)
                if que1 != "PRAZNO":
                    matrix[i][j] = que1

                que2 = user2.vrati_stanje(i * 10 + j)
                if que2 != "PRAZNO":
                    matrix[i][j] = que2

                if( que1 == "PRAZNO" and que2 == "PRAZNO"):
                    matrix[i][j] = deque(['.'] * 9)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                print(f"matrica[{i}][{j}] = {matrix[i][j]}")


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

