import numpy as np
import datetime

async def calculate_statistics(coords_with_date: list[datetime.date, float, float]):
    coords_without_date = [x[1:] for x in coords_with_date]
    coords: list = get_coords()
    coords.extend(coords_without_date)
    if len(coords) % 5 == 0:
        update_statistics(coords)
    return 

async def update_statistics(coords: list):
    data = np.array(coords)

    x_bin_size = 1.0
    y_bin_size = 1.0

    x_bins = np.arange(data[:, 0].min(), data[:, 0].max() + x_bin_size, x_bin_size)
    y_bins = np.arange(data[:, 1].min(), data[:, 1].max() + y_bin_size, y_bin_size)

    hist, x_edges, y_edges = np.histogram2d(data[:, 0], data[:, 1], bins=[x_bins, y_bins])

    max_freq_index = np.unravel_index(hist.argmax(), hist.shape)
    max_freq = hist[max_freq_index]

    most_frequent_x_center = (x_edges[max_freq_index[0]] + x_edges[max_freq_index[0] + 1]) / 2
    most_frequent_y_center = (y_edges[max_freq_index[1]] + y_edges[max_freq_index[1] + 1]) / 2

    print(f"Наиболее частая область: около ({most_frequent_x_center}, {most_frequent_y_center})")
    print(f"Количество точек в этой области: {max_freq}")
    return
