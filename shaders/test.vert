#version 330

in vec3 pos;
in vec2 uv;

uniform mat4 model;
uniform mat4 proj;

out vec2 texcoord;

void main()
{
    texcoord = uv;
    gl_Position = proj * model * vec4(pos, 1);
}
