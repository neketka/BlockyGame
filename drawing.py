from OpenGL.GL import *


class Uniform:
    def __init__(self, location, value=None):
        self.__location = location
        self.__value = value

    def getLocation(self):
        return self.__location

    def setValue(self, value):
        self.__value = value

    def getValue(self):
        return self.__value


class Viewport:
    def __init__(self, x, y, w, h):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h

    def set(self, x=None, y=None, w=None, h=None):
        if x is not None:
            self.__x = x
        if y is not None:
            self.__y = y
        if w is not None:
            self.__w = w
        if h is not None:
            self.__h = h

    def setCurrent(self):
        glViewport(self.__x, self.__y, self.__w, self.__h)


class DrawingOperation:
    def __init__(self, viewport, shader, uniforms, vao):
        self.__shader = shader
        self.__vao = vao
        self.__viewport = viewport
        self.__uniforms = uniforms

    def draw(self, length=None):
        self.__shader.use()
        for uniform in self.__uniforms:
            self.__shader.setUniform(uniform.getLocation(), uniform.getValue())
        self.__vao.bind()
        self.__viewport.setCurrent()
        glDrawElements(GL_TRIANGLES, self.__vao.getLength() if length is None else length, GL_UNSIGNED_INT, None)

    def drawInstanced(self, instances, length=None):
        self.__shader.use()
        for uniform in self.__uniforms:
            self.__shader.setUniform(uniform.getLocation(), uniform.getValue())
        self.__vao.bind()
        self.__viewport.setCurrent()
        glDrawElementsInstanced(GL_TRIANGLES, self.__vao.getLength() if length is None else length,
                                GL_UNSIGNED_INT, None, instances)
