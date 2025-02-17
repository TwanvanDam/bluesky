import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import geopandas
from mpl_toolkits.basemap import Basemap

#Load data
pop = np.genfromtxt('./population_1km.csv', delimiter=',')
# Replace non-positive values with a small positive number
pop[pop <= 0] = 1e0
x = np.genfromtxt('./x_1km.csv', delimiter=',')
y = np.genfromtxt('./y_1km.csv', delimiter=',')

origin_lat = 52.307
origin_lon = 4.761
earth_radius = 6371000  # in meters

lat = origin_lat + (y*1.05 / earth_radius) * (180 / np.pi)
lon = origin_lon + (x / (earth_radius * np.cos(np.pi * origin_lat / 180))) * (180 / np.pi)

nature = geopandas.read_file("./natura2000.gpkg")
nature = nature.to_crs(epsg=4326)



m = Basemap(projection='merc', llcrnrlat=50.5, urcrnrlat=54,
            llcrnrlon=2, urcrnrlon=7.5, resolution='i')
x_map, y_map = m(lon,lat)

# Plot the data
m.drawcountries(linewidth=2)
m.pcolormesh(x_map, y_map, pop, cmap='Reds', norm=colors.LogNorm(vmin=np.min(pop), vmax=np.max(pop)),alpha=0.5)
plt.colorbar(label='Population')

for i in range(len(nature)):
    gebied = nature.iloc[i]
    for poly in gebied["geometry"].geoms:
        x, y = zip(*poly.exterior.coords[:])
        x_map, y_map = m(x,y)
        plt.plot(x_map,y_map,color='g')
        plt.fill(x_map,y_map, alpha=0.5,color='g')
plt.savefig("./Population_data/kaart.png")
plt.show()