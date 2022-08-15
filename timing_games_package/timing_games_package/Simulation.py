import random
import numpy as np
from timing_games_package import Functions as fun

def initialize_player_strategies(config):
    '''
    Function to run first simulation step to initialize each player's initial strategy
    :param config: dict, dictionary contains simulation parameters
    :return: array, initial strategies;  ndarray, sample sets (None if sampling is none), give each player an array of random other players to sample
    '''
    # game type for starting distribution: set to fear or greed for respective distributions
    # any value other than fear or greed will yield a random start
    game = config['game_type']
    num_bots = config['num_bots']
    lam = config['lambda']
    gam = config['gamma']
    rho = config['rho']
    sampling = config['sampling']
    xmin = config['xmin']
    xmax = config['xmax']

    # calculate the theoretical cdf
    cdfx = np.round(np.arange(config['cdfmin'], config['cdfmax'], 0.01), 2)

    if game == "fear":
        cdfy = gam - rho + np.sqrt((gam + rho) ** 2 - 4 * ((1 + rho) * (gam - 1) * (1 + lam ** 2))/(1 + 2 * lam * cdfx - cdfx ** 2))
        y_ind = 0
        cdfy = cdfy/2
    elif game == "greed":
        cdfy = gam - rho - np.sqrt((gam + rho) ** 2 - 4 * gam * rho * (1 + lam ** 2)/(1 + 2 * lam * cdfx - cdfx ** 2))
        y_ind = len(cdfy) - 1
        cdfy = cdfy/2

    strategies = []
    sample_sets = []

    # set initial strategies and sampling
    # these calculations are inexact because we have a finite number of players
    # greed, fear, and random starting distributions have differing calculations
    if game == "fear":
        for i in range(num_bots):
            # y_ind is the index in the cdf to compare to
            # we increment it until it is greater than or equal to the percentage of players set so far
            if (i+1)/num_bots <= cdfy[y_ind]:
                strategies.append(cdfx[y_ind])
            else:
                while y_ind < len(cdfy) - 1 and (i+1)/num_bots > cdfy[y_ind]:
                    y_ind = y_ind + 1
                # there are some rounding issues when we reach the end of the cdf
                # if we reach the end (for the last few players), just use the last value
                if y_ind >= len(cdfy):
                    strategies.append(cdfx[len(cdfy)])
                else:
                    strategies.append(cdfx[y_ind])
            # strategies.append(random.random() * (xmax - xmin) + xmin)
            # give each player a wait time
            # wait_times.append(random.randint(0, wait_time))
            # give each player an array of random other players to sample
            if sampling is not None:
                # to_add = []
                other_player_index_list = list(range(num_bots))
                other_player_index_list.remove(i)
                # for j in range(sampling):
                #     val = random.randint(0, num_bots - 1)
                #     # if we've got this player in the sample set already or player i himself, try again
                #     if val in to_add or val == i:
                #         j = j - 1
                #     else:
                #         to_add.append(val)
                to_add = random.sample(other_player_index_list, sampling)
                sample_sets.append(to_add)
    elif game == "greed":
        i = num_bots
        while i > 0:
            # y_ind is the index in the cdf to compare to
            # we decrement it until it is less than or equal to the percentage of players set so far
            if (i+1)/num_bots >= cdfy[y_ind]:
                strategies.append(cdfx[y_ind])
            else:
                while y_ind > 0 and (i+1)/num_bots < cdfy[y_ind]:
                    y_ind = y_ind - 1
                # there are some rounding issues when we reach the end of the cdf
                # if we reach the end (for the last few players), just use the last value
                if y_ind == 0:
                    strategies.append(cdfx[0])
                else:
                    strategies.append(cdfx[y_ind])
            # strategies.append(random.random() * (xmax - xmin) + xmin)
            # give each player a wait time
            # wait_times.append(random.randint(0, wait_time))
            # give each player an array of random other players to sample
            if sampling is not None:
                to_add = []
                for j in range(sampling):
                    val = random.randint(0, num_bots - 1)
                    # if we've got this player in the sample set already or player i himself, try again
                    if val in to_add or val == i:
                        j = j - 1
                    else:
                        to_add.append(val)
                sample_sets.append(to_add)
            i = i - 1
    else:
        for i in range(num_bots):
            strategies.append(random.random() * (xmax - xmin) + xmin)
            # give each player a wait time
            # wait_times.append(random.randint(0, wait_time))
            # give each player an array of random other players to sample
            if sampling is not None:
                to_add = []
                for j in range(sampling):
                    val = random.randint(0, num_bots - 1)
                    # if we've got this player in the sample set already or player i himself, try again
                    if val in to_add or val == i:
                        j = j - 1
                    else:
                        to_add.append(val)
                sample_sets.append(to_add)
    strategies = np.round(np.array(strategies), 2)

    return strategies, sample_sets


