# Returns the position in group for a given timing n (for a given n, how many strategies are less than n)
# optional parameter seed denotes which set of players to sample (-1 for no sampling)
import numpy as np
def get_position(n, seed, strats, sample_sets, config):
    '''

    :param n: float, timing n
    :param seed: index of player i, default to none
    :param strats: array, current strategies
    :param sample_sets: ndarray, sample sets (None if sampling is none), give each player an array of random other players to sample
    :param config: dict, dictionary containing simulation parameters
    :return: float, position for timing n
    '''
    # positions are approximated more accurately by adding 0 to the value for greed and 1 for fear game
    if config['game_type'] == 'fear':
        pos = 1
    elif config['game_type'] == 'greed':
        pos = 0
    else:
        pos = 0.5
    samples = []
    # if using sampling, get the strategies of the sampled players
    if (seed is not None) and (config['sampling'] is not None):
        for samp in sample_sets[seed]:
            samples.append(strats[samp])
    # otherwise check all strategies
    else:
        samples = strats
    # compare to strategies to calculate position
    for strat in samples:
        if n > strat:
            pos = pos + 1
    return pos

# Returns ties at timing n
# optional parameter seed denotes which set of players to sample (-1 for no sampling)
def get_tie(n, seed, strats, sample_sets, config):
    '''

    :param n: float, timing n
    :param seed: index of player i, default to none
    :param strats: array, current strategies
    :param sample_sets: ndarray, sample sets (None if sampling is none), give each player an array of random other players to sample
    :param config: dict, dictionary containing simulation parameters
    :return: float, ties for timing n
    '''
    # this is only here to fix rounding comparison issues
    n = round(n,2)

    tie = 0
    samples = []
    # if using sampling, get the strategies of the sampled players
    if (seed is not None) and (config['sampling'] is not None):
        for samp in sample_sets[seed]:
            samples.append(strats[samp])
    # otherwise check all strategies
    else:
        samples = strats
    # compare to strategies to calculate position
    for strat in samples:
        # more rounding stuff due to float precision errors
        strat = round(strat, 2)
        if n == strat:
            tie = tie + 1
    return tie


def get_index(n, seed, strats, sample_sets, config):
    '''

    :param n: float, timing n
    :param seed: index of player i, default to none
    :param strats: array, current strategies
    :param sample_sets: ndarray, sample sets (None if sampling is none), give each player an array of random other players to sample
    :param config: dict, dictionary containing simulation parameters
    :return: float, ties for timing n
    '''
    # this is only here to fix rounding comparison issues
    n = round(n,2)

    samples = []
    # if using sampling, get the strategies of the sampled players
    if (seed is not None) and (config['sampling'] is not None):
        for samp in sample_sets[seed]:
            samples.append(strats[samp])
        # find the right closest strategy's index
        samples_minus_n = np.round(samples - n, 2)
        test_tie_positive = np.any(samples_minus_n>0)
        if (samples_minus_n==0).any() == True:
            sample_index = np.where(samples_minus_n == 0)[0]
            index = []
            for i in sample_index:
                index.append(sample_sets[seed][i])
        elif test_tie_positive == True:
            samples_minus_n_min = min([i for i in samples_minus_n if i > 0])
            sample_index = np.where(samples_minus_n == samples_minus_n_min)[0][0]
            index = sample_sets[seed][sample_index]
        else:
            index = config['sampling']


    # otherwise check all strategies
    else:
        samples = strats
        samples_minus_n = samples - n
        samples_minus_n = np.round(samples - n, 2)
        test_tie_positive = np.any(samples_minus_n>0)
        if (samples_minus_n==0).any() == True:
            index = np.where(samples_minus_n == 0)[0]
        elif test_tie_positive == True:
            samples_minus_n_min = min([i for i in samples_minus_n if i > 0])
            index = np.where(samples_minus_n == samples_minus_n_min)[0][0]
        else:
            index = len(strats)




    return index


# Returns the payoff at timing n
def get_y(n, strats, index, sample_sets, config, seed=None, use_bandwidth=False):
    '''

    :param n: float, timing n
    :param strats: array, current strategies
    :param sample_sets: ndarray, sample sets (None if sampling is none), give each player an array of random other players to sample
    :param config: dict, dictionary containing simulation parameters
    :param seed: index of player i, default to none
    :param use_bandwidth:
    :return: float, payoff
    '''
    # calculate the timing component

    if config['purification'] is not None:
        purification = config['purification']
    else:
        purification = 0.
    num_bots = config['num_bots']

    ux = 1 + (2 * config['lambda'] * n) - (n * n)
    ties = get_tie(n, seed, strats, sample_sets, config)
    pos = get_position(n, seed, strats, sample_sets, config)
    e = (2 * purification * index) / (num_bots - 1) - purification
    if ties == 0:
        q = pos/num_bots
        vy = (1 - ((1-e)*q)/config['gamma']) * (1 + ((1-e)*q)/config['rho'])
    # if there are ties, calculate the average of the position components over the tie range
    elif ties > 0:
        vy = 0
        for j in range(ties):
            vy += (1 - ((1-e)*(pos+j)/len(strats))/config['gamma']) * (1 + ((1-e)*(pos+j)/len(strats))/config['rho'])
        vy = vy/ties
    # otherwise just use the regular formula
    if (config['bandwidth'] is not None) and use_bandwidth:
        ux = 0
        start_x = n - config['bandwidth']
        for i in range(21):
            ux += 1 + (2 * config['lambda'] * start_x) - (start_x * start_x)
            start_x += config['bandwidth']/10
        ux = ux/21
    return ux * vy


def data_logging(var_name_list, round_num, history):
    for var in var_name_list:
        history[var, round_num] = eval({var})

    return history


