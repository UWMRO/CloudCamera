
import numpy as np


def create_circle_mask(radius: int, img_shape: tuple[int, int], x_center: int | None = None, y_center: int | None = None) -> np.ndarray:
    centers = [img_shape[0]/2, img_shape[1]/2]
    if x_center:
        centers[0] = x_center
    if y_center:
        centers[1] = y_center

    mask = np.full(img_shape, True)
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            if ((i-centers[0]) ** 2) + ((j-centers[1])**2) > (radius**2):
                mask[i, j] = False

    return mask


def make_wedge_mask(radius: int, img_shape: tuple[int, int], ) -> np.ndarray:
    raise NotImplementedError()
