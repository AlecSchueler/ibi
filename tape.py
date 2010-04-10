import ibiexceptions

class Tape:
    ptr = 0
    
    def __init__(self, length = 30000):
        self.tape = [0] * length
        self.length = length

    def update_ptr(self, dir):
        self.ptr += dir
        if self.ptr < 0:
            raise ibiexceptions.TapeError("pointer moved before first cell")
        elif self.ptr >= self.length:
            raise ibiexceptions.TapeError("pointer moved after final cell")

    def update_cell(self, dir):
        self.tape[self.ptr] += dir
        if 0 > self.tape[self.ptr]:
            raise TapeError("cell value below 0")
        elif self.tape[self.ptr] > 126:
            raise TapeError("cell value above 126")

    def replace_cell(self, new_val):
        if type(new_val) == str:
            self.tape[self.ptr] = ord(new_val)
        else:
            self.tape[self.ptr] = int(new_val)

    def __repr__(self):
        # this might be pretty unsemantic;
        # have a think about it
        return chr(self.tape[self.ptr])

    def __len__(self):
        return len(self.tape)

    def __getitem__(self, key):
        return self.tape[key]

