# main.py
from collections import deque
from Interfejs import Interfejs
from User import User


def main():
    interfejs = Interfejs()
    interfejs.zapocni_igru()
    user1 = User(8*8)
    user2 = User(8*8)

    interfejs.nacrtaj_pocetno_stanje(user1, user2)
    interfejs.nacrtaj_trenutno_stanje(user1, user2)


if __name__ == "__main__":
    main()
