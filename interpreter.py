import sys

import ibiexceptions
import tape

class Interpreter:
    jump_list = {}
    ptr = 0

    def __init__(self, running_tape = None, tape_settings =
        {'length': 30000}):
        if running_tape is None:
            self.tape = tape.Tape(**tape_settings)
        else:
            self.tape = running_tape

        self.instructions = {
            # {"instruction": [func, [args]]}
            # {"instruction": [func, None]}
            "+": [self.tape.update_cell
                ,[1]],
            "-": [self.tape.update_cell
                ,[-1]],
            ">": [self.tape.update_ptr
                ,[1]],
            "<": [self.tape.update_ptr
                ,[-1]],
            ".": [self.output
                ,None],
            ",": [self.input
                ,None],
            "[": [self.start_loop
                ,None],
            "]": [self.end_loop
                ,None]
            }

    def feed_program(self, prog):
        self.prog = [char for char in prog if char in
                    self.instructions.keys()]
        self._pop_jumplist()

    def _pop_jumplist(self):
        tmp_lst = []
        for pos, cmd in enumerate(self.prog):
            if cmd == '[':
                tmp_lst.append(pos)
            elif cmd == ']':
                try:
                    start = tmp_lst.pop()
                except:
                    raise ibiexceptions.SyntaxError("unmatched ']'")
                self.jump_list[pos] = start
                self.jump_list[start] = pos
        if tmp_lst:
            raise ibiexceptions.SyntaxError("unmatched '['")


    def _ex_instruction(self, instruction):
        func, args = self.instructions[instruction]
        if args is None:
            func()
        else:
            func(*args)

    def ex_prog(self):
        self.ptr = 0
        while self.ptr < len(self.prog):
            self._ex_instruction(self.prog[self.ptr])
            self.ptr += 1

    def output(self):
        sys.stdout.write(`self.tape`)

    def input(self):
        ch = sys.stdin.read(1)
        if ch:
            self.tape.replace_cell(ch)
        else:
            # ch will be '' if an EOF is given
            self.tape.replace_cell(4)

    def start_loop(self):
        if self.tape[self.tape.ptr] == 0:
            self.ptr = self.jump_list[self.ptr]

    def end_loop(self):
        if self.tape[self.tape.ptr] != 0:
            self.ptr = self.jump_list[self.ptr]

