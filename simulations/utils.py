import numpy

__all__ = [
    "build_banded_matrix"
]

def build_banded_matrix(band, num_rows):
    band = numpy.asarray(band)
    p = numpy.zeros(num_rows-1, dtype=band.dtype)
    b = numpy.concatenate((p,band,p))
    s = b.strides[0]

    return numpy.lib.stride_tricks.as_strided(
        b[num_rows-1:], shape=(num_rows, len(band)+num_rows-1), strides=(-s,s)
    )
