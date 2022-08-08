from timing_games_package import Simulation
from timing_games_package.Configuration import sim_config_init
from Functions import data_logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mpl_toolkits import mplot3d
# matplotlib.use('Qt5Agg')

# sim_idx = 0
# jump_result = []
# while sim_idx <= 200:
if __name__ == '__main__':
    # Initialize a dictionary to store history data and game round index
    history = {}
    round_idx = 0

    # Set up simulation configuration
    sim_config = sim_config_init()

    # Simulate players' initial strategies and payoffs
    strategies, sample_sets = Simulation.initialize_player_strategies(sim_config)
    x, y, strat_x, strat_y, strategies_y, quantile = Simulation.calculate_payoff(sim_config, strategies, sample_sets)

    # Log data for the initial round
    # history = data_logging(['strategies', 'x', 'y', 'strat_x', 'strat_y'], round_idx, history) # To Do
    history['strategies', round_idx] = strategies.copy()
    history['x', round_idx] = x
    history['y', round_idx] = y
    history['strat_x', round_idx] = strat_x
    history['strat_y', round_idx] = strat_y
    history['strategies_y', round_idx] = strategies_y
    history['quantile', round_idx] = quantile
    history['max_strat_x'] = [max(strat_x)]
    history['min_strat_x'] = [min(strat_x)]
    history['avg_strat_x'] = [np.mean(strat_x)]

    history['first_strat_x'] = [strat_x[0]]
    history['first_strat_y'] = [strat_y[0]]
    history['last_strat_x'] = [strat_x[-1]]
    history['last_strat_y'] = [strat_y[-1]]
    history['max_strat_y'] = [max(strat_y)]

    # Iterate simulation to update players' strategies and payoff
    max_game_length = sim_config['game_length']
    while round_idx < max_game_length:
        round_idx += 1
        strategies = Simulation.update_player_strategies(x, y, strategies, sample_sets, sim_config)
        x, y, strat_x, strat_y, strategies_y, quantile = Simulation.calculate_payoff(sim_config, strategies, sample_sets)

        # Log data for the round
        history['strategies', round_idx] = strategies.copy()
        history['x', round_idx] = x
        history['y', round_idx] = y
        history['strat_x', round_idx] = strat_x
        history['strat_y', round_idx] = strat_y
        history['strategies_y', round_idx] = strategies_y
        history['quantile', round_idx] = quantile

        # Break simulation when detecting player's stretegy jump
        prev_max_strat_x = max(history['strat_x', round_idx-1])
        current_max_strat_x = max(strat_x)
        current_max_strat_y = max(strat_y)
        first_strat_x = strat_x[0]
        first_strat_y = strat_y[0]
        last_strat_x = strat_x[-1]
        last_strat_y = strat_y[-1]
        history['max_strat_x'].append(current_max_strat_x)
        history['min_strat_x'].append(min(strat_x))
        history['avg_strat_x'].append(np.mean(strat_x))

        history['first_strat_x'].append(first_strat_x)
        history['first_strat_y'].append(first_strat_y)
        history['last_strat_x'].append(last_strat_x)
        history['last_strat_y'].append(last_strat_y)

        history['max_strat_y'].append(current_max_strat_y)
        # if current_max_strat_x - prev_max_strat_x > 1:
        # if (round(abs(current_max_strat_x - history['first_strat_x'][0]), 2) <= 0.01) & (round_idx >= 50):
        # if (round(abs(first_strat_x - history['first_strat_x'][0]), 2) <= 0.01) & (round_idx >= 50):
        if round_idx >= 2:
            print(f'Jump detected, x jumps from {prev_max_strat_x} to {current_max_strat_x}')
        #     print(f'loop detected')
            break
        print(round_idx)
