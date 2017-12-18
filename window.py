from sdl2 import *
from sdl2.video import *
from texture import TextureUnitManager
from OpenGL.GL import *
import ctypes


class Window:
    def __init__(self, title, w, h):
        SDL_Init(SDL_INIT_VIDEO)
        self.__window = SDL_CreateWindow(title.encode("utf-8"), 100, 100, 800, 600,
                                         SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 2)
        SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
        self.__context = SDL_GL_CreateContext(self.__window)
        TextureUnitManager.inst = TextureUnitManager(glGetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS))
        self.__events = {"delete": [], "render": [], "logic": [], "resize": []}

    def __logic(self):
        for e in self.__events["logic"]:
            e()

    def __render(self):
        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for e in self.__events["render"]:
            e()
        SDL_GL_SwapWindow(self.__window)

    def __resize(self, w, h):
        for e in self.__events["resize"]:
            e(w, h)

    def __destroy(self):
        for e in self.__events["delete"]:
            e()
        SDL_GL_DeleteContext(self.__context)
        SDL_DestroyWindow(self.__window)

    def registerEvent(self, event, callback):
        self.__events[event].append(callback)

    def run(self):
        SDL_ShowWindow(self.__window)
        running = True
        while running:
            event = SDL_Event()
            while SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_WINDOWEVENT:
                    if event.window.event == SDL_WINDOWEVENT_RESIZED:
                        self.__resize(event.window.data1, event.window.data2)
            self.__logic()
            self.__render()
        self.__destroy()
