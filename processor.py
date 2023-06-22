import argparse
import re


def trim_blanks(text_lines):
    return [line.strip() for line in text_lines if line.strip()]


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def write_file(filename, content):
    content += '\n'
    with open(filename, 'w') as f:
        f.write(content)


def complete(text_lines):
    newlines = []

    for line in text_lines:
        newline = line

        newline = re.sub(r' *… *', ' … ', newline)
        newline = re.sub(r'sb.?', 'sb.', newline)
        newline = re.sub(r'sth.?', 'sth.', newline)

        if ' … ' in newline:
            newlines.append(newline.replace(' … ', '…'))

        newlines.append(newline)

    return newlines


def uniquefy_lines(text_lines):
    line_set = set(text_lines)
    return list(line_set)


def parse_args():
    parser = argparse.ArgumentParser(description='Processing text.')
    parser.add_argument('filepaths',
                        metavar='filepath',
                        type=str,
                        nargs='+',
                        help='input an absolute or a relative filepath')
    parser.add_argument('-c', '--complete',
                        dest="should_complete",
                        action='store_true',
                        help='complete "sb" -> "sb.", "sth" -> "sth." etc.')
    parser.add_argument('-o', '--override',
                        dest="should_override",
                        action='store_true',
                        help='override the original file, otherwise simply'
                        + ' print the result')
    parser.add_argument('-s', '--sort',
                        dest="should_sort",
                        action='store_true',
                        help='sort all lines in alphabetical order')

    return parser.parse_args()


def main():
    args = parse_args()

    for fp in args.filepaths:
        text = read_file(fp)
        text_lines = text.split('\n')

        text_lines = trim_blanks(text_lines)

        if args.should_complete:
            text_lines = complete(text_lines)

        text_lines = uniquefy_lines(text_lines)

        if args.should_sort:
            text_lines = sorted(text_lines)

        text = '\n'.join(text_lines)
        if args.should_override:
            write_file(fp, text)
        else:
            print(text)


if __name__ == '__main__':
    main()
