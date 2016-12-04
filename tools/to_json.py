# -*- coding: utf-8 -*-
import re
import json

FILE = './data/raw_data.txt'
CYRILLIC = re.compile('^([\u0400-\u04ff]+)(.*)', re.DEBUG)
CHINESE = re.compile('[\u4e00-\u9fff]')

class WordItem(object):
    def __init__(self, word, variant, meaning):
        self.word = word
        self.variant = variant
        self.meaning = meaning
    def __str__(self):
        return self.word



def get_key_value_from_txt(filename=FILE):
    result = {}
    with open(filename, 'rb') as f:
        for line in f:
            data = line.decode('utf8').split(" = ")
            word = data[0]
            info = "".join(data[1:])
            variant_meaning = info.split("|")
            if len(variant_meaning) == 1: # no variant
                variant = []
                meaning = variant_meaning[0].strip()
            else:
                variant = []
                for var in variant_meaning[:-1]:
                    if CHINESE.search(var):
                        matcher = CYRILLIC.match(var)
                        meaning += matcher.groups()[1].strip()
                        variant.append(matcher.groups()[0])
                    else:
                        variant.append(var)
                # variant = variant_meaning[:-1]
                meaning = variant_meaning[-1]
                matcher = CYRILLIC.match(meaning)
                if matcher:
                    meaning = matcher.groups()[1].strip()
                    variant.append(matcher.groups()[0])


            result[word] = WordItem(word=word, variant=variant, meaning=meaning)
    return result


def reformat(word_item_dict, output='./data/json_data.json'):
    with open(output, 'wb') as f:
        json_str = json.dumps([v.__dict__ for v in word_item_dict.values()], ensure_ascii=False, indent=4)
        f.write(json_str.encode('utf-8'))

def format_check(word_item_dict):
    error_format_dict = {}
    for k, v in word_item_dict.items():
        for var in v.variant:
            if CHINESE.search(var):
                error_format_dict[k] = v
                break
    return error_format_dict


if __name__ == "__main__":
    word_info = get_key_value_from_txt()
    reformat(word_info)
