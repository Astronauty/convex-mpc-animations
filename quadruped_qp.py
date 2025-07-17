from manim import *
import numpy as np

class QuadrupedCostFunction(Scene):
    def construct(self):
        world_frame = Axes(
            x_range=[0, 1],
            y_range=[-0, 1],
            x_length=1,
            y_length=1,
            axis_config={
                "tip_width": 0.25,
                "tip_height": 0.25
            }
        )       
        # self.add(world_frame)
        world_frame.to_corner(DOWN + LEFT)
        world_frame.shift(0.5*UP)
        world_frame.set_color(GRAY)
        
        world_frame_label = Text("W", font_size=24)
        world_frame_label.next_to(world_frame, 1E-5*(DOWN+LEFT))

        quadruped_body = Rectangle(
            width=2.5,
            height=1.0,
            fill_color=BLUE,
            fill_opacity=0.7,
            # stroke_color=WHITE,
            stroke_width=2
        )
        
        local_frame = Axes(
            x_range=[0, 1],
            y_range=[-0, 1],
            x_length=0.25,
            y_length=0.25,
            axis_config={
                "tip_width": 0.1,
                "tip_height": 0.1
            }
        )       
        
        
        
        local_frame_label = Text("B", font_size=24)
        
        self.align_local_to_world(local_frame, world_frame, world_coords=(2,1))
        quadruped_body.move_to(world_frame.c2p(2, 1))
        local_frame_label.next_to(local_frame, 1E-5*(DOWN+LEFT))
        self.add(quadruped_body, local_frame_label)
        
        
        
        # local_frame.move_to(quadruped_body.get_center())
        quadruped = VGroup(quadruped_body, local_frame, local_frame_label)
        # local_frame.move_to(world_frame.c2p(0, 0))
        self.add(world_frame, world_frame_label, local_frame)


        # Create a line connecting the origins of the world and local frames
        world_origin = world_frame.c2p(0, 0)
        local_origin = local_frame.c2p(0, 0)
        connecting_line = Line(
            world_origin, 
            local_origin,
            color=YELLOW,
            stroke_width=2,
            stroke_opacity=0.8
        )

        # Add an arrow to better visualize the connection
        position_vector = Arrow(
            world_origin,
            local_origin,
            buff=0,
            color=YELLOW,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.1
        )

        # Position label
        position_label = MathTex(r"p_{WB}", font_size=24).next_to(position_vector, UP, buff=0.1)

        # Add elements to scene
        self.add(connecting_line, position_vector, position_label)

        # Update the line when the quadruped moves
        # self.add_updater_to_line(position_vector, world_frame, local_frame)
        # self.add_updater_to_line(connecting_line, world_frame, local_frame)
        # self.add_updater_to_label(position_label, position_vector)
        self.wait(2)


        qp = MathTex(r"\underset{u_1 ... u_{N-1}}{min}", r" \quad &J = \sum_{k=1}^N \; x^TQx + u^T R u \\ s.t. \quad &x_{k+1} = Ax_k + Bu_k, \quad \forall k \\ &x_0 = x_{init}", font_size=40)


        qp.to_edge(UP)
        
        self.add(qp)
        self.wait(2)
        self.play(quadruped.animate.shift(RIGHT*2))
        
        

        

    def align_local_to_world(self, local_frame: Mobject, world_frame: Mobject, 
                            local_coords: tuple = (0, 0), world_coords: tuple = (0, 0)):
        """
        Shift `local_frame` so that the point at `local_coords` in local_frame's coordinate
        system aligns exactly with the point at `world_coords` in world_frame's coordinate system.

        Parameters:
        - local_frame: the Mobject (e.g., Axes) to move
        - world_frame: the Mobject (e.g., Axes) defining the target coordinate system
        - local_coords: (x, y) in the local frame's data coordinates to align
        - world_coords: (X, Y) in the world frame's data coordinates to align to
        """
        target_point = world_frame.c2p(*world_coords)
        local_point = local_frame.c2p(*local_coords)
        shift_vector = target_point - local_point
        local_frame.shift(shift_vector)
        
        


        
