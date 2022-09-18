"""A module for translating between alignments and edits sequences."""

import re


def split_pairs(cigar: str) -> list[tuple[int, str]]:
    """Split a CIGAR string into a list of integer-operation pairs.

    Args:
        cigar (str): A CIGAR string

    Returns:
        list[tuple[int, str]]: A list of pairs, where the first element is
        an integer and the second an edit operation.

    >>> split_pairs("1M1D6M1I4M")
    [(1, 'M'), (1, 'D'), (6, 'M'), (1, 'I'), (4, 'M')]

    """
    return [(int(i), op) for i, op in re.findall(r"(\d+)([^\d]+)", cigar)]


def cigar_to_edits(cigar: str) -> str:
    """Expand the compressed CIGAR encoding into the full list of edits.

    Args:
        cigar (str): A CIGAR string

    Returns:
        str: The edit operations the CIGAR string describes.

    >>> cigar_to_edits("1M1D6M1I4M")
    'MDMMMMMMIMMMM'

    """

    cigar_list = split_pairs(cigar)

    edits = ""

    for pair in cigar_list:
        # Goes through every pair and adds the character an amout of times corresponing to the front integer of the pair.
        edits += pair[1] * pair[0]

    return edits


def split_blocks(x: str) -> list[str]:
    """Split a string into blocks of equal character.

    Args:
        x (str): A string, but we sorta think it would be edits.

    Returns:
        list[str]: A list of blocks.

    >>> split_blocks('MDMMMMMMIMMMM')
    ['M', 'D', 'MMMMMM', 'I', 'MMMM']

    """
    return [m[0] for m in re.findall(r"((.)\2*)", x)]


def edits_to_cigar(edits: str) -> str:
    """Encode a sequence of edits as a CIGAR.

    Args:
        edits (str): A sequence of edit operations

    Returns:
        str: The CIGAR encoding of edits.

    >>> edits_to_cigar('MDMMMMMMIMMMM')
    '1M1D6M1I4M'

    """

    cigar = ""

    for i in range(len(edits)):

        if i == 0:
            # Starts a count of the repeating characters with the first character as a reference.
            character = edits[i]
            count = 1

        else:

            if edits[i] == character:
                # Continues the count if the next character is a repeating character.
                count += 1

            else:
                # Appends the corresponding count and character pair to the cigar string
                cigar += f'{count}{character}'
                # Starts a new count of the repeating characters with the current character as a reference.
                character = edits[i]
                count = 1
                
    cigar += f'{count}{character}'

    return cigar
