from OpenGL.GL import *


class Uniform:
    def __init__(self, location):
        self.__location = location
        self.__value = None

    def getLocation(self):
        return self.__location

    def setValue(self, value):
        self.__value = value

    def getValue(self):
        return self.__value


class DrawingOperation:
    def __init__(self, shader, uniforms, vboBindings, ibo):
        self.__shader = shader
        self.__vboBindings = vboBindings
        self.__ibo = ibo
        self.__uniforms = uniforms

    def draw(self, length=None):
        self.__shader.use()
        for uniform in self.__uniforms:
            self.__shader.setUniform(uniform.getLocation(), uniform.getValue())
        for vboBinding in self.__vboBindings:
            vboBinding.bindData()
        glDrawElements(GL_TRIANGLES, self.__ibo.getLength() if length is None else length, GL_UNSIGNED_INT, 0)

    def drawInstanced(self, instances, length=None):
        self.__shader.use()
        for uniform in self.__uniforms:
            self.__shader.setUniform(uniform.getLocation(), uniform.getValue())
        for vboBinding in self.__vboBindings:
            vboBinding.bindData()
        glDrawElementsInstanced(GL_TRIANGLES, self.__ibo.getLength() if length is None else length,
                                GL_UNSIGNED_INT, 0, instances)