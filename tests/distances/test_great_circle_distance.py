import numpy as np

from vehicle_location_service.distances import great_circle_distance_matrix


def test_great_circle_distance():
    sources = np.array([[-23.456, -46.456]])
    destinations = np.array([[-23.456, -46.456], [-23.789, -46.789]])

    distance_matrix = great_circle_distance_matrix(sources, destinations)

    assert distance_matrix.shape == (1, 2)
