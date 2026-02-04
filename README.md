# Raspberry Pi Pico Experiments
The project's prupose is to allow testing things on the raspberry pi pico as fast as possible and to then transform the gained knowledge into production ready code in a standalone project.

## Tips & Tricks

### Copying / running code on the pico
0. cd into project folder
1. python -m venv venv creates a virtual environment
2. source ./venv/bin/activate activates the virtual environment
3. pip install -r requirements.txt (installs all packages)
4. Make sure you'r in your python environment (venv activated).
5. Make sure mpremote is installed (via pip install mpremote).
6. copy file to raspberry pi pico: mpremote cp main.py :main.py
7. start the script: mpremote reset

8. pip freeze > requirements.txt (updates the package file with newly installed packages)

### Running with print output
1. mpremote cp main.py :main.py
2. mpremote repl
3. (inside repl:) exec(open('main.py').read())
4. executing 3. also brings everything into scope from the main.py file
5. Alternative: a soft reset (control-d) does the same as 3.

### Connecting to the python repl
1. Connect the raspberry pi without pressing the button (its only for firmware flashing)
2. make sure nothing runs currently by running i.e.: mpremote ls
2. mpremote repl
3. (alternative to the 2.:) screen /dev/tty.usbmodem1101 115200
2. exit with control-a-k and the press 'y' to confirm

### Flash / install packages, drivers, libraries or other micropython shit
1. mpremote mip install ssd1306
