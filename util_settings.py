import time



#################### SETTINGS ####################
PARALLEL_MODE = 'serial'
N_COMPLEX = 3
N_POINTS = 1000
N_EVOLUTION_SAMPLE = 5
N_GEN_OFFSPRING = 5
N_EVOLUTIONS = 5
MAX_ITERS = 1
LOG_FILE = 'testing.log' # str(time.time()) + '.log'



#################### MISC FUNCTIONS ####################
def parallel_compute_helper(ch):
	return(ch.compute())


def parallel_evolve_helper(ch):
	ch.evolve()
	return(0)


def get_time_string():
	t = time.time()
	return(time.strftime('[%d-%m-%y %H:%M:%S]: '))


def compute_centroid(chL):
	vectors = [ch.args for ch in chL]
	return([sum([args[i] for args in vectors ])/len(vectors) for i in range(len(vectors[0]))])
	
