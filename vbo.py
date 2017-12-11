from OpenGL.GL import *
import numpy as np


class AttribBinding:
    def __init__(self, _float, location, size, length):
        self.__location = location
        self.__size = size
        self.__length = length
        self.__float = _float

    def getLocation(self):
        return self.__location

    def isFloat(self):
        return self.__float

    def getSize(self):
        return self.__size

    def getLength(self):
        return self.__length


class VBOBinding:
    def __init__(self, vboId, bindings, divisor=None):
        self.__vboId = vboId
        self.__bindings = bindings
        self.__size = 0
        self.__divisor = divisor
        for x in bindings:
            self.__size += x.getSize()

    def bindData(self):
        offset = 0
        for x in self.__bindings:
            glVertexAttribPointer(x.getLocation(), x.getLength(), GL_INT if x.isFloat() else GL_FLOAT,
                                  GL_FALSE, self.__size, offset)
            if self.__divisor is not None:
                glVertexAttribDivisor(x.getLocation(), self.__divisor)
            glEnableVertexAttribArray(x.getLocation())
            offset += x.getSize()


class VBO:
    def __init__(self, data: np.ndarray, index=False, dynamic=False):
        arr = data.flatten()
        self.__id = glGenBuffers(1)
        self.__target = GL_ELEMENT_ARRAY_BUFFER if index else GL_ARRAY_BUFFER
        self.__length = len(arr)
        self.bind()
        glBufferData(self.__target, arr, GL_DYNAMIC_DRAW if dynamic else GL_STATIC_DRAW)

    def bind(self):
        glBindBuffer(self.__target, self.__id)

    def createBinding(self, bindings):
        return VBOBinding(self.__id, bindings)

    def getLength(self):
        return self.__length

    def delete(self):
        glDeleteBuffers(1, [self.__id])