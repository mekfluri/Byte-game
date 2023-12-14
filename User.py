from collections import deque
from HashTable import HashTable

class User:
    def __init__(self, is_human,oznaka):

        self.is_human = is_human
        self.stanja = deque()
        self.oznaka=oznaka
        self.stekovi=deque()
        self.hashTable = HashTable(16)
        self.broj_slozenih = 0

    def dodaj_stanje(self, broj, stek):
        self.hashTable.set_val(broj, stek)


    def vrati_stanje(self, broj):
        return self.hashTable.get_val(broj)

    def obrisi_stanje(self, broj):
        self.hashTable.delete_val(broj)

    def prikazi_stanje(self):
        print(f"User HashTable stanje: {str(self.hashTable)}")

    def __str__(self):
        return f"User: {str(self.hashTable)}"

    def broj_slozenih_stekova(self,polje):
        for red in polje:
          for stek in red:
            if all(c != '.' for c in stek) and stek[0] == self.oznaka and len(stek)==8:
                self.broj_slozenih += 1

        return self.broj_slozenih
