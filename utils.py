import random
from palettable.colorbrewer.diverging import BrBG_9, PRGn_9, PiYG_9, PuOr_9, RdBu_9, RdGy_9, RdYlBu_9, RdYlGn_9, Spectral_9
from palettable.colorbrewer.sequential import Blues_9, BuGn_9, BuPu_9, GnBu_9, Greens_9, Greys_9, OrRd_9, Oranges_9, PuBuGn_9, PuBu_9, PuRd_9, Purples_9, RdPu_9, Reds_9, YlGnBu_9, YlGn_9, YlOrBr_9, YlOrRd_9


diverging_themes = [BrBG_9, PRGn_9, PiYG_9, PuOr_9, RdBu_9, RdGy_9, RdYlBu_9, RdYlGn_9, Spectral_9]
diverging_themes = [c.mpl_colors for c in diverging_themes]

sequential_themes = [Blues_9, BuGn_9, BuPu_9, GnBu_9, Greens_9, Greys_9, OrRd_9, Oranges_9, PuBuGn_9, PuBu_9, PuRd_9, Purples_9, RdPu_9, Reds_9, YlGnBu_9, YlGn_9, YlOrBr_9, YlOrRd_9]
sequential_themes = [c.mpl_colors for c in sequential_themes]


def random_diverging():
    '''
        theme is a list of 9 rgb colors
        0 - 3:  Color A dark -> light
        4:      White
        5 - 8:  Color B light -> dark
    '''
    c = random.choice(diverging_themes)
    theme = {
        'kite_bg': c[8],
        'kite_hl': c[5],

        'planet_bg': c[0],
        'planet_hl': c[4],

        'checkpoint_bg': c[1],
        'trace_bg': c[7],
        'canon_bg': c[2],
        'main_bg': c[6],
    }
    return theme


def random_sequential():
    '''
        theme is a list of 9 rgb colors
        0 - 8:  light -> dark
    '''
    c = random.choice(sequential_themes)
    theme = {
        'kite_bg': c[7],
        'kite_hl': c[0],

        'planet_bg': c[8],
        'planet_hl': c[0],

        'checkpoint_bg': c[2],
        'trace_bg': c[0],
        'canon_bg': c[4],
        'main_bg': c[3],
    }
    return theme


if __name__ == '__main__':
    theme = random_diverging()
    theme = random_sequential()