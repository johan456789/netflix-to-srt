from __future__ import annotations
import sys
import pysrt
from pysrt import SubRipFile
from tqdm import tqdm


def stack_subs(subs: SubRipFile) -> SubRipFile:
    remove_list = []  # list of unwanted indexes
    sub_index = subs[0].index  # existing starting index

    # stack subs with the same start and end time
    prev_start = subs[-1].start  # get a valid time for comparison
    prev_end = subs[-1].end
    append_index = -1
    for index, sub in enumerate(subs):
        cur_start = sub.start
        cur_end = sub.end
        if cur_start == prev_start and cur_end == prev_end:
            subs[append_index].text += '\n' + sub.text
            remove_list.append(index)
        else:
            append_index = index
        prev_start = cur_start
        prev_end = cur_end

    # remove orphaned subs in reverse order
    for index in remove_list[::-1]:
        del subs[index]

    # reindex remaining subs
    for index in range(len(subs)):
        subs[index].index = index + sub_index
    
    return subs


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Usage: python stack_srt.py file1.txt [[file2.txt]...]')
        exit(1)

    for f in tqdm(sys.argv[1:]):
        print(f)
        subs = pysrt.open(f)
        subs = stack_subs(subs)
        subs.save(f, encoding='utf-8')
