#version 330

#if defined VERTEX_SHADER

uniform mat4 m_proj;
uniform mat4 m_model;
uniform mat4 m_cam;

in vec3 in_position;
in vec3 in_normal;

in vec3 in_color;
in vec3 in_origin;
in mat3 in_basis;

out vec3 v_vert;
out vec3 v_norm;
out vec3 v_color;

void main() {
    v_vert = in_origin + in_basis * in_position;
    v_norm = in_basis * in_normal;
    v_color = in_color;
	gl_Position = m_proj * m_cam * m_model * vec4(v_vert, 1.0);
}

#elif defined FRAGMENT_SHADER

uniform vec3 Light;
uniform sampler2D Texture;

in vec3 v_vert;
in vec3 v_norm;
in vec3 v_color;

out vec4 f_color;

void main() {
    float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
    f_color = vec4(v_color * lum, 1.0);
}

#endif
