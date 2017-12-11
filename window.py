import pygame
from vbo import *
from shader import *
from drawing import *
import numpy as np
import glmath


class Window:
    def __init__(self, title, w, h):
        pygame.init()
        pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.set_caption(title)

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

        self.drawing = DrawingOperation(self.shader, [],
            [self.vbo.createBinding([AttribBinding(False, self.shader.getAttribLocation("pos"), 4, 3)])], self.ibo)

    def __logic(self):
        pass

    def __render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.drawing.draw()
        pygame.display.flip()

    def __resize(self, w, h):
        pass

    def __destroy(self):
        self.shader.delete()
        self.vbo.delete()
        self.ibo.delete()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__logic()
            self.__render()
        self.__destroy()
