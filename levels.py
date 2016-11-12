import random

test_level = {
    # General parameters
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((300,390), (750,390)),
    'planet_radius': (50,50),
    'planet_mass': (250,250),

    # Rocket data
    'acc': 0.1, # dist / s
    'acc_angular': 10, # deg / s

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 68, # Which position on planet (90 = east)
    'canon_max_angle': 60, # How much does it move
    'canon_velocity': 10
}

def random_level():
    level = {
        # General parameters
        'gravity_constant': 12,
        'simulation_box': (1100,720),
        'sim_speedup': 30,

        # Rocket data
        'acc': 0.1, # dist / s
        'acc_angular': 10, # deg / s

        # Canon data
        'canon_max_angle': 60, # How much does it move
        'canon_velocity': 10
    }

    # Planet positions
    n_planets = random.choice([1,2,2,2,3,3])
    pos = []
    if n_planets == 1:
        pos.append((550, 360))

    elif n_planets == 2:
        p1 = random.randrange(200, 350)
        p2 = random.randrange(700, 850)
        pos += [(p1, 360), (p2, 360)]

    else:
        for i in range(n_planets):
            pos.append((random.randrange(200, 850), random.randrange(250, 520)))

    mass, radius = [], []
    for i in range(n_planets):
        scale = 2*(0.5-random.random())
        mass.append(250 + scale * 80)
        radius.append(50 + scale * 5)

    level['planet_pos'] = pos
    level['planet_mass'] = mass
    level['planet_radius'] = radius

    # Canon position
    level['canon_planet'] = random.randrange(n_planets)
    level['canon_planet_angle'] = random.randrange(360)

    return level