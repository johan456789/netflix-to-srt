import os
import argparse
import codecs
import pysrt
from tqdm import tqdm

from to_srt import to_srt
from strip_html import strip_html
from stack_srt import stack_subs

SUPPORTED_EXTENSIONS = [".xml", ".vtt"]

if __name__ == "__main__":
    directory = "."
    help_text = u"path to the {} directory (defaults to current directory)"
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=directory,
                        help=help_text.format("input", directory))
    parser.add_argument("-o", "--output", type=str, default=directory,
                        help=help_text.format("output", directory))
    a = parser.parse_args()
    filenames = [fn for fn in os.listdir(a.input)
                 if fn[-4:].lower() in SUPPORTED_EXTENSIONS]

    for fn in tqdm(filenames):
        with codecs.open("{}/{}".format(a.input, fn), 'rb', "utf-8") as f:
            text = f.read()
            text = to_srt(text, fn[-4:])
            text = strip_html(text)
            subs = stack_subs(pysrt.from_string(text))
            subs.save("{}/{}.srt".format(a.output, fn), encoding='utf-8')
