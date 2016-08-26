import time
import generic_io



#################### SETTINGS ####################
PARALLEL_MODE = 'serial'
OBJF_MODE = 'generic'
OBJF_EXE = './a.out'
SAMPLE_SPACE = [(-1, 1)]
N_COMPLEX = 3
N_POINTS = 10
N_EVOLUTION_SAMPLE = 5
N_GEN_OFFSPRING = 10
N_EVOLUTIONS = 10
MAX_ITERS = 10
LOG_FILE = 'testing.log' # str(time.time()) + '.log'
IO = generic_io.io



#################### MISC FUNCTIONS ####################
def parallel_compute_helper(ch):
	ch.compute()
	return(0)


def parallel_evolve_helper(ch):
	ch.evovlve()
	return(0)


def get_time_string():
	t = time.time()
	return(time.strftime('[%d-%m-%y %H:%M:%S]: '))


def compute_centroid(chL):
	vectors = [ch.args for ch in chL]
	return([sum([args[i] for args in vectors ])/len(vectors) for i in range(len(vectors[0]))])
	
