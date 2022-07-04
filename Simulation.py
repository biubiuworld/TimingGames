import random
import numpy as np
import Functions as fun

def initialize_player_strategies(config):
    '''
    Function to run first simulation step to initialize each player's initial strategy
    :param config: dict, dictionary contains simulation parameters
    :return:
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
            if i/num_bots <= cdfy[y_ind]:
                strategies.append(cdfx[y_ind])
            else:
                while y_ind < len(cdfy) - 1 and i/num_bots > cdfy[y_ind]:
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
                to_add = []
                for j in range(sampling):
                    val = random.randint(0, num_bots - 1)
                    # if we've got this player in the sample set already, try again
                    if val in to_add or val == j:
                        j = j - 1
                    else:
                        to_add.append(val)
                sample_sets.append(to_add)
    elif game == "greed":
        i = num_bots
        while i > 0:
            # y_ind is the index in the cdf to compare to
            # we decrement it until it is less than or equal to the percentage of players set so far
            if i/num_bots >= cdfy[y_ind]:
                strategies.append(cdfx[y_ind])
            else:
                while y_ind > 0 and i/num_bots < cdfy[y_ind]:
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
                    # if we've got this player in the sample set already, try again
                    if val in to_add or val == j:
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
                    # if we've got this player in the sample set already, try again
                    if val in to_add or val == j:
                        j = j - 1
                    else:
                        to_add.append(val)
                sample_sets.append(to_add)
    strategies = np.round(np.array(strategies), 2)

    return strategies, sample_sets


def calculate_payoff(config, strategies, sample_sets):
    '''

    :param config: dict, dictionary contains simulation parameters
    :param strategies:
    :param sample_sets:
    :return:
    '''

    lam = config['lambda']
    gam = config['gamma']
    rho = config['rho']
    xmin = config['xmin']
    xmax = config['xmax']
    # set the array of possible x values
    x = np.arange(xmin, xmax, 0.01)
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
    # calculate positional component, including ties
    for i in range(len(positions)):
        if ties[i] == 0:
            vy.append((1 - (positions[i]/len(strategies))/gam) * (1 + (positions[i]/len(strategies))/rho))
        else:
            total = 0
            for j in range(ties[i]):
                total += (1 - ((positions[i]+j)/len(strategies))/gam) * (1 + ((positions[i]+j)/len(strategies))/rho)
            total = total/ties[i]
            vy.append(total)
    y = ux * vy
    strat_x = np.sort(strategies)
    strat_y = []
    # calculate bubble positions
    for strat in strat_x:
        strat_y.append(fun.get_y(strat, strategies, sample_sets, config, seed=None, use_bandwidth=False, strategies=None))
    return x, y, strat_x, strat_y

# Loops through all players and moves them if they are ready to move
def update_player_strategies(x, y, strategies, sample_sets, config):
    '''

    :param x: numpy array, time array
    :param y: numpy array, payoff array w.r.t each element in x
    :param strategies: list, list containing previous strategies of each player
    :param config: dict, dictionary containing simulation parameters
    :return:
    '''

    theta = config['theta']
    asynchronous = config['asynchronous']
    trembling = config['trembling']
    # loop over all players
    static_strats = np.copy(strategies)
    best_possible = max(y)
    for i in range(len(strategies)):
        if asynchronous is True:
            static_strats = strategies
        chance = theta * (best_possible - fun.get_y(static_strats[i], static_strats, sample_sets, config, use_bandwidth=True, strategies=strategies))
        chance = max(chance, 1e-3)
        y1 = []
        for val in x:
            y1.append(fun.get_y(val, strategies, sample_sets, config, seed=i, use_bandwidth=True, strategies=strategies))
#         print(f'{i} needs to compare payoff in y1 {y1}')
        # find the best observed payoff
        best = max(y1)
        # if there are multiple timings with the best payoff, choose randomly
        indices = [k for k, j in enumerate(y1) if j == best]
        choice = random.choice(indices)
        choice = x[choice]
        # apply trembling
        strategies[i] = choice + round((random.random() * trembling - trembling/2), 2)



    return strategies




