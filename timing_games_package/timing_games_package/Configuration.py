import math


def sim_config_init(game_type= 'fear', lgr=(10,1.1,0.5), sampling=None, purification=None,
                    trembling=0., bandwidth=None,
                    num_bots=20, move_percent=1.0, game_length=1000, xrange=(2,10),
                    ):
    '''
    Specify simulation configuration parameters
    :param game_type: string, game type
    :param lgr: tuple, (lambda, gamma, rho), default to (10,1.1,0.5)
    :param sampling: int, number of players to sample (give each player an array of random other players to sample), default to None
    :param purification: idiosyncratic shifts of perceived landscape
    :param trembling: float, trembling range, default to 0, trembles in jump destination
    :param theta: float, constant for calculating player move chance, default to 0.2
    :param bandwidth: float, smoothing bandwidth, default to None
    :param asynchronous: boolean, game synchronicity, False means all players decide their moves based on the previous tick, True means players see moves as they happen, default to False
    :param num_bots: int, number of bots, default to 20
    :param game_length: int, game length, default to 1000
    :param xrange: tuple, strategy range
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


    # smoothing bandwidth
    # set to -1 to disable
    config['bandwidth'] = bandwidth

    # game type
    config['game_type'] = game_type

    # lambda/gamma/rho params
    config['lambda'] = lgr[0]
    config['gamma'] = lgr[1]
    config['rho'] = lgr[2]

    # based on gamma and rho, override game type
    if (config['game_type'] != 'other') and (config['gamma'] >= (config['rho'] + 4/3)):
        config['game_type'] = 'greed'
    elif (config['game_type'] != 'other') and (config['gamma'] <= (config['rho'] + 2/3)):
        config['game_type'] = 'fear'

    # rush range (MUST BE CORRECT IF STARTING AT CDF)
    if config['game_type'] == 'fear':
        config['cdfmin'] = max(0, round((config['lambda'] - math.sqrt(1+config['lambda']**2) * math.sqrt(1-(16*(1+config['rho'])*(config['gamma']-1))/((config['gamma'] +3*config['rho'])*(3*config['gamma'] +config['rho'])))),2))
        config['cdfmax'] = config['lambda']
    elif config['game_type'] == 'greed':
        config['cdfmin'] = config['lambda']
        config['cdfmax'] = config['lambda'] + math.sqrt(1+config['lambda']**2)/(math.sqrt(1+16*config['rho']*config['gamma']/((3*config['gamma']-3*config['rho']-2)*(config['gamma']-config['rho']+2))))


    # number of bots
    config['num_bots'] = num_bots

    # move percentage
    config['move_percent'] = move_percent

    # game length
    config['game_length'] = game_length

    # x bound
    if (config['game_type'] == 'fear') or (config['game_type'] == 'greed'):
        config['xmin'] = max(0 , config['cdfmin']-2)
        config['xmax'] = config['cdfmax'] + 3
    else:
        config['xmin'] = xrange[0]
        config['xmax'] = xrange[1]


    return config