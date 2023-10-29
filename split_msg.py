from collections.abc import Generator
import argparse

from splitting import split_html, SPLITTER

MAX_LEN = 4096


def split_message(source: str, max_len=MAX_LEN) -> Generator[str]:
    '''Splits the original message (`source`) into fragments of the specified
    length (`max_len`).'''
    return split_html(source, max_len)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='My example explanation')
    parser.add_argument(
        '--max-len',
        type=int,
        default=MAX_LEN,
        help=f'maximum message length (default: {MAX_LEN})'
    )
    parser.add_argument(
        'file',
        type=str,
        help='file address'
    )

    params = parser.parse_args()
    file = open(params.file)
    result = split_message(file.read(), params.max_len)
    print(f'{SPLITTER}<hr>{SPLITTER}'.join(result))
