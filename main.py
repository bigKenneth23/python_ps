from Photoshop import Photoshop
from sys import argv, exit

def main(argv: list[str]) -> int:
    argc = len(argv)

    if argc < 3:
        print("Invalid arguments, expected target file + target filters.")
        return 1

    file = argv[1]
    filters = argv[2:]

    if len(filters) == 1:
        filters = filters[0]

    ps = Photoshop(file, filters)

    if not ps.status:
        return 2
    
    print(f"{file} has succesfully been edited and cloned into the output directory!")
    return 0


if __name__ == "__main__":
    exit(main(argv))