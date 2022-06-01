import OpenGL
from ctypes import *
import glm

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

from helpers import *

width = 800
height = 600

vertices = [
   # COORDINATES  /COLORS        / TexCoord
    0.5, 0.0, 0.5, 0.0, 1.0, 0.0, 0.0, 0.0, # Vertex 0 Top Right Green
    0.5, 0.0, -0.5, 0.0, 0.0, 1.0, 0.0, 0.0, # Vertex 1 Bottom Right Blue
    -0.5, 0.0, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, # Vertex 2 Bottom Left Yellow
    -0.5, 0.0, 0.5, 1.0, 1.0, 0.0, 0.0, 0.0, # Vertex 3 Top Left Yellow
    0.0, 1.5, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, # Vertex 4 Pyramid top Red
] 

# PYRAMID
indices = [
     0, 1, 2, # Triangle 1
    0, 3, 2, # Triangle 2
    0, 1, 4, # Triangle 3
    1, 2, 4, # Triangle 4
    2, 3, 4, # Triangle 5
    3, 0, 4, # Triangle 6
]







vertex_shader = """
#version 330 core

// Positions/Coordinates
layout (location = 0) in vec3 aPos;
// Colors
layout (location = 1) in vec3 aColor;
// Texture Coordinates
layout (location = 2) in vec2 aTex;


// Outputs the color for the Fragment Shader
out vec3 color;
// Outputs the texture coordinates to the fragment shader
out vec2 texCoord;

// Controls the scale of the vertices
uniform float scale;

// Inputs the matrices needed for 3D viewing with perspective
uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;


void main()
{
	// Outputs the positions/coordinates of all vertices
	gl_Position = proj * view * model * vec4(aPos, 1.0);
	// Assigns the colors from the Vertex Data to "color"
	color = aColor;
	// Assigns the texture coordinates from the Vertex Data to "texCoord"
	texCoord = aTex;
}
"""

fragment_shader = """
#version 330 core

// Outputs colors in RGBA
out vec4 FragColor;

// Inputs the color from the Vertex Shader
in vec3 color;

void main()
{
	FragColor = vec4(color, 1.0);
}
"""


# make context
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutCreateWindow("Pyramid")
# WITHOUT THIS YOU WILL HAVE TRANSPARENT COLORS & TRANSPARENT FACES OF THE SHAPE
glEnable(GL_DEPTH_TEST);


# compile shaders
vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)

# create program
program = glCreateProgram()
glAttachShader(program, vertex_shader)
glAttachShader(program, fragment_shader)
glLinkProgram(program)

# use program
glUseProgram(program)

# create a vertex array object (VAO)
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

# create a vertex buffer object (VBO)
id = 0
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)

# create a element buffer object (EBO)
ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(
    GL_ELEMENT_ARRAY_BUFFER, # target
    len(indices) * 100, # size
    (c_int * len(indices))(*indices), # data
    GL_STATIC_DRAW # usage
)


# copy data to the GPU
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 5, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)

# specify the format of the "position" attribute
# glVertexAttribPointer(layout, numComponents, type, GL_FALSE, stride, offset);
# VAO1.LinkAttrib(0, 3, GL_FLOAT, 8 * sizeof(float), (void *)0);

#bind vbo
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 8, c_void_p(0))
glEnableVertexAttribArray(0)
glBindBuffer(GL_ARRAY_BUFFER, 0)

glBindBuffer(GL_ARRAY_BUFFER, vbo)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 8, c_void_p(3 * sizeof(c_float)))
glEnableVertexAttribArray(1)
glBindBuffer(GL_ARRAY_BUFFER, 0)

glBindBuffer(GL_ARRAY_BUFFER, vbo)
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, sizeof(c_float) * 8, c_void_p(6 * sizeof(c_float)))
glEnableVertexAttribArray(2)
glBindBuffer(GL_ARRAY_BUFFER, 0)

#unbind VAO & EBO & VBO
glBindVertexArray(0)
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);



def set_uniform_shader_variable(name, value):
    global program
    location = glGetUniformLocation(program, name)
    if type(value) == glm.vec3:
        glUniform3fv(location, 1, glm.value_ptr(value))
    elif type(value) == glm.mat4:
        glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(value))
    else:
        print("Unsupported type")

# render function
rotation = 0.0


model_1 = 0.0
model_2 = 1.0
model_3 = 0.0

def render():


    model = glm.mat4(1.0);
    view = glm.mat4(1.0);
    proj = glm.mat4(1.0);

    global rotation
    rotation += 0.2

    model = glm.rotate(model, glm.radians(rotation), glm.vec3(model_1, model_2, model_3))
    view = glm.translate(view, glm.vec3(0.0, -0.5, -3.0))
    proj = glm.perspective(glm.radians(45.0), width / height, 0.1, 100.0)

    set_uniform_shader_variable("model", model)
    set_uniform_shader_variable("view", view)
    set_uniform_shader_variable("proj", proj)

    # bind vao
    glBindVertexArray(vao)

    # start drawing
    # glClearColor(0.5, 0.5, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glDrawArrays(GL_TRIANGLES, 0, len(vertices))
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, c_void_p(0))
    glutSwapBuffers()

    # poll events
    glutPostRedisplay()


def key_pressed(*args):
    global model_1
    global model_2
    global model_3
    global rotation

    amount = 0.01

    if args[0] == b'q':
        model_1 += amount
    elif args[0] == b'a':
        model_1 -= amount
    elif args[0] == b'w':
        model_2 += amount
    elif args[0] == b's':
        model_2 -= amount
    elif args[0] == b'e':
        model_3 += amount
    elif args[0] == b'd':
        model_3 -= amount
    elif args[0] == b'r':
        rotation += 4.0
    elif args[0] == b'f':
        rotation -= 4.0
   
    print(args[0])
        


    
# render every millisecond
glutDisplayFunc(render)
# register callback functions
glutKeyboardFunc(key_pressed)
glutMainLoop()

# cleanup
glDisableVertexAttribArray(0)
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)
glUseProgram(0)
glDeleteProgram(program)
glDeleteBuffers(1, vbo)
glDeleteVertexArrays(1, vao)
