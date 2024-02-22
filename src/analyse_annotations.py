#!/usr/bin/env python
# -*- coding: utf8 -*-

''''Analyse annotation results'''

import random
from tabulate import tabulate
from sklearn.metrics import cohen_kappa_score
random.seed(45)


def get_annotations(in_file, idx):
    '''Read in annotations from tab-separated file'''
    return [x.strip().split('\t')[idx] for x in open(in_file, 'r', encoding="utf-8")][1:]


def get_info(in_file):
    '''Read the information from tab-separated file'''
    anno = []
    corpora = []
    sents = []
    for line in open(in_file, 'r', encoding="utf-8"):
        line = line.strip().split('\t')
        anno.append(line[-2])
        corpora.append(line[-3])
        sents.append(line[0])
    return anno, corpora, sents


def numbers_per_corpus(all_corpora, anno_options, res):
    '''Get the numbers per subcorpus'''
    full_res = []
    full_print = []
    # Loop over all corpora to get results for each
    for corpus in all_corpora:
        results = []
        for an in anno_options:
            results.append(res[corpus].count(an))
        # Add RT + PT as separate number
        results.append(results[-2] + results[-1])
        full_res.append(results)
        print_str = [corpus] + [str(x) for x in results]
        full_print.append(print_str)
    return full_print


def show_results(anno, single_double, corpora, all_corpora, lang, sents):
    '''Get all the annotation results here and print them in an aggregated table'''
    anno_options = ["WLN", "NRT", "PRT", "RTE", "PT"]
    print_t = [f"For {lang}"] + anno_options + ["RT+PT"]

    res = {}
    # Each corpus has a list of annotations
    for corp in all_corpora:
        res[corp] = []

    # Double annotations we select randomly, so we have to keep track
    seen_sents_not_picked = {}
    seen_sents_picked = {}
    rand_nums = [i for i in range(0,len(anno))]
    random.shuffle(rand_nums)
    added_double = 0
    for idx, an in enumerate(anno):
        if single_double[idx] == "double":
            # Randomly decide if we take this annotation
            # If we don't, we have to keep track of this
            # Since we will not select it later
            if sents[idx] in seen_sents_not_picked:
                # We already skipped this annotation, so keep it now
                res[corpora[idx]].append(an)
                added_double += 1
            elif sents[idx] in seen_sents_picked:
                # Already seen and used, skip
                pass
            else:
                # New sentence, not seen before, 50/50 if we keep it, or take the next
                # Randomization is done by checking is shuffled list of 0-200 is even/uneven
                # This makes it reproducible
                if rand_nums[idx] % 2 == 0:
                    res[corpora[idx]].append(an)
                    seen_sents_picked[sents[idx]] = 1
                    added_double += 1
                else:
                    seen_sents_not_picked[sents[idx]] = 1
        else:
            res[corpora[idx]].append(an)

    # For each subcorpus, get the numbers
    full_print = numbers_per_corpus(all_corpora, anno_options, res)

    # Print a nice looking table
    print(tabulate(full_print, headers=print_t, tablefmt="fancy_grid"))


def compare_annotations(d1, d2):
    '''Compare annotations of two annotators and return statistics'''
    same, total = 0, 0
    a1 = []
    a2 = []
    for key in d1:
        if key not in d2:
            raise ValueError("Double annotation not found")
        # Always add 1 for the total, only add 1 to same
        # if annotations are the same
        total += 1
        if d1[key] == d2[key]:
            same += 1
        a1.append(d1[key])
        a2.append(d2[key])
    return same, total, a1, a2


def inter_annotator(anno1, anno2, single_double1, single_double2, sents1, sents2):
    '''Calculate how often anno1 and anno2 agree'''

    # First agregate all double annotations and save in dict
    d1 = {}
    d2 = {}
    for idx, (a1, a2) in enumerate(zip(anno1, anno2)):
        if single_double1[idx] == "double":
            d1[sents1[idx]] = a1
        if single_double2[idx] == "double":
            d2[sents2[idx]] = a2

    # Now loop over the annotations and compare
    same, total, a1, a2 = compare_annotations(d1, d2)

    # Return percentage of overlap and cohens kappa score
    overlap =  round(float(same) / float(total) * 100, 1)
    ck_score = round(cohen_kappa_score(a1, a2), 3)
    return overlap, ck_score


def mono():
    '''Analysis of the mono-lingual manual annotation experiments'''
    for lang in ["sq", "bg", "bo", "hr", "is", "mk", "mt", "me", "sr", "tr"]:
        # Read in annotator 1 and 2
        anno1 = get_annotations(f"anno/annotator1.tsv.shuf.{lang}.eval.tsv", 2)
        anno2 = get_annotations(f"anno/annotator2.tsv.shuf.{lang}.eval.tsv", 2)
        assert len(anno1) == len(anno2)

        # Filenames differ so make sure to fix this
        if lang == "bo":
            other_lang = "bs"
        elif lang == "me":
            other_lang = "cnr"
        else:
            other_lang = lang

        # Read in original .shuf file so we can get the corpus information back
        anno1_file = f"anno/annotator1_with_info.tsv.shuf.{other_lang}"
        anno2_file = f"anno/annotator2_with_info.tsv.shuf.{other_lang}"
        single_double1, corpora1, sents1 = get_info(anno1_file)
        single_double2, corpora2, sents2 = get_info(anno2_file)
        assert len(single_double1) == len(single_double2) == len(anno1)

        # # Get unique corpora that we have for this language
        corpora = sorted(list(set(corpora1)))

        # Per individual annotator
        print (f"\nFor {lang} (annotator 1):\n")
        show_results(anno1, single_double1, corpora1, corpora, lang, sents1)
        print (f"\nFor {lang} (annotator 2):\n")
        show_results(anno2, single_double2, corpora2, corpora, lang, sents2)

        # Loop over corpora and get annotations per corpus
        # Treat anno1 and anno2 as a single annotator, but only for single annotations
        print (f"\nFor {lang} (combined):\n")
        show_results(anno1 + anno2, single_double1 + single_double2, 
                     corpora1 + corpora2, corpora, lang, sents1 + sents2)

        # Get inter-annotator agreement scores
        overlap, ck_score = inter_annotator(anno1, anno2, single_double1, 
                                            single_double2, sents1, sents2)
        print (f"\n{lang}: overlap of {overlap}% and cohen-kappa of {ck_score}\n")


if __name__ == "__main__":
    mono()
