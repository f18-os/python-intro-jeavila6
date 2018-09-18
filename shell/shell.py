#! /usr/bin/env python3

import os
import sys
import re


def execute(pgm):
    """Execute pgm -- program with arguments."""
    args = pgm.split()
    if '/' in args[0]:  # args[0] is a path
        os.execve(args[0], args, os.environ)
    else:
        for directory in re.split(':', os.environ['PATH']):  # try each directory in PATH
            try:
                os.execve(f'{directory}/{args[0]}', args, os.environ)
            except FileNotFoundError:
                pass
    print('Could not exec', args[0], file=sys.stderr)
    sys.exit(1)


while True:
    print('$ ', end='')
    cmd = input()
    if not cmd.split():
        continue  # ignore empty command
    if cmd == 'exit':
        break  # terminate with 'exit' command

    try:
        ret_val = os.fork()
    except OSError as e:
        print('Fork failed:', e, file=sys.stderr)
        continue

    if ret_val:  # parent
        child_pid, child_esi = os.wait()  # wait until child completes, store its process id and exit status indicator
        child_exit_stat = child_esi >> 8  # get exit status from exist status indicator
        if child_exit_stat:
            print('Child terminated with exit status', child_exit_stat, file=sys.stderr)

    else:  # child
        cmd_split = re.split('([<>|])', cmd)
        if len(cmd_split) == 3 and cmd_split[1] in ['<', '>']:  # command is in format: *program* [args] {<|>} *file*
            pgm, redir_op, file = cmd_split
            if redir_op == '<':  # input redirection
                os.close(0)
                sys.stdin = open(file.strip(), 'r')
                fd = sys.stdin.fileno()
            else:  # output redirection
                os.close(1)
                sys.stdout = open(file.strip(), 'w')
                fd = sys.stdout.fileno()
            os.set_inheritable(fd, True)
            execute(pgm)

        if len(cmd_split) == 3 and cmd_split[1] == '|':  # command is in format: *program* [args] | *program* [args]
            pgm1, pipe, pgm2 = cmd_split
            pipe_read, pipe_write = os.pipe()
            try:
                ret_val = os.fork()
            except OSError as e:
                print('Fork failed:', e, file=sys.stderr)
                continue
            if ret_val:  # parent
                child_pid, child_esi = os.wait()
                child_exit_stat = child_esi >> 8
                if child_exit_stat:
                    print('Child terminated with exit status', child_exit_stat, file=sys.stderr)
                os.dup2(pipe_read, 0)
                execute(pgm2)
            else:  # child
                os.dup2(pipe_write, 1)
                execute(pgm1)

        execute(cmd_split[0])  # command is in some other format
