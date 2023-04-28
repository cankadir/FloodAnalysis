#%%

import geopandas as gpd
import pandas as pd
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42
import matplotlib.pyplot as plt
import seaborn as sns

#%%

path = r'C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\MapPluto_HowardBeach.geojson'
lots = gpd.read_file( path )
#lots = lots[['BBL','geometry']]
lots['TideZone'] = "Not in"
lots = lots.to_crs(epsg=4326)
lots.head()

# %%

path = r'C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\Pluto_underSandy.geojson'
u50 = gpd.read_file( path )
u50['TideZone'] = "Sandy"

reduced_lots = lots[ ~lots['BBL'].isin(u50['BBL']) ]
lots = reduced_lots.append( u50 )

print(len(lots))

# %%

path = r'C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\Pluto_under2100HT.geojson'
u50 = gpd.read_file( path )
u50['TideZone'] = "2100"

reduced_lots = lots[ ~lots['BBL'].isin(u50['BBL']) ]
lots = reduced_lots.append( u50 )

print(len(lots))
# %%

path = r'C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\Pluto_under2080HT.geojson'
u50 = gpd.read_file( path )
u50['TideZone'] = "2080"

reduced_lots = lots[ ~lots['BBL'].isin(u50['BBL']) ]
lots = reduced_lots.append( u50 )

print(len(lots))

#%%

path = r'C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\Pluto_under2050HT.geojson'
u50 = gpd.read_file( path )
u50['TideZone'] = "2050"

reduced_lots = lots[ ~lots['BBL'].isin(u50['BBL']) ]
lots = reduced_lots.append( u50 )

print(len(lots))
# %%

path = r'C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\Pluto_under2020HT.geojson'
u20 = gpd.read_file( path )
u20['TideZone'] = "2020"

reduced_lots = lots[ ~lots['BBL'].isin(u20['BBL']) ]

lots = reduced_lots.append( u20 )

#%%

import matplotlib.pyplot as plt

lots.plot(column="TideZone",categorical=True)


# %%

path = r'C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\MapPluto_HowardBeach_Tide2.geojson'
lots.to_file( path, driver="GeoJSON")
# %% Visuals
#Map Pluto
path = "/Users/saraeichner/Dropbox/FloodWatch_Repo/GIS/Process_Data/FA_Pluto.geojson"
gdf = gpd.read_file( path )

import seaborn as sns
gr = gdf.groupby( by='TideZone', as_index=False).size()

gr['perc'] = (gr['size'] / gr['size'].sum()) * 100
gr

sns.barplot(data = gr , y='TideZone' , x = 'perc' ,orient='h' , color = 'black')
plt.grid(axis="x")
plt.savefig( "/Users/saraeichner/Dropbox/FloodWatch_Repo/GIS/Process_Data/TideZones.pdf" )

# %%
path = r"C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\FA_311.geojson"
gdf = gpd.read_file( path )

gr = gdf.groupby(by='Descriptor' , as_index = False ).size()
gr = gr.sort_values(by='size',ascending=False)

gr = gr[ gr['Descriptor'] != 'Leak (Use Comments) (WA2)' ]

sns.barplot(data=gr , y='Descriptor' , x = 'size' , orient='h', color = 'black')
plt.grid(axis="x")
sns.despine(top=True,right=True,bottom=True)
plt.savefig( r"C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\311_Group.pdf" )
plt.show()

# %% Time 

path = r"C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\FA_311.geojson"
gdf = gpd.read_file( path )

gdf['Created Date'] = pd.to_datetime( gdf['Created Date'] )
gdf = gdf[ gdf['Descriptor'] != 'Leak (Use Comments) (WA2)' ]
gdf = gdf[ gdf['Descriptor'] != 'Hydrant Leaking (WC1)' ]
gdf = gdf[ gdf['Descriptor'] != 'Water Meter Broken/Leaking - Private Residence (CMR)' ]

