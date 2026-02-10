# diashow
a simple image viewer based on mdfind and PyQt6

there are 2 executables:
1. `diashow_mdfind.py` takes a pattern as argument and generates a json list of image paths using mdfind
2. `diashow_play.py` takes that json list and displays the images using PyQt6

both execs are based on `broiler` and both have .toml config files

by adding

`ds() { $HOME/code/diashow_mdfind.py "$1" && $HOME/code/diashow_play.py; }`

to your shell’s rc file, you can do things like:

$ `ds 'tag:mountain AND (tag:america OR tag:africa)'`

but you can also generate JSON lists of image paths on your own…
