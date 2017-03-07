import subprocess
import threading
import random
import time
import numpy as np
import multiprocessing as mp

from util_settings import *



class Complex:
	def __init__(self, compute_handles, controller):
		self.compute_handles = compute_handles
		self.controller = controller


	def update_compute_handles(self, compute_handles):
		self.compute_handles = compute_handles
		return(0)


	def evolve(self):
		for _ in range(self.controller.n_evolutions):
			all_args = np.array([ch.args for ch in self.compute_handles])
			h = np.array([[np.min(all_args[:,i]), np.max(all_args[:,i])] for i in range(self.controller.sample_space.shape[0])])

			evolution_sample =  []
			while len(evolution_sample) < self.controller.n_evolution_sample:
				i = self.controller.generate_random()
				ch = self.compute_handles[i]
				if ch not in evolution_sample: evolution_sample.append([ch, i])

			for _ in range(self.controller.n_gen_offspring):
				evolution_sample.sort(key=lambda x : x[0].value)
				centroid = compute_centroid([ch[0] for ch in evolution_sample[:-1]])

				r = 2 * centroid - evolution_sample[-1][0].args
				if np.any(self.controller.sample_space[:,0] - r) > 0 or np.any(self.controller.sample_space[:,1] - r < 0):
					r = np.array([random.uniform(r[0], r[1]) for r in h])
				ch = ComputeHandle(r, self.controller)
				ch.compute()

				if ch.value < evolution_sample[-1][0].value: evolution_sample[-1][0] = ch
				else:
					r = (centroid + evolution_sample[-1][0].args) / 2
					ch = ComputeHandle(r, self.controller)
					ch.compute()
					if ch.value < evolution_sample[-1][0].value: evolution_sample[-1][0] = ch
					else:
						r = np.array([random.uniform(r[0], r[1]) for r in h])
						ch = ComputeHandle(r, self.controller)
						ch.compute()
						evolution_sample[-1][0] = ch

			for (ch, i) in evolution_sample:
				self.compute_handles[i] = ch
		return(0)



class ComputeHandle:
	def __init__(self, args, controller):
		self.args = np.array(args)
		self.controller = controller
		self.value = False


	def compute(self):
		if self.controller.objf_mode == 'generic':
			str_args = [str(arg) for arg in self.args]
			if not self.value: self.value = float(subprocess.check_output([self.controller.function] + str_args))
		elif self.controller.objf_mode == 'python':
			if not self.value: self.value = self.controller.function(self.args)
		return(self.value)



class SCEController:
	def __init__(
		self,
		objf_mode,
		function,
		sample_space,
		parallel_mode=PARALLEL_MODE,
		n_complex=N_COMPLEX,
		n_points=N_POINTS,
		n_evolution_sample = N_EVOLUTION_SAMPLE,
		n_gen_offspring = N_GEN_OFFSPRING,
		n_evolutions = N_EVOLUTIONS,
		max_iters=MAX_ITERS,
		log_file = LOG_FILE
	):
		
		# loading in input variables
		self.parallel_mode = parallel_mode
		self.objf_mode = objf_mode
		self.function = function
		self.sample_space = sample_space
		self.n_complex = n_complex
		self.n_points = n_points
		self.n_evolution_sample = n_evolution_sample
		self.n_gen_offspring = n_gen_offspring
		self.n_evolutions = n_evolutions
		self.max_iters = max_iters

		# configuring other variables
		self.best_value = float('inf')
		self.best_args = None
		self.prob = [2.0 * (self.n_points - i ) / (self.n_points * (self.n_points + 1)) for i in range(self.n_points)]
		for i in range(1, self.n_points): self.prob[i] += self.prob[i - 1]
		self.iters = 0
		self.log_file = open(log_file, 'w')
		self.log = []
		self.add_log('SCE controller initialized')

		# starting SCE algorithm
		self.main_loop()


	def main_loop(self):
		self.init_complexes()
		while self.iters < self.max_iters:
			self.evolve_complexes()
			self.shuffle_complexes()

			for c in self.complexes:
				if c.compute_handles[0].value < self.best_value:
					self.best_value = c.compute_handles[0].value
					self.best_args = c.compute_handles[0].args
		return(0)
			

	def add_log(self, log_message):
		formatted_message = get_time_string() + 'CONTROLLER: ' + log_message
		self.log_file.write(formatted_message + '\n')
		self.log.append(formatted_message)
		return(0)


	def generate_random(self):
		r = random.random()
		for i in range(self.n_points):
			if r < self.prob[i]: return(i)


	def init_complexes(self):
		self.add_log('first initialization of complexes (iteration {0})...'.format(self.iters))
		compute_handles = [np.array([random.uniform(r[0], r[1]) for r in self.sample_space]) for _ in range(self.n_complex * self.n_points)]
		compute_handles = [ComputeHandle(args, self) for args in compute_handles]
		self.eval_compute_handles(compute_handles)
		compute_handles.sort(key=lambda x : x.value)

		self.complexes = []
		for i in range(self.n_complex):
				c = Complex([compute_handles[i + j * self.n_complex] for j in range(self.n_points)], self)
				self.complexes.append(c)

		self.add_log('complexes initialized (iteration {0})'.format(self.iters))
		self.iters += 1
		return(0)


	def shuffle_complexes(self):
		compute_handles = [ch for c in self.complexes for ch in c.compute_handles]
		compute_handles.sort(key=lambda x : x.value)
		
		for i in range(self.n_complex):
			self.complexes[i].update_compute_handles([compute_handles[i + j * self.n_complex] for j in range(self.n_points)])

		self.add_log('complexes shuffled (iteration {0})'.format(self.iters))
		self.iters += 1
		return(0)

	
	def evolve_complexes(self):
		if self.parallel_mode == 'serial':
			for c in self.complexes: c.evolve()

		elif self.parallel_mode == 'threaded':
			threads = []
			for c in self.complexes: threads.append(threading.Thread(target=c.evolve))
			for t in threads:
				t.start()
				t.join()
		
		else:
			for c in self.complexes: c.evolve()

		self.add_log('evolving complexes (iteration {0})...'.format(self.iters))
		self.add_log('complexes evolved (iteration {0})'.format(self.iters))
		return(0)


	def eval_compute_handles(self, compute_handles):
		if self.parallel_mode == 'serial':
			for ch in compute_handles: ch.compute()
		
		elif self.parallel_mode == 'threaded':
			threads = []
			for ch in compute_handles: threads.append(threading.Thread(target=ch.compute))
			for t in threads:
				t.start()
				t.join()

		else:
			pool = mp.Pool(self.parallel_mode)
			val = pool.map(parallel_compute_helper, compute_handles)
			for chi in range(len(compute_handles)):
				compute_handles[chi].value = val[chi]

		return(0)


