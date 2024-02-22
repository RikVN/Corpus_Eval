#!/usr/bin/env python
# -*- coding: utf8 -*-

'''Extract data from the MaCoCu corpora

   Also transliterate Croatian/Serbian/Bosnian/Montenegrin data to latin'''

import sys
import argparse
import random
from prevert import dataset
from transliterate import translit
random.seed(34)

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", type=str, required=True,
                        help="Input file with MaCoCu corpus in XML format")
    parser.add_argument("-o", "--output_file", type=str, required=True,
                        help="Output file to write to")
    parser.add_argument("-l", "--languages", nargs="*", required=True,
                        help="Language iso codes, can be multiple, e.g. hbs_lat and hbs_cyr")
    parser.add_argument("-k", "--keep", type=int, default=0,
                        help="Amount of shuffled instances we keep - default 0 means all")
    parser.add_argument("-m", "--min_length", type=int, default=1,
                        help="Keep paragraphs that have at least X tokens")
    args = parser.parse_args()
    return args


def shuffle_by_number(in_list):
    '''Shuffle in list by numbers'''
    nums = [num for num in range(len(in_list))]
    random.shuffle(nums)
    keep = []
    for num in nums:
        keep.append(in_list[num] + [str(num)])
    return keep


def main():
    '''Main function'''
    args = create_arg_parser()

    # Use the prevert package to easily load data
    data_set = dataset(args.input_file)
    paras = []
    lengths = []
    too_short = 0

    # Loop over all documents
    for idx, doc in enumerate(data_set):
        if idx % 1000000 == 0 and idx > 0:
            print (f"Processed {idx} docs, saved {len(paras)} paragraphs")

        # Only take documents if it's in the correct language
        if eval(doc.meta['lang_distr'])[0][0] in args.languages:
            # Loop over paragraphs and add them all
            for idx_par, par in enumerate(doc):
                str_par = str(par).strip()

                # Only keep if at least X tokens
                if len(str_par.split()) >= args.min_length:
                    lengths.append(len(str_par.split()))

                    # Do transliteration for Cyrillic documents that are recognized as hbs_cyr
                    # Treat them all as Serbian in the package
                    if "hbs_cyr" in args.languages and eval(doc.meta['lang_distr'])[0][0] == "hbs_cyr":
                        tr = translit(str_par, 'sr', reversed=True)
                        if tr != str_par:
                            str_par = tr
                    if str_par:
                        heading = par.meta["heading"] if 'heading' in par.meta else "no"
                        info = [str_par, par.meta["lm_score"], par.meta["id"], par.meta["quality"],
                                heading, doc.meta["url"], doc.meta["crawl_date"],
                                doc.meta["lang_distr"], len(str_par.split()), idx, idx_par]
                        paras.append([str(x) for x in info])
                else:
                    too_short += 1

    # Shuffle and print statistics
    print (f"Found {len(paras)} paragraphs, excluded {too_short} because of length < {args.min_length}\n")
    print (f"Average token length of all long enough paragraphs: {round(float(sum(lengths)) / float(len(lengths)), 1)}")
    paras_shuffled = shuffle_by_number(paras)
    keep_num = args.keep if (args.keep > 0 and args.keep < len(paras_shuffled)) else len(paras_shuffled)

    # Calculate lengths
    paras_shuffled = paras_shuffled[0:keep_num]
    keep_lengths = [int(x[-4]) for x in paras_shuffled]
    print (f"Average token length of all kept paragraphs ({len(paras_shuffled)}): {round(float(sum(keep_lengths)) / float(len(keep_lengths)), 1)}")

    # Write output
    print (f"\nKeep {keep_num} paragraphs and write to {args.output_file}")
    with open(args.output_file, "w", encoding="utf8") as out_f:
        for para in paras_shuffled:
            out_f.write("\t".join(para) + '\n')
    out_f.close()


if __name__ == '__main__':
    # For logging purposes
    print("Generated by command:\npython", " ".join(sys.argv)+'\n')
    main()
