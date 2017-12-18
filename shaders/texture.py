from OpenGL.GL import *
from sdl2 import *
import queue


class TextureUnitManager:
    inst = None

    def __init__(self, units):
        self.__units = units
        self.__available = {}
        self.__ageSort = queue.Queue()
        for i in range(0, units):
            self.__available[i - units - 1] = i
            self.__ageSort.put(i - units - 1)
        TextureUnitManager.inst = self

    def acquireUnit(self, id):
        if id in self.__available:
            return self.__available[id]
        else:
            oldId = self.__ageSort.get()
            unit = self.__available[oldId]
            self.__available.pop(oldId)
            self.__available[id] = unit
            self.__ageSort.put(id)
            return unit

    @staticmethod
    def getInstance():
        return TextureUnitManager.inst


class TextureFormatType:
    Unsigned=0, Signed=1, Float=2


class TextureFormat: # R -> G -> B -> A -> Type
    __table = {
        2: {
            2: {
                2: {
                    2: GL_RGBA2
                }
            }
        },
        3: {
            3: {
                2: {
                    0: GL_R3_G3_B2
                }
            }
        },
        4: {
            4: {
                4: {
                    0: GL_RGB4,
                    4: GL_RGBA4
                }
            }
        },
        5: {
            5: {
                5: {
                    0: GL_RGB5,
                    1: GL_RGB5_A1
                }
            }
        },
        8: {
            0: {
                0: {
                    0: GL_R8
                }
            },
            8: {
                0: {
                    0: GL_RG8
                },
                8: {
                    0: GL_RGB8,
                    8: GL_RGBA8
                }
            }
        },
        10: {
            10: {
                10: {
                    0: GL_RGB10,
                    2: {
                        TextureFormatType.Float: GL_RGB10_A2,
                        TextureFormatType.Signed: GL_RGB10_A2,
                        TextureFormatType.Unsigned: GL_RGB10_A2UI
                    }
                }
            }
        },
        11: {

        },
        12: {
            12: {
                12: {
                    0: GL_RGB12
                    12: GL_RGBA12
                }
            }
        },
        16: {
            0: {
                0: {
                    0: {
                        TextureFormatType.Signed: GL_R16,
                        TextureFormatType.Float: GL_R16F,
                        TextureFormatType.Unsigned: GL_R16
                    }
                }
            },
            16: {
                0: {
                    0: {
                        TextureFormatType.Float: GL_RG16F,
                        TextureFormatType.Unsigned: GL_RG16,
                        TextureFormatType.Signed: GL_RG16
                    }
                },
                16: {
                    0: {
                        TextureFormatType.Float: GL_RGB16F
                    },
                    16: {
                        TextureFormatType.Unsigned: GL_RGBA16,
                        TextureFormatType.Signed: GL_RGBA16,
                        TextureFormatType.Float: GL_RGBA16F
                    }
                }
            }
        },
        32: {
            0: {
                0: {
                    0: {
                        TextureFormatType.Float: GL_R32F
                    }
                }
            }
            32: {
                0: {
                    0: {
                        TextureFormatType.Float: GL_RG32F
                    }
                }
                32: {
                    0: {
                        TextureFormatType.Float: GL_RGB32F
                    }
                    32: {
                        TextureFormatType.Float: GL_RGBA32F
                    }
                }
            }
        }
    }
    def __init__(self, r, g=0, b=0, a=0, type=TextureFormatType.Float):


class Texture2D:
    def __init__(self, path):
        surface = SDL_LoadBMP(path.encode("utf-8"))
        data = surface.contents
        self.__id = glGenTextures(1)
        self.bind()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, data.w, data.h, 0, GL_RGB, GL_UNSIGNED_BYTE, data.pixels)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        SDL_FreeSurface(surface)

    def bind(self):
        unit = TextureUnitManager.getInstance().acquireUnit(self.__id)
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, self.__id)
        return unit


class TextureCubemap:
    def __init__(self, paths):
        self.__id = glGenTextures(1)
        binding = GL_TEXTURE_CUBE_MAP_POSITIVE_X
        for path in paths:
            surface = SDL_LoadBMP(path.encode("utf-8"))
            data = surface.contents
            glBindTexture(binding, self.__id)
            glTexImage2D(binding, 0, GL_RGB, data.w, data.h, 0, GL_RGB, GL_UNSIGNED_BYTE, data.pixels)
            glTexParameteri(binding, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(binding, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(binding, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(binding, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            binding += 1

    def bind(self):
        unit = TextureUnitManager.getInstance().acquireUnit(self.__id)
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.__id)
        return unit


class Texture2DArray:
    def __init__(self, width, height, layers):
        self.__id = glGenTextures(1)
        self.__width = width
        self.__height = height
        self.bind()
        glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_RGB, width, height, layers, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    def bind(self):
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.__id)

    def setLayer(self, layer, data):
        self.bind()
        glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0, 0, 0, layer, self.__width, self.__height,
                        1, GL_RGB, GL_UNSIGNED_BYTE, data)