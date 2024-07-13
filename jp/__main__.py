import argparse
from utils.manage_file import read_file
from utils.validate_json import tokenize
def main():
    # define parser
    parser = argparse.ArgumentParser(description="json parser")
    # add arguments
    parser.add_argument("filepath", type=str, help="path to parsable file.")
    # get the file path
    args = parser.parse_args()
    fp = args.filepath
    # read and tokenize the contents
    try:
        data = read_file(fp)
    except Exception:
        print(f"coudn't open file: {fp}")
        return 1
    try:
        tokens = tokenize(data)
        # report to user
        if tokens == None:
            print("Non-json or defected data detected")
            return 2
        else:
            print(tokens)
    except Exception:
        print("Something went wrong:(")
        return 3
    
    
    return 0

if __name__ == "__main__":
    main()