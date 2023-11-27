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


    def unos_poteza(self):
        pozicija_polja = input("Unesite poziciju polja").upper()
        mesto_na_steku = input("Unesite mesto figure na steku")
        smer_pomeranja = input("Unesite smer pomeranja figure").upper()




    def print_stack_matrix(self,stack,fleg):
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
            if(fleg == 0):
              for _ in range(9):
                 print(' ', end=' ')
            else:
                for row in matrix1:
                    for i, element in enumerate(row):
                        if i == len(row) - 1:
                            if element == 0:
                                print('.', end=' ')
                            else:
                                print(element, end=' ')
                        else:
                            print(element, end=' ')


    def nacrtaj_pocetno_stanje(self, user1, user2):
        n = self.velicina_table +1
        m = self.velicina_table

        matrix = [[deque(['.'] * 8) for _ in range(n)] for _ in range(n)]

        for j in range(1, n):
            matrix[0][j].append(str(j))
        for i, letter in enumerate(string.ascii_uppercase[:n - 1]):
            matrix[i + 1][0].append(letter)



        for i in range(2, n-1):
            for j in range(1, n):
                if i % 2 == 0 and j % 2 == 0:

                    matrix[i][j].append('X')
                    user1.dodaj_stanje((i * 10 + j), matrix[i][j])
                if i % 2 != 0 and j % 2 != 0:
                    matrix[i][j].append('O')
                    user2.dodaj_stanje((i * 10 + j), matrix[i][j])

        for i in range(n):
            for j in range(n):
                if (i == 1 and i % 2 != 0 and j % 2 != 0) or (i == m and i % 2 == 0 and j % 2 == 0):

                    self.print_stack_matrix(matrix[i][j], 1)

                else:
                    self.print_stack_matrix(matrix[i][j], 0)
            print('\n')



    def nacrtaj_trenutno_stanje(self, user1, user2):
        n = self.velicina_table + 1
        m = self.velicina_table
        matrix = [[deque(['.'] * 8) for _ in range(n)] for _ in range(n)]

        for j in range(1, n):
            matrix[0][j].append(str(j))
        for i, letter in enumerate(string.ascii_uppercase[:n - 1]):
            matrix[i + 1][0].append(letter)

        for i in range(2, n - 1):
            for j in range(1, n):
               que =  user1.vrati_stanje(i*10+j)
               if que != "PRAZNO":
                   matrix[i][j] = que

               que = user2.vrati_stanje(i * 10 + j)
               if que != "PRAZNO":
                   matrix[i][j] = que

        for i in range(n):
            for j in range(n):
                    if (i == 1 and i % 2 != 0 and j % 2 != 0) or (i == m and i % 2 == 0 and j % 2 == 0):

                       self.print_stack_matrix(matrix[i][j], 1)

                    else:
                        self.print_stack_matrix(matrix[i][j], 0)


            print('\n')



