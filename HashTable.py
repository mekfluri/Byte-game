class HashTable:


    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [[] for _ in range(self.size)]

    def values(self):
        all_values = []
        for bucket in self.hash_table:
            for key, value in bucket:
                all_values.append(value)
        return all_values
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

        for key in range(matrix_size * matrix_size):
            value = hash_table.get_val(key)
            if value is not None:
                row = key // matrix_size
                col = key % matrix_size
                matrix[row][col] = value

        return matrix

    def matricu_u_hash(hash_table,matrix):
        hash_table = HashTable(1)

        for row_index, row in enumerate(matrix):
            for col_index, value in enumerate(row):
                key = row_index * len(matrix) + col_index
                hash_table.set_val(key, value)

        return hash_table
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)