# diashow
a simple image viewer based on mdfind and PyQt6

there are 2 executables:
1. `diashow_mdfind.py` takes a pattern as argument and generates a json list of image paths using mdfind
2. `diashow_play.py` takes that json list and displays the images using PyQt6

both execs are based on `broiler` and both have .toml config files
