import geopandas as gpd
import matplotlib.pyplot as plt

def plot_geospatial_data(geodata, attribute):
    geodata.plot(column=attribute, cmap='OrRd', legend=True)
    plt.show()
