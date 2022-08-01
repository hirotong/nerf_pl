import numpy as np
import re
import sys

def read_pfm(filename):
    with open(filename, 'rb') as file:
        color = None
        width = None
        height = None
        scale = None
        endian = None

        header = file.readline().decode('utf-8').rstrip()
        if header == 'PF':
            color = True
        elif header == 'Pf':
            color = False
        else:
            raise Exception('Not a PFM file.')

        if dim_match := re.match(
            r'^(\d+)\s(\d+)\s$', file.readline().decode('utf-8')
        ):
            width, height = map(int, dim_match.groups())
        else:
            raise Exception('Malformed PFM header.')

        scale = float(file.readline().rstrip())
        if scale < 0:  # little-endian
            endian = '<'
            scale = -scale
        else:
            endian = '>'  # big-endian

        data = np.fromfile(file, f'{endian}f')
        shape = (height, width, 3) if color else (height, width)

        data = np.reshape(data, shape)
        data = np.flipud(data)
    return data, scale


def save_pfm(filename, image, scale=1):
    with open(filename, "wb") as file:
        color = None

        image = np.flipud(image)

        if image.dtype.name != 'float32':
            raise Exception('Image dtype must be float32.')

        if len(image.shape) == 3 and image.shape[2] == 3:  # color image
            color = True
        elif len(image.shape) == 2 or len(image.shape) == 3 and image.shape[2] == 1:  # greyscale
            color = False
        else:
            raise Exception('Image must have H x W x 3, H x W x 1 or H x W dimensions.')

        file.write('PF\n'.encode('utf-8') if color else 'Pf\n'.encode('utf-8'))
        file.write(f'{image.shape[1]} {image.shape[0]}\n'.encode('utf-8'))

        endian = image.dtype.byteorder

        if endian == '<' or endian == '=' and sys.byteorder == 'little':
            scale = -scale

        file.write(('%f\n' % scale).encode('utf-8'))

        image.tofile(file)