import random
import itertools as it


tutorial1_level = {
    # General parameters
    'name': 'tutorial1',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((550,390), ),
    'planet_radius': (75,),
    'planet_mass': (280,),
    'planet_img': ('trees1',),

    # Rocket data
    'acc': 0.05, # dist / s

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 350, # Which position on planet (90 = east)
    'canon_max_angle': 80, # How much does it move
    'canon_velocity': 7.8,

    # Checkpoint data
    'checkpoint_planet': (0,0,0),
    'checkpoint_angle': (40,90,180),
    'checkpoint_segment': ((110,220), (160,270),(110,220)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 2, 3),

    # Intro popup
    'intro_title': 'LIFTOFF!',
    'intro_text': 'launch at the right moment\nto pass all checkpoints\n\nHint: tap on a planet to restart'

}

tutorial2_level = {
    # General parameters
    'name': 'tutorial2',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((550,390), ),
    'planet_radius': (75,),
    'planet_mass': (280,),
    'planet_img': ('trees1',),

    # Rocket data
    'acc': 0.04, # dist / s

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 0, # Which position on planet (90 = east)
    'canon_max_angle': 75, # How much does it move
    'canon_velocity': 7.5,

    # Checkpoint data
    'checkpoint_planet': (0,0,0,0),
    'checkpoint_angle': (0,90,180,270),
    'checkpoint_segment': ((150,250),(150,250),(150,250),(150,250)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 2, 3),

    # Intro popup
    'intro_title': 'LIFTOFF!',
    'intro_text': 'pass all checkpoints\nto progress to the next level\n\nHint: tap on a planet to restart'

    # 'intro_title': 'ROUND ORBIT',
    # 'intro_text': 'accelerating and braking\nshows the most effect\non the opposite side of the planet'

}


tutorial3_level = {
    # General parameters
    'name': 'tutorial3',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((400,390), ),
    'planet_radius': (75,),
    'planet_mass': (280,),
    'planet_img': ('city1',),

    # Rocket data
    'acc': 0.045, # dist / s

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 0, # Which position on planet (90 = east)
    'canon_max_angle': 75, # How much does it move
    'canon_velocity': 7.,

    # Checkpoint data
    'checkpoint_planet': (0,0,0,0),
    'checkpoint_angle': (270, 90, 0, 180),
    'checkpoint_segment': ((100,170),(260,440), (150,230), (150,230)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 2, 3),

    # Intro popup
    'intro_title': 'FAR AWAY',
    'intro_text': 'do go gentle into\nthat good night'
    # 'intro_title': 'FAR AWAY',
    # 'intro_text': 'accelerate at the right time\nfrom a small circular orbit'

}


tutorial4_level = {
    # General parameters
    'name': 'tutorial4',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((550,390), ),
    'planet_radius': (75,),
    'planet_mass': (280,),
    'planet_img': ('city2',),

    # Rocket data
    'acc': 0.049, # dist / s

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 10, # Which position on planet (90 = east)
    'canon_max_angle': 75, # How much does it move
    'canon_velocity': 7.5,

    # Checkpoint data
    'checkpoint_planet': (0,0,0),
    'checkpoint_angle': (90,180,270),
    'checkpoint_segment': ((250,380), (160,255),(250,380)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 2, 3),

    # Intro popup
    'intro_title': 'PERFECTING ORBITS',
    'intro_text': 'do go gentle into\nthat good night'

}


two_planet_level = {
    # General parameters
    'name': 'two_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((280,390), (770,390)),
    'planet_radius': (70,70),
    'planet_mass': (250,250),
    'planet_img': ('city2','mountain1'),

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

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}


planet_moon_level = {
    # General parameters
    'name': 'planet_moon',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((280,390), (850,390)),
    'planet_radius': (70,30),
    'planet_mass': (200,50),
    'planet_img': ('trees1','mountain1'),

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

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}

planet_moon_planet_level = {
    # General parameters
    'name': 'planet_moon_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((200,390), (550,390), (900,390)),
    'planet_radius': (70,30,70),
    'planet_mass': (180,50,180),
    'planet_img': ('trees1','mountain1','village1'),

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

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}


