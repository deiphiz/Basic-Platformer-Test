import cProfile
import pstats
import main

cProfile.run('main.main().play_game()', 'mainprof.pf')
mainprof = pstats.Stats('mainprof.pf')
mainprof.strip_dirs().sort_stats(-1).print_stats()
raw_input