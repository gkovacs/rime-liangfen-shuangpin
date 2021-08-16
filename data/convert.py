#!/usr/bin/env python3

from Pinyin2Hanzi import all_pinyin

all_pinyin_set = set(all_pinyin())

all_pinyin_set.add('yue')
all_pinyin_set.add('xue')
all_pinyin_set.add('jue')
all_pinyin_set.add('que')
all_pinyin_set.add('lue')

all_pinyin_set.remove('lo')

# from https://github.com/district10/shuangpin-heatmap/blob/master/data/shuangpin.json

shuangpin = {
 "sheng": {
     "b": "b",
     "c": "c",
     "d": "d",
     "f": "f",
     "g": "g",
     "h": "h",
     "j": "j",
     "k": "k",
     "l": "l",
     "m": "m",
     "n": "n",
     "p": "p",
     "q": "q",
     "r": "r",
     "s": "s",
     "t": "t",
     "w": "w",
     "x": "x",
     "y": "y",
     "z": "z",
     "ch": "i",
     "sh": "u",
     "zh": "v"
 },
 "yun": {
     "a": "a",
     "ai": "d",
     "an": "j",
     "ang": "h",
     "ao": "c",
     "e": "e",
     "ei": "w",
     "en": "f",
     "eng": "g",
     "i": "i",
     "ia": "x",
     "ian": "m",
     "iang": "l",
     "iao": "n",
     "ie": "p",
     "iong": "s",
     "in": "b",
     "ing": "k",
     "iu": "q",
     "o": "o",
     "ong": "s",
     "ou": "z",
     "u": "u",
     "ua": "x",
     "uai": "k",
     "uan": "r",
     "uang": "l",
     "ue": "t",
     "ui": "v",
     "un": "y",
     "uo": "o",
     "v": "v",
     "ve": "t"
 },
 "other": {
     "a": "aa",
     "ai": "ai",
     "an": "an",
     "ang": "ah",
     "ao": "ao",
     "e": "ee",
     "ei": "ei",
     "en": "en",
     "eng": "eg",
     "er": "er",
     "o": "oo",
     "ou": "ou"
 }
}


# invalid = set([
#   'bs',
#   'bx',
#   'bv',
#   'bt',
#   'cx',
#   'ck',
#   'cl',
#   'ct',
# ])

manual_mapping = {
  'jue': 'jt',
  'que': 'qt',
  'yue': 'yt',
  'xue': 'xt',
  'lue': 'lt',
}

keys_to_pinyin = {}
pinyin_to_keys = {}
for sheng_pinyin,sheng_key in shuangpin['sheng'].items():
  for yun_pinyin,yun_key in shuangpin['yun'].items():
    key = sheng_key + yun_key
    pinyin = sheng_pinyin + yun_pinyin
    if pinyin not in all_pinyin_set:
      continue
    if pinyin in manual_mapping:
      continue
    if key in keys_to_pinyin:
      print(key, keys_to_pinyin[key], pinyin)
    if pinyin in pinyin_to_keys:
      print(key, keys_to_pinyin[key], pinyin)
    keys_to_pinyin[key] = pinyin
    pinyin_to_keys[pinyin] = key
for pinyin,key in shuangpin['other'].items():
  if key in keys_to_pinyin:
    print(key, keys_to_pinyin[key], pinyin)
  if pinyin in pinyin_to_keys:
    print(key, keys_to_pinyin[key], pinyin)
  keys_to_pinyin[key] = pinyin
  pinyin_to_keys[pinyin] = key
for pinyin,key in manual_mapping.items():
  keys_to_pinyin[key] = pinyin
  pinyin_to_keys[pinyin] = key


output = []
at_start = True

for line in open('liangfen.dict.yaml', 'rt'):
  if at_start:
    if line.strip() == 'name: liangfen':
      output.append('name: liangfen_shuangpin\n')
      continue
    if line.strip() == '...':
      at_start = False
    output.append(line)
    continue
  if '\t' not in line:
    output.append(line)
    continue
  char,pinyin = line.split('\t')
  char = char.strip()
  pinyin = pinyin.strip()
  keys_list = []
  for pinyin1,keys1 in pinyin_to_keys.items():
    if not pinyin.startswith(pinyin1):
      continue
    for pinyin2,keys2 in pinyin_to_keys.items():
      if pinyin1+pinyin2 == pinyin:
        keys_list.append(keys1 + keys2)
  #if len(keys_list) > 1:
  #  #print('more than one way to enter:', char, pinyin)
  if len(keys_list) == 0:
    #print('cannot enter', char, pinyin)
    continue
  for keys in keys_list:
    output.append(char + '\t' + keys + '\n')

outfile = open('../liangfen_shuangpin.dict.yaml', 'wt')
for line in output:
  outfile.write(line)