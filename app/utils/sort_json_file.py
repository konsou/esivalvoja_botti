import json


def sort_json_file(filename: str) -> None:
    with open(filename, encoding='utf-8') as f:
        contents = json.load(f)

    print(contents)
    print(list(contents))

    list_to_sort = []
    for key, value in contents.items():
        list_to_sort.append((key, value))

    print(list_to_sort)
    sorted_list = sorted(list_to_sort)
    print(sorted_list)

    json_string = "{\n"
    for item in sorted_list:
        escaped_list = str(item[1]).replace('"', '\\"')
        json_string = f'{json_string}  "{item[0]}": {escaped_list},\n'

    json_string = json_string[:-2]
    json_string = json_string + "\n}"

    json_string = json_string.replace("'", '"')

    with open(f"{filename}-ordered.json", 'w', encoding='utf8') as f:
        f.write(json_string)


if __name__ == '__main__':
    sort_json_file('../json_data/string_replacements.json')
