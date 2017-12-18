#version 330

out vec4 fragment;

in vec2 texcoord;
uniform sampler2D tex;

void main()
{
	fragment = texture(tex, texcoord);
}
