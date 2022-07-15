from operator import index
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

filePath = "C:\\Users\jorn-\\Documents\\school\\y2\\thesis\\cuffling\\code\\Cuff_sensor\\data\\IntuitivenessExperiment\\1\\Pos1TouchOutput.csv"
columns = ['x','y','z','rx','ry','rz']
df = pd.read_csv(filePath,sep=';')
df.columns = columns
df.head()

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot3D(df['x'], df['y'], df['z'], 'red')
plt.show()