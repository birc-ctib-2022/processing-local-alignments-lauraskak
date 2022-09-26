"""A module for translating between alignments and edits sequences."""


def align(x: str, y: str, edits: str) -> tuple[str, str]:
    """Align two sequences from a sequence of edits.

    Args:
        x (str): The first sequence to align.
        y (str): The second sequence to align
        edits (str): The list of edits to apply, given as a string

    Returns:
        tuple[str, str]: The two rows in the pairwise alignment

    >>> align("ACCACAGTCATA", "ACAGAGTACAAA", "MDMMMMMMIMMMM")
    ('ACCACAGT-CATA', 'A-CAGAGTACAAA')

    """

    # Better variable name, I think
    seq1 = x
    seq2 = y

    # The two aligned files are saved at there variables
    align1 = ""
    align2 = ""

    # Extra int adds to i, if a gap has accured. Otherwise the alignments are not recreated properly
    int1 = 0 
    int2 = 0

    for o in edits:

        if o == "M": 
            # If the two bases are matched or mismatched the corresponding bases are appended to the align variables.
            align1 += seq1[int1]
            align2 += seq2[int2]
            int1 += 1
            int2 += 1

        elif o == "D":
            # If the second sequence contains a gap, a gap character is added and 1 is added to the extra int variable.
            align1 += seq1[int1]
            align2 += "-"
            int1 += 1

        elif o == "I":
            # If the first sequence contains a gap, a gap character is added and 1 is added to the extra int variable.
            align1 += "-"
            align2 += seq2[int2]
            int2 += 1

    return (align1, align2)


def edits(x: str, y: str) -> str:
    """Extract the edit operations from a pairwise alignment.

    Args:
        x (str): The first row in the pairwise alignment.
        y (str): The second row in the pairwise alignment.

    Returns:
        str: The list of edit operations as a string.

    >>> edits('ACCACAGT-CATA', 'A-CAGAGTACAAA')
    'MDMMMMMMIMMMM'

    """

    # Better variable name, I think
    align1 = x
    align2 = y

    # The two aligned files are saved at there variables
    edits = ""

    if len(align1) == len(align2):

        for i in range(len(align1)):

            if align1[i] != "-" and align2[i] != "-":
                # If the bases are matches or mismatches, then M is added to edits
                edits += "M"

            elif align1[i] != "-" and align2[i] == "-":
                # If there is a gap, "-", in align2, then a D is added
                edits += "D"

            elif align1[i] == "-" and align2[i] != "-":
                # If there is a gap, "-", in align1, then a I is added
                edits += "I"

            else:
                print("Invalid alignment")

    else:
        print("Invalid alignment")

    return edits


#print(align("ACCACAGTCATA", "ACAGAGTACAAA", "MDMMMMMMIMMMM"))