import queue
from collections import deque




class Node:
    def __init__(self, queue, key):
        self.stek = queue
        self.komsije = []
        self.key = key


class Chessboard:
    def __init__(self):
        self.board = {}

    def add_square(self, square, queue1, key):
        if square not in self.board:
            self.board[square] = Node(queue1, key)

    def add_diagonal_edges(self, velicina_table):
        squares = list(self.board.keys())
        for square in squares:
            col, row = ord(square[0]) - 96, int(square[1:])


            if (col + row) % 2 == 0:

                if col > 1 and row <= velicina_table:
                    self.add_edge(square, f"{chr(96 + col - 1)}{row + 1}")

                #gore desno
                if col <= velicina_table and row <= velicina_table:
                    self.add_edge(square, f"{chr(96 + col + 1)}{row + 1}")

    def print_graph(self):
        for square, node in self.board.items():
            neighbors_str = ", ".join(node.komsije)
            print(f" Key: {node.key}, Neighbors: {neighbors_str}, Stack: {list(node.stek)}")

    def number_to_letter(self, number):
        # Dodaje vrednost slova 'a' i oduzima 1 kako bi dobio odgovarajuće slovo
        ascii_value = ord('a') + number - 1

        # Pretvara ASCII vrednost u slovo
        letter = chr(ascii_value)

        return letter

    def add_edge(self, square1, square2):
        if square1 in self.board and square2 in self.board:
            if abs(int(square1[1:]) - int(square2[1:])) == 1:
              self.board[square1].komsije.append(square2)
              self.board[square2].komsije.append(square1)

    def letter_to_number(slef,letter):

        lower_case_letter = letter.lower()

        ascii_value = ord(lower_case_letter)

        position = ascii_value - ord('a') + 1

        return position

    def bfs_shortest_paths(self, start_key, end_key):
        # Inicijalizacija reda za BFS
        queue = deque([(start_key, [start_key])])

        # Skup za praćenje posećenih čvorova
        visited = set()

        # Lista za čuvanje svih najkraćih puteva
        shortest_paths = []

        while queue:
            current_key, current_path = queue.popleft()

            if current_key == end_key:
                # Ako smo stigli do ciljnog čvora, dodajemo trenutni put u listu najkraćih puteva
                shortest_paths.append(current_path)
                continue

            if current_key not in visited:
                visited.add(current_key)

                # Dodajemo ključeve komšija trenutnog čvora u red sa ažuriranim putanjama
                for neighbor_key in self.board[current_key].komsije:
                    queue.append((neighbor_key, current_path + [neighbor_key]))

        return shortest_paths

    def dfs(self, start_node,  visited, matrix, velicinatable, user1, user2):
        node = self.board[start_node]

        if node.key not in visited:
            print(f"Visited node: {node.key}")
            visited.append(node.key)



            row_number = int(node.key[1:])
            letter = str(node.key[0])
            print(row_number)
            if letter == 'a' or letter == self.number_to_letter(velicinatable):
                node.stek = deque(['.'] * 9)
            else:
              j = self.letter_to_number(letter)
              if row_number % 2 == 0 and j % 2 == 0:
                node.stek = deque(['.'] * 8)
                node.stek.append('X')
                user1.dodaj_stanje((row_number * 10 + j), matrix[row_number][j])
              if row_number % 2 != 0 and j % 2 != 0:
                node.stek = deque(['.'] * 8)
                node.stek.append('O')
                user2.dodaj_stanje((row_number * 10 + j), matrix[row_number][j])
            matrix[self.letter_to_number(letter)][row_number] = node.stek
            print(f"Square: {node.key}, Neighbors: {node.komsije}, Stack: {list(node.stek)}")
            for neighbor in node.komsije:
                self.dfs(neighbor, visited, matrix, velicinatable, user1, user2)
        return matrix



    def dfs_trenutno(self, square, visited, matrix, velicinatable, user1, user2):
        node = self.board[square]

        if node.key not in visited:
            print(f"Visited node: {node.key}")
            visited.append(node.key)

            row_number = int(node.key[1:])
            letter = str(node.key[0])
            j = self.letter_to_number(letter)


            que = user1.vrati_stanje(row_number * 10 + j)
            if que != "PRAZNO":
                matrix[row_number][j] = que

            que = user2.vrati_stanje(row_number * 10 + j)
            if que != "PRAZNO":
                matrix[row_number][j] = que
            print(f"Square: {node.key}, Neighbors: {node.komsije}, Stack: {list(node.stek)}")
            for neighbor in node.komsije:
                self.dfs(neighbor, visited, matrix, velicinatable, user1, user2)
        return matrix