planet_moon_planet2_level = {
    # General parameters
    'name': 'planet_moon_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((215,300), (550,550), (830,290)),
    'planet_radius': (55,20,55),
    'planet_mass': (150,60,150),
    'planet_img': ('train1','mountain1','city1'),

    # Rocket data
    'acc': 0.05,

    # Canon data
    'canon_planet': 2,
    'canon_planet_angle': 240, # Which position on planet (90 = east)
    'canon_max_angle': 80, # How much does it move
    'canon_velocity': 6.5,

    # Checkpoints
    # Angle = 43.025, 223.025
    # Distance = 205.183 --> 102.5915 +- 16
    'checkpoint_planet': (0,1,1,2),
    'checkpoint_angle': (235,180,0,135),
    'checkpoint_segment': ((70,140),(35,85),(35,85),(70,140)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}

planet_moon_planet3_level = {
    # General parameters
    'name': 'planet_moon_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((150,390), (550,390), (950,390)),
    'planet_radius': (25,75,25),
    'planet_mass': (70,180,70),
    'planet_img': ('mountain1','village1','mountain1'),

    # Rocket data
    'acc': 0.055, # Dont put too much energy in the system

    # Canon data
    'canon_planet': 1,
    'canon_planet_angle': 10, # Which position on planet (90 = east)
    'canon_max_angle': 80, # How much does it move
    'canon_velocity': 5.5,

    # Checkpoints
    'checkpoint_planet': (0,2,1,1),
    'checkpoint_angle': (270,90,0,180),
    'checkpoint_segment': ((35,100),(35,100),(175,275),(175,275)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}

triple_planet3_level = {
    # General parameters
    'name': 'triple_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((215,490), (690,330), (830,480)),
    'planet_radius': (75,60,60),
    'planet_mass': (200,150,135),
    'planet_img': ('mountain1','city1','train1'),

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
    'checkpoint_segment': ((180,250),(155,220),(86.5915+3,118.5915-3),(74,124)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}

triple_planet2_level = {
    # General parameters
    'name': 'triple_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((250,290), (160,500), (860,410)),
    'planet_radius': (55,52,63),
    'planet_mass': (150,145,175),
    'planet_img': ('city2','trees1','train1'),

    # Rocket data
    'acc': 0.05,

    # Canon data
    'canon_planet': 2,
    'canon_planet_angle': 270, # Which position on planet (90 = east)
    'canon_max_angle': 80, # How much does it move
    'canon_velocity': 6.5,

    # Checkpoints
    # Angle = 43.025, 223.025
    # Distance = 205.183 --> 102.5915 +- 16
    'checkpoint_planet': (0,0,1,1,2,2),
    'checkpoint_angle': (45,225,225,45,225,45),
    'checkpoint_segment': ((75,135),(75,135),(75,135),(75,135),(75,135),(75,135)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}

angle1 = 18.435
mid1 = 158.114

triple_planet_level = {
    # General parameters
    'name': 'triple_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((250,360), (550,460), (850,360)),
    'planet_radius': (48,48,48),
    'planet_mass': (140,130,140),
    'planet_img': ('mountain1','trees1','city1'),

    # Rocket data
    'acc': 0.05,

    # Canon data
    'canon_planet': 1,
    'canon_planet_angle': 180, # Which position on planet (90 = east)
    'canon_max_angle': 75, # How much does it move
    'canon_velocity': 6.75,

    # Checkpoints
    # Angle = 43.025, 223.025
    # Distance = 205.183 --> 102.5915 +- 16
    'checkpoint_planet': (0,1,1,1,2),
    'checkpoint_angle': (270-angle1, 270-angle1, 90+angle1, 0, 90+angle1),
    'checkpoint_segment': ((70,120), (mid1-23,mid1+23), (mid1-23,mid1+23), (80,120), (70,120)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}

quad_planet4_level = {
    # General parameters
    'name': 'triple_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((405,215), (695,215), (405,505), (695,505)),
    'planet_radius': (38,38,38,38),
    'planet_mass': (90,90,90,90),
    'planet_img': ('city1','trees1','city2','mountain1'),

    # Rocket data
    'acc': 0.05,

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 350, # Which position on planet (90 = east)
    'canon_max_angle': 75, # How much does it move
    'canon_velocity': 7,

    # Checkpoints
    # Angle = 43.025, 223.025
    # Distance = 205.183 --> 102.5915 +- 16
    'checkpoint_planet': (0,1,3,2),
    'checkpoint_angle': (45,135,225,315),
    'checkpoint_segment': ((50,100),(50,100),(50,100),(50,100)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}


quad_planet_level = {
    # General parameters
    'name': 'triple_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((425,220), (960,315), (190,405), (675,500)),
    'planet_radius': (25,65,65,25),
    'planet_mass': (60,140,140,60),
    'planet_img': ('mountain1','trees1','city2','mountain1'),

    # Rocket data
    'acc': 0.05,

    # Canon data
    'canon_planet': 2,
    'canon_planet_angle': 340, # Which position on planet (90 = east)
    'canon_max_angle': 75, # How much does it move
    'canon_velocity': 6.,

    # Checkpoints
    # Angle = 43.025, 223.025
    # Distance = 205.183 --> 102.5915 +- 16
    'checkpoint_planet': (0,1,2,3),
    'checkpoint_angle': (45,90,270,225),
    'checkpoint_segment': ((35,80),(75,135),(75,135),(35,80)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}

quad_planet2_level = {
    # General parameters
    'name': 'triple_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((550,460), (550,160), (150,460), (950,460)),
    'planet_radius': (65,24,30,30),
    'planet_mass': (145,45,55,55),
    'planet_img': ('city1','mountain1','mountain1','mountain1'),

    # Rocket data
    'acc': 0.05,

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 340, # Which position on planet (90 = east)
    'canon_max_angle': 75, # How much does it move
    'canon_velocity': 6.,

    # Checkpoints
    # Angle = 43.025, 223.025
    # Distance = 205.183 --> 102.5915 +- 16
    'checkpoint_planet': (1,1,2,2,3,3),
    'checkpoint_angle': (0,180,270,90,270,90),
    'checkpoint_segment': ((35,80),(35,80),(45,92),(45,92),(45,92),(45,92)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}

quad_planet3_level = {
    # General parameters
    'name': 'triple_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((355,215), (745,215), (205,505), (895,505)),
    'planet_radius': (24,24,56,56),
    'planet_mass': (60,60,125,125),
    'planet_img': ('mountain1','mountain1','trees1','city1'),

    # Rocket data
    'acc': 0.05,

    # Canon data
    'canon_planet': 2,
    'canon_planet_angle': 95, # Which position on planet (90 = east)
    'canon_max_angle': 80, # How much does it move
    'canon_velocity': 5.5,

    # Checkpoints
    # Angle = 43.025, 223.025
    # Distance = 205.183 --> 102.5915 +- 16
    'checkpoint_planet': (0,1,2,3),
    'checkpoint_angle': (90,270,270,90),
    'checkpoint_segment': ((50,100),(50,100),(80,150),(80,150)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}

quint_planet_level = {
    # General parameters
    'name': 'triple_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((205,225), (895,225), (205,515), (895,515), (550,370)),
    'planet_radius': (35,35,35,35,50),
    'planet_mass': (70,70,70,70,120),
    'planet_img': ('train1','trees1','city2','mountain1','city1'),

    # Rocket data
    'acc': 0.05,

    # Canon data
    'canon_planet': 4,
    'canon_planet_angle': 10, # Which position on planet (90 = east)
    'canon_max_angle': 80, # How much does it move
    'canon_velocity': 6.5,

    # Checkpoints
    # Angle = 43.025, 223.025
    # Distance = 205.183 --> 102.5915 +- 16
    'checkpoint_planet': (0,1,2,3),
    'checkpoint_angle': (45,315,315,45),
    'checkpoint_segment': ((50,100),(50,100),(50,100),(50,100)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}


black_hole_level = {
    # General parameters
    'name': 'one_planet',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 15,

    # Planet data
    'planet_pos': ((550,360), (100,360)),
    'planet_radius': (35,35),
    'planet_mass': (10000,70),
    'planet_img': ('wind1','city1'),

    # Rocket data
    'acc': 0.05,

    # Canon data
    'canon_planet': 1,
    'canon_planet_angle': 15, # Which position on planet (90 = east)
    'canon_max_angle': 1, # How much does it move
    'canon_velocity': 10,

    # Checkpoints
    # Angle = 43.025, 223.025
    # Distance = 205.183 --> 102.5915 +- 16
    'checkpoint_planet': (0,0),
    'checkpoint_angle': (0,180),
    'checkpoint_segment': ((50,100),(50,100)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (10, 300, 6000)
}



one_push_level = {
    # General parameters
    'name': 'one_push',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((300,390), (550,390), (800,390)),
    'planet_radius': (70,30,70),
    'planet_mass': (220,-80,220),
    'planet_img': ('city2','wind1','gras1'),

    # Rocket data
    'acc': 0.06, # dist / s

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 182, # Which position on planet (90 = east)
    'canon_max_angle': 80, # How much does it move
    'canon_velocity': 6.5,

    # Checkpoint data
    'checkpoint_planet': (0,0,2,2),
    'checkpoint_angle': (270, 90, 90, 270),
    'checkpoint_segment': ((130,200),(100,140),(130,200),(100,140)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6),

    'intro_title': 'STORM WARNING',
    'intro_text': 'the wind blows you away'
}

triangle_push_level = {
    # General parameters
    'name': 'triangle_push',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((300,390), (550,690), (800,390)),
    'planet_radius': (70,25,70),
    'planet_mass': (220,-40,220),
    'planet_img': ('gras1','wind1','trees1'),

    # Rocket data
    'acc': 0.065, # dist / s

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 182, # Which position on planet (90 = east)
    'canon_max_angle': 80, # How much does it move
    'canon_velocity': 6.5,

    # Checkpoint data
    'checkpoint_planet': (0,2,1),
    'checkpoint_angle': (270,90,180),
    'checkpoint_segment': ((125,225),(125,225),(50,110)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}


diamond_push_level = {
    # General parameters
    'name': 'diamond_push',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((300,390), (550,670), (550,50), (800,390)),
    'planet_radius': (70,25,25,70),
    'planet_mass': (240,-35,-35,240),
    'planet_img': ('trees1','wind1','wind1','village1'),

    # Rocket data
    'acc': 0.065, # dist / s

    # Canon data
    'canon_planet': 0,
    'canon_planet_angle': 182, # Which position on planet (90 = east)
    'canon_max_angle': 80, # How much does it move
    'canon_velocity': 6.5,

    # Checkpoint data
    'checkpoint_planet': (0,3,1),
    'checkpoint_angle': (270,90,180),
    'checkpoint_segment': ((125,225),(125,225),(260,340)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}


double_push_level = {
    # General parameters
    'name': 'double_push',
    'gravity_constant': 12,
    'simulation_box': (1100,720),
    'sim_speedup': 30,

    # Planet data
    'planet_pos': ((100,390), (550,390), (1000,390)),
    'planet_radius': (25,70,25),
    'planet_mass': (-50,240,-50),
    'planet_img': ('wind1','city1','wind1'),

    # Rocket data
    'acc': 0.065, # dist / s

    # Canon data
    'canon_planet': 1,
    'canon_planet_angle': 90, # Which position on planet (90 = east)
    'canon_max_angle': 80, # How much does it move
    'canon_velocity': 7.,

    # Checkpoint data
    'checkpoint_planet': (0,2),
    'checkpoint_angle': (90,270),
    'checkpoint_segment': ((50,100),(50,100)),

    # Stars (number of kites (checkpoint points) you need for a star)
    'stars': (1, 3, 6)
}

# progression_cycle = it.cycle([tutorial4_level, two_planet_level,
#         planet_moon_level, planet_moon_planet_level, triple_planet_level])


progression_levels = [
    # tutorial1_level,
    tutorial2_level,
    tutorial3_level,
    # tutorial4_level,

    two_planet_level,
    planet_moon_level,

    planet_moon_planet_level,
    planet_moon_planet2_level,
    planet_moon_planet3_level,

    triple_planet_level,
    triple_planet2_level,
    triple_planet3_level,

    quad_planet_level,
    quad_planet2_level,
    quad_planet3_level,
    quad_planet4_level,

    quint_planet_level,
    # black_hole_level

    #one_push_level,
    #diamond_push_level,
    #triangle_push_level,
    #double_push_level
]

n_levels = len(progression_levels)


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