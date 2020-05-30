import re
import gluonnlp as nlp

moses_tokenizer = nlp.data.SacreMosesTokenizer()

corpus = open('corpus-annot.txt', 'r').read()
splitted_corpus = corpus.split('<eos>')

corpus_orig = open('corpus_orig.txt', 'a')
corpus_masked = open('corpus_masked.txt', 'a')

for function in splitted_corpus:
    start = re.findall('def\s+[a-zA-Z_\-1-9]+\s?\(.+\).*:', function)
    if start:
        start = start[0]
        if '[' not in start:
            try:
                if '->' in start:
                    remove_return_type = re.split('(->\s*)(.+)(:)', start)
                    return_type_content = moses_tokenizer(remove_return_type[2])
                    return_masked = ''.join([remove_return_type[0], remove_return_type[1]] + [' '.join(['MASKTOKEN' for mask in return_type_content])] + [remove_return_type[3]])
                else:
                    return_masked = start
                remove_args_type = re.split('(\(.+\))', return_masked)
                args = re.split(',', remove_args_type[1][1:-1])
                args_splitted = []
                for arg in args:
                    arg_splitted = re.split(':', arg)
                    if len(arg_splitted) == 1:
                        args_splitted.extend(arg_splitted)
                    else:
                        type_content = moses_tokenizer(arg_splitted[1])
                        args_splitted.append(arg_splitted[0]+': '+' '.join(['MASKTOKEN' for mask in type_content]))
                result = remove_args_type[0] + '(' + ','.join(args_splitted) + ')' + remove_args_type[2]
                if len(moses_tokenizer(function+'<eos>')) == len(moses_tokenizer(result+function[len(start):]+'<eos>')):
                    corpus_orig.write(function+'<eos>')
                    corpus_masked.write(result+function[len(start):]+'<eos>')
            except:
                pass
