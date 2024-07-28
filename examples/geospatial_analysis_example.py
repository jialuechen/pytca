import geopandas as gpd
import matplotlib.pyplot as plt
from pytca.analysis.geospatial import plot_geospatial_data

# Example data: This would typically be loaded from a file or database.
# Here, we create a simple GeoDataFrame for demonstration purposes.
data = {
    'geometry': [
        'POINT (10 50)',
        'POINT (12 54)',
        'POINT (14 52)',
        'POINT (10 48)',
        'POINT (16 49)'
    ],
    'value': [100, 200, 150, 250, 300]
}
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy([10, 12, 14, 10, 16], [50, 54, 52, 48, 49]))

# Plot the geospatial data
plot_geospatial_data(gdf, 'value')

# Show plot
plt.show()
