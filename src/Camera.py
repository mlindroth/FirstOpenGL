from pyrr import Matrix44, Quaternion, Vector3, vector
import numpy as np

class Camera:
    """
        Controls:
            Move:
                Forward - W
                Backwards - S

            Strafe:
                Up - up arrow
                Down - down arrow
                Left - A
                Right - D

            Rotate:
                Left - Q
                Right - E

            Zoom:
                In - X
                Out - Z
    """

    def __init__(self, ratio):
        self.mat_projection = None
        self.mat_lookat = None

        self._zoom_step = 1.0
        self._move_vertically = 1.0
        self._move_horizontally = 1.0
        self._rotate_horizontally = 1.0
        self._rotate_vertically = 1.0

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

    def move_forward(self):
        self._camera_position = self._camera_position + self._camera_direction * self._move_horizontally
        self.build_look_at()

    def move_backwards(self):
        self._camera_position = self._camera_position - self._camera_direction * self._move_horizontally
        self.build_look_at()

    def strafe_left(self):
        self._camera_position = self._camera_position - vector.normalize(self._camera_direction ^ self._camera_up) * self._move_horizontally
        self.build_look_at()

    def strafe_right(self):
        self._camera_position = self._camera_position + vector.normalize(self._camera_direction ^ self._camera_up) * self._move_horizontally
        self.build_look_at()

    def strafe_up(self):
        self._camera_position = self._camera_position + self._camera_up * self._move_vertically
        self.build_look_at()

    def strafe_down(self):
        self._camera_position = self._camera_position - self._camera_up * self._move_vertically
        self.build_look_at()

    def rotate_left(self):
        rotation = Quaternion.from_y_rotation(2 * float(self._rotate_horizontally) * np.pi / 180)
        self._camera_direction = rotation * self._camera_direction
        self.build_look_at()

    def rotate_right(self):
        rotation = Quaternion.from_y_rotation(-2 * float(self._rotate_horizontally) * np.pi / 180)
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
