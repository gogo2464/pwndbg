#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pwndbglib.wrappers

cmd_name = "readelf"

@pwndbglib.wrappers.OnlyWithCommand(cmd_name)
def get_jmpslots():
    local_path = pwndbglib.file.get_file(pwndbglib.proc.exe)
    cmd = get_jmpslots.cmd + ["--relocs", local_path]
    readelf_out = pwndbglib.wrappers.call_cmd(cmd)

    return filter(_extract_jumps, readelf_out.splitlines())

def _extract_jumps(line):
    '''
     Checks for records in `readelf --relocs <binary>` which has type e.g. `R_X86_64_JUMP_SLO`
     NOTE: Because of that we DO NOT display entries that are not writeable (due to FULL RELRO)
     as they have `R_X86_64_GLOB_DAT` type.

    It might be good to display them seperately in the future.
    '''
    try:
        if "JUMP" in line.split()[2]:
            return line
        else:
            return False
    except IndexError:
        return False
