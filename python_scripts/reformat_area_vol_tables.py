# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 12:12:23 2017

@author: dan
"""

import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\workspace\sandbar_process\plotting_out\003L\003L_Merge_Site_Table.csv",sep=':')

df = df.replace('NA*', np.nan,regex=True)

df.to_csv(r"C:\workspace\NAU_OFR_Appendix_D\003L\input\table2.csv",sep=',',header=False)