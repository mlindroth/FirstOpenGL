import os
import struct

from pyrr import Matrix44
from colorsys import hls_to_rgb as hls
from random import uniform

import moderngl as mgl
import moderngl_window as mglw

from windows import CameraWindow


def random_color():
    return hls(uniform(0.0, 1.0), 0.5, 0.5)


# creation of car meta-data
cars = []
rows = 100
width = 100
spacing = 2

for r in range(rows):
    cars += [{'color': random_color(),
              'pos': ((spacing*width)/2-(spacing*i), 0.0, (spacing*rows)/2-(spacing*r)),
              'angle': uniform(-0.5, 0.5)} for i in range(width)]


class GraphicsEngine(CameraWindow):
    gl_version = (3, 3)
    title = "FirstOpenGL Project"
    window_size = (1920, 1080)
    vsync = True
    fullscreen = False
    resizable = True

    resource_dir = os.path.normpath(os.path.join(__file__, '../../data'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True

        self.prog = self.load_program('shaders/default.glsl')
        self.m_proj = self.prog['m_proj']
        self.light = self.prog['Light']

        obj = self.load_scene('models/lowpoly_toy_car.obj')

        self.prog['m_model'].write(Matrix44.from_translation([0.0, 0.0, 0], dtype='f4'))

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

    def render(self, time, frame_time):
        self.light.value = tuple(self.camera.position)

        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(mgl.DEPTH_TEST)

        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_cam'].write(self.camera.matrix)

        self.vbo.write(b''.join(struct.pack(
            '15f',
            *car['color'],
            *car['pos'],
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
        ) for car in cars))
        self.vao.render(instances=len(cars))


if __name__ == '__main__':
    GraphicsEngine.run()
