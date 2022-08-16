import math


def sim_config_init(lgr=(10,1.1,0.5), sampling=None, purification=None,
                    trembling=0., theta=0.05, bandwidth=None, asynchronous=True,
                    num_bots=20, game_length=1000,
                    ):
    '''
    Specify simulation configuration parameters
    :param lgr: tuple, (lambda, gamma, rho), default to (10,1.1,0.5)
    :param sampling: int, number of players to sample (give each player an array of random other players to sample), default to None
    :param purification: idiosyncratic shifts of perceived landscape
    :param trembling: float, trembling range, default to 0, trembles in jump destination
    :param theta: float, constant for calculating player move chance, default to 0.2
    :param bandwidth: float, smoothing bandwidth, default to None
    :param asynchronous: boolean, game synchronicity, False means all players decide their moves based on the previous tick, True means players see moves as they happen, default to False
    :param num_bots: int, number of bots, default to 20
    :param game_length: int, game length, default to 1000
    :return: config, dictionary containing all simulation configuration parameters
    '''

    config = {}

    # set to -1 to disable
    config['sampling'] = sampling

    # constant e in purification specs
    # set to -1 to disable
    config['purification'] = purification

    # trembling range
    # set to 0 to have no effect
    config['trembling'] = trembling

    # constant for calculating player move chance
    config['theta'] = theta

    # smoothing bandwidth
    # set to -1 to disable
    config['bandwidth'] = bandwidth

    # lambda/gamma/rho params
    config['lambda'] = lgr[0]
    config['gamma'] = lgr[1]
    config['rho'] = lgr[2]
    # specify game type
    if config['gamma'] < (config['rho'] + 2/3):
        config['game_type'] = 'fear'
    elif config['gamma'] > (config['rho'] + 4/3):
        config['game_type'] = 'greed'
    else:
        config['game_type'] = 'other'

    # rush range (MUST BE CORRECT IF STARTING AT CDF)
    config['cdfmin'] = round((config['lambda'] - math.sqrt(1+config['lambda']**2) * math.sqrt(1-(16*(1+config['rho'])*(config['gamma']-1))/((config['gamma'] +3*config['rho'])*(3*config['gamma'] +config['rho'])))),2)
    config['cdfmax'] = config['lambda']

    # game synchronicity
    # False means all players decide their moves based on the previous tick
    # True means players see moves as they happen
    config['asynchronous'] = asynchronous

    # number of bots
    config['num_bots'] = num_bots

    # game length
    config['game_length'] = game_length

    # x bound
    config['xmin'] = 0
    config['xmax'] = config['lambda'] + 3

    return config