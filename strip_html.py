import sys
from bs4 import BeautifulSoup
from tqdm import tqdm


def strip_html(s: str) -> str:
    soup = BeautifulSoup(s, features='lxml')
    s = ''.join(soup.findAll(text=True))
    return s

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Usage: python strip_html.py file1.txt [[file2.txt]...]')
        exit(1)

    for f in tqdm(sys.argv[1:]):
        with open(f, 'r+') as fp:
            data = strip_html(fp.read())
            fp.seek(0)
            fp.write(data)
            fp.truncate()
