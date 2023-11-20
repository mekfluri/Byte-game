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
