from operator import index
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

filePath1 = "C:\\Users\jorn-\\Documents\\school\\y2\\thesis\\cuffling\\code\\Cuff_sensor\\data\\IntuitivenessExperiment\\1\\Pos1TouchOutput.csv"
filePath2 = "C:\\Users\jorn-\\Documents\\school\\y2\\thesis\\cuffling\\code\\Cuff_sensor\\data\\IntuitivenessExperiment\\1\\Pos1KeyboardOutput.csv"
filePath3 = "C:\\Users\jorn-\\Documents\\school\\y2\\thesis\\cuffling\\code\\Cuff_sensor\\data\\IntuitivenessExperiment\\1\\Pos1KRISOutput.csv"

columns = ['x','y','z','rx','ry','rz']
df1 = pd.read_csv(filePath1,sep=';')
df2 = pd.read_csv(filePath2,sep=';')
df3 = pd.read_csv(filePath3,sep=';')
df1.columns = columns
df2.columns = columns
df3.columns = columns

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot3D(df1['x'], df1['y'], df1['z'], 'red')
ax.plot3D(df2['x'], df2['y'], df2['z'], 'blue')
ax.plot3D(df3['x'], df3['y'], df3['z'], 'green')
plt.show()