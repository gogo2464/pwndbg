#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess
import tempfile

import gdb

import pwndbglib.commands
import pwndbglib.vmmap

parser = argparse.ArgumentParser(description="ROP gadget search with ropper.",
                                epilog="Example: ropper -- --console; ropper -- --search 'mov e?x'")
parser.add_argument('argument', nargs='*', type=str,
                    help='Arguments to pass to ropper')


@pwndbglib.commands.ArgparsedCommand(parser)
@pwndbglib.commands.OnlyWithFile
def ropper(argument):
    with tempfile.NamedTemporaryFile() as corefile:

        # If the process is running, dump a corefile so we get actual addresses.
        if pwndbglib.proc.alive:
            filename = corefile.name
            gdb.execute('gcore %s' % filename)
        else:
            filename = pwndbglib.proc.exe

        # Build up the command line to run
        cmd = ['ropper',
               '--file',
               filename] 
        cmd += argument

        try:
            io = subprocess.call(cmd)
        except Exception:
            print("Could not run ropper.  Please ensure it's installed and in $PATH.")