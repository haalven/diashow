#! /usr/bin/env python3

# collect absolut image paths (slides),
# by using the fast 'mdfind' tool in macOS,
# shuffle the paths,
# save the list to ~/.slides.json,
# syntax: diashow_mdfind <pattern>

import sys, pathlib, tomllib, argparse, subprocess, random, json

# ANSI SGR formatting sequences
def ft(code) -> str:
    return '\x1b[' + str(code) + 'm'
def fc(code) -> str:
    return ft('38;5;' + str(code))

# formatted warnings
def warn(msg):
    print(fc(196) + str(msg) + ft(0), file=sys.stderr)

# read configuration file
def read_configuration(my_path: pathlib.Path) -> dict:
    config_path = my_path.with_suffix('.toml')
    try:
        with open(config_path, 'rb') as f:
            return tomllib.load(f)
    except Exception as e:
        warn('TOML error: ' + str(e))
        return {}

# parse arguments
def get_arguments(my_name: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=my_name)
    parser.add_argument('PATTERN',
                        type=str,
                        help='see mdfind')
    return parser.parse_args()

# mdfind
def mdfind(pattern: str) -> list:
    shell_cmd = ('mdfind', pattern)
    returned = subprocess.run(shell_cmd, capture_output=True, text=True)
    result_list = returned.stdout.split('\n')
    while '' in result_list:
        result_list.remove('')
    return result_list

# json serialization
def json_save(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# main program
def main() -> int:

    # my path
    my_path = pathlib.Path(__file__)
    my_dir  = my_path.parent
    my_name = my_path.name

    # read TOML config
    config = read_configuration(my_path)

    # get the arguments
    arguments = get_arguments(my_name)

    # get the negative list
    negative_list = mdfind(str(config['negative']))

    # get the positive list
    result_list = mdfind(str(arguments.PATTERN))

    # filtered list
    filtered_list = [p for p in result_list if p not in negative_list]
    print('results:', len(filtered_list))

    # collect image files according to extension
    imgpath_list = []
    for item in filtered_list:
        imgpath = pathlib.Path(item)
        if imgpath.suffix.lower() in config['extensions']:
            imgpath_list.append(str(imgpath))

    # no images found
    if len(imgpath_list) == 0:
        warn('no image files found.')
        return 1
    else:
        imgpath_len = len(imgpath_list)

    # sort paths alphabetically
    sorted_list = sorted(imgpath_list)

    # shuffle the paths
    shuffled_list = random.shuffle(imgpath_list)

    # save the list
    if config['shuffled']:
        json_save(shuffled_list, config['slidesfile'])
    else:
        json_save(sorted_list, config['slidesfile'])

    print(f'found {imgpath_len} images')
    return 0

if __name__ == '__main__':
    sys.exit(main())