#     print(f'Simulation {sim_idx} finished')
#     jump_result.append(round_idx)
#     sim_idx += 1
# jump_result = np.array(jump_result)
# pd.DataFrame(jump_result).to_csv("200sim_jump_round_trembling0.2_bots20_asyTrue.csv")
# plt.hist(jump_result)
# plt.title('200 simulations - Jump periods when trembling = 0.2 and asynchronous = true')
# plt.grid()
# plt.show()
# plt.savefig('200sim_jump_round_trembling0.2_bots20_asyTrue.png', bbox_inches='tight')
    # count = 0
    # for i in range(len(history['y',0])):
    #     if history['y',0][i] >= 27.545:
    #         count += 1
    #         print(history['y',0][i])
    # print(count)

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
    # plot_max_strat_x = np.array(history['max_strat_x'])
    # plot_max_strat_y = np.array(history['max_strat_y'])
    #
    first_strat_x = np.array(history['first_strat_x'])
    first_strat_y = np.array(history['first_strat_y'])
    #
    # plot_last_strat_x = np.array(history['last_strat_x'])
    # plot_last_strat_y = np.array(history['last_strat_y'])
    # # plt.plot(sample_plot_max_strat_x, sample_plot_max_strat_y, 'ro', fillstyle='none')
    # plt.scatter(sample_plot_max_strat_x, sample_plot_max_strat_y, c=range(len(sample_plot_max_strat_x)), cmap=plt.get_cmap('Blues'))
    # plt.scatter(plot_max_strat_x, plot_max_strat_y, c=range(len(plot_max_strat_x)), cmap=plt.get_cmap('Blues'))
    plt.scatter(first_strat_x, first_strat_y, c=range(len(first_strat_x)), cmap=plt.get_cmap('Accent'))
    plt.colorbar(label="periods")
    plt.scatter(history['strat_x', 0], history['strat_y', 0], alpha=0.5, label='inital strategies')
    plt.axvline(x=first_strat_x[0], color='r', label=str(first_strat_x[0]))
    plt.axvline(x=0.65, color='b', label=0.65)
    plt.axvline(x=10, color='g', label=10)
    plt.title('Strategies over periods')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('payoff')
    plt.grid()
    plt.show()
    plt.savefig('onesim_history_strat_x_y_round_trembling0_bots20_asyFalse.png', bbox_inches='tight')


    ax = plt.axes(projection='3d')
    for i in range(round_idx+1):
        ax.plot3D(history['strat_x', i], history['strat_y', i], i, 'o', fillstyle='none', markersize=5, alpha=0.7)
    ax.set_xlabel('x')
    ax.set_ylabel('payoff y')
    ax.set_zlabel('round')

#plot 3d
    ax = plt.axes(projection='3d')
    for i in range(round_idx+1):
        ax.plot3D(history['x', i], history['y', i], i, alpha=0.5)
        ax.plot3D(history['strat_x', i], history['strat_y', i], i, 'o', fillstyle='none', markersize=5, alpha=0.7)
    ax.set_title('strategies and payoff landscape from period 0 to 20')
    ax.set_xlabel('x')
    ax.set_ylabel('payoff y')
    ax.set_zlabel('round')
    plt.savefig('onesim_3d_periodjump_strat_x_y_round_trembling0.2_bots20_asyTrue.png', bbox_inches='tight')


    plt.plot(history['x', 1], history['y', 1])
    plt.plot(history['strat_x', 1], history['strat_y', 1], 'ro', fillstyle='none')
    # plt.text(history['strat_x', 2][0], history['strat_y', 23][0], 'All bots clump at 1.25')
    # plt.axvline(x=1.25, color='b', label=1.25)
    # plt.axvline(x=1.26, color='r', label=1.26)
    plt.title('Strategies in period 1 (previous)')
    plt.xlabel('x')
    plt.ylabel('payoff')
    plt.grid()
    # plt.legend()
    plt.show()
    plt.savefig('onesim_period1_strat_x_y_round_trembling0_bots20_asyFalse.png', bbox_inches='tight')

#plot quantile
    plt.plot(history['x', 0], history['quantile', 0])
    # plt.plot(history['strat_x', 1], history['strat_y', 1], 'ro', fillstyle='none')
    # plt.text(history['strat_x', 2][0], history['strat_y', 23][0], 'All bots clump at 1.25')
    # plt.axvline(x=1.25, color='b', label=1.25)
    # plt.axvline(x=1.26, color='r', label=1.26)
    plt.title('quantile in period 0 (new)')
    plt.xlabel('timing')
    plt.ylabel('quantile')
    plt.grid()
    # plt.legend()
    plt.show()
    plt.savefig('onesim_period0_strat_x_quantile_round_trembling0_bots20_asyFalse_new.png', bbox_inches='tight')



    period = 2
    plt.plot(history['x', period], history['y', period])
    plt.scatter(history['strategies', period][:5], history['strategies_y', period][:5], label='0-25%', marker='s', color='black')
    # plt.scatter(history['strategies', 2][5:10], history['strategies_y', 2][5:10], label='0.25-0.5')
    # plt.scatter(history['strategies', 2][10:15], history['strategies_y', 2][10:15], label='0.5-0.75')
    plt.scatter(history['strategies', period][5:15], history['strategies_y', period][5:15], label='25%-75%', alpha = 0.5, color='red')
    plt.scatter(history['strategies', period][15:20], history['strategies_y', period][15:20], label='75%-100%', alpha = 0.5, marker='x', color='green')
    # plt.text(history['strat_x', 2][0], history['strat_y', 23][0], 'All bots clump at 1.25')
    # plt.axvline(x=1.25, color='b', label=1.25)
    # plt.axvline(x=1.26, color='r', label=1.26)
    plt.title('Strategies in period 20')
    plt.xlabel('x')
    plt.ylabel('payoff')
    plt.grid()
    plt.legend()
    plt.show()
    plt.savefig('onesim_jump_strat_x_y_round_trembling0.2_bots20_asyTrue.png', bbox_inches='tight')

