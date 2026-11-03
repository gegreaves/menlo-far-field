def read_header(filepath):
    header = []

    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("#"):
                header.append(line.removeprefix("#").strip())
            else:
                break

    return header
