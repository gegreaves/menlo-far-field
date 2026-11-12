def read_header(filepath):
    """
    Reads the header of a THz data file and returns it as a list of strings.
    The header lines are expected to start with a '#' character.
    """
    header = []

    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("#"):
                header.append(line.removeprefix("#").strip())
            else:
                break

    return header
