import OpenGL
from ctypes import *
import glm
import random
import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

import random
from helpers import *
from PIL import Image

width = 800
height = 600

factor = 0.55

texcoord_0 = [1,0]
texcoord_1 = [0,0]
texcoord_2 = [0,0]
texcoord_3 = [0,0]
texcoord_4 = [0.5,2]

vertices = [
   # COORDINATES  /COLORS        / TexCoord
    0.5, 0.0, 0.5, 0.0, 1.0, 0.0, texcoord_0[0], texcoord_0[1], # Vertex 0 Top Right Green
    0.5, 0.0, -0.5, 0.0, 0.0, 1.0, texcoord_1[0], texcoord_1[1], # Vertex 1 Bottom Right Blue
    -0.5, 0.0, -0.5, 0.0, 1.0, 0.0, texcoord_2[0], texcoord_2[1], # Vertex 2 Bottom Left Green
    -0.5, 0.0, 0.5, 1.0, 1.0, 0.0, texcoord_3[0], texcoord_3[1], # Vertex 3 Top Left Yellow
    0.0, 1.5, 0.0, 1.0, 0.0, 0.0, texcoord_4[0], texcoord_4[1], # Vertex 4 Pyramid Top Red
] 

attributes_in_vertex = 8
total_vertices = int(len(vertices) / attributes_in_vertex)

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
out vec4 position;
flat out int instanceID;

// Controls the scale of the vertices
uniform float scale;

// Inputs the matrices needed for 3D viewing with perspective
uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;




float cube_root(float x)
{
    return pow(x, 1.0 / 3.0);
}

float dec(float x)
{
    return x - floor(x);
}


float strip_dec(float x)
{
    return int(x) % 1;
}

void main()
{
    // line the shapes next to each other on the x-axis based on gl_InstanceID
    // move the location of the pyramid based on the gl_InstanceID
    
    float distance = 4.0;
    float cube_radius = ceil(cube_root(2500));
    float squared = pow(cube_radius, 2);
   
    // left-right horizontal
    // floor(((77 % 16) / 16) * 5)
    float move_z = floor(((gl_InstanceID % int(squared)) / squared) * cube_radius) * distance;

    // 
    // height 
    //
    //    64 / 16 = 4th level
    //
    float move_y = floor(gl_InstanceID / squared) * distance;

    // towards me
    float move_x = floor(gl_InstanceID % int(cube_radius)) * distance;

    
    
    
    gl_Position = proj * view * vec4(aPos.x + move_x, aPos.y + move_y, aPos.z + move_z, 1.0);
    position = proj * view * vec4(aPos.x + move_x, aPos.y + move_y, aPos.z + move_z, 1.0);
	// Assigns the colors from the Vertex Data to "color"
	color = aColor;
	// Assigns the texture coordinates from the Vertex Data to "texCoord"
	texCoord = aTex;
    instanceID = gl_InstanceID;
}
"""

fragment_shader = """
#version 330 core

// Outputs colors in RGBA
out vec4 FragColor;

// Inputs the color from the Vertex Shader
in vec3 color;
in vec4 position;
// Inputs the texture coordinates from the Vertex Shader
in vec2 texCoord;

flat in int instanceID;

// Inputs the texture sampler
uniform float count;
uniform sampler2D imageTextureFoxNews;
uniform sampler2D imageTextureCnn;
uniform sampler2D imageTextureMsnbc;
uniform sampler2D imageTextureAbc;




