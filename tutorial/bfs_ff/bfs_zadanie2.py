# Simple example of BFS algorithm adapted from https://github.com/shkolovy/path-finder-algorithms          

from pprint import pprint
from collections import deque
import copy
import numpy as np
#from PIL import Image
import numpy as np
import csv
import re
import math


def find_path(map, start, end):
    """Find the shortest path from start to end point"""
    path_check = 0
    row_index = 0
    column_index = 0
    no_wall_check = 0
    min_distance_of_conection = 50.0
    x_map_size = len(map)
    y_map_size = len(map[0])
    z_map_size = len(map[0][0])
    matrix_shape = (x_map_size, y_map_size, z_map_size)

    path = []
    paths = []


    paths.append([start])

    while path_check == 0:

        points = []
        points_checks = []

        random_point = generate_random_points(matrix_shape, 1) # vygeneruje nahodny bod v mape
        index = 0
        a = 0
        b = 0
        first_tuples = [row[0] for row in paths]
        while a <= row_index: # vytvori list bodov ktore nemaju koliziu medzi sebou a generovanim bodom
            if False == is_wall_between(map, first_tuples[a], random_point):
                points.append(first_tuples[a])
                points_checks.append(a)
                index += 1
                no_wall_check = 1
            a += 1

        if no_wall_check == 1:
            min_distance = 0.0
            min_distance_last = 1000.0
            point_of_min_dis = 0
            while b <= (index-1): # ziska najbizsi bod a jeho poziciu v paths
                min_distance = distance_betwen_points(points[b], random_point)
                if min_distance < min_distance_last:
                    min_distance_last = min_distance
                    point_of_min_dis = points_checks[b]
                b += 1

            no_wall_check = 0
            # pripojenie novej cesty k paths
            row_index += 1
            paths.append([])
            paths[row_index].append(tuple(random_point[0]))
            paths[row_index].extend(paths[point_of_min_dis])

            first_tuples = [row[0] for row in paths]
            # skontroluje ci je blizko ciela
            D = distance_betwen_start_end(paths[row_index][0], end)
            print(D)
            if D <= min_distance_of_conection:
                if False == is_wall_between(map, first_tuples[row_index], [end]):
                    path.extend(paths[row_index])
                    path = path[::-1]
                    path_check = 1

    return path

def generate_random_points(matrix_shape, num_points):
    # Generate random 3D points inside a given matrix.

    x_size, y_size, z_size = matrix_shape
    points = []

    for p in range(num_points):
        # Generate random coordinates within the matrix bounds
        x = np.random.randint(0, x_size)
        y = np.random.randint(0, y_size)
        z = np.random.randint(0, z_size)

        points.append((x, y, z))

    return points

def is_wall_between(matrix, start, target):
    x1, y1, z1 = start
    x2 = target[0][0]
    y2 = target[0][1]
    z2 = target[0][2]

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    # Calculate steps needed to traverse the line
    steps = max(abs(dx), abs(dy), abs(dz))

    # Increment values for each step
    step_x = dx / steps if steps != 0 else 0
    step_y = dy / steps if steps != 0 else 0
    step_z = dz / steps if steps != 0 else 0

    # Traverse the line between start and target points
    current_x, current_y, current_z = x1, y1, z1
    for p in range(int(steps) + 1):
        current_x = round(current_x)
        current_y = round(current_y)
        current_z = round(current_z)

        # Check if the current position is inside the matrix
        if (
            0 <= current_x < len(matrix) and
            0 <= current_y < len(matrix[0]) and
            0 <= current_z < len(matrix[0][0])
        ):
            # Check if there is a wall at the current position
            if matrix[current_x][current_y][current_z] == 1:
                return True  # There is a wall between the points

        current_x += step_x
        current_y += step_y
        current_z += step_z

    return False  # No wall between the points

def distance_betwen_points(start, end):
    # Euclidean distance between two 3D points.
    x = end[0][0]
    y = end[0][1]
    z = end[0][2]
    end = (x, y, z)
    distance = math.sqrt(
        (end[0] - start[0]) ** 2 +
        (end[1] - start[1]) ** 2 +
        (end[2] - start[2]) ** 2
    )

    return distance

def distance_betwen_start_end(start, end):
    # Euclidean distance between two 3D points.
    distance = math.sqrt(
        (end[0] - start[0]) ** 2 +
        (end[1] - start[1]) ** 2 +
        (end[2] - start[2]) ** 2
    )

    return distance

def init():

    path2 = []

    file_path = 'mission_2_simple.csv' # rozmery 183, 144, 60
    numeric_pattern = re.compile(r'\d+\.\d+')
    coordinates_values = []



    # Read the CSV file and extract coordinates values.
    with open(file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            for cell in row:
                numeric_matches = re.findall(numeric_pattern, cell)
                coordinates_values.extend(numeric_matches)

    coordinates_values = [float(value) for value in coordinates_values]

    # Print the extracted coordinates.
    print(coordinates_values)

    coordinates = []

    for i in range(0, len(coordinates_values), 3):
        tuple_of_numbers = (coordinates_values[i], coordinates_values[i + 1], coordinates_values[i + 2])
        coordinates.append(tuple_of_numbers)

    # Print the coordinates.
    print(coordinates)



    for j in range(1, len(coordinates)):

        coordinat_end = coordinates[j]
        coordinat_start = coordinates[j - 1]
        x = coordinat_start[0]
        x_rounded = math.floor((x * 100) / 10)
        y = coordinat_start[1]
        y_rounded = math.floor((y * 100) / 10)
        z = coordinat_start[2]
        z_rounded = math.floor((z * 100) / 10)
        x2 = coordinat_end[0]
        x2_rounded = math.floor((x2 * 100) / 10)
        y2 = coordinat_end[1]
        y2_rounded = math.floor((y2 * 100) / 10)
        z2 = coordinat_end[2]
        z2_rounded = math.floor((z2 * 100) / 10)


        # loading map --------------------
        file_path2 = 'matrix_3d.npy'
        loaded_3d_map = np.load(file_path2)
        print(loaded_3d_map[0][0][0])

        path1 = find_path(loaded_3d_map, (x_rounded, y_rounded, z_rounded), (x2_rounded, y2_rounded, z2_rounded))

        print(path1)
        path2.extend(path1)  #rozsiruje cestu o dalsiu cestu z dalsej mapy ciklus bi sa mal opakovat az do vtedy dokedy su prejdene vsetky mapi


    # upravit------------------
    file_path = "shortened_map.txt"  # vypis mapi do suboru txt

    with open(file_path, 'w') as file:

        for item in path2:
            file.write(str(-(item[0]/10)) + " " + str(-(item[1]/10)) + " " + str(item[2]/10) + "\n")

        file.write(str(-(coordinat_end[0])) + " " + str(-(coordinat_end[1])) + " " + str(coordinat_end[2]) + "\n")

    # Close the file
    file.close()

    print(path2)

if __name__ == "__main__":
    init()
