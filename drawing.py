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
    def __init__(self, shader, uniforms, vao):
        self.__shader = shader
        self.__vao = vao
        self.__uniforms = uniforms

    def draw(self, length=None):
        self.__shader.use()
        for uniform in self.__uniforms:
            self.__shader.setUniform(uniform.getLocation(), uniform.getValue())
        self.__vao.bind()
        glDrawElements(GL_TRIANGLES, self.__vao.getLength() if length is None else length, GL_UNSIGNED_INT, None)

    def drawInstanced(self, instances, length=None):
        self.__shader.use()
        for uniform in self.__uniforms:
            self.__shader.setUniform(uniform.getLocation(), uniform.getValue())
        self.__vao.bind()
        glDrawElementsInstanced(GL_TRIANGLES, self.__vao.getLength() if length is None else length,
                                GL_UNSIGNED_INT, 0, instances)