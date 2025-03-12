from numpy import tan, deg2rad, arctan, rad2deg
from math import floor

feet = 3.28084
knots = 1.852
cruise_angle = 3.39
slow_angle = 4.23

start_angle = 2.91
first_angle = 3.09

def required_height(distance, angle=cruise_angle, start=False):
    angle = deg2rad(angle)
    if start == True:
        manouvre_distance = 1000 / feet / tan(deg2rad(start_angle))
    elif start == False:
        manouvre_distance = 1000 / feet / tan(deg2rad(first_angle))
    else:
        manouvre_distance = 1000 / feet / tan(angle)
    height = (distance - manouvre_distance / 1000) * tan(angle)
    height = feet * height * 1000 + 1000
    return height

def required_distance(height, angle=cruise_angle):
    angle = deg2rad(angle)
    distance = height / feet / tan(angle) / 1000
    return distance


def angle_finder(vertical, horizontal):
    dis_per_min = horizontal / 60 * knots * 1000
    height_per_min = vertical / feet
    angle = arctan(height_per_min/dis_per_min)
    angle = rad2deg(angle)
    return angle

def angle_finder_2(alt, dist):
    alt = alt / feet
    dist = dist * 1000
    angle = arctan(alt/dist)
    angle = rad2deg(angle)
    return angle

print(floor(required_height(29.6, start=True)))
print(floor(required_height(76.9, start=True)))