void main()
{

    vec4 texture_colors;
    
    if(instanceID % 4 == 0)
    {
	    texture_colors = texture2D(imageTextureFoxNews, texCoord);
    }
    else if (instanceID % 4 == 1)
    {
        texture_colors = texture2D(imageTextureCnn, texCoord);
    }
    else if (instanceID % 4 == 2)
    {
        texture_colors = texture2D(imageTextureMsnbc, texCoord);
    }
    else if (instanceID % 4 == 3)
    {
        texture_colors = texture2D(imageTextureAbc, texCoord);
    }

   
    

    //shine light from position that was passed in
    vec3 diffuse_color = vec3(1.0, 1.0, 1.0);
    vec3 specular_color = vec3(1.0, 1.0, 1.0);
    vec3 ambient_color = vec3(1.0, 1.0, 1.0);
    float shininess = .60;
    float light_intensity = 0.05;
    float ambient_intensity = 0.0;
    float diffuse_intensity = 2.0;
    float specular_intensity = 10.0;
    
    vec3 normal = normalize(position.xyz);
    
    float locations[2] = {200.0,2.0};
    float location = 0.0;


    vec3 view_position, light_position, view_direction, light_direction, reflect_direction;
    float diffuse_factor, specular_factor;
    vec4 diffuse_color_final, specular_color_final;
    int j = 0;

    
    //to iterate through the location array
    for(j = 0; j < 3; j++)
    {
        location = locations[j];
        light_position = vec3(-5.0, location, 0.0);
        view_position = vec3(location, location, 300.0);
        light_direction = normalize(light_position - position.xyz);
        view_direction = normalize(view_position - position.xyz);
        diffuse_factor = max(dot(light_direction, normal), 0.0);
        reflect_direction = reflect(light_direction, normal);
        diffuse_color_final += vec4(diffuse_color * diffuse_factor, 1.0) * light_intensity;
        specular_factor = pow(max(dot(view_direction, reflect_direction), 0.0), shininess);
        specular_color_final += vec4(specular_color * light_intensity * specular_intensity * specular_factor, 256.0);
    }
    

    
    vec4 ambient_color_final = vec4(ambient_color * light_intensity * ambient_intensity, 1.0);
    vec4 final_color = diffuse_color_final + specular_color_final + ambient_color_final;

    // get x & y from the texture
    float texCoordX = texCoord.x;
    float texCoordY = texCoord.y;
    // get resolution variables from the texture
    float resolutionX = texture_colors.x;
    float resolutionY = texture_colors.y;
    

    FragColor = final_color * texture_colors;

}
"""

def bind_vao_to_vbo(vbo, location_in_shader, elements_in_attribute, element_type, values_as_is_bool, stride, offset):
    #
    # location in shader - a number that represents the attribute that's listed ON the top of shader
    # elements in attribute - how many elements are in the attribute
    # element type - the type of each element
    # values as-is bool - are the values as-is?
    # stride - stride is the size of a single vertex!! So if you have 3 for position, 3 for color, and 2 for texture, the stride is 8
    # offset - offset is the distance away from the zero element in the vertex/vertice array
    #
    # binds the vao to the vbo
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    # defines the attribute in the shader
    glVertexAttribPointer(location_in_shader, elements_in_attribute, element_type, values_as_is_bool, stride, offset)
    # enables the attribute in the shader
    glEnableVertexAttribArray(location_in_shader)
    # unbinds the vao from the vbo
    glBindBuffer(GL_ARRAY_BUFFER, 0)

def set_uniform_shader_variable(name, value):
    global program
    location = glGetUniformLocation(program, name)
    if type(value) == glm.vec3:
        glUniform3fv(location, 1, glm.value_ptr(value))
    elif type(value) == glm.mat4:
        glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(value))
    elif type(value) == int:
        # typically used for scale & translation & textures
        glUniform1i(location, value)
    elif type(value) == float:
        glUniform1f(location, value)
    else:
        print("Unsupported type")

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

class Texture:

    def __init__(self, filepath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = Image.open(filepath)
        image_width, image_height = image.size
        image_bytes = image.tobytes('raw', 'RGBA', 0, -1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_bytes)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self, fragment_shader_location):
        glActiveTexture(GL_TEXTURE0 + fragment_shader_location)
        glBindTexture(GL_TEXTURE_2D,self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))


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

# create program & link shaders
program = glCreateProgram()
glAttachShader(program, vertex_shader)
glAttachShader(program, fragment_shader)
glLinkProgram(program)

# use program that consists of shaders
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




# copy index data to GPU (from the EBO)
glBufferData(
    GL_ELEMENT_ARRAY_BUFFER, # target
    len(indices) * sizeof(c_int), # size in bytes
    (c_int * len(indices))(*indices), # data to be sent to the buffer
    GL_STATIC_DRAW # usage 
)

# copy vertices data to the GPU (from the VBO)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(c_float), (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)

# define each attribute of each Vertex Array Object (VAO) & bind it to the Vertex Buffer Object (VBO)
# these three functions pertain to ONE vertex each, which has attributes like position, color, and texture
bind_vao_to_vbo(vbo, 0, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 8, c_void_p(0))
bind_vao_to_vbo(vbo, 1, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 8, c_void_p(3 * sizeof(c_float)))
bind_vao_to_vbo(vbo, 2, 2, GL_FLOAT, GL_FALSE, sizeof(c_float) * 8, c_void_p(6 * sizeof(c_float)))

#unbind VAO & EBO (the VBO is already unbound)
glBindVertexArray(0)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);








#
#
#   TEXTURES
#
#
fox_news_texture = Texture("fox_news_square_rbga.png")
cnn_texture = Texture("cnn_rbga.png")
msnbc_texture = Texture("msnbc_rbga.png")
abc_texture = Texture("abc_rbga.png")

# define variables for render function
rotation = 0.0
rotation_speed = 0.2
model_1 = 0.0
model_2 = 1.0
model_3 = 0.0
translate_1 = -10
translate_2 = -10
translate_3 = -20
proj_radians = 45.0
proj_1 = 0.1
proj_2 = 100.0
count = 0.0

# def debug():
#     model = glm.mat4(1.0);
#     view = glm.mat4(1.0);
#     proj = glm.mat4(1.0);
#     global rotation
#     rotation += 0.2
#     model = glm.rotate(model, glm.radians(rotation), glm.vec3(model_1, model_2, model_3))
#     view = glm.translate(view, glm.vec3(0.0, -0.5, -10.0))
#     proj = glm.perspective(glm.radians(45.0), width / height, 0.1, 100.0)
#     print("model: \n", model)
#     print("view: \n", view)
#     print("proj: \n", proj)

# debug()

def render():
    model = glm.mat4(1.0);
    view = glm.mat4(1.0);
    proj = glm.mat4(1.0);
    global rotation
    global rotation_speed
    global count
    rotation += rotation_speed
    model = glm.rotate(model, glm.radians(rotation), glm.vec3(model_1, model_2, model_3))
    view = glm.translate(view, glm.vec3(translate_1, translate_2, translate_3))
    proj = glm.perspective(glm.radians(proj_radians), width / height, proj_1, proj_2)
    set_uniform_shader_variable("model", model)
    set_uniform_shader_variable("view", view)
    set_uniform_shader_variable("proj", proj)
    set_uniform_shader_variable("imageTextureFoxNews",0)
    set_uniform_shader_variable("imageTextureCnn",1)
    set_uniform_shader_variable("imageTextureMsnbc",2)
    set_uniform_shader_variable("imageTextureAbc",3)
    set_uniform_shader_variable("count",count)
    count += .02

    # use texture
    fox_news_texture.use(0)
    cnn_texture.use(1)
    msnbc_texture.use(2)
    abc_texture.use(3)
    
    # bind vao
    glBindVertexArray(vao)
    # start drawing
    # glClearColor(0.5, 0.5, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glDrawArrays(GL_TRIANGLES, 0, len(vertices))
    # glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, c_void_p(0))
    glDrawElementsInstanced(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, c_void_p(0), 2500)
    glutSwapBuffers()
    # poll events
    glutPostRedisplay()


def key_pressed(*args):
    global model_1
    global model_2
    global model_3
    global rotation_speed
    global translate_1
    global translate_2
    global translate_3
    global proj_radians
    global proj_1
    global proj_2
    amount = 0.1
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
        rotation_speed += amount
    elif args[0] == b'f':
        rotation_speed -= amount
    elif args[0] == b't':
        translate_1 -= amount
    elif args[0] == b'g':
        translate_1 += amount
    elif args[0] == b'y':
        translate_2 -= amount
    elif args[0] == b'h':
        translate_2 += amount
    elif args[0] == b'u':
        translate_3 += amount
    elif args[0] == b'j':
        translate_3 -= amount
    elif args[0] == b'i':
        proj_radians += amount
    elif args[0] == b'k':
        proj_radians -= amount
    elif args[0] == b'o':
        proj_1 += amount
    elif args[0] == b'l':
        proj_1 -= amount
    elif args[0] == b'p':
        proj_2 += amount
    elif args[0] == b';':
        proj_2 -= amount


# define callbacks
glutDisplayFunc(render)
glutKeyboardFunc(key_pressed)
glutMainLoop()

# cleanup
glDisableVertexAttribArray(0)
fox_news_texture.cleanup()
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)
glUseProgram(0)
glDeleteProgram(program)
glDeleteBuffers(1, vbo)
glDeleteVertexArrays(1, vao)
