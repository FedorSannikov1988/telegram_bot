import json
from pathlib import Path


def load_answer_for_user(path_for_file: str | Path):

    try:
        with open(path_for_file, 'r', encoding='utf-8') as f_r_j:
            read_dict: dict = json.load(f_r_j)
            return read_dict

    except FileNotFoundError:
        print('файл не найден')


path_for_urls = \
    Path('answers', 'users', 'data_storage_text', 'urls.json')
path_for_users_answers = \
    Path('answers', 'users', 'data_storage_text', 'users_answers.json')

all_answer_for_user: dict = \
    load_answer_for_user(path_for_file=
                         path_for_users_answers)
all_urls: dict = \
    load_answer_for_user(path_for_file=
                         path_for_urls)


if __name__ == '__main__':
    json_file_path = Path('data_storage_text', 'users_answers.json')
    all_answer_for_user: dict = \
        load_answer_for_user(path_for_file=
                             json_file_path)
    print(all_answer_for_user)

    json_file_path = Path('data_storage_text', 'urls.json')
    all_urls: dict = \
        load_answer_for_user(path_for_file=
                             json_file_path)
    print(all_urls)
