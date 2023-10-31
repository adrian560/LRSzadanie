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


START_COL = "S"
END_COL = "E"
VISITED_COL = "x"
OBSTACLE_COL = "#"
PATH_COL = "@"
FUTURE_OBSTACLE_COL = "*"

def scan_grid(grid, start=(0, 0)):
    """Scan all grid, so we can find a path from 'start' to any point"""

    q = deque()
    q.append(start)
    came_from = {start: None}
    while len(q) > 0:
        current_pos = q.popleft()
        neighbors = get_neighbors(grid, current_pos[0], current_pos[1])
        for neighbor in neighbors:
            if neighbor not in came_from:
                q.append(neighbor)
                came_from[neighbor] = current_pos

    return came_from

def get_neighbors(grid, row, col):
    height = len(grid)
    width = len(grid[0])

    neighbors = [(row + 1, col), (row, col - 1), (row - 1, col), (row, col + 1)]

    # make path nicer
    if (row + col) % 2 == 0:
        neighbors.reverse()

    # check borders
    neighbors = filter(lambda t: (0 <= t[0] < height and 0 <= t[1] < width), neighbors)
    # check obstacles
    neighbors = filter(lambda t: (grid[t[0]][t[1]] != OBSTACLE_COL), neighbors)

    return neighbors

def parse_pgm(data):
    lines = data.split("\n")
    metadata = {}
    pixel_data = []

    # Loop through lines and parse data
    for line in lines:
        # Skip comments
        if line.startswith("#"):
            continue
        # Check for magic number P2
        elif line == "P2":
            metadata["type"] = "P2"
        # Check for width and height
        elif "width" not in metadata:
            metadata["width"], metadata["height"] = map(int, line.split())
        # Check for max gray value
        elif "max_gray" not in metadata:
            metadata["max_gray"] = int(line)
        # Parse pixel data
        else:
            pixel_data.append(list(map(int, line.split())))
    return metadata, pixel_data

def replace_values_in_array(pixel_data):
    for i in range(len(pixel_data)):
        for j in range(len(pixel_data[i])):
            if pixel_data[i][j] == 255:
                pixel_data[i][j] = '.'
            elif pixel_data[i][j] == 0:
                pixel_data[i][j] = '#'
    return pixel_data

def write_2d_array_to_file(pixel_data, filename):
    max_width = max(len(str(item)) for row in pixel_data for item in row)  # Find the maximum width of the items
    with open(filename, 'w') as file:
        for row in pixel_data:
            # Create a formatted string with even spacing, write it to the file
            line = ''.join(f'{item:>{max_width+1}}' for item in row)
            file.write(line + '\n')

def write_pgm(pixel_data, filename, max_value=255):
    # Ensure max_value is valid
    max_value = min(max(max_value, 0), 255)

    # Determine the dimensions of the image
    height = len(pixel_data)
    width = len(pixel_data[0]) if height > 0 else 0

    # Write header and pixel data to file
    with open(filename, 'w') as f:
        f.write(f"P2\n{width} {height}\n{max_value}\n")
        for row in pixel_data:
            f.write(' '.join(map(str, row)) + '\n')

def convert_to_numeric(pixel_data):
    """
    Convert a 2D array of '.' and '#' symbols to a 2D array of 0 and 255 values, respectively.

    :param pixel_data: 2D array containing '.' and '#' symbols.
    :return: A new 2D array with numerical values.
    """
    return [[255 if pixel == '.' else 0 for pixel in row] for row in pixel_data]

def enlarge_walls(filtered_data, runs):
    index = 0
    index2 = 0
    index3 = 0
    row_index = 0
    col_index = 0

    while index < runs:

        for row in filtered_data:
            for data in row:
                if filtered_data[row_index][col_index] == OBSTACLE_COL:
                    while index2 < 3:
                        while index3 < 3:
                            try:
                                if filtered_data[row_index - 1 + index2][col_index - 1 + index3] == "." :
                                    filtered_data[row_index - 1 + index2][col_index - 1 + index3] = FUTURE_OBSTACLE_COL
                            except:
                                pass
                            index3 += 1

                        index2 +=1
                        index3 = 0

                    index2 = 0
                    index3 = 0

                col_index += 1

            row_index += 1
            col_index = 0

        col_index = 0
        row_index = 0
        for row in filtered_data:
            for data in row:
                if data == FUTURE_OBSTACLE_COL:
                    filtered_data[row_index][col_index] = OBSTACLE_COL
                col_index += 1
            row_index += 1
            col_index = 0

        index += 1
        col_index = 0
        row_index = 0

    return filtered_data

def find_path(start, end, came_from):
    """Find the shortest path from start to end point"""

    path = [end]

    current = end
    while current != start:
        current = came_from[current]
        path.append(current)

    # reverse to have Start -> Target
    # just looks nicer
    path.reverse()

    return path

