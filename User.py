from collections import deque

from HashTable import HashTable


class User:
    def __init__(self, hash_table_size):
        self.hashTable = HashTable(hash_table_size)

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

