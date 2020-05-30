import re
import os

def extract_functions_from_file(file_path):

    source = open(file_path, "r", errors='ignore').readlines()

    def get_indent_level(s):
        indent = re.findall(r'^\s*', s)
        indent_lvl = len(indent[0])
        return indent_lvl

    def get_function_body(start_line_index, source_code):
        indent_level = get_indent_level(source_code[start_line_index])
        function = source_code[start_line_index][indent_level:]
        for line_index in range(start_line_index+1, len(source_code)):
            if source_code[line_index] == '\n':  # empty line
                continue
            # if source_code[line_index].startswith('#'):  # comment
            #     continue
            else:
                indent_level_body = get_indent_level(source_code[line_index])
                if indent_level_body > indent_level:
                    function += source_code[line_index][indent_level:]
                else:
                    break
        return function

    functions = []
    for line_index in range(len(source)):
        if re.match(r'^\s*def\s', source[line_index]): #function start
            functions.append(get_function_body(line_index, source))

    return functions


def extract_functions_from_project(project_path):
    functions_list = []
    for name in os.listdir(project_path):
        obj_path = project_path + '/' + name
        if os.path.isdir(obj_path):
            functions_list.extend(extract_functions_from_project(obj_path))
        if os.path.isfile(obj_path) and name.endswith('.py'):
            # files_list.append(obj_path)
            functions_list.extend(extract_functions_from_file(obj_path))
    return functions_list

repos_names = os.listdir('2020-04-11')
print(len(repos_names))
for repo_index in range(178, len(repos_names)):
    if os.path.isdir('2020-04-11/'+repos_names[repo_index]):
        print(repos_names[repo_index], repo_index)
        functions = extract_functions_from_project('2020-04-11/'+repos_names[repo_index])
        final_text = '</==/>\n'.join(functions)
        file_to_write = open('extracted_functions/'+repos_names[repo_index]+'.py', 'w')
        file_to_write.write(final_text)
        file_to_write.close()
