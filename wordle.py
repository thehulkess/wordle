import random
import sys

__words = []
__answers = []
__l_dedup = {}

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

def score_freq_sum(word, frequency):
    sum = 0
    for c in __l_dedup[word]:
            sum = sum + frequency[c]
    return sum

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

def _filter(x, in_, wrong, verboten):
    for k in in_:
        if x[k] != in_[k]:
            return False

    for k in wrong:
        if x[k] == wrong[k] or wrong[k] not in x:
            return False

    for k in verboten:
        if k in x:
            return False

    return True

def filter_list(l, inp, word):
    result = parse_input(inp, word)
    in_ = result['in']
    wrong = result['wrong']
    verboten = result['verboten']

    return [x for x in l if _filter(x, in_, wrong, verboten)]

def generate_guess(l):
    f = frequencies(l)
    max_score = -1
    max_word = None

    for w in l:
        score = score_freq_sum(w,f)
        if score >= max_score:
            max_score = score
            max_word = w

    return max_word

def eval_guess(word, inp):
    res = ''

    if inp not in __words:
        return 'naw'

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

def load_word_list(fn, l):
    word_file = open(fn, 'r')
    raw_lines = word_file.readlines()

    for line in raw_lines:
        line = line.strip().lower()
        if len(line) == 5:
            l.append(line)

def load_words():
    for w in __answers:
        __words.append(w)

    load_word_list('wordle-words.txt', __words)

def load_answers():
    load_word_list('wordle-answers.txt', __answers)

def init():
    load_answers()
    load_words()

    for w in __words:
        chrs = set()
        for c in w:
            chrs.add(c)
        __l_dedup[w] = chrs

def play():
    l = __answers
    word = random.choice(l)
    while True:
        inp = input("Guess: ")
        res = eval_guess(word, inp)
        print(res)
        if res == 'GGGGG':
            print('yay')
            exit(0)

def test():
    sum = 0
    max = 0
    wcount = 0
    ftable = {}

    for word in __answers:
        l = __answers.copy()
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

def cheat():
    l = __answers
    while True:
        word = generate_guess(l)
        print("Try: ", word, " (chosen out of: ",len(l),")")
        inp = input("Result: ")
        if inp == "GGGGG":
            print("yay!")
            exit(0)
        if inp == "naw":
            l.remove(word)
        else:
            l = filter_list(l, inp, word)

init()

try:
    assert (sys.version_info[0] == 3), "Run with python version 3. Usage: python3 wordle.py"

except Exception as e:
    print (e)
    sys.exit(1)

if sys.argv[0] == 'play_wordle.py':
    play()
elif sys.argv[0] == 'test_wordle.py':
    test()
else:
    cheat()
