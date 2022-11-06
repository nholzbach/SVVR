
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_csv('cars.csv')
sns.set_style("darkgrid")

import numpy as np; np.random.seed(1)
plt.rcParams["figure.figsize"] = (15,10)
plt.rcParams.update({'font.size': 20})

x = data.horsepower
y = data.MPG
names = data.model
year = data.year + 1900

norm = plt.Normalize(1,4)

def s(data):
    return 0.00005*data**2 

fig,ax = plt.subplots()
ax.set_title("Horsepower vs Miles Per Gallon for a variety of cars from 1970-1982")
ax.set_xlabel("Horsepower (hp)")
ax.set_ylabel("Miles Per Gallon (MPG)")

markers = ['o', 's', '^', 'D', '*']
colours = {'US':'red', 'Europe':'green', 'Japan':'blue'}

data8 = data[data.cylinders == 8]
data6 = data[data.cylinders == 6]
data5 = data[data.cylinders == 5]
data4 = data[data.cylinders == 4]
data3 = data[data.cylinders == 3]

sc0 = plt.scatter(data8.horsepower, data8.MPG, s=s(data8.weigth),c= data8.origin.apply(lambda x: colours[x]), alpha=0.4, marker='o')
sc1 = plt.scatter(data6.horsepower, data6.MPG, s=s(data6.weigth),c= data6.origin.apply(lambda x: colours[x]), alpha=0.4, marker='s')
sc2 = plt.scatter(data5.horsepower, data5.MPG, s=s(data5.weigth),c= data5.origin.apply(lambda x: colours[x]), alpha=0.4, marker='^', label='5')
sc3= plt.scatter(data4.horsepower, data4.MPG, s=s(data4.weigth),c= data4.origin.apply(lambda x: colours[x]), alpha=0.4, marker='D', label='4')
sc4 = plt.scatter(data3.horsepower, data3.MPG, s=s(data3.weigth),c= data3.origin.apply(lambda x: colours[x]), alpha=0.4, marker='*', label='3')
f = lambda m,c: plt.plot([],[],marker=m, color=c, ls="none")[0]

handles = [f("s", colours[i]) for i in colours]
handles += [f(markers[i], "k") for i in range(5)]
labels = ['US', "Europe", "Japan"] + ["8", "6", '5', '4', '3']

ax.legend(handles, labels, ncol=3, frameon = True, markerscale=2, shadow=True)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(sc,ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}".format(([year[n] for n in ind["ind"]]), 
                           ", ".join([names[n] for n in ind["ind"]]))
    annot.set_text(text)
    # annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    sc_list = [sc0, sc1, sc2, sc3, sc4]
    for sc in sc_list:
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(sc,ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()
# plt.savefig('cars.png', dpi=300, bbox_inches='tight')

