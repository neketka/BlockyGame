from OpenGL.GLUT import *
from vbo import *
from shader import *
from drawing import *
import numpy as np
import glmath
import sys


class Window:
    def __init__(self, title, w, h):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(w, h)
        self.window = glutCreateWindow(title.encode('utf-8'))
        glutIdleFunc(self.__logic)
        glutCloseFunc(self.__destroy)
        glutDisplayFunc(self.__render)
        glutReshapeFunc(self.__resize)
        self.shader = Shader(ShaderStage(ShaderStageType.VertexShader, "./shaders/test.vert"),
                             ShaderStage(ShaderStageType.FragmentShader, "./shaders/test.frag"))

        self.vbo = VBO(np.array([
            [-1, -1, 1],
            [0, 1, 1],
            [1, -1, 1]
        ], np.float32), )

        self.ibo = VBO(np.array([
            0, 1, 2
        ]))

        self.drawing = DrawingOperation(self.shader, [],
            [self.vbo.createBinding([AttribBinding(False, self.shader.getAttribLocation("pos"), 4, 3)])], self.ibo)

    def __logic(self):
        pass

    def __render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.drawing.draw()
        glutSwapBuffers()

    def __resize(self, w, h):
        pass

    def __destroy(self):
        self.shader.delete()
        self.vbo.delete()
        self.ibo.delete()

    def run(self):
        glutMainLoop()
