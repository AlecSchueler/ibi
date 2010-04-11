import readline
import shlex
import subprocess
import sys

import interpreter


CLI_FUNCS = {}


class Cli_frontend:

    def __init__(self, running_tape = None, tape_settings =
                 {"length": 30000}):
        if running_tape is not None:
            self.interpreter = interpreter.Interpreter(
                               tape_settings = tape_settings)
        else:
            self.interpreter = interpreter.Interpreter()

    def handle_line(self, line):
        if not line:return
        line = shlex.split(line)
        if line[0].startswith("!"):
            line[0] = line[0].strip("!")
            p = subprocess.Popen(line)
        elif line[0] in CLI_FUNCS:
            CLI_FUNCS[line[0]](line)
        else:
            self.interpreter.feed_program(''.join(line))
            self.interpreter.ex_prog()

    def set_prompt(self):
        self.prompt = "\n%05d:%03d$ " % (self.interpreter.tape.ptr,
                                         self.interpreter.tape.cell_val)
    
    def main(self):
        while True:
            self.set_prompt()
            try:
                self.handle_line(raw_input(self.prompt))
            except EOFError:
                break


def cli_func(func):
    opf = opt_parse(func)
    CLI_FUNCS[func.__name__] = opf
    return opf


def opt_parse(func):
    # this should be done with opt_parse so we get error handling
    # and defaults and other niceties
    def opt_parsed_func(args):
        opt_dict = {}
        args.pop(0)
        for i in range(len(args)-1):
            if args[i].startswith("-"):
                opt_dict[args[i].strip("-")] = args[i + 1]
        func(opt_dict)
    return opt_parsed_func

