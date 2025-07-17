from manim import *
import numpy as np

class RigidBodyPrismAnimation(ThreeDScene):
    def construct(self):
        # Set up the 3D camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Create a coordinate system
        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            z_length=6,
        ).set_color(GRAY)
        
        # Add axis labels
        x_label = Text("X", font_size=24).next_to(axes.x_axis, RIGHT)
        y_label = Text("Y", font_size=24).next_to(axes.y_axis, UP)
        z_label = Text("Z", font_size=24).next_to(axes.z_axis, OUT)
        
        # Create a rectangular prism using a scaled cube
        prism = Cube(
            side_length=1,
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=2
        )
        # Scale to make it rectangular
        prism.scale([2, 1.5, 1])
        
        # Set initial position
        prism.move_to([-4, -3, 0])
        
        # Add title
        title = Text("3D Rigid Body Motion", font_size=36, color=YELLOW)
        title.to_edge(UP)
        
        # Show initial setup
        self.add(axes, x_label, y_label, z_label, title)
        self.play(Create(prism), run_time=2)
        self.wait(1)
        
        # Animation 1: Linear translation along X-axis
        self.play(
            prism.animate.shift(RIGHT * 8),
            run_time=3,
            rate_func=smooth
        )
        self.wait(0.5)
        
        # Animation 2: Translation along Y-axis with rotation
        self.play(
            prism.animate.shift(UP * 6).rotate(PI/2, axis=Z_AXIS),
            run_time=3,
            rate_func=smooth
        )
        self.wait(0.5)
        
        # Animation 3: Complex 3D movement with rotation about multiple axes
        self.play(
            prism.animate.shift(LEFT * 4 + DOWN * 3 + OUT * 2)
                    .rotate(PI/3, axis=X_AXIS)
                    .rotate(PI/4, axis=Y_AXIS),
            run_time=4,
            rate_func=smooth
        )
        self.wait(0.5)
        
        # Animation 4: Circular motion in XY plane
        # First move to starting position for circular motion
        self.play(
            prism.animate.move_to([0, 0, 2]),
            run_time=2
        )
        
        # Create circular path
        def circular_motion(t):
            radius = 3
            angle = 2 * PI * t
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            z = 2  # Keep constant Z
            return np.array([x, y, z])
        
        # Animate circular motion with rotation
        self.play(
            UpdateFromAlphaFunc(
                prism,
                lambda mob, alpha: mob.move_to(circular_motion(alpha))
                                    .rotate(PI/10, axis=Z_AXIS)
            ),
            run_time=6,
            rate_func=linear
        )
        self.wait(0.5)
        
        # Animation 5: Helical motion (spiral)
        def helical_motion(t):
            radius = 2
            height_rate = 4
            angle = 4 * PI * t
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            z = height_rate * t - 2  # Move from z=-2 to z=2
            return np.array([x, y, z])
        
        # Reset position for helical motion
        prism.move_to([2, 0, -2])
        
        self.play(
            UpdateFromAlphaFunc(
                prism,
                lambda mob, alpha: mob.move_to(helical_motion(alpha))
                                    .rotate(PI/8, axis=Y_AXIS)
                                    .rotate(PI/12, axis=X_AXIS)
            ),
            run_time=8,
            rate_func=smooth
        )
        self.wait(1)
        
        # Animation 6: Figure-8 motion in 3D
        def figure_eight_3d(t):
            scale = 2
            x = scale * np.cos(2 * PI * t)
            y = scale * np.sin(4 * PI * t) / 2
            z = scale * np.sin(2 * PI * t) * np.cos(2 * PI * t)
            return np.array([x, y, z])
        
        # Reset for figure-8
        prism.move_to([0, 0, 0])
        
        self.play(
            UpdateFromAlphaFunc(
                prism,
                lambda mob, alpha: mob.move_to(figure_eight_3d(alpha))
                                    .rotate(PI/6, axis=[1, 1, 1])
            ),
            run_time=6,
            rate_func=smooth
        )
        self.wait(1)
        
        # Final animation: Return to center with tumbling motion
        self.play(
            prism.animate.move_to(ORIGIN)
                    .rotate(2*PI, axis=X_AXIS)
                    .rotate(2*PI, axis=Y_AXIS)
                    .rotate(2*PI, axis=Z_AXIS),
            run_time=4,
            rate_func=smooth
        )
        
        # Change camera angle for final view
        self.move_camera(
            phi=60 * DEGREES,
            theta=45 * DEGREES,
            gamma=0 * DEGREES,
            run_time=3
        )
        
        # Final pause
        self.wait(2)


