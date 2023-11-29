# main.py
from collections import deque, defaultdict

from Graph import Chessboard, Node
from Interfejs import Interfejs
from User import User




def main():
    interfejs = Interfejs()
    velicinaTable = interfejs.zapocni_igru()
    user1 = User(velicinaTable*velicinaTable)
    user2 = User(velicinaTable*velicinaTable)



    chessboard = Chessboard()

    interfejs.kreiraj_tablu(velicinaTable, chessboard)

    chessboard.add_diagonal_edges(velicinaTable)

    #interfejs.inicijalni_prikaz_table(chessboard, velicinaTable, user1, user2)
    #interfejs.trenutni_prikaz_table(chessboard, velicinaTable, user1, user2)

    interfejs.nacrtaj_pocetno_stanje(user1,user2)
    interfejs.nacrtaj_trenutno_stanje(user1, user2)
if __name__ == "__main__":
    main()
