from OpenGL.GL import *


class VAO:
    def __init__(self, bindings, ibo):
        self.__id = glGenVertexArrays(1)
        self.__len = ibo.getLength()
        glBindVertexArray(self.__id)
        for b in bindings:
            b.bindData()
        ibo.bind()

    def getLength(self):
        return self.__len

    def bind(self):
        glBindVertexArray(self.__id)
