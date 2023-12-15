class HashTable:


    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [[] for _ in range(self.size)]


    def set_val(self, key, val):

        hashed_key = hash(key) % self.size


        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record

            if record_key == key:
                found_key = True
                break

        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))

    def get_val(self, key):
        
        hashed_key = hash(key) % self.size


        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record


            if record_key == key:
                found_key = True
                break


        if found_key:
            return record_val
        else:
            return "PRAZNO"


    def delete_val(self, key):

        hashed_key = hash(key) % self.size

        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return

    def delete(self):
        self.hash_table.clear()

    def hashumatricu(hash_table, matrix_size):
        matrix = [[''] * matrix_size for _ in range(matrix_size)]

    def matricu_u_hash(self, matrix):
        if matrix is None:
            print("Error: Matrix is None.")
            return None

        hash_table = HashTable(1)

        try:
            for row_index, row in enumerate(matrix):
                for col_index, value in enumerate(row):
                    key = row_index * len(matrix) + col_index
                    hash_table.insert(key, value)
        except TypeError as e:
            print(f"Error: {e}")

        return hash_table

    def __str__(self):
        return "".join(str(item) for item in self.hash_table)