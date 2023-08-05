from svgpathtools import *

# https://gist.github.com/mathandy/78a0e52da43f8990545389998389e9ba

def path_contains(path: Path, point):
    
    # find a point that's definitely outside path
    xmin, xmax, ymin, ymax = path.bbox()
    B = (xmin + 1) + 1j*(ymax + 1)

    AB_line = Path(Line(point, B))
    number_of_intersections = len(AB_line.intersect(path))
    if number_of_intersections % 2:  # if number of intersections is odd
        return True
    else:
        return False

def path_intersects(path1: Path, path2: Path):
    return len(path1.intersect(path2)) > 0