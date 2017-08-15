from database import Entry
from translator import GlosbeTranslator
import argparse
import sys


# Import functions; Very temporary.
# TODO: Addon system for import and export with indivitual modules.
#       Add parser entry for every addon.
def import_raw(args):
    tr = GlosbeTranslator('en', 'nl')
    for item in args:
        entry = tr.translate(item)
        entry.save()


def import_kobo(args):
    pass


def import_stdin():
    tr = GlosbeTranslator('en', 'nl')
    for line in sys.stdin:
        entry = tr.translate(line)
        entry.save()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Action', dest='action')

    parser_import = subparsers.add_parser(
            'import', help='Import new words into database')
    parser_import.add_argument(
            '-k', '--kobo', help='Import from kobo database file')
    parser_import.add_argument(
            '-r', '--raw', nargs='+',
            help='Import list of words, seperated with space')
    parser_import.add_argument('-i', '--stdin', action='store_true',
                               help='Import every line from stdin')

    parser_export = subparsers.add_parser(
                              'export', help='Export saved words to file')
    parser_export.add_argument('-o', '--output', help='Location to save file')
    parser_export.add_argument('-s', '--style', choices=['json', 'anki'],
                               default='json', help='The output style')

    args = parser.parse_args()
    if args.action == 'import':
        if args.raw:
            import_raw(args.raw)
        elif args.kobo:
            import_kobo(args.kobo)
        elif args.stdin:
            import_stdin()
    elif args.action == 'export':
        out = Entry.export(args.style)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(out)
        else:
            print(out)


if __name__ == '__main__':
    main()