#plot 2d
    for i in range(16):
        plt.plot(history['x', i], history['y', i], alpha=0.5)
        plt.plot(history['strat_x', i], history['strat_y', i], 'o', fillstyle='none')
        plt.show()

    # create a round array for x
    x_round = list(range(0, round_idx+1))*len(history['x', 0])
    x_round.sort()
    x_round_array = np.array(x_round)

    history_x = history['x', 0]
    for i in range(1, round_idx+1):
        history_x = np.append(history_x, history['x', i])

    history_y = history['y', 0]
    for i in range(1, round_idx+1):
        history_y = np.append(history_y, history['y', i])

    # create a round array for strategies
    strategies_round = list(range(0, round_idx+1))*len(history['strategies', 0])
    strategies_round.sort()
    strategies_round_array = np.array(strategies_round)

    history_strat_x = history['strat_x', 0]
    for i in range(1, round_idx + 1):
        history_strat_x = np.append(history_strat_x, history['strat_x', i])

    history_strat_y = history['strat_y', 0]
    for i in range(1, round_idx + 1):
        history_strat_y = np.append(history_strat_y, history['strat_y', i])

    history_strategies = history['strategies', 0]
    for i in range(1, round_idx + 1):
        history_strategies = np.append(history_strategies, history['strategies', i])

    history_strat_x_y_round = pd.DataFrame(data=[history_strat_x, history_strat_y, strategies_round_array]).T
    history_strat_x_y_round.columns = ['strat_x', 'strat_y', 'round']
    history_strat_x_y_round.to_csv('history_strat_x_y_round.csv', index=False)

    history_strategies_round = pd.DataFrame(data=[history_strategies, strategies_round_array]).T
    history_strategies_round.columns = ['strategies', 'round']
    history_strategies_round.to_csv('history_strategies_round.csv', index=False)

    history_x_y_round = pd.DataFrame(data=[history_x, history_y, x_round_array]).T
    history_x_y_round.columns = ['x', 'y', 'round']
    history_x_y_round.to_csv('history_x_y_round.csv', index=False)

    ax = plt.axes(projection='3d')
    ax.plot3D(x_round_array, history_x, history_y, alpha=0.5)
    ax.plot3D(strategies_round_array, history_strat_x, history_strat_y, 'go', fillstyle='none', markersize=5, alpha=0.7)
    ax.set_ylabel('x')
    ax.set_zlabel('payoff y')
    ax.set_xlabel('round')

    ax = plt.axes(projection='3d')
    ax.scatter3D(history_strat_x, history_strat_y, strategies_round_array, c=range(len(strategies_round_array)), cmap=plt.get_cmap('Accent_r'), alpha=0.7)
    ax.set_xlabel('x')
    ax.set_ylabel('payoff y')
    ax.set_zlabel('round')

    #strategies over rounds
    for i in range(round_idx+1):
        plot_round = np.array([i]*len(history['strategies', 0]))
        plt.plot(plot_round,  history['strategies', i], 'ro', fillstyle='none')
        # plt.ylim([0, 3])
        # plt.scatter(plot_round[:5], history['strategies', i][:5], alpha = 0.3, label='0-0.25', c='red')
        # plt.scatter(plot_round[5:15], history['strategies', i][5:15], alpha = 0.3, label='0.25-0.75', c='green')
        # plt.scatter(plot_round[15:20], history['strategies', i][15:20], alpha = 0.3, label='0.75-1', c='blue')
        plt.title('Strategies over periods')
        plt.xlabel('period')
        plt.ylabel('strategy')
        plt.grid()
        # plt.legend()
        plt.show()
        plt.savefig('twosim_500periods_strategies_round_trembling0._bots20_asyFalse_theta0.05.png', bbox_inches='tight')