def shorten_path(path):
    point_previous = path[0]
    point_previous2 = path[0]
    point_previous3 = path[0]
    point_previous4 = path[0]
    path_short = []
    sur1 = 0
    sur2 = 0
    index = 0
    index2 = 0
    check = 0

    for point_curent in path:
        if index == 0:
            path_short.append(point_curent)
            index2 += 1

        elif index <= 3:
            pass

        elif ((point_curent[0] - point_previous[0]) == sur3 and (point_curent[1] - point_previous[1]) == sur4) or check == 1:
            check = 0
            pass

        elif (point_curent[0] - point_previous[0]) != sur3 or (point_curent[1] - point_previous[1]) != sur4:
            path_short.append(point_previous)
            index2 += 1
            check = 1


        if index > 0:
            sur1 = point_curent[0] - point_previous[0]
            sur2 = point_curent[1] - point_previous[1]
            sur3 = point_previous[0] - point_previous2[0]
            sur4 = point_previous[1] - point_previous2[1]

        point_previous4 = point_previous3
        point_previous3 = point_previous2
        point_previous2 = point_previous
        point_previous = point_curent

        index += 1

    path_short.append(point_curent)

    return path_short

def draw_path(path, grid):
    for row, col in path:
        grid[row][col] = PATH_COL

    # draw start and end
    start_pos = path[0]
    end_pos = path[-1]
    grid[start_pos[0]][start_pos[1]] = START_COL
    grid[end_pos[0]][end_pos[1]] = END_COL

    return grid

def init():
    x = 0 # suradnica start position
    x_rounded = 0
    x2 = 0 # suradnica end position
    x2_rounded = 0
    y = 0 # suradnica start position
    y_rounded = 0
    y2 = 0 # suradnica end position
    y2_rounded = 0
    z = 0
    j = 0
    map_name = "map_025.pgm"
    path2 = []

    file_path = 'mission_1_all.csv'
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
        x_rounded = math.floor((x * 100) / 5)
        coordinat_start = coordinates[j - 1]
        x = coordinat_start[0]
        y = coordinat_start[1]
        y_rounded = math.floor((y * 100) / 5)
        z = coordinat_start[2]
        x2 = coordinat_end[0]
        x2_rounded = math.floor((x2 * 100) / 5)
        y2 = coordinat_end[1]
        y2_rounded = math.floor((y2 * 100) / 5)

        if z < 0.50:
            map_name = "map_025.pgm"

        elif (z >= 0.50) and (z < 0.90):
            map_name = "map_075.pgm"

        elif (z >= 0.90) and (z < 1.15):
            map_name = "map_100.pgm"

        elif (z >= 1.15) and (z < 1.40):
            map_name = "map_125.pgm"

        elif (z >= 1.40) and (z < 1.60):
            map_name = "map_150.pgm"

        elif (z >= 1.60) and (z < 1.78):
            map_name = "map_175.pgm"

        elif (z >= 1.78) and (z < 1.90):
            map_name = "map_180.pgm"

        elif (z >= 1.90) and (z < 2.15):
            map_name = "map_200.pgm"

        elif z >= 2.15:
            map_name = "map_225.pgm"



        with open(map_name, "rb") as file:
            byte_data = file.read()
            data = byte_data.decode("utf-8")

        metadata, pixel_data = parse_pgm(data)

        pixel_data = replace_values_in_array(pixel_data)
        filtered_data = [sublist for sublist in pixel_data if sublist]

        filtered_data_pgm = convert_to_numeric(filtered_data)
        write_pgm(filtered_data_pgm, 'map.pgm')

        filtered_data = enlarge_walls(filtered_data, 4)

        start_pos = (y_rounded, x_rounded)  # start position in map original (250, 300) (x_rounded, y_rounded) 140, 260
        directions = scan_grid(filtered_data, start_pos)

        path1 = find_path(start_pos, (y2_rounded, x2_rounded), directions)  # end position in map original(50, 35) (x2_rounded, y2_rounded)200, 173

        path1 = shorten_path(path1)

        index_path = 0
        l = [z]
        for iteracia in path1: # rozsiruje path o tretiu z suradnicu (x, y) na (x, y, z)
            iteracia = list(iteracia)
            iteracia.extend(l)
            iteracia = tuple(iteracia)
            path1[index_path] = iteracia
            print(iteracia)
            index_path += 1

        print(path1)
        path2.extend(path1)  #rozsiruje cestu o dalsiu cestu z dalsej mapy ciklus bi sa mal opakovat az do vtedy dokedy su prejdene vsetky mapi


    file_path = "shortened_map.txt"  # vypis mapi do suboru txt
    with open(file_path, 'w') as file:

        for item in path2:
            file.write(str(-(item[1]/20)+((5*14)/20)) + " " + str(-(item[0]/20)+((5*14)/20)) + " " + str(item[2]) + "\n")
        coordinat_end = coordinates[j]
        file.write(str(-(coordinat_end[0])+((5*14)/20)) + " " + str(-(coordinat_end[1])+((5*14)/20)) + " " + str(coordinat_end[2]) + "\n")

    # Close the file
    file.close()

    # odtialto dole mozme ignorovat toto robi len to vykreslovanie cety do tej mapy path_output

#    grid_with_path1 = draw_path(path1, copy.deepcopy(filtered_data))

 #   grid_with_path1_converted = convert_to_numeric(grid_with_path1)

    print(path2)

 #   write_pgm(grid_with_path1_converted, 'path_output.pgm')

if __name__ == "__main__":
    init()

