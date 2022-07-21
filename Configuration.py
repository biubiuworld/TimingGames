import math


def sim_config_init(game_type='fear', sampling=None, purification=None,
                    trembling=0., theta=0.05, bandwidth=None, asynchronous=False,
                    lgr=(10,1.1,0.5),
                    num_bots=20, game_length=1000,
                    x_bound=(0,13)):
    '''
    Specify simulation configuration parameters
    :param game_type: str, game type, default to 'fear'
    :param sampling: int, number of players to sample (chosen randomly per player at the start of the round), default to None
    :param purification:
    :param trembling: float, trembling range, default to 0
    :param theta: float, constant for calculating player move chance, default to 0.2
    :param bandwidth: float, smoothing bandwidth, default to None
    :param asynchronous: boolean, game synchronicity, False means all players decide their moves based on the previous tick, True means players see moves as they happen, default to False
    :param lgr: tuple, (lambda, gamma, rho), default to (10,1.1,0.5)
    :param cdf_bound: tuple, rush range, default to (1.256,10)
    :param num_bots: int, number of bots, default to 20
    :param game_length: int, game length, default to 600
    :param x_bound: tuple, min and max time, default to from 0 to 13
    :return: config, dictionary containing all simulation configuration parameters
    '''

    config = {}
    config['game_type'] = game_type

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
    config['xmin'] = x_bound[0]
    config['xmax'] = x_bound[1]

    return config