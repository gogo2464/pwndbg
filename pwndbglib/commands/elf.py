#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elftools.elf.elffile import ELFFile

import pwndbglib.commands
from pwndbglib.color import message


@pwndbglib.commands.ArgparsedCommand('Prints the section mappings contained in the ELF header.')
@pwndbglib.commands.OnlyWithFile
def elfheader():
    local_path = pwndbglib.file.get_file(pwndbglib.proc.exe)

    with open(local_path, 'rb') as f:
        elffile = ELFFile(f)
        sections = []
        for section in elffile.iter_sections():
            start = section['sh_addr']

            # Don't print sections that aren't mapped into memory
            if start == 0:
                continue

            size = section['sh_size']
            sections.append((start, start + size, section.name))

        sections.sort()

        for start, end, name in sections:
            print('%#x - %#x ' % (start, end), name)


@pwndbglib.commands.ArgparsedCommand('Prints any symbols found in the .got.plt section if it exists.')
@pwndbglib.commands.OnlyWithFile
def gotplt():
    print_symbols_in_section('.got.plt', '@got.plt')


@pwndbglib.commands.ArgparsedCommand('Prints any symbols found in the .plt section if it exists.')
@pwndbglib.commands.OnlyWithFile
def plt():
    print_symbols_in_section('.plt', '@plt')


def get_section_bounds(section_name):
    local_path = pwndbglib.file.get_file(pwndbglib.proc.exe)

    with open(local_path, 'rb') as f:
        elffile = ELFFile(f)

        section = elffile.get_section_by_name(section_name)

        if not section:
            return (None, None)

        start = section['sh_addr']
        size = section['sh_size']
        return (start, start + size)


def print_symbols_in_section(section_name, filter_text=''):
    start, end = get_section_bounds(section_name)

    if start is None:
        print(message.error('Could not find section'))
        return

    symbols = get_symbols_in_region(start, end, filter_text)

    if not symbols:
        print(message.error('No symbols found in section %s' % section_name))

    for symbol, addr in symbols:
        print(hex(int(addr)) + ': ' + symbol)


def get_symbols_in_region(start, end, filter_text=''):
    symbols = []
    ptr_size = pwndbglib.typeinfo.pvoid.sizeof
    addr = start
    while addr < end:
        name = pwndbglib.symbol.get(addr)
        if name != '' and '+' not in name and filter_text in name:
            symbols.append((name, addr))
        addr += ptr_size

    return symbols