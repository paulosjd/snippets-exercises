    >>> a = np.array([1, 2, 3, 4])
    >>> a + np.array([2, 3, 4, 5])
    array([3, 5, 7, 9])
    >>> y = np.sin(a)

Inplace operations:

    >>> ary = np.arange(10, 22).reshape((3,4))
    >>> ary[:, 2] += 5
    >>> ary
    array([[10, 11, 17, 13],
           [14, 15, 21, 17],
           [18, 19, 25, 21]])
    >>> ary[:, 2] *= 5