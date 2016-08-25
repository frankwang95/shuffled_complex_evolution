#import subprocess
import threading
import random



PARALLEL_MODE = 'serial'
OBJF_MODE = 'generic'
OBJF_EXE = 'a.exe'
SAMPLE_SPACE = [(0, 1)]
N_COMPLEX = 5
N_POINTS = 10
MAX_ITERS = 10



class Complex:
    def __init__(self, sample, controller):
        self.sample = sample
        self.controller = controller

    def update_sample(self):
        return(0)

    def cce(self):
        return(0)



class GenericComputeHandle:
    def __init__(self, args, controller):
        self.args = args
        self.controller = controller
        self.eval = False


    def compute(self):
        self.eval = float(subprocess.check_output(self.controller.objf_exe + ' '.join(self.args)))
        return(0)



class PythonComputeHande:
    def __init__(self, args, controller):
        self.args =args
        self.controller = controller
        self.eval = False



class SCEController:
    def __init__(
        self,
        parallel_mode=PARALLEL_MODE,
        objf_mode=OBJF_MODE,
        objf_exe=OBJF_EXE,
        sample_space=SAMPLE_SPACE,
        n_complex=N_COMPLEX,
        n_points=N_POINTS,
        max_iters=MAX_ITERS
        ):

        self.parallel_mode = parallel_mode
        self.objf_mode = objf_mode
        self.objf_exe = objf_exe
        self.sample_space = sample_space
        self.n_complex = n_complex
        self.n_points = n_points
        self.max_iters = max_iters

        self.dim = len(self.sample_space)
        self.log = []

        self.init_complexes()

        while self.max_iters > 0:
            self.max_iters -= 1

        print('DONE')


    def init_complexes(self):
        sample = [random.uniform(r[0], r[1]) for r in self.sample_space for _ in range(self.n_complex * self.n_points)]
        sample = [GenericComputeHandle(arg, self) for arg in sample]
        #self.eval_compute_handles(sample)

        self.complexs = []
        return(0)


    def eval_compute_handles(self, compute_handles):
        if self.parallel_mode == 'serial':
            for ch in compute_handles: ch.compute()
        if self.parallel_mode == 'threaded':
            for ch in compute_handles: threading.Thread(target=ch.compute)
        else:
            pool = mp.Pool(self.parallel_mode)
            pool.map()


    def iter_complexes(self):
        return(0)





SCEController()
#subprocess.check_output(['echo', '$PATH'])