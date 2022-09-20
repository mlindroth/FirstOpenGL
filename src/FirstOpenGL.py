import os
import struct

from colorsys import hls_to_rgb as hls
from random import uniform

import moderngl as mgl
import moderngl_window as mglw

from Camera import Camera


def random_color():
    return hls(uniform(0.0, 1.0), 0.5, 0.5)


cars = []
cars += [{'color': random_color(),
          'pos': (i * 2.0 - 9.0, 0.0, 1.5),
          'angle': uniform(-0.5, 0.5)} for i in range(10)]

cars += [{'color': random_color(),
          'pos': (i * 2.0 - 9.0, 0.0, -1.5),
          'angle': uniform(-0.5, 0.5)} for i in range(10)]


class PerspectiveProjection(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "FirstOpenGL Project"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True

    resource_dir = os.path.normpath(os.path.join(__file__, '../../data'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader='''
                            #version 330

                            uniform mat4 Mvp;

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
                                gl_Position = Mvp * vec4(v_vert, 1.0);
                            }
                        ''',
            fragment_shader='''
                            #version 330

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
                        ''',
        )

        self.camera = Camera(self.aspect_ratio)
        self.mvp = self.prog['Mvp']
        self.light = self.prog['Light']

        obj = self.load_scene('lowpoly_toy_car.obj')

        self.vbo = self.ctx.buffer(struct.pack(
            '15f',
            1.0, 1.0, 1.0,
            0.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
        ) * len(cars))
        vao_wrapper = obj.root_nodes[0].mesh.vao
        vao_wrapper.buffer(self.vbo, '3f 3f 9f/i', ['in_color', 'in_origin', 'in_basis'])
        self.vao = vao_wrapper.instance(self.prog)

        self.states = {
            self.wnd.keys.W: False,     # forward
            self.wnd.keys.S: False,     # backwards
            self.wnd.keys.UP: False,    # strafe Up
            self.wnd.keys.DOWN: False,  # strafe Down
            self.wnd.keys.A: False,     # strafe left
            self.wnd.keys.D: False,     # strafe right
            self.wnd.keys.Q: False,     # rotate left
            self.wnd.keys.E: False,     # rotare right
            self.wnd.keys.Z: False,     # zoom in
            self.wnd.keys.X: False,     # zoom out
        }

    def move_camera(self):
        if self.states.get(self.wnd.keys.W):
            self.camera.move_forward()

        if self.states.get(self.wnd.keys.S):
            self.camera.move_backwards()

        if self.states.get(self.wnd.keys.UP):
            self.camera.strafe_up()

        if self.states.get(self.wnd.keys.DOWN):
            self.camera.strafe_down()

        if self.states.get(self.wnd.keys.A):
            self.camera.strafe_left()

        if self.states.get(self.wnd.keys.D):
            self.camera.strafe_right()

        if self.states.get(self.wnd.keys.Q):
            self.camera.rotate_left()

        if self.states.get(self.wnd.keys.E):
            self.camera.rotate_right()

        if self.states.get(self.wnd.keys.Z):
            self.camera.zoom_in()

        if self.states.get(self.wnd.keys.X):
            self.camera.zoom_out()

    def key_event(self, key, action, modifiers):
        if key not in self.states:
            print(key, action)
            return

        if action == self.wnd.keys.ACTION_PRESS:
            self.states[key] = True
        else:
            self.states[key] = False

    def render(self, time, frame_time):
        self.move_camera()

        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(mgl.DEPTH_TEST)

        self.mvp.write((self.camera.mat_projection * self.camera.mat_lookat).astype('f4'))

        self.vbo.write(b''.join(struct.pack(
            '15f',
            *car['color'],
            *car['pos'],
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
        ) for car in cars))
        self.vao.render(instances=len(cars))

        self.vao.render(instances=len(cars))


if __name__ == '__main__':
    PerspectiveProjection.run()
