# Lample and Connea follow Devlin et al. (2018) approach to pick 15% of subword randomly
# and replacing it by reserved word ([MASK])80% of the time, by a random work 10% of the time
# and remaining unchanged 10% of the time.
import re
import gluonnlp as nlp
import random
from collections import Counter


moses_tokenizer = nlp.data.SacreMosesTokenizer()
moses_detokenizer = nlp.data.SacreMosesDetokenizer()

corpus = open('corpus_orig.txt', 'r').read()
splitted_corpus = corpus.split('<eos>')
vocab = list(set(moses_tokenizer(' '.join(splitted_corpus))))
vocab_len = len(vocab)

corpus_masked = open('corpus_masked_15.txt', 'a')

for function in splitted_corpus:
    function_tokenized = moses_tokenizer(function)
    function_masked = []
    for token in function_tokenized:
        token_luck = random.randint(1, 200)
        if token_luck <= 30: #token is masked
            if token_luck <= 24:
                function_masked.append('MASKTOKEN')
            elif 25 <= token_luck <= 27:
                token_num = random.randint(0, vocab_len)
                function_masked.append(vocab[token_num])
            else:
                function_masked.append(token)
        else:
            function_masked.append(token)
    result = moses_detokenizer(function_masked)
    if len(moses_tokenizer(function + '<eos>')) == len(moses_tokenizer(result + '<eos>')):
        corpus_masked.write(result + '<eos>')
    else:
        print(moses_tokenizer(function + '<eos>'))
        print(moses_tokenizer(result + '<eos>'))
        print(result)




