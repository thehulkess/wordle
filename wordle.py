import random
import sys

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

l_dedup = {}
def score_freq_sum(word, frequency):
    sum = 0
    for c in l_dedup[word]:
            sum = sum + frequency[c]
    return sum

def score_freq_max(word, frequency):
    max = 0
    seen = set()
    for c in word:
        if c not in seen:
            if max < frequency[c]:
                max = frequency[c]
            seen.add(c)
        else:
            pass
    return max

def score_random(word, frequency):
    return random.random()

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

def generate_guess(l):
    f = frequencies(l)
    max_score = 0
    max_word = None

    for w in l:
        score = score_freq_sum(w,f)
        if score > max_score:
            max_score = score
            max_word = w

    return max_word

def arrange_list(l):
    f = frequencies(l)
    l.sort(key=lambda x: score_freq_sum(x,f), reverse=True)

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

word_file = open('words.txt', 'r')
raw_lines = word_file.readlines()
lines = []
# Strips the newline character
for line in raw_lines:
    if len(line) == 6:
        line = line.strip().lower()
        lines.append(line)
    
l = lines

for w in l:
    chrs = set()
    for c in w:
        chrs.add(c)
    l_dedup[w] = chrs

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
    ftable = {}
    
    for word in lines:
        l = lines.copy()
        count = 0
        while True:
            guess = generate_guess(l)
            count = count + 1
            res = eval_guess(word, guess)
            if res == "GGGGG":
                break
            l = filter_list(l, res, guess)
        sum = sum + count
        if count > max:
            max = count
        if count in ftable:
            ftable[count] = ftable[count]+1
        else:
            ftable[count] = 1
        wcount = wcount + 1

    print("Words\tGuesses\tAvg\tMax")
    print(wcount,"\t", sum, "\t", round(sum/wcount,2), "\t", max)
    print("\n\nCount\tFrequency\n---")
    sum_failed = 0
    for k in sorted(ftable):
        print(k,"\t",ftable[k])
        if k > 6:
            sum_failed = sum_failed + ftable[k]

    print("\nPercent of words that will not be solved in 6 guesses: ",
          round((sum_failed*100)/wcount,2))
            
else:    
    while True:
        word = generate_guess(l)
        print("Try: ", word, " (choosen out of: ",len(l),")")
        while True:
            inp = input("Result: ")
            if inp == "naw":
                l.remove(l[0])
                word = generate_guess(l)
                print("Try: ",word)
            else:
                break
        if inp == "GGGGG":
            print("yay!")
            exit(0)
        l = filter_list(l, inp, word)
