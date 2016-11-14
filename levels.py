import random
import itertools as it

test_level = {
    # General parameters
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((225,500), (710,350), (850,500)),
    'planet_radius': (50,45,42),
    'planet_mass': (200,150,120),

    # Rocket data
    'acc': 0.1,

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 180, # Which position on planet (90 = east)
    'canon_max_angle': 75, # How much does it move
    'canon_velocity': 8.5
}



one_planet_level = {
    # General parameters
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((550,390), ),
    'planet_radius': (75,),
    'planet_mass': (280,),
    'planet_img': ('city1',),

    # Rocket data
    'acc': 0.06, # dist / s

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 10, # Which position on planet (90 = east)
    'canon_max_angle': 75, # How much does it move
    'canon_velocity': 7.5,

    # Checkpoint data
    'checkpoint_planet': (0,0,0),
    'checkpoint_angle': (90,180,270),
    'checkpoint_segment': ((250,380), (160,255),(250,380)),
    'checkpoint_reward': (1,1,1)

}


two_planet_level = {
    # General parameters
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((280,390), (770,390)),
    'planet_radius': (70,70),
    'planet_mass': (250,250),
    'planet_img': ('city1','mountain1'),

    # Rocket data
    'acc': 0.055, # dist / s

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 68, # Which position on planet (90 = east)
    'canon_max_angle': 60, # How much does it move
    'canon_velocity': 7.5,

    # Checkpoint data
    'checkpoint_planet': (0,0,1),
    'checkpoint_angle': (270,90,90),
    'checkpoint_segment': ((125,200),(228,262),(80,130)),
    'checkpoint_reward': (1,2,1)

}


moon_level = {
    # General parameters
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((280,390), (850,390)),
    'planet_radius': (70,30),
    'planet_mass': (200,50),
    'planet_img': ('city1','mountain1'),

    # Rocket data
    'acc': 0.05, # Less than usual to make direct start impossible

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 200, # Which position on planet (90 = east)
    'canon_max_angle': 60, # How much does it move
    'canon_velocity': 6,

    # Checkpoints
    'checkpoint_planet': (0,1,1),
    'checkpoint_angle': (270,90,270),
    'checkpoint_segment': ((125,250),(50,110),(180,230)),
    'checkpoint_reward': (1,1,1)
}

planet_moon_planet_level = {
    # General parameters
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((200,390), (550,390), (900,390)),
    'planet_radius': (70,30,70),
    'planet_mass': (180,50,180),
    'planet_img': ('city1','mountain1','train1'),

    # Rocket data
    'acc': 0.0525, # Dont put too much energy in the system

    # Canon data
    'canon_planet': 1,
    'canon_planet_angle': 280, # Which position on planet (90 = east)
    'canon_max_angle': 60, # How much does it move
    'canon_velocity': 5.5,

    # Checkpoints
    'checkpoint_planet': (0,2,1,1),
    'checkpoint_angle': (270,90,0,180),
    'checkpoint_segment': ((85,250),(85,250),(45,80),(45,80)),
    'checkpoint_reward': (1,1,2,2)
}


triple_planet_level = {
    # General parameters
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((215,490), (690,330), (830,480)),
    'planet_radius': (75,60,60),
    'planet_mass': (200,150,120),
    'planet_img': ('mountain1','train1','city1'),

    # Rocket data
    'acc': 0.05,

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 180, # Which position on planet (90 = east)
    'canon_max_angle': 75, # How much does it move
    'canon_velocity': 6,

    # Checkpoints
    # Angle = 43.025, 223.025
    # Distance = 205.183 --> 102.5915 +- 16
    'checkpoint_planet': (0,1,1,2),
    'checkpoint_angle': (270,223.025,43.025,43.025),
    'checkpoint_segment': ((200,250),(180,220),(86.5915+3,118.5915-3),(70,110)),
    'checkpoint_reward': (1,1,2,1)
}



progression_cycle = it.cycle([one_planet_level, two_planet_level,
        moon_level, planet_moon_planet_level, triple_planet_level])


progression_levels = [
    ['one_planet', one_planet_level],
    ['planet_moon', moon_level],
    ['two_planet', two_planet_level],
    ['planet_moon_planet', planet_moon_planet_level],
    ['triple_planet', triple_planet_level]
]


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