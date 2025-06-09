from Photoshop import Photoshop
from sys import argv, exit

def main(argv: list[str]) -> int:
    argc = len(argv)

    if argc < 3:
        if argv[1] != "METHODS":
            print("Invalid arguments, expected target file + target filters.")
            return 1
        else:
            Photoshop(None, "METHODS")
            return

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
    example_argv = [0,"sloth.jpg", 'Brightness', "blur", 'Greyscale', 'Sepia', 'Invert', 'Oppose', 'Spotlight', 'Mirrorx', 'Mirror', 'Flipx', 'Flip', 'Rotate']
    exit(main(argv))