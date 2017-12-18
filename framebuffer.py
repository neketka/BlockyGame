from OpenGL.GL import *


class Framebuffer:
    def __init__(self, colorAttachments, depthAttachment=None, depthStencilAttachment=None):
        if colorAttachments is None:
            self.__id = 0
            return
        self.__id = glGenFramebuffers(1)
        for color in colorAttachments:
            color.attach(self.__id)
        if depthAttachment is not None:
            depthAttachment.attach(self.__id)
        elif depthStencilAttachment is not None:
            depthStencilAttachment.attach(self.__id)

    def clear(self, color, depth, stencil):
        mask = 0
        if color:
            mask |= GL_COLOR_BUFFER_BIT
        if depth:
            mask |= GL_DEPTH_BUFFER_BIT
        if stencil:
            mask |= GL_STENCIL_BUFFER_BIT
        self.bind()
        glClear(mask)

    def bind(self):
        if Framebuffer.Bound == self.__id:
            return
        glBindFramebuffer(GL_FRAMEBUFFER, self.__id)
        Framebuffer.Bound = self.__id

    def delete(self):
        glDeleteFramebuffers(1, [self.__id])

    Bound = 0
    DisplayFramebuffer = None

Framebuffer.DisplayFramebuffer = Framebuffer(None)
