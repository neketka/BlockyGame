from OpenGL.GLUT import *
import sys

def display():
    glutSwapBuffers()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("BlockyGame")
    glutDisplayFunc(display)
    glutMainLoop()


if __name__ == "__main__":
    main()

