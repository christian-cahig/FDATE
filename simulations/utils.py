import numpy, os, pickle

__all__ = [
    "build_banded_matrix",
    "save_simulation"
]

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
