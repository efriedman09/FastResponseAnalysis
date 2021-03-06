from glob import glob
import healpy as hp
from scipy import sparse
import numpy as np
import time
import pickle

def glob_allsky_scans(delta_t, rate, low_stats=False):
    """
    Glob the all-sky scans together
    """
    #n_per_job = {1000.: 1000, 172800.: 50, 2678400.: 30}
    #jobs_per_window = {1000.: 20, 172800.: 100, 2678400.: 100}

    files = glob('/data/user/apizzuto/fast_response_skylab/fast-response/trunk/precomputed_background/trials/{:.1f}_mHz_seed_*_delta_t_{:.1e}.npz'.format(rate, delta_t))
    nside = 256
    npix = hp.nside2npix(nside)
    maps = sparse.csr_matrix((0, npix), dtype=float)
    
    #print len(files)
    #return None
    print 'Starting to load at {}'.format(time.ctime())
    final_ind = -1 if not low_stats else 20
    for f in files[:final_ind]:
        scan = sparse.load_npz(f)
        maps = sparse.vstack((maps, scan))

    # Change format of sparse array
    print "Starting to change from COO to CSR at {}".format(time.ctime())
    scans = maps.tocsr()
    print "Finished at {}".format(time.ctime())
    
    # Save the sparse array
    stats_str = '' if not low_stats else '_low_stats'
    outfilename = 'precomputed_trials_delta_t_{:.2e}_trials_rate_{:.1f}{}.npz'.format(delta_t, rate, stats_str)
    scan_path = '/data/user/apizzuto/fast_response_skylab/fast-response/trunk/precomputed_background/glob_trials/'
    sparse.save_npz(scan_path+outfilename, scans)
    
    return maps

for rate in [6.2, 6.4, 6.6, 6.8, 7.0, 7.2]:
    for low_stats in [True, False]:
        print("Rate: {} mHz, low stats: {}".format(rate, low_stats))
        maps = glob_allsky_scans(1000., rate, low_stats=low_stats)
        del maps
        print ('')

for rate in [7.0, 7.2]:
    for low_stats in [True]:
        print("Rate: {} mHz, low stats: {}".format(rate, low_stats))
        maps = glob_allsky_scans(2.*86400., rate, low_stats=low_stats)
        del maps
        print ('')