def calculate_payoff(config, strategies, sample_sets):
    '''

    :param config: dict, dictionary contains simulation parameters
    :param strategies: array, current strategies
    :param sample_sets: ndarray, sample sets (None if sampling is none), give each player an array of random other players to sample
    :return: x: array of possible x; y: array of payoff given timing x; strat_x: sorted strategies from low to high;
             strat_y: array of payoffs given sorted strategies; strategies_y: array of payoffs given strategies
    '''

    lam = config['lambda']
    gam = config['gamma']
    rho = config['rho']
    xmin = config['xmin']
    xmax = config['xmax']
    # set the array of possible x values
    x = np.round(np.arange(xmin, xmax, 0.01),2)
    positions = []
    ties = []
    # set up initial values for landscape positions and ties
    for val in x:
        positions.append(fun.get_position(val, None, strategies, sample_sets, config))
        ties.append(fun.get_tie(val, None, strategies, sample_sets, config))
    positions = np.array(positions)
    # calculate timing component
    ux = 1 + (2 * lam * x) - (x * x)
    vy = []
    quantile = []
    # calculate positional component, including ties
    for i in range(len(positions)):
        if ties[i] == 0:
            vy.append((1 - (positions[i]/len(strategies))/gam) * (1 + (positions[i]/len(strategies))/rho))
            quantile.append(positions[i]/len(strategies))
        else:
            total = 0
            total_quantile = 0
            for j in range(ties[i]):
                total += (1 - ((positions[i]+j)/len(strategies))/gam) * (1 + ((positions[i]+j)/len(strategies))/rho)
                total_quantile += (positions[i])/len(strategies)
            total = total/ties[i]
            vy.append(total)
            total_quantile = total_quantile/ties[i]
            quantile.append(total_quantile)
    y = ux * vy
    strat_x = np.sort(strategies)
    strat_y = []
    strategies_y = []
    # calculate bubble positions
    for strat in strat_x:
        strat_y.append(fun.get_y(strat, strategies, sample_sets, config, seed=None, use_bandwidth=False))
    for strat in strategies:
        strategies_y.append(fun.get_y(strat, strategies, sample_sets, config, seed=None, use_bandwidth=False))
    return x, y, strat_x, strat_y, strategies_y, quantile

# Loops through all players and moves them if they are ready to move
def update_player_strategies(x, y, strategies, strategies_y, sample_sets, config):
    '''

    :param x: numpy array, array of possible x
    :param y: numpy array, payoff array w.r.t each element in x
    :param strategies: list, list containing previous strategies of each player
    :param config: dict, dictionary containing simulation parameters
    :return: strategies: list, list containing updated strategies of each player
    '''

    theta = config['theta']
    asynchronous = config['asynchronous']
    trembling = config['trembling']

    if asynchronous is True:
        best_possible = max(y)
        # who gets move(i.i.d)
        #distances_from_best_payoff = abs(strategies_y-best_possible)
        #selected_player_index = random.choices(players_index, weights=distances_from_best_payoff,k=1)
        selected_player_index = random.randint(0, len(strategies)-1)
        selected_player_strategy = strategies[selected_player_index]
        selected_player_payoff = strategies_y[selected_player_index]
        # find best payoff index
        # if there are multiple timings with the best payoff, choose randomly
        indices = [k for k, j in enumerate(y) if j == best_possible]
        best_choice = random.choice(indices)
        best_choice = x[best_choice]
        choice_set = np.array([best_choice, selected_player_strategy])
        # moving chance
        if theta is not None:
            # choice = random.choices(choice_set, weights=[theta, 1-theta], k=1)
            chance = theta + 10*(best_possible - selected_player_payoff)/best_possible
            chance = min(chance, theta+0.05)
            chance = max(chance, theta-0.05)
            choice = random.choices(choice_set, weights=[chance, 1-chance], k=1)
        # apply trembling
            strategies[selected_player_index] = choice[0] + round((random.random() * trembling - trembling/2), 2)
        else:
            strategies[selected_player_index] = best_choice + round((random.random() * trembling - trembling/2), 2)
    # if all players make move simultaneously
    else:
        selected_player_index = None
    # loop over all players
        static_strats = np.copy(strategies)
        best_possible = max(y)
        for i in range(len(strategies)):
            y1 = []
            for val in x:
                y1.append(fun.get_y(val, static_strats, sample_sets, config, seed=i, use_bandwidth=True))
    #         print(f'{i} needs to compare payoff in y1 {y1}')
            # find the best observed payoff
            best = max(y1)
            # if there are multiple timings with the best payoff, choose randomly
            indices = [k for k, j in enumerate(y1) if j == best]
            best_choice = random.choice(indices)
            best_choice = x[best_choice]
            choice_set = np.array([best_choice, static_strats[i]])
            # moving chance
            if theta is not None:
                chance = theta + 10*(best_possible - fun.get_y(static_strats[i], static_strats, sample_sets, config, use_bandwidth=True))/best_possible
                chance = min(chance, theta+0.05)
                chance = max(chance, theta-0.05)
                choice = random.choices(choice_set, weights=[chance, 1-chance], k=1)
            # apply trembling
                strategies[i] = choice[0] + round((random.random() * trembling - trembling/2), 2)
            else:
                strategies[i] = best_choice + round((random.random() * trembling - trembling/2), 2)

    return strategies, selected_player_index




