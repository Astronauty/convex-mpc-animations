from manim import *

class ShowQuadraticEquation(Scene):
    def construct(self):
        equation = MathTex(
            "\min_{x} \\frac{1}{2} x^T P x + q^T x"
        )
        # equation.scale(1.2)
        equation.to_edge(UP)

        self.play(Write(equation))
        self.wait(2)
