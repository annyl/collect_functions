from git import Repo
import json
import os
import shutil
from multiprocessing import Pool

from extract_functions_dir import extract_functions_from_project


def collect_functions(start_repo_num):
    for day in range(15, 16):
        date = '2020-04-' + str(day)
        print('Processing date ', date)
        os.mkdir(date)
        os.mkdir(date)

        with open(date + '.txt', 'r') as json_file:
            data_file = json.load(json_file)
        print(len(data_file[date]))
        for i in range(start_repo_num, start_repo_num+684): #up to 2000 for 04-10
            repo_name = data_file[date][i]['name']
            assert isinstance(i, object)
            print(repo_name, i)
            try:
                Repo.clone_from(data_file[date][i]['clone_url'], date+'/'+repo_name)

                functions = extract_functions_from_project(date+'/'+repo_name)
                if len(functions) > 0:
                    final_text = '</==/>\n'.join(functions)
                    file_to_write = open(date + '/' + repo_name + '.py', 'w')
                    file_to_write.write(final_text)
                    file_to_write.close()
                shutil.rmtree(date+'/'+repo_name, ignore_errors=True)
            except:
                continue


if __name__ == '__main__':
    with Pool(3) as p:
        print(p.map(collect_functions, [4450, 5134, 5818]))


