import os
import re

ext_func_path = '/Volumes/MyPassport/extracted_functions/'

for dirname in os.listdir(ext_func_path):
    date_dir_path = os.path.join(ext_func_path + dirname)
    if os.path.isdir(date_dir_path):
        annot_path = os.path.join(date_dir_path, 'annot_functions')
        if os.path.exists(annot_path):
            continue
        else:
            os.mkdir(annot_path)
            annot_func_path = os.path.join(date_dir_path, 'annot_functions')
            repos_files = os.listdir(date_dir_path)
            for i in range(len(repos_files)):
                name = repos_files[i]
                obj_path = os.path.join(date_dir_path, name)
                print("Processing the following file: {}, {}".format(obj_path, i))
                if os.path.isfile(obj_path) and name.endswith('.py'):
                    file = open(obj_path, 'r', errors="ignore").read()
                    functions = file.split('</==/>\n')
                    functions_annot = []
                    for function in functions:
                        add = False
                        first_line = function.split('\n')[0]
                        first_line = first_line.split('#')[0] # remove comments
                        if first_line.count(':') > 1 or '->' in first_line:
                            first_line = ''.join(re.split("\'.*:.*\'", first_line)) # semicolon may be contained in a string
                            first_line = ''.join(re.split('\".*:.*\"', first_line))
                            first_line = ''.join(re.split("lambda\s+[a-zA-Z_,\s]+\s*:", first_line)) # semicolon may be contained in lambda definition
                            first_line = ''.join(re.split("\[[-\d\s\+:]*\]", first_line)) # intervals may contain semicolon
                            if first_line.count(':') > 1 or '->' in first_line:
                                functions_annot.append(function)
                    if len(functions_annot) > 0:
                        final_text = '</==/>\n'.join(functions_annot)
                        file_to_write = open(os.path.join(annot_func_path, name), 'w')
                        file_to_write.write(final_text)
                        file_to_write.close()
