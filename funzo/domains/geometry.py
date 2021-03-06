
from __future__ import division

from six.moves import zip

import numpy as np


__all__ = [
    'discretize_space',
    'distance_to_segment',
    'edist',
    'normangle',
    'trajectory_length',
]


def discretize_space(*extents, **kwargs):
    """ Discretize a continuous space

    Transform an N-dimensional continuous space represented by linear extents
    in each axis.

    Parameters
    -----------
    extents : tuples
        1D tuples representing (min, max, step) for each coordinate axis of the
        the continuous space

    Returns
    --------
    X1, X2, ..., XN : numpy.ndarray
        N dimensional arrays for traversing the discretized cells of the final
        space

    """
    coords = (np.arange(e[0], e[1], e[2]) for e in extents)
    cell_indices = np.meshgrid(*coords, indexing='ij')
    return cell_indices


def normangle(theta, start=0):
    """ Normalize an angle to be in the range :math:`[0, 2\pi]`

    Parameters
    -----------
    theta : float
        input angle to normalize

    start: float
        input start angle (optional, default: 0.0)

    Returns
    --------
    res : float
        normalized angle or :math:`\infty`

    """
    if theta < np.inf:
        while theta >= start + 2 * np.pi:
            theta -= 2 * np.pi
        while theta < start:
            theta += 2 * np.pi
        return theta
    else:
        return np.inf


def trajectory_length(traj):
    """ Compute the length of a 2D trajectory

    Parameters
    -----------
    traj : array-like
        Trajectory representing the path traveled as an array of
        shape [n_waypoints x frame_size]. Frame encodes information at
        every time step e.g [x, y, theta, ...]

    Returns
    ---------
    path_length : float
        Length of the path as a sum of Euclidean distance between successive
        way-points.
    """

    traj = np.asarray(traj)
    if traj.ndim != 2:
        raise ValueError("Trajectory must be a two dimensional array")

    d = np.diff(traj[:, 0:2], axis=0)
    n = np.linalg.norm(d, axis=1)

    return np.sum(n)


def edist(v1, v2):
    """ Euclidean distance between two 2D vectors """
    return np.hypot(v1[0] - v2[0], v1[1] - v2[1])


def distance_to_segment(point, line_start, line_end):
    """ Distance from a 2D point to a line segment

    Parameters
    -----------
    point : array-like, shape (2,)
        A point in 2D
    line_start, line_end : array-like, shape (2,)
        Start and end point of the line

    Returns
    -------
    dist : float
        The distance from the point to the line segment if inside is true,
         otherwise None
    inside : bool
        Flag indicating if th distance is within the two perpendicular lines
         from the line segment ends

    """
    xa, ya = line_start[0], line_start[1]
    xb, yb = line_end[0], line_end[1]
    xp, yp = point[0], point[1]

    # x-coordinates
    A = xb - xa
    B = yb - ya
    C = yp * B + xp * A
    a = 2 * ((B * B) + (A * A))
    b = -4 * A * C + (2 * yp + ya + yb) * A * B - (2 * xp + xa + xb) * (B * B)
    c = 2 * (C * C) - (2 * yp + ya + yb) * C * B + \
        (yp * (ya + yb) + xp * (xa + xb)) * (B * B)
    if b * b < 4 * a * c:
        return None, False
    x1 = (-b + np.sqrt((b * b) - 4 * a * c)) / (2 * a)
    x2 = (-b - np.sqrt((b * b) - 4 * a * c)) / (2 * a)

    # y-coordinates
    A = yb - ya
    B = xb - xa
    C = xp * B + yp * A
    a = 2 * ((B * B) + (A * A))
    b = -4 * A * C + (2 * xp + xa + xb) * A * B - (2 * yp + ya + yb) * (B * B)
    c = 2 * (C * C) - (2 * xp + xa + xb) * C * B + \
        (xp * (xa + xb) + yp * (ya + yb)) * (B * B)
    if b * b < 4 * a * c:
        return None, False
    y1 = (-b + np.sqrt((b * b) - 4 * a * c)) / (2 * a)
    y2 = (-b - np.sqrt((b * b) - 4 * a * c)) / (2 * a)

    # Put point candidates together
    candidates = ((x1, y2), (x2, y2), (x1, y2), (x2, y1))
    distances = (edist(candidates[0], point), edist(candidates[1], point),
                 edist(candidates[2], point), edist(candidates[3], point))
    max_index = np.argmax(distances)
    cand = candidates[max_index]
    dmax = distances[max_index]

    start_cand = (line_start[0] - cand[0], line_start[1] - cand[1])
    end_cand = (line_end[0] - cand[0], line_end[1] - cand[1])
    dotp = (start_cand[0] * end_cand[0]) + (start_cand[1] * end_cand[1])

    inside = False
    if dotp <= 0.0:
        inside = True

    return dmax, inside
