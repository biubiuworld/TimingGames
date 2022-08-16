# TimingGames
Simulation for timing games.

# 1 Install package and run simulation
## 1.1 clone git repository
- In the terminal, navigate to a directory where you wish to clone this git repository to.
- Run `git clone https://github.com/biubiuworld/TimingGames.git`

## 1.2 install package
- In the terminal, navigate to the directory where this git repository is cloned at.
- Run `pip install -e timing_games_package` in the terminal.
- If seeing `command not found: pip`, try `pip3 install -e timing_games_package`.
- After installation, run `pip list` or `pip3 list` and make sure `timing_games_package` is on the Python package list.

## 1.3 modules
- `Configuration` - set up simulation configuration parameters
- `Functions` - contain various commonly-used low level functions.
- `Simulation` - contain high level simulation functions.

## 1.4 run simulation
- If `jupyter notebook` is not installed, in the terminal, run `pip install notebook` or `pip3 install notebook`.
- Make a copy of Timing_game_simulation.ipynb in this folder and open it in Jupyter Notebook 

## 1.5 update package
- In the terminal, navigate to the directory where this git repository is cloned at.
- Run `git checkout`, then run `git fetch`, and finally run `git pull`
- Run `pip install --upgrade timing_games_package` in the terminal.
- If seeing `command not found: pip`, try `pip3 install --upgrade timing_games_package`.


# 2 Run simulation on jupyter notebook without installing package
## 1.1 install packages
- Open a terminal.
- Run `pip install -U pip setuptools` or `pip3 install -U pip setuptools`.
- Run `python3 -m pip install numpy`.
- Run `python3 -m pip install matplotlib`.
- Run `python3 -m pip install pandas`.

## 1.2 download script file
- Download 'TimingGames_simulation_version1.1.ipynb'.

## 1.3 open jupyter notebook
- Run `python3 -m notebook` in the terminal to open jupyter notebook in a new browser.
- Open the downloaded file through the new browser.
- Run the script based on the instructions inside the file. 
