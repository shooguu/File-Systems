class Buffer:
    def __init__(self, block_size: int):
        self.M = ['' for _ in range(block_size)]
        self.buffer = ['' for _ in range(block_size)]

    
    def read_block(self, position: int) -> None:
        
        return self.M[position]
        

    def write_to_M(self, char: str, start_position: int) -> None:
        '''
        Given a buffer and num_of_char, the buffer is written
        into a character array M
        '''
        self.M[start_position] = char


    def number_of_bytes_in_M(self) -> int:
        counter = 0
        for i in self.M:
            if i != '':
                counter += 1
        return counter