import glob
from argparse import ArgumentParser
from similarity_checker import calculate_similarity

def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('check_file', help='File to check for plagiarism')
    parser.add_argument('check_dir', help='Dir to search for similar files')

    return parser.parse_args()

def main():
    args = parse_arguments()
    check_file = args.check_file
    check_dir = args.check_dir

    docxs_in_dir = glob.glob(f'{check_dir}/*.docx')

    if len(docxs_in_dir) == 0:
        print('No docx files in specified dir')
        exit()

    for item in calculate_similarity(check_file, docxs_in_dir):
        print(f'{item[1]}% - {item[0]}')

if __name__ == '__main__':
    main()