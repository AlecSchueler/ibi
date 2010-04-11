import ibiexceptions

class Tape:
    ptr = 0
    
    def __init__(self, length = 30000):
        self.tape = [0] * length
        self.length = length
        self.cell_val = self.tape[self.ptr]

    def _update_cell_val(func):
        def call_func_and_update(*args):
            func(*args)
            self.cell_val = self.tape[self.ptr]
        return call_func_and_update

    @_update_cell_val
    def update_ptr(self, dir):
        self.ptr += dir
        if self.ptr >= self.length or self.ptr < 0:
            raise ibiexceptions.TapeError

    @_update_cell_val
    def update_cell(self, dir):
        self.tape[self.ptr] += dir
        if 0 > self.tape[self.ptr] > 126:
            raise TapeError

    @_update_cell_val
    def replace_cell(self, new_val):
        if type(new_val) == str:
            self.tape[self.ptr] = ord(new_val)
        else:
            self.tape[self.ptr] = int(new_val)

    def __repr__(self):
        # this might be pretty unsemantic;
        # have a think about it
        return repr(chr(self.cell_val))

    def __len__(self):
        return len(self.tape)

    def __getitem__(self, key):
        return self.tape[key]

