import pandas as pd
import numpy as np

# Generate a sample dataset with specific latitude and longitude ranges
np.random.seed(42)

# Create a DataFrame with latitude, longitude, and datetime columns
num_points = 400
latitudes_start = np.random.uniform(low=44.33, high=44.53, size=num_points)
longitudes_start = np.random.uniform(low=25.96, high=26.23, size=num_points)
latitudes_end = np.random.uniform(low=44.33, high=44.53, size=num_points)
longitudes_end = np.random.uniform(low=25.96, high=26.23, size=num_points)
datetimes = pd.date_range(start='2023-01-01', periods=num_points, freq='H')
id_cursa = [f'Cursa_{i}' for i in range(num_points)]
nume_sofer = [f'Sofer_{i}' for i in range(num_points)]

data = pd.DataFrame({
    'latitude_start': latitudes_start,
    'longitude_start': longitudes_start,
    'latitude_end': latitudes_end,
    'longitude_end': longitudes_end,
    'datetime': datetimes,
    'id_cursa': id_cursa,
    'nume_sofer': nume_sofer
})

# Save the DataFrame to a CSV file
csv_path = "./coordinates_sample_data.csv"
data.to_csv(csv_path, index=False)

print(f"CSV file saved as {csv_path}")
