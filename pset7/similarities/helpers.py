from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    a_lines = a.split('\n')
    b_lines = b.split('\n')
    
    return list({line for line in a_lines if line in b_lines})


def sentences(a, b):
    """Return sentences in both a and b"""

    a_sent = sent_tokenize(a)
    b_sent = sent_tokenize(b)
    
    return list({sent for sent in a_sent if sent in b_sent})


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    
    a_sub = [a[i:i+n] for i in range(len(a) - n + 1)]
    b_sub = [b[i:i+n] for i in range(len(b) - n + 1)]
    
    return list({sub for sub in a_sub if sub in b_sub})
