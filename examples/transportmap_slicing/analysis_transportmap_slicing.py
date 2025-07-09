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
#print(rbc.keys())

s = rbc["s"]
print("s =")
print(s)

#Expected s positions inside elements
ns = 10
s_list = [1.0, 0.226, 0.224, 0.226, 0.224, 0.226]
s_ref = []
s_sum = 0.0
for si in s_list:
    s_ref += list(np.arange(s_sum, s_sum+si, si/ns))
    s_sum += si
s_ref += [s_sum]
s_ref = np.array(s_ref)
print("s_ref =", s_ref)

# Plot
# import matplotlib.pyplot as plt
# plt.plot(s, '-*')
# plt.plot(s_ref, '-+')
# plt.xlabel('point idx')
# plt.ylabel('s [m]')
# plt.show()
#
# for i in range(len(s_ref)):
#     print(i, s_ref[i], s[i])

# Test
assert np.allclose(s, s_ref)

#Check final beam parameters
sigx = rbc["sig_x"].iloc[-1]
sigy = rbc["sig_y"].iloc[-1]
sigpx = rbc["sig_px"].iloc[-1]
sigpy = rbc["sig_py"].iloc[-1]

alpha_x = rbc["alpha_x"].iloc[-1]
alpha_y = rbc["alpha_y"].iloc[-1]
beta_x = rbc["beta_x"].iloc[-1]
beta_y = rbc["beta_y"].iloc[-1]

print("Got Twiss parameters:")
print(sigx,sigy,sigpx,sigpy,alpha_x,alpha_y,beta_x,beta_y)

assert np.allclose([sigx,sigy,sigpx,sigpy,alpha_x,alpha_y,beta_x,beta_y],
                   [
                       0.0001612829767676,
                       0.0001568457636428,
                       0.0004050672730967,
                       0.0010418673927829,
                       -2.3604038755161776,
                       6.333668362033799,
                       1.0206899618213794,
                       0.9653001388099148
                   ]
                  )
