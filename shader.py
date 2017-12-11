from OpenGL.GL import *
import numpy


class ShaderStageType:
    VertexShader = GL_VERTEX_SHADER
    FragmentShader = GL_FRAGMENT_SHADER


class ShaderStage:
    def __init__(self, stage_type, path):
        self.__id = glCreateShader(stage_type)
        with open(path, "r") as f:
            file = f.read()
            glShaderSource(self.__id, file.encode("utf-8"))
            glCompileShader(self.__id)
        print(self.getInfoLog())

    def getInfoLog(self):
        return glGetShaderInfoLog(self.__id)

    def getId(self):
        return self.__id

    def __del__(self):
        glDeleteShader(self.__id)


class Shader:
    def __init__(self, *shaders):
        self.__id = glCreateProgram()
        for s in shaders:
            glAttachShader(self.__id, s.getId())
        glLinkProgram(self.__id)

    def getInfoLog(self):
        return glGetProgramInfoLog(self.__id)

    def delete(self):
        glDeleteProgram(self.__id)

    def use(self):
        glUseProgram(self.__id)

    def getUniformLocation(self, name):
        return glGetUniformLocation(self.__id, name.encode("utf-8"))

    def getAttribLocation(self, name):
        return glGetAttribLocation(self.__id, name.encode("utf-8"))

    def setUniform(self, location, value):
        if isinstance(value, int):
            glUniform1i(location, numpy.int32(value))
        elif isinstance(value, float):
            glUniform1f(location, numpy.float32(value))
        elif isinstance(value, numpy.ndarray):
            value = value.flatten()
            length = len(value)
            if length == 2:
                glUniform2fv(location, value)
            elif length == 3:
                glUniform3fv(location, value)
            elif length == 4:
                glUniform4fv(location, value)
            elif length == 9:
                glUniformMatrix3fv(location, 1, False, value)
            elif length == 16:
                glUniformMatrix4fv(location, 1, False, value)