# TimingGames
Simulation for timing games.

## clone git repository
- In the terminal, navigate to a directory where you wish to clone this git repository to.
- Run `git clone https://github.com/biubiuworld/TimingGames.git`

## install package
- In the terminal, navigate to the directory where this git repository is cloned at.
- Run `pip install -e timing_games_package` in the terminal.
- If seeing `command not found: pip`, try `pip3 install -e timing_games_package`.
- After installation, run `pip list` or `pip3 list` and make sure `timing_games_package` is on the Python package list.

## modules
- `Configuration` - set up simulation configuration parameters
- `Functions` - contain various commonly-used low level functions.
- `Simulation` - contain high level simulation functions.

## run simulation
- If `jupyter notebook` is not installed, in the terminal, run `pip install notebook` or `pip3 install notebook`.
- Make a copy of Timing_game_simulation.ipynb in this folder and open it in Jupyter Notebook 

## update package
- In the terminal, navigate to the directory where this git repository is cloned at.
- Run `git pull` in the terminal.
- Run `pip install --upgrade timing_games_package` in the terminal.
- If seeing `command not found: pip`, try `pip3 install --upgrade timing_games_package`.