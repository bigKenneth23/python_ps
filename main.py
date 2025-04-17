from Photoshop import Photoshop
from sys import argv, exit

def main(argv: list[str]) -> int:
    argc = len(argv)

    if argc != 3:
        print("ERROR: Expected 2 arguments (target file, edit mode)")
        return 1
    
    file_name = argv[1].strip()
    edit_mode = argv[2].strip()

    if not file_name:
        print("ERROR: No file name provided.")
        return 2

    if not edit_mode:
        print("ERROR: No edit mode provided.")
        return 3

    cont = Photoshop(file_name, edit_mode)

    if cont.status:
        print("Program successful, new image is contained within the Output/ directory.")
        return 0

    print("ERROR: Invalid file name or edit mode, program did not complete task successfully.")
    return 4 
    


if __name__ == "__main__":
    exit(main(argv))