gdf = gdf[ gdf['Descriptor'].isin(gr[ gr['size'] > 5 ]['Descriptor'].tolist()) ]

gdf['month'] = gdf['Created Date'].dt.month
gdf['year'] = gdf['Created Date'].dt.year
gdf = gdf[ gdf['year'] < 2021 ]
gdf['season'] = None

gdf.loc[ gdf['month'].isin([1,2,3]) , "season" ] = 'Q1'
gdf.loc[ gdf['month'].isin([4,5,6]) , "season" ] = 'Q2'
gdf.loc[ gdf['month'].isin([7,8,9]) , "season" ] = 'Q3'
gdf.loc[ gdf['month'].isin([10,11,12]) , "season" ] = 'Q4'

pt = pd.pivot_table( data = gdf[["Descriptor",'year','season']].copy() , index="Descriptor" , columns = ['year','season'] , aggfunc=len )

pt = pt.reindex( pt.sum(axis=1).sort_values(ascending=False).index.tolist() )

plt.figure( figsize=(12,3))
sns.heatmap( data = pt , cmap = 'autumn_r')

plt.savefig( r"C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\311_Time.pdf" )
plt.show()


# %%

gr[ gr['size'] > 2 ]['Descriptor'].tolist()
# %%
pt.sum(axis=1).sort_values(ascending=False).index.tolist()


# %%

path = r"C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\FW_Filteres.geojson"
gdf = gpd.read_file( path )

gdf['Date and Time of Observation'] = pd.to_datetime( gdf['Date and Time of Observation'] )

gdf.head()
# %%

gdf.columns = [
    'ObjectID', 'time',
    'flooded now',
    'what flooded',
    'O_What Flooded',
    'How Deep',
    'Weather',
    'O_Weather',
    'Cause', 'O_Cause',
    'Additional Comments', 'Contact Information', 'May we contact you?',
    'Photo', 'Longitude', 'Latitude', 'geometry'
]
gdf.head()

# %%
gdf['time'] = pd.to_datetime( gdf['time'] )
gdf['Weather']  = gdf['Weather'].fillna("NA")

gdf = gdf.set_index( 'time' )
#%%
gr = gdf.resample("1M").size().reset_index()

gr.columns = ['time','count']

plt.figure( figsize=(12,6))
gr.plot(kind='bar',x='time',y='count')
sns.despine(top=True,right=True,left=True)
plt.grid(axis='y')
plt.savefig( r"C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\FW_DataTime.pdf" )

plt.show()

# %%
g = gdf.groupby([pd.Grouper(freq="M"),'How Deep']).size().reset_index()
g.columns = ['time','depth','count']

#g.plot(kind='scatter',x='time',y='depth')
plt.figure( figsize=(15,3) )
sns.scatterplot( data = g , x = 'time' , y='depth')
sns.despine(top=True,right=True,left=True)
plt.grid(axis='y')
plt.xticks(rotation=90)
plt.savefig( r"C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\FW_DepthTime.pdf" )

plt.show()
# %%
pd.set_option('display.max_columns', None)
path = r"C:\Users\csucuogl\Dropbox\FloodWatch_Repo\Process_Data\FA_311.geojson"
gdf = gpd.read_file( path )

gdf.head()
# %%

gdf.groupby(by='Status').size()
# %%
gdf['Created Date'] = pd.to_datetime( gdf['Created Date'] )
gdf['Closed Date'] = pd.to_datetime( gdf['Closed Date'] )

times = []
for i,r in gdf.iterrows():
    t = ( r['Closed Date']  - r['Created Date'] ).seconds/3600
    times.append( t )
    #print(t)


gdf['elapsed'] = times

gdf['elapsed'].hist( bins = 96)

# %%
len( gdf[ gdf['elapsed'] > gdf['elapsed']] )
# %%

gdf['elapsed'].quantile(0.5)
# %%

gdf.groupby( by='Agency' ).size()
# %%
