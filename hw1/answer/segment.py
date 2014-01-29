#since we have up to 4-grams in the training data, we may use 4-grams model
import sys, codecs


prob = {}
N = float(0.0) 

def probGen(path):
    global prob, N    
    lines = codecs.open(path,"r",encoding="utf-8").readlines()
    for line in lines:
        freq = float(line.split()[0])
        N = N + freq
    for line in lines:
        w = line.split()
        char = w[1]
        p = float(w[0])/N
        t = {char: p}
        prob.update(t)
    
def Pw(word):
    try:
        return prob[word]
    except:
        
        return 10./(N*10000**len(word))
        
def splits(charlist, L=20):
    return [("".join(charlist[:s+1]), "".join(charlist[s+1:]))
            for s in range(min(len(charlist),L))]

def Pwords(words):
    product = 1
    for w in words:
        product = product * Pw(w)
    return product
    
def memo(f):
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo
    
@memo
def segment(sentence):
    if not sentence: return []
    charlist = list(sentence)   
    candidates = [[first]+segment(rem) for first,rem in splits(charlist)]
    return max(candidates, key=Pwords)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        old = sys.stdout
        sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
        # ignoring the dictionary provided in sys.argv[1]
        probGen(sys.argv[0])
        for line in sys.stdin:
            line = line[:-1]
            s = ""
            for w in segment(line.rstrip()):
                s = s + " " + w
            print s
        sys.stdout = old
    else:
        print >>sys.stderr, "usage: python", sys.argv[0], "frequencies < inputfile"
    
