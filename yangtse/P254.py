from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data=pd.read_csv(r'../data/Haiti.csv')
# print(data)
data=data[(data.LATITUDE>18)&(data.LATITUDE<20)&(data.LONGITUDE>-75)&(data.LONGITUDE<-70)&data.CATEGORY.notnull()]
# print(data)
def to_cat_list(catstr):
    stripped=(x.strip() for x in catstr.split(','))
    return [x for x in stripped if x]
def get_all_categories(cat_series):
    cat_sets=(set(to_cat_list(x)) for x in cat_series)
    return sorted(set.union(*cat_sets))
def get_english(cat):
    code,names=cat.split('.')
    if '|' in names:
        names=names.split('|')[1]
    return code,names.strip()
# print(get_english('2. Urgences logistiques | Vital Lines'))
all_cats=get_all_categories(data.CATEGORY)
english_mapping=dict(get_english(x) for x in all_cats)
# print(english_mapping['2a'])
def get_code(seq):
    return [x.split('.')[0] for x in seq if x]
all_codes=get_code(all_cats)
code_index=pd.Index(np.unique(all_codes))
dummy_frame=pd.DataFrame(np.zeros((len(data),len(code_index))),index=data.index,columns=code_index)
# print(str(dummy_frame._ix[:,:6]))
for row,cat in zip(data.index,data.CATEGORY):
    codes=get_code(to_cat_list(cat))
    dummy_frame.iloc[row][codes]=1
data=data.join(dummy_frame.add_prefix('category_'))
def basic_haiti_map(ax=None,lllat=17.25,urlat=20.05,lllon=-75,urlon=-71):
    m=Basemap(ax=ax,projection='stere',
              lon_0=(urlon+lllon)/2,
              lat_0=(urlat+lllat)/2,
              llcrnrlat=lllat,
              urcrnrlat=urlat,
              llcrnrlon=lllon,
              urcrnrlon=urlon,
              resolution='f')
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    return m
fig,axes=plt.subplots(nrows=2,ncols=2)