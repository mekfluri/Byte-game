# main.py8
from collections import deque
from collections import deque, defaultdict

from Graph import Chessboard
from Interfejs import Interfejs

from User import User




def main():
    interfejs = Interfejs()
    velicinaTable = interfejs.zapocni_igru()
    user1, user2 = interfejs.vrati_korisnike()
    interfejs.nacrtaj_pocetno_stanje()
    tabla = interfejs.vrati_tablu()

    while not interfejs.proveri_kraj_igre(user1,user2, tabla):
      interfejs.odigraj_potez()
      tabla=interfejs.vrati_tablu()
      interfejs.prikazi_stanje_igre()




if __name__ == "__main__":
    main()
