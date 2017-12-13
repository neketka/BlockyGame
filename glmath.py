import numpy as np
import math


def identity():
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], np.float32)


def translate(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], np.float32)


def scale(x, y, z):
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ], np.float32)


def rotationX(theta):
    sn = math.sin(theta)
    cs = math.cos(theta)
    return np.array([
        [1, 0, 0, 0],
        [0, cs, sn, 0],
        [0, -sn, cs, 0],
        [0, 0, 0, 1]
    ], np.float32)


def rotationY(theta):
    sn = math.sin(theta)
    cs = math.cos(theta)
    return np.array([
        [cs, 0, -sn, 0],
        [0, 1, 0, 0],
        [sn, 0, cs, 0],
        [0, 0, 0, 1]
    ], np.float32)


def rotationZ(theta):
    sn = math.sin(theta)
    cs = math.cos(theta)
    return np.array([
        [cs, sn, 0, 0],
        [-sn, cs, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], np.float32)


def perspective(fovy, aspect, zNear, zFar):
    top = zNear * math.tan(0.5 * fovy)
    bottom = -top
    left = bottom * aspect
    right = top * aspect
    x = (2.0 * zNear) / (right - left)
    y = (2.0 * zFar) / (top - bottom)
    a = (right + left) / (right - left)
    b = (top + bottom) / (top - bottom)
    c = -(zFar + zNear) / (zFar - zNear)
    d = -(2.0 * zFar * zNear) / (zFar - zNear)
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [a, b, c, -1],
        [0, 0, d, 0]
    ], np.float32)


def ortho(width, height, zNear, zFar):
    left = -width / 2
    right = width / 2
    bottom = -height / 2
    top = height / 2
    invRL = 1.0 / (right - left)
    invTB = 1.0 / (top - bottom)
    invFN = 1.0 / (zFar - zNear)
    return np.array([
        [2 * invRL, 0, 0, 0],
        [0, 2 * invTB, 0, 0],
        [0, 0, -2 * invFN, 0],
        [-(right + left) * invRL, -(top+bottom) * invTB, -(zFar + zNear) * invFN, 1]
    ], np.float32)


def normalize(x):
    return np.divide(x, np.linalg.norm(x))


def lookAt(eye, target, up):
    z = normalize(np.subtract(eye, target))
    x = normalize(np.cross(up, z))
    y = normalize(np.cross(z, x))
    return np.array([
        [x[0], y[0], z[0], 0],
        [x[1], y[1], z[1], 0],
        [x[2], y[2], z[2], 0],
        [
            -((x[0] * eye[0]) + (x[1] * eye[1]) + (x[2] * eye[2])),
            -((y[0] * eye[0]) + (y[1] * eye[1]) + (y[2] * eye[2])),
            -((z[0] * eye[0]) + (z[1] * eye[1]) + (z[2] * eye[2])),
            1
        ]
    ], np.float32)