class RigidBodyPhysicsSimulation(ThreeDScene):
    """
    A more advanced animation showing physics-based motion with trajectory tracking
    """
    def construct(self):
        # Set up the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Create coordinate system
        axes = ThreeDAxes(
            x_range=[-8, 8, 2],
            y_range=[-6, 6, 2],
            z_range=[-4, 8, 2],
            x_length=10,
            y_length=8,
            z_length=8,
        ).set_color(GRAY_B)
        
        # Create the rigid body (prism)
        body = Cube(
            side_length=1,
            fill_color=RED,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=1.5
        )
        # Scale to make it rectangular
        body.scale([1.5, 1, 0.8])
        
        # Initial conditions
        initial_pos = np.array([-6, 4, 6])
        body.move_to(initial_pos)
        
        # Title
        title = Text("Physics-Based Rigid Body Motion", font_size=32, color=YELLOW)
        title.to_edge(UP)
        
        # Create trajectory tracker
        trajectory = VMobject()
        trajectory.set_points_as_corners([initial_pos])
        trajectory.set_color(GREEN)
        trajectory.set_stroke(width=3)
        
        # Show setup
        self.add(axes, title)
        self.play(Create(body), run_time=1.5)
        self.wait(0.5)
        
        # Simulate projectile motion with rotation
        def projectile_motion(t):
            # Physics parameters
            g = 9.8  # gravity
            v0 = np.array([4, -1, -3])  # initial velocity
            
            # Position calculation
            pos = initial_pos + v0 * t - 0.5 * g * UP * t**2
            
            # Bounce off ground (z = -3)
            if pos[2] < -3:
                pos[2] = -3 + abs(pos[2] + 3) * 0.7  # damped bounce
            
            return pos
        
        # Animate the motion
        dt = 0.1
        total_time = 6
        steps = int(total_time / dt)
        
        for i in range(steps):
            t = i * dt
            new_pos = projectile_motion(t)
            
            # Update trajectory
            if i > 0:
                trajectory.add_points_as_corners([new_pos])
            
            # Update body position and rotation
            self.play(
                body.animate.move_to(new_pos)
                      .rotate(PI/10, axis=[1, 0.5, 0.3]),
                run_time=dt,
                rate_func=linear
            )
            
            # Add trajectory
            if i % 5 == 0:  # Update trajectory every 5 steps
                self.add(trajectory.copy())
        
        self.wait(2)


# Additional scene for simple demonstration
class SimplePrismMotion(ThreeDScene):
    """
    A simpler version for quick demonstration
    """
    def construct(self):
        # Set camera
        self.set_camera_orientation(phi=70 * DEGREES, theta=35 * DEGREES)
        
        # Create a simple prism
        prism = Cube(side_length=1.5, fill_color=PURPLE, fill_opacity=0.7)
        
        # Title
        title = Text("Simple 3D Prism Motion", font_size=36)
        title.to_edge(UP)
        
        self.add(title)
        self.play(Create(prism))
        
        # Simple motions
        self.play(prism.animate.shift(RIGHT * 3), run_time=2)
        self.play(prism.animate.rotate(PI/2, axis=UP), run_time=2)
        self.play(prism.animate.shift(UP * 2), run_time=2)
        self.play(prism.animate.rotate(PI, axis=RIGHT), run_time=2)
        self.play(prism.animate.shift(OUT * 2), run_time=2)
        
        # Rotate camera view
        self.move_camera(
            phi=45 * DEGREES,
            theta=60 * DEGREES,
            run_time=3
        )
        
        self.wait(2)
