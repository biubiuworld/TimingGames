import Simulation
from Configuration import sim_config_init
from Functions import data_logging
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
from mpl_toolkits import mplot3d
matplotlib.use('Qt5Agg')

sim_idx = 0
jump_result = []
while sim_idx <= 2:
    if __name__ == '__main__':
        # Initialize a dictionary to store history data and game round index
        history = {}
        round_idx = 0

        # Set up simulation configuration
        sim_config = sim_config_init()

        # Simulate players' initial strategies and payoffs
        strategies, sample_sets = Simulation.initialize_player_strategies(sim_config)
        x, y, strat_x, strat_y = Simulation.calculate_payoff(sim_config, strategies, sample_sets)

        # Log data for the initial round
        # history = data_logging(['strategies', 'x', 'y', 'strat_x', 'strat_y'], round_idx, history) # To Do
        history['strategies', round_idx] = strategies
        history['x', round_idx] = x
        history['y', round_idx] = y
        history['strat_x', round_idx] = strat_x
        history['strat_y', round_idx] = strat_y
        history['max_strat_x'] = [max(strat_x)]
        history['min_strat_x'] = [min(strat_x)]
        history['avg_strat_x'] = [np.mean(strat_x)]

        history['max_strat_y'] = [max(strat_y)]

        # Iterate simulation to update players' strategies and payoff
        max_game_length = sim_config['game_length']
        while round_idx < max_game_length:
            round_idx += 1
            strategies = Simulation.update_player_strategies(x, y, strategies, sample_sets, sim_config)
            x, y, strat_x, strat_y = Simulation.calculate_payoff(sim_config, strategies, sample_sets)

            # Log data for the round
            history['strategies', round_idx] = strategies
            history['x', round_idx] = x
            history['y', round_idx] = y
            history['strat_x', round_idx] = strat_x
            history['strat_y', round_idx] = strat_y

            # Break simulation when detecting player's stretegy jump
            prev_max_strat_x = max(history['strat_x', round_idx-1])
            current_max_strat_x = max(strat_x)
            current_max_strat_y = max(strat_y)
            history['max_strat_x'].append(current_max_strat_x)
            history['min_strat_x'].append(min(strat_x))
            history['avg_strat_x'].append(np.mean(strat_x))

            history['max_strat_y'].append(current_max_strat_y)
            if current_max_strat_x - prev_max_strat_x > 1:
            # if (round(abs(current_max_strat_x - history['max_strat_x'][0]), 2) <= 0.5) & (round_idx >= 50):
            # if round_idx >= 5:
                print(f'Jump detected, x jumps from {prev_max_strat_x} to {current_max_strat_x}')
                # print(f'loop detected')
                break
            print(round_idx)
        print(f'Simulation {sim_idx} finished')
    jump_result.append(round_idx)
    sim_idx += 1
jump_result = np.array(jump_result)
plt.hist(jump_result)
plt.show()
    # Plot max, min, and avg strat_x over time
    # plt.plot(range(round_idx+1), history['max_strat_x'])
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # # ax.scatter(history['max_strat_x'], history['max_strat_y'], range(round_idx + 1), 'ro')
    # ax.plot3D(history['x'], history['y'], round_idx, 'green')
    # for i in range(round_idx):
    #     plt.plot(history['max_strat_x'][i], history['max_strat_y'][i], 'ro', fillstyle='none')
    # sample_plot_max_strat_x = np.array(history['max_strat_x'][::2])
    # sample_plot_max_strat_y = np.array(history['max_strat_y'][::2])
    # # plt.plot(sample_plot_max_strat_x, sample_plot_max_strat_y, 'ro', fillstyle='none')
    # plt.scatter(sample_plot_max_strat_x, sample_plot_max_strat_y, c=range(len(sample_plot_max_strat_x)), cmap=plt.get_cmap('Blues'))
    # # plt.plot(range(round_idx+1), history['min_strat_x'])
    # # plt.plot(range(round_idx+1), history['avg_strat_x'])
    # plt.show()
    # pd.DataFrame(history['strat_x']).to_csv("cdf.csv", header=None, index=None)

