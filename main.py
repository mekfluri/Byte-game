# main.py
from collections import deque
from collections import deque, defaultdict

from Graph import Chessboard
from Interfejs import Interfejs

from User import User




def main():
    interfejs = Interfejs()
    velicinaTable = interfejs.zapocni_igru()
    user1, user2 = interfejs.vrati_korisnike()
    tabla = interfejs.vrati_tablu()

    while not interfejs.proveri_kraj_igre(user1,user2,tabla):
      interfejs.unos_poteza()
      interfejs.najblizi_element()
      chessboard = Chessboard()
      interfejs.najkraci_put()
      interfejs.validan_potez()

if __name__ == "__main__":
    main()
