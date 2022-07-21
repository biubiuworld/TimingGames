# Returns the position in group for a given timing n (for a given n, how many strategies are less than n)
# optional parameter seed denotes which set of players to sample (-1 for no sampling)
def get_position(n, seed, strats, sample_sets, config):
    '''

    :param n:
    :param seed:
    :param strats:
    :param sample_sets:
    :param config:
    :return:
    '''
    # positions are approximated more accurately by adding 0.5 to the value
    pos = 1
    samples = []
    # if using sampling, get the stratgies of the sampled players
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

    :param n:
    :param seed:
    :param strats:
    :param sample_sets:
    :param config:
    :return:
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


# Returns the payoff at timing n
def get_y(n, strats, sample_sets, config, seed=None, use_bandwidth=False, strategies=None):
    '''

    :param n: float
    :param strats:
    :param sample_sets:
    :param config:
    :param seed:
    :param use_bandwidth:
    :param strategies:
    :return:
    '''
    # calculate the timing component
    ux = 1 + (2 * config['lambda'] * n) - (n * n)
    ties = get_tie(n, seed, strats, sample_sets, config)
    pos = get_position(n, seed, strats, sample_sets, config)
    if (seed is not None) and (config['purification'] is not None):
        puriVal = 1 - (config['purification'] * seed/len(strategies))
    else:
        puriVal = 1
    vy = (1 - (pos * puriVal/len(strats))/config['gamma']) * (1 + (pos * puriVal/len(strats)/config['rho']))
    # if there are ties, calculate the average of the position components over the tie range
    if ties > 0:
        vy = 0
        for j in range(ties):
            vy += (1 - ((pos+j) * puriVal/len(strats))/config['gamma']) * (1 + ((pos+j) * puriVal/len(strats))/config['rho'])
        vy = vy/ties
    # otherwise just use the regular formula
    if (config['bandwidth'] is not None) and use_bandwidth:
        ux = 0
        start_x = n - config['bandwidth']
        for i in range(config['num_bots']+1):
            ux += 1 + (2 * config['lambda'] * start_x) - (start_x * start_x)
            start_x += config['bandwidth']/10
            ties = get_tie(n, seed, strats, sample_sets, config)
            pos = get_position(n, seed, strats, sample_sets, config)
            vy = (1 - (pos * puriVal/len(strats))/config['gamma']) * (1 + (pos * puriVal/len(strats)/config['rho']))
            # if there are ties, calculate the average of the position components over the tie range
            if ties > 0:
                vy1 = 0
                for j in range(ties):
                    vy1 += (1 - ((pos+j) * puriVal/len(strats))/config['gamma']) * (1 + ((pos+j) * puriVal/len(strats))/config['rho'])
                vy1 = vy/ties
        ux = ux/(config['num_bots']+1)
    return ux * vy


def data_logging(var_name_list, round_num, history):
    for var in var_name_list:
        history[var, round_num] = eval({var})

    return history


