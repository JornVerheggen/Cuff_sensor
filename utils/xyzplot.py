#%%
import pandas as pd
import matplotlib.pyplot as plt
#%%
df = pd.read_csv("ousideInfluence.csv",delimiter=';',names=['t','x','y','z','rx','ry','rz'])
df.head()
# %%

plt.plot(df['x'])
plt.plot(df['y'])
plt.plot(df['z'])
# plt.plot(df['rx'])
# plt.plot(df['ry'])
# plt.plot(df['rz'])
plt.show

plt.xlabel('time')
plt.ylabel('Output [m]')
# %%
