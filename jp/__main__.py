import argparse
from utils.manage_file import read_file
from utils.validate_json import is_json
def main():
    # define parser
    parser = argparse.ArgumentParser(description="json parser")
    # add arguments
    parser.add_argument("filepath", type=str, help="path to parsable file.")
    # get the file path
    args = parser.parse_args()
    filepath = args.filepath
    # report to user
    if is_json(read_file(filepath)):
        print("json data detected...")
        return 0
    else:
        print("non-json data detected...")
        return 1
    
if __name__ == "__main__":
    main()