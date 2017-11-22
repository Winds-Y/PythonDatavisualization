import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
map=Basemap(projection='cyl',lat_0=90,lon_0=-105,
            llcrnrlat=20.41,urcrnrlat=52.03,
            llcrnrlon=-128.67,urcrnrlon=-67.52,
            rsphere=6371200.,resolution='l',area_thresh=10000)
map.drawmapboundary()
# map.fillcontinents()
map.drawstates()
map.drawcoastlines()
map.drawcountries()
map.drawcounties()
parallels=np.arange(0.,90,10.)
map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
meridians=np.arange(-150.,-60.,10.)
map.drawmeridians(meridians=meridians,labels=[0,0,0,1],fontsize=10)
posi=pd.read_csv('../data/2014_us_cities.csv')
lat=np.array(posi['lat'])
lon=np.array(posi['lon'])
pop=np.array(posi['pop'],dtype=float)
size=(pop/np.max(pop))*1000
x,y=map(lon,lat)
plt.subplot(1,2,1)
plt.scatter(x,y,s=size)
# map.scatter(x,y,s=size)
plt.subplot(1,2,2)
plt.scatter(lon,lat)
plt.title('Population distribution in America')
plt.show()