from manim import *
from manim.utils.space_ops import rotation_matrix


class LinearTransformation3DScene(ThreeDScene):
    """A ThreeDScene demonstrating scaling, rotation, and shearing transformations
    on a 3D grid and the standard basis vectors (i, j, k)."""

    def construct(self):
        # Set up axes and a 2D grid (NumberPlane) lying on the XY-plane (z = 0)
        axes = ThreeDAxes()
        grid = NumberPlane(x_range=(-4, 4, 1), y_range=(-4, 4, 1), faded_lines_ratio=2)
        grid.set_opacity(0.5)

        # Standard basis vectors
        i_vec = Arrow3D(start=ORIGIN, end=RIGHT, color=RED)
        j_vec = Arrow3D(start=ORIGIN, end=UP, color=GREEN)
        k_vec = Arrow3D(start=ORIGIN, end=OUT, color=BLUE)

        # Labels for basis vectors
        i_label = MathTex("\\hat{i}", color=RED).next_to(i_vec.get_end(), RIGHT)
        j_label = MathTex("\\hat{j}", color=GREEN).next_to(j_vec.get_end(), UP)
        k_label = MathTex("\\hat{k}", color=BLUE).next_to(k_vec.get_end(), OUT)

        # Initial camera orientation
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        # Create initial scene
        self.play(Create(axes), Create(grid))
        self.play(GrowArrow(i_vec), FadeIn(i_label),
                  GrowArrow(j_vec), FadeIn(j_label),
                  GrowArrow(k_vec), FadeIn(k_label))
        self.wait(1)

        # -------------------- Scaling --------------------
        scaling_matrix = [[2, 0, 0],
                          [0, 1, 0],
                          [0, 0, 1]]
        scaling_text = Text("Scaling by 2 along x-axis").to_edge(UP)

        self.play(Write(scaling_text))
        self.wait(0.5)
        self.play(
            grid.animate.apply_matrix(scaling_matrix),
            i_vec.animate.apply_matrix(scaling_matrix), i_label.animate.apply_matrix(scaling_matrix),
            j_vec.animate.apply_matrix(scaling_matrix), j_label.animate.apply_matrix(scaling_matrix),
            k_vec.animate.apply_matrix(scaling_matrix), k_label.animate.apply_matrix(scaling_matrix),
            run_time=3
        )
        self.wait(1)
        self.play(FadeOut(scaling_text))

        # -------------------- Rotation --------------------
        angle_z = 45 * DEGREES
        rotation_mat = rotation_matrix(angle_z, OUT)  # Rotate about Z-axis
        rotation_text = Text("Rotation about Z-axis by 45°").to_edge(UP)

        self.play(Write(rotation_text))
        self.wait(0.5)
        self.play(
            grid.animate.apply_matrix(rotation_mat),
            i_vec.animate.apply_matrix(rotation_mat), i_label.animate.apply_matrix(rotation_mat),
            j_vec.animate.apply_matrix(rotation_mat), j_label.animate.apply_matrix(rotation_mat),
            k_vec.animate.apply_matrix(rotation_mat), k_label.animate.apply_matrix(rotation_mat),
            run_time=3
        )
        self.wait(1)
        self.play(FadeOut(rotation_text))

        # -------------------- Shearing --------------------
        shear_matrix = [[1, 1, 0],  # shear x by y
                        [0, 1, 0],
                        [0, 0, 1]]
        shear_text = Text("Shearing: x → x + y").to_edge(UP)

        self.play(Write(shear_text))
        self.wait(0.5)
        self.play(
            grid.animate.apply_matrix(shear_matrix),
            i_vec.animate.apply_matrix(shear_matrix), i_label.animate.apply_matrix(shear_matrix),
            j_vec.animate.apply_matrix(shear_matrix), j_label.animate.apply_matrix(shear_matrix),
            k_vec.animate.apply_matrix(shear_matrix), k_label.animate.apply_matrix(shear_matrix),
            run_time=3
        )
        self.wait(2)
        self.play(FadeOut(shear_text))

        # End scene with a slow camera rotation for aesthetics
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, run_time=4)
        self.wait(2)