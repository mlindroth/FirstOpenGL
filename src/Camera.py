from pyrr import Matrix44, Quaternion, Vector3, vector
import numpy as np


class Camera:
    """
        Controls:
            Translate:
                Forward - W
                Backwards - S
                Up - up arrow
                Down - down arrow
                Left - A
                Right - D

            Pitch/Yaw:
                Left - Q
                Right - E
                Up - R
                Down - F

            Zoom:
                In - X
                Out - Z
    """

    def __init__(self, ratio):
        self.mat_projection = None
        self.mat_lookat = None

        self._zoom_step = 1.0
        self._movement_speed = 0.5
        self._rotation_speed = 1.0

        self._field_of_view_degrees = 45.0
        self._z_near = 0.1
        self._z_far = 1000.0
        self._ratio = ratio
        self.build_projection()

        self._camera_position = Vector3([5.0, 5.0, 5.0])
        self._camera_direction = Vector3([-1.0, -1.0, -1.0])
        self._camera_up = Vector3([0.0, 1.0, 0.0])
        self._cameras_target = Vector3([0.0, 0.0, 0.0])
        self.build_look_at()

    def zoom_in(self):
        self._field_of_view_degrees = self._field_of_view_degrees - self._zoom_step
        self.build_projection()

    def zoom_out(self):
        self._field_of_view_degrees = self._field_of_view_degrees + self._zoom_step
        self.build_projection()

    def translate_forward(self):
        self._camera_position = self._camera_position + self._camera_direction * self._movement_speed
        self.build_look_at()

    def translate_backwards(self):
        self._camera_position = self._camera_position - self._camera_direction * self._movement_speed
        self.build_look_at()

    def translate_left(self):
        self._camera_position = self._camera_position - vector.normalize(self._camera_direction ^ self._camera_up) * self._movement_speed
        self.build_look_at()

    def translate_right(self):
        self._camera_position = self._camera_position + vector.normalize(self._camera_direction ^ self._camera_up) * self._movement_speed
        self.build_look_at()

    def translate_up(self):
        self._camera_position = self._camera_position + self._camera_up * self._movement_speed
        self.build_look_at()

    def translate_down(self):
        self._camera_position = self._camera_position - self._camera_up * self._movement_speed
        self.build_look_at()

    def yaw_left(self):
        rotation = Quaternion.from_y_rotation(2 * float(self._rotation_speed) * np.pi / 180)
        self._camera_direction = rotation * self._camera_direction
        self.build_look_at()

    def yaw_right(self):
        rotation = Quaternion.from_y_rotation(-2 * float(self._rotation_speed) * np.pi / 180)
        self._camera_direction = rotation * self._camera_direction
        self.build_look_at()

    def pitch_up(self):
        rotation = Quaternion.from_axis_rotation(np.cross(self._camera_up, self._camera_direction),
                                                 -2 * float(self._rotation_speed) * np.pi / 180)
        self._camera_direction = rotation * self._camera_direction
        self.build_look_at()

    def pitch_down(self):
        rotation = Quaternion.from_axis_rotation(np.cross(self._camera_up, self._camera_direction),
                                                 2 * float(self._rotation_speed) * np.pi / 180)
        self._camera_direction = rotation * self._camera_direction
        self.build_look_at()

    def build_look_at(self):
        self._cameras_target = (self._camera_position + self._camera_direction)
        self.mat_lookat = Matrix44.look_at(
            self._camera_position,
            self._cameras_target,
            self._camera_up)

    def build_projection(self):
        self.mat_projection = Matrix44.perspective_projection(
            self._field_of_view_degrees,
            self._ratio,
            self._z_near,
            self._z_far)
