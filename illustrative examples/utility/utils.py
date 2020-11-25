import numpy, os, pickle

__all__ = [
    "SimulationData",
    "build_banded_matrix",
    "save_simulation"
]

class SimulationData():
    def __init__(self, R:float=0, L:float=1e3, G:float=0, C:float=1e3,
                 X:float=1.0, T:float=1.0,
                 num_x_points:int=100,
                 num_t_points:int=1000,
                 mu_0=None, xi_0=None,
                 nu_0=None, nu_X=None, gamma_0=None, gamma_X=None,
                 name:str="Simulation"):
        
        self.set_line_parameters(R, L, G, C)
        self.set_domain(X, T, num_x_points, num_t_points)
        if (mu_0 is not None) or (xi_0 is not None):
            self.initial_conditions(mu_0, xi_0)
        if (nu_0 is not None) or (nu_X is not None) or (gamma_0 is not None) or (gamma_X is not None):
            self.boundary_conditions(nu_0, nu_X, gamma_0, gamma_X)
        self.name = name
    
    def set_line_parameters(self, R=None, L=None, G=None, C=None):
        try:
            if set([R, L, G, C]) == {None}:
                print("Line parameters are retained.")
            if R is not None:
                self.line["R"] = R
                self.line["beta"] = R / self.line["L"]
                print("Line parameters 'R' and 'beta' are adjusted.")
            if L is not None:
                self.line["L"] = L
                self.line["beta"] = self.line["R"] / L
                print("Line parameters 'L' and 'beta' are adjusted.")
            if G is not None:
                self.line["G"] = G
                self.line["alpha"] = G / self.line["C"]
                print("Line parameters 'G' and 'alpha' are adjusted.")
            if C is not None:
                self.line["C"] = C
                self.line["alpha"] = self.line["G"] / C
                print("Line parameters 'G' and 'alpha' are adjusted.")
        except AttributeError:
            self.line = {
                "R" : R, "L" : L, "G" : G, "C" : C,
                "c" : 1. / numpy.sqrt(L*C), "c squared" : 1. / (L*C),
                "alpha" : G/C, "beta" : R/L
            }
            print("Line parameters initialized.")

    def set_domain(self, X=None, T=None, num_x_points=None, num_t_points=None):
        try:
            if set([X, T, num_x_points, num_t_points]) == {None}:
                print("Domain parameters are retained.")
            if X is not None:
                self.domain["X"] = X
                print("Domain parameter 'X' is adjusted.")
            if T is not None:
                self.domain["T"] = T
                print("Domain parameter 'T' is adjusted.")
            if num_x_points is not None:
                self.domain["K"] = num_x_points-1
                self.domain["x step"] = self.domain["X"] / (num_x_points-1)
                print("Domain parameters 'K' and 'x step' are adjusted.")
            if num_t_points is not None:
                self.domain["N"] = num_t_points-1
                self.domain["t step"] = self.domain["T"] / (num_t_points-1)
                print("Domain parameters 'N' and 't step' are adjusted.")
        except AttributeError:
            self.domain = {
                "X" : X, "T" : T, "K" : num_x_points-1, "N" : num_t_points-1,
                "x step" : X / (num_x_points-1), "t step" : T / (num_t_points-1),
            }
            print("Domain parameters initialized.")

    def initial_conditions(self, mu_0, xi_0:float=0):
        self.init_condition_value = mu_0
        self.init_condition_deriv = lambda u_k_0 : u_k_0 + xi_0 * self.domain["t step"]
    
    def boundary_conditions(self, nu_0=None, nu_X=None, gamma_0=None, gamma_X=None):
        self.dirichlet_sending_end = nu_0
        self.dirichlet_receiving_end = nu_X
        
        if gamma_0 is not None:
            self.neumann_sending_end = lambda u_1_n : u_1_n - gamma_0 * self.domain["x step"]
        
        if gamma_X is not None:
            self.neumann_receiving_end = lambda u_Kless1_n : u_Kless1_n + gamma_X * self.domain["x step"]
    
    def get_x_domain(self):
        return numpy.array([0+k*self.domain["x step"] for k in range(self.domain["K"]+1)])
    
    def get_t_domain(self):
        return numpy.array([0+n*self.domain["t step"] for n in range(self.domain["N"]+1)])

    def get_CFL_number(self):
        return self.line["c"] * self.domain["t step"] / self.domain["x step"]
    
    def set_analytic_soln(self, analytic_soln):
        self.analytic_soln = analytic_soln

def build_banded_matrix(band, num_rows):
    band = numpy.asarray(band)
    p = numpy.zeros(num_rows-1, dtype=band.dtype)
    b = numpy.concatenate((p,band,p))
    s = b.strides[0]

    return numpy.lib.stride_tricks.as_strided(
        b[num_rows-1:], shape=(num_rows, len(band)+num_rows-1), strides=(-s,s)
    )

def save_simulation(domain:dict, line_params:dict, update_eqn_params:dict, results:dict, simulation_id:str="simulation", save_dir="./"):
    simulation = {
        "domain" : domain, "line parameters" : line_params,
        "update eqn parameters" : update_eqn_params,
        "results" : results,
        "simulation id" : simulation_id
    }
    
    with open(os.path.join(save_dir, simulation_id+".pkl"), 'wb') as file:
        pickle.dump(simulation, file)
    
    print("Simulation saved to " + os.path.join(save_dir, simulation_id+".pkl" + "."))
    
    del file
