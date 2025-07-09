#!/usr/bin/env python3
#
# Copyright 2022-2025 ImpactX contributors
# Authors: Axel Huebl, Chad Mitchell, Kyrre Sjobak
# License: BSD-3-Clause-LBNL
#
# -*- coding: utf-8 -*-

import numpy as np
import glob
import pandas as pd

def read_file(file_pattern):
    for filename in glob.glob(file_pattern):
        df = pd.read_csv(filename, delimiter=r"\s+")
        if "step" not in df.columns:
            step = int(re.findall(r"[0-9]+", filename)[0])
            df["step"] = step
        yield df

def read_time_series(file_pattern):
    """Read in all CSV files from each MPI rank (and potentially OpenMP
    thread). Concatenate into one Pandas dataframe.

    Returns
    -------
    pandas.DataFrame
    """
    return pd.concat(
        read_file(file_pattern),
        axis=0,
        ignore_index=True,
    )  # .set_index('id')

# Load analysis from envelope simulation
rbc = read_time_series("diags/reduced_beam_characteristics.*")
s = rbc["s"]
print("s =")
print(s)

#Expected s positions inside elements
ns = 10
s1  = 0.31
s2 = 0.226
s_ref = []
s_ref += list(np.arange(0,s1,s1/ns))
s_ref += list(np.arange(s1,s1+s2,s2/ns))
s_ref += [s1+s2]
s_ref = np.array(s_ref)
print("s_ref =", s_ref)

# Plot
import matplotlib.pyplot as plt
plt.plot(s, '-*')
plt.plot(s_ref, '-+')
plt.xlabel('point idx')
plt.ylabel('s [m]')
plt.show()

# Test
assert np.allclose(s, s_ref)
