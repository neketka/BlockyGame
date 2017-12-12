from vbo import *
from vao import *
from shader import *
from drawing import *
from sdl2 import *
from sdl2.video import *
import ctypes
import numpy as np
import glmath


class Window:
    def __init__(self, title, w, h):
        SDL_Init(SDL_INIT_VIDEO)
        self.__window = SDL_CreateWindow(title.encode("utf-8"), 100, 100, 800, 600,
                                         SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
        SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
        self.__context = SDL_GL_CreateContext(self.__window)

        self.shader = Shader(ShaderStage(ShaderStageType.VertexShader, "./shaders/test.vert"),
                             ShaderStage(ShaderStageType.FragmentShader, "./shaders/test.frag"))

        self.vbo = VBO(np.array([
            [-1, -1, 1],
            [0, 1, 1],
            [1, -1, 1]
        ], np.float32))

        self.ibo = VBO(np.array([
            0, 1, 2
        ], np.uint32), True)

        self.vao = VAO([self.vbo.createBinding([AttribBinding(False, self.shader.getAttribLocation("pos"), 4, 3)])],
                       self.ibo)

        self.drawing = DrawingOperation(self.shader, [], self.vao)

    def __logic(self):
        pass

    def __render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.drawing.draw()
        SDL_GL_SwapWindow(self.__window)

    def __resize(self, w, h):
        pass

    def __destroy(self):
        self.shader.delete()
        self.vbo.delete()
        self.ibo.delete()
        self.vao.delete()
        SDL_GL_DeleteContext(self.__context)
        SDL_DestroyWindow(self.__window)

    def run(self):
        SDL_ShowWindow(self.__window)
        running = True
        while running:
            event = SDL_Event()
            while SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == SDL_QUIT:
                    running = False
            self.__logic()
            self.__render()
        self.__destroy()
