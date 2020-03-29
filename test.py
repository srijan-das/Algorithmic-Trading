import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

exp_ret = [0.1,0.2,0.15]
rsk = [0.07,0.1,0.2]

data = pd.DataFrame({'Expected Returns':exp_ret,'Risk':rsk}, index=['INV 1','INV 2','INV 3'])

data = data.transpose()

print(data.corrwith())