from term import codec
from term.basetypes import Term
from typing import Generator

import struct
import sys

from TestTools import outputInit, outputLn

def _mailbox_gen() -> Generator[Term, None, None]:
    while True:
        outputLn("In mailbox gen")
        len_bin = sys.stdin.buffer.read(4)
        if len(len_bin) != 4:
            return None
        (length,) = struct.unpack("!I", len_bin)
        (term, rest) = codec.decode(sys.stdin.buffer.read(length))
        yield term


def _port_gen() -> Generator[None, Term, None]:
    while True:
        outputLn("In Port Gen")
        term = codec.encode((yield))
        outputLn("In port gen with term: " + str(term))
        binary = struct.pack("!I", len(term))
        outputLn("Binary: " + str(binary))
        sys.stdout.buffer.write(binary)
        sys.stdout.buffer.write(term)

def stdio_port_connection() -> (
    tuple[Generator[Term, None, None], Generator[None, Term, None]]
):
    outputLn("In STDIO port connection")
    port = _port_gen()
    next(port)
    return _mailbox_gen(), port