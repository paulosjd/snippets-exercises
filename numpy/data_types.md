NumPy stores values using its own data types, which are distinct from Python types like float and str. This is because the core of NumPy is written in a programming language called C, which stores data differently than the Python data types.
These mostly map to Python data types, like float, and str. Data types additionally end with a suffix that indicates how many bits of memory they take up. So `int32` is a 32 bit integer data type, and `float64` is a 64 bit float data type.

**np.generic**

    In[234]: ', '.join([str(a) for a in np.ScalarType])
    Out[233]: "<class 'int'>, <class 'float'>, <class 'complex'>, <class 'int'>, <class 'bool'>, <class 'bytes'>, <class 'str'>, <class 'memoryview'>, <class 'numpy.complex128'>, <class 'numpy.timedelta64'>, <class 'numpy.int32'>, <class 'numpy.uint8'>, <class 'numpy.float64'>, <class 'numpy.void'>, <class 'numpy.int64'>, <class 'numpy.uint32'>, <class 'numpy.object_'>, <class 'numpy.int8'>, <class 'numpy.int32'>, <class 'numpy.uint64'>, <class 'numpy.int16'>, <class 'numpy.uint32'>, <class 'numpy.str_'>, <class 'numpy.datetime64'>, <class 'numpy.float32'>, <class 'numpy.bool_'>, <class 'numpy.float64'>, <class 'numpy.complex128'>, <class 'numpy.float16'>, <class 'numpy.bytes_'>, <class 'numpy.uint16'>, <class 'numpy.complex64'>"

Python defines only one type of a particular data class (there is only one integer type, one floating-point type, etc.). For scientific computing, however, more control is often needed.

In NumPy, there are 24 new fundamental Python types to describe different types of scalars. These type descriptors are mostly based on the types available in the C language that CPython is written in, with several additional types compatible with Python types.
Array scalars have the same attributes and methods as ndarrays.

Array scalars live in a hierarchy of data types. They can be detected using the hierarchy: For example, `isinstance(val, np.generic)` will return `True` if val is an array scalar object. Alternatively, what kind of array scalar is present can be determined using other members of the data type hierarchy. Thus, for example `isinstance(val, np.complexfloating)` will return `True` if val is a complex valued type

**`class numpy.dtype`**

Data type object describes how the bytes in the fixed-size block of memory corresponding to an array item should be interpreted. It describes the following aspects of the data:

Type of the data (integer, float, Python object, etc.)

Size of the data (how many bytes is in e.g. the integer)

Byte order of the data (little-endian or big-endian)

If the data type is structured, an aggregate of other data types, (e.g., describing an array item consisting of an integer and a float),

What are the names of the fields of the structure, by which they can be accessed,

What is the data-type of each field, and

Which part of the memory block each field takes.

If the data type is a sub-array, what is its shape and data type.`

    # Examples
    >>> dt = np.dtype(float)   # Python-compatible floating-point number
    >>> dt = np.dtype(int)     # Python-compatible integer
    >>> dt = np.dtype(object)  # Python object
    >>> dt = np.dtype('b')  # byte, native byte order
    >>> dt = np.dtype('>H') # big-endian unsigned short
    >>> dt = np.dtype('<f') # little-endian single-precision float
    >>> dt = np.dtype('d')  # double-precision floating-point number
    >>> dt = np.dtype('i4')   # 32-bit signed integer
    >>> dt = np.dtype('f8')   # 64-bit floating-point number
    >>> dt = np.dtype('c16')  # 128-bit complex floating-point number
    >>> dt = np.dtype('a25')  # 25-length zero-terminated bytes
    >>> dt = np.dtype('U25')  # 25-character string

