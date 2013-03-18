import cProfile
import pstats
import main

cProfile.run('main.main()', 'mainprof')
cProfile.run('import oldmain', 'oldmainprof')

mainprof = pstats.Stats('mainprof')
oldmainprof = pstats.Stats('oldmainprof')

mainprof.strip_dirs().sort_stats(-1).print_stats()
raw_input
oldmainprof.strip_dirs().sort_stats(-1).print_stats()
raw_input