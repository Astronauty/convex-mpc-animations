from manim import *
import numpy as np

class SimpleCoordinateFrame(Scene):
    def construct(self):
        # Create a simple 2D coordinate system with white axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=4,
            axis_config={"color": WHITE},
            tips=False,
        )
        
        # axes.shift(LEFT*3)
        axes.to_edge(LEFT)
        # Add axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("f(x)")
        
        # Show the axes
        self.add(axes, x_label, y_label)
        
        def nonlinear_func(x):
            return x**4 + x**3 - 2*x**2 + 0.5*x + 0.5

        graph = axes.plot(nonlinear_func, color=BLUE, x_range=[-3, 3])
        
        # Mathematical program expression
        
        
        
        cost_func_eq = MathTex("\min_{x} f(x)")
        # self.add(cost_func_eq)
        cost_func_eq.to_corner(UP + RIGHT)
        cost_func_eq.shift(LEFT)
        
        self.play(Create(graph))
        self.wait(1)
        self.play(Write(cost_func_eq))
        
        self.wait(1)
    
        
        
        
        self.wait(2)



    
    