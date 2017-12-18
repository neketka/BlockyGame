from window import *
from texture import *
from framebuffer import *
from drawing import *
from shader import *
from vbo import *
from vao import *
import glmath
import numpy as np


class BlockRegistry:
    def __init__(self, w, h, maxId):
        self.__ids = {}

    def registerNormalBlock(self, id, path):
        pass


class BlockyGame:
    def __init__(self):
        self.__window = Window("Blocky Game", 800, 600)
        self.__window.registerEvent("logic", self.logic)
        self.__window.registerEvent("render", self.render)
        self.__window.registerEvent("resize", self.resize)

        self.texture = Texture2D("./testimage.bmp")
        self.shader = Shader(ShaderStage(ShaderStageType.VertexShader, "./shaders/test.vert"),
                             ShaderStage(ShaderStageType.FragmentShader, "./shaders/test.frag"))
        self.viewport = Viewport(0, 0, 800, 600)

        self.vbo = VBO(np.array([
            -1, -1, 0, 0, 0,
            -1, 1, 0, 0, 1,
            1, 1, 0, 1, 1,
            1, -1, 0, 1, 0
        ], np.float32))

        self.ibo = VBO(np.array([
            0, 1, 2, 2, 3, 0
        ], np.int32), True)

        self.vao = VAO([self.vbo.createBinding([
            AttribBinding(True, self.shader.getAttribLocation("pos"), 12, 3),
            AttribBinding(True, self.shader.getAttribLocation("uv"), 8, 2)
        ])], self.ibo)

        self.model = Uniform(self.shader.getUniformLocation("model"), glmath.translate(0, 0, -5))
        self.proj = Uniform(self.shader.getUniformLocation("proj"), glmath.perspective(3.14 / 2, 800 / 600, 0.3, 1000))
        self.tex = Uniform(self.shader.getUniformLocation("tex"), self.texture)

        self.drawing = DrawingOperation(self.viewport, self.shader, [self.model, self.proj, self.tex], self.vao)
        self.angle = 0

    def logic(self):
        self.model.setValue(np.matmul(glmath.translate(0, 0, -5), glmath.rotationY(self.angle)))
        self.angle += 0.01

    def render(self):
        Framebuffer.DisplayFramebuffer.clear(True, True, False)
        self.drawing.draw()

    def resize(self, w, h):
        self.viewport.set(w=w, h=h)
        self.proj.setValue(glmath.perspective(3.14 / 2, w / h, 0.3, 1000))

    def start(self):
        self.__window.run()
