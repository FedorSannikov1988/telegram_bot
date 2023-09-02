import json
from pathlib import Path


def load_answer_for_user(path_for_file: str | Path):

    try:
        with open(path_for_file, 'r', encoding='utf-8') as file_read_json:
            read_dict: dict = json.load(file_read_json)
            return read_dict

    except FileNotFoundError:
        empty_dict: dict = {}
        with open(path_for_file, 'w', encoding='utf-8') as file_create_json:
            json.dump(empty_dict, file_create_json)
        print('файл пуст')


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
    # нужно ли и можно ли оставлять такие хвосты
    # (я имею в виду if __name__ == '__main__':)
    # или после удачного тестирования безжалостно
    # удалять ?
    all_answer_for_user_path = Path('data_storage_text', 'users_answers.json')
    all_answer_for_user: dict = \
        load_answer_for_user(path_for_file=
                             all_answer_for_user_path)
    print(all_answer_for_user)
    
    all_urls_path = Path('data_storage_text', 'urls.json')
    all_urls: dict = \
        load_answer_for_user(path_for_file=
                             all_urls_path)
    print(all_urls)
