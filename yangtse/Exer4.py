import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

path='../data/usagov_bitly_data2012-03-16-1331923249.txt'
records=[json.loads(line) for line in open(path)]
frame=pd.DataFrame(records)
# 第一问：用pandas对所在城市进行计数，并绘制最常出现的10个城市的水平条形图
def count_city():
    # print(records[0])
    # cy_counts=frame['cy'].value_counts()
    clean_cy=frame['cy'].fillna('Missing')
    clean_cy[clean_cy=='']="Unknown"
    cy_counts=clean_cy.value_counts()
    print('第一问对城市进行计数：')
    print(cy_counts)

    x= list(cy_counts.index)[:10]
    y= cy_counts[:10].tolist()
    x_pos=np.arange(len(x))
    plt.barh(x_pos, y)
    plt.yticks(x_pos,x,rotation=45)
    plt.title('最常出现的10个城市水平条形图')
    plt.savefig('../data/question1.png')
    plt.show()

# 第二问：使用bit.ly访问记录数据集，根据经纬度(longitude latitude)，绘制所有用户位置的散点图
def make_scatter():
    clean_ll=frame['ll'].fillna('Missing')
    clean_ll[clean_ll == ''] = "Unknown"
    latitude=[]
    longitude=[]
    for content in clean_ll.tolist():
        if type(content)==list:
            latitude.append(content[0])
            longitude.append(content[1])
    # print(latitude)
    map = Basemap(projection='cyl', lat_0=35, lon_0=120,
                  llcrnrlat=20.41, urcrnrlat=52.03,
                  llcrnrlon=-128.67, urcrnrlon=-67.52,
                  rsphere=6371200., resolution='l', area_thresh=10000)
    map.drawmapboundary()
    # map.fillcontinents()
    map.drawstates()
    map.drawcoastlines()
    map.drawcountries()
    map.drawcounties()

    parallels = np.arange(0., 90, 10.)
    map.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    meridians = np.arange(-150., -60., 10.)
    map.drawmeridians(meridians=meridians, labels=[0, 0, 0, 1], fontsize=10)

    x,y=map(longitude,latitude)
    plt.scatter(x,y,s=10)
    # map.scatter(x,y,s=10)
    plt.title('所有用户的经纬度散点图')
    plt.savefig('../data/question2.png')
    plt.show()


# 第三问：使用金融危机数据spx.csv绘制折线图，并标注最大值和最小值
def make_spx_plot():
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    data=pd.read_csv('../data/spx.csv',index_col=0,parse_dates=True)
    spx=data['SPX']
    time=spx.index.tolist()
    value=spx.tolist()
    resource={'time':time,'value':value}
    spx_frame=pd.DataFrame(resource)
    max_time=spx_frame[spx_frame.value==spx.max()].time.tolist()[0]
    min_time=spx_frame[spx_frame.value==spx.min()].time.tolist()[0]
    # print(type(max_time.tolist()[0]),max_time.tolist()[0])
    # print(spx_frame[spx_frame.value==spx.min()].time)
    max_year=max_time.year
    max_month=max_time.month
    max_day=max_time.day

    min_year = min_time.year
    min_month = min_time.month
    min_day = min_time.day
    # print(max_time.year)
    # print(max_time.month)
    # print(max_time.day)

    spx.plot(ax=ax,style='k-')
    crisis_data=[
        (datetime(max_year,max_month,max_day),'Max of bull market'),
        (datetime(min_year,min_month,min_day),'Min of bull market')
    ]
    for date,label in crisis_data:
        ax.annotate(label,xy=(date,spx.asof(date)+50),
                    xytext=(date,spx.asof(date)+200),
                    arrowprops=dict(facecolor='black'),
                    horizontalalignment='left',verticalalignment='top')
        ax.set_xlim(['2/1/1990','1/1/2011'])
        ax.set_ylim([0,1800])
        ax.set_title('Important dates in 2008-2009 financial crisis')
    plt.savefig('../data/question3.png')
    plt.show()

# 第四问：使用小费数据tips.csv，分析聚会规模对小费金额的影响，并绘制柱状图
# （计算不同聚会人数的小费平均值）
def tips_affect():
    tips=pd.read_csv('../data/tips.csv')
    # print(tips)
    size_series=tips['size']
    size_set=set(size_series)
    size_list=list(size_set)
    # print(set(size_series))
    # print(tips['size'].tolist())
    mean_value=[]
    for size in size_set:
        sub_tip=tips[tips['size']==size]
        # print(sub_tip)
        mean_value.append(float(sub_tip['tip'].mean()))
        # print(sub_tip['tip'].mean())
    # print(size_list)
    # print(mean_value)
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.set_title('聚会规模对小费的影响')
    ax.set_xlabel('聚会规模')
    ax.set_ylabel('小费均值')
    ax.bar(size_list,mean_value)
    # plt.bar(size_list,mean_value)
    plt.savefig('../data/question4.png')
    plt.show()


if __name__=='__main__':
    count_city()
    make_scatter()
    make_spx_plot()
    tips_affect()