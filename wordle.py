import random
import sys

word_file = open('words.txt', 'r')
raw_lines = word_file.readlines()
lines = []
# Strips the newline character
for line in raw_lines:
    if len(line) == 6:
        line = line.strip().lower()
        lines.append(line)
    
def frequencies(lines):
    frequency = {}
    count = 0

    for l in lines:
        count = count + 5
        for c in l:
            if c not in frequency:
                frequency[c] = 0
            frequency[c] = frequency[c] + 1

    norm_frequency = {}
    for k in frequency:
        norm_frequency[k] = frequency[k] / count
    return norm_frequency

def score_freq(word, frequency):
    sum = 0
    seen = set()
    for c in word:
        if c not in seen:
            #if sum < frequency[c]:
            #    sum = frequency[c]
            sum = sum + frequency[c]
            seen.add(c)
        else:
            #sum = 0
            #break
            pass
    return sum

def score_random(word, frequency):
    return random.random()

def no_duplicates(word):
    char_set = set()
    for c in word:
        if c in char_set:
            return False
        else:
            char_set.add(c)
    return True

def parse_input(inp, word):
    result = {}
    verboten = set()
    in_place = {}
    wrong_place = {}

    result['verboten'] = verboten
    result['in'] = in_place
    result['wrong'] = wrong_place

    count = 0
    for c in inp:
        if c == 'G':
            in_place[count] = word[count]
        if c == 'R':
            verboten.add(word[count])
        if c == 'Y':
            wrong_place[count] = word[count]
        count = count + 1

    return result

def filter_list(l, inp, word):
    result = parse_input(inp, word)
    in_place = result['in']
    for k in in_place:
        l = list(filter(lambda x: x[k] == in_place[k], l))

    wrong_place = result['wrong']
    for k in wrong_place:
        l = list(filter(lambda x: x[k] != wrong_place[k] and wrong_place[k] in x, l))

    verboten = result['verboten']
    for k in verboten:
        l = list(filter(lambda x: not k in x, l))
    
    return l

def arrange_list(l):
    f = frequencies(l)
    l.sort(key=lambda x: score_freq(x,f), reverse=True)

def eval_guess(word,inp):
    res = ''
    count = 0
    for i in inp:
        if word[count] == i:
            res = res + 'G'
        elif i in word:
            res = res + 'Y'
        else:
            res = res + 'R'
        count = count + 1
    return res

    
l = lines

if sys.argv[0] == 'play_wordle.py':
    word = random.choice(l)
    while True:
        inp = input("Guess: ")
        res = eval_guess(word, inp)
        print(res)
        if res == 'GGGGG':
            print('yay')
            exit(0)

if sys.argv[0] == 'test_wordle.py':
    sum = 0
    max = 0
    wcount = 0
    for word in lines:
        l = lines.copy()
        count = 0
        while True:
            arrange_list(l)
            guess = l[0]
            count = count + 1
            res = eval_guess(word, guess)
            if res == "GGGGG":
                break
            #if count == 4:
                #print("failed with: ",word)
            #    break
            l = filter_list(l, res, guess)
        sum = sum + count
        if count > max:
            max = count
        wcount = wcount + 1
        #if wcount % 10 == 0:
        #    print(wcount, sum, sum/wcount, max)
        #if wcount == 2000:
        #    break
    print(wcount, sum, sum/wcount, max)
            
else:    
    while True:
        arrange_list(l)
        word = l[0]
        print("Try: ", word)
        while True:
            inp = input("result: ")
            if inp == "naw":
                l.remove(l[0])
                word = l[0]
                print("Try: ",word)
            else:
                break
        if inp == "GGGGG":
            print("yay!")
            exit(0)
        l = filter_list(l, inp, word)
