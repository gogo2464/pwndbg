#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gdb

import pwndbglib.commands
import pwndbglib.regs


class segment(gdb.Function):
    """Get the flat address of memory based off of the named segment register.
    """
    def __init__(self, name):
        super(segment, self).__init__(name)
        self.name = name
    def invoke(self, arg=0):
        result = getattr(pwndbglib.regs, self.name)
        return result + arg

segment('fsbase')
segment('gsbase')

@pwndbglib.commands.ArgparsedCommand("Prints out the FS base address.  See also $fsbase.")
@pwndbglib.commands.OnlyWhenRunning
def fsbase():
    """
    Prints out the FS base address.  See also $fsbase.
    """
    print(hex(int(pwndbglib.regs.fsbase)))


@pwndbglib.commands.ArgparsedCommand("Prints out the GS base address.  See also $gsbase.")
@pwndbglib.commands.OnlyWhenRunning
def gsbase():
    """
    Prints out the GS base address.  See also $gsbase.
    """
    print(hex(int(pwndbglib.regs.gsbase)))