from OpenGL.GL import *
from sdl2.sdlimage import *
import queue


class TextureUnitManager:
    inst = None

    def __init__(self, units):
        self.__units = units
        self.__available = {}
        self.__ageSort = queue.Queue()
        for i in range(0, units):
            self.__available[i - units] = i
            self.__ageSort.put(i - units)
        TextureUnitManager.inst = self

    def acquireUnit(self, id):
        if id in self.__available:
            return self.__available[id]
        else:
            oldId = self.__ageSort.get()
            unit = self.__available[oldId]
            self.__available.pop(id)
            self.__available[id] = unit
            self.__ageSort.put(id)
            return unit

    @staticmethod
    def getInstance():
        return TextureUnitManager.inst


class Texture2D:
    def __init__(self, path):
        surface = IMG_Load(path.encode("utf-8"))
        data = surface.contents
        self.__id = glGenTextures(1)
        self.bind()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, data.w, data.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data.pixels)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def bind(self):
        unit = TextureUnitManager.getInstance().acquireUnit(self.__id)
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, self.__id)
        return unit
