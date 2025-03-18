import math

def get_distance(points):
    """
    Calculate the Euclidean distance between two points.

    Args:
        points (list): A list containing two points, each represented as a tuple (x, y).

    Returns:
        float: The Euclidean distance between the two points.
    """
    (x1, y1), (x2, y2) = points
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_angle(p1, p2, p3):
    """
    Calculate the angle between three points.

    Args:
        p1, p2, p3 (tuple): Points represented as tuples (x, y).

    Returns:
        float: The angle in degrees.
    """
    a = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    b = (p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2
    c = (p3[0] - p1[0]) ** 2 + (p3[1] - p1[1]) ** 2
    angle = math.acos((a + b - c) / math.sqrt(4 * a * b))
    return math.degrees(angle)
