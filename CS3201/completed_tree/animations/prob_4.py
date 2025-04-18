from manim import *

class TreeNode(VGroup):
    def __init__(self, label):
        super().__init__()
        self.circle = Circle(radius=0.4, color=WHITE).set_fill(BLUE, opacity=0.5)
        self.text = Text(str(label), font_size=24).move_to(self.circle.get_center())
        self.add(self.circle, self.text)
        self.label = label
        self.height_text = None

class CheckBalanceWithStack(Scene):
    def construct(self):
        # --- Build Tree ---
        nodes = {i: TreeNode(i) for i in range(1, 6)}
        nodes[1].move_to(UP * 2)
        nodes[2].move_to(nodes[1].get_center() + DOWN * 1.5 + LEFT * 2)
        nodes[3].move_to(nodes[1].get_center() + DOWN * 1.5 + RIGHT * 2)
        nodes[4].move_to(nodes[2].get_center() + DOWN * 1.5 + LEFT * 1)
        nodes[5].move_to(nodes[4].get_center() + DOWN * 1.5 + LEFT * 1)

        edges = VGroup(
            Line(nodes[1].get_bottom(), nodes[2].get_top()),
            Line(nodes[1].get_bottom(), nodes[3].get_top()),
            Line(nodes[2].get_bottom(), nodes[4].get_top()),
            Line(nodes[4].get_bottom(), nodes[5].get_top())
        )

        self.play(FadeIn(*nodes.values()), Create(edges))

        # --- Add C Code Block ---
        code_lines = [
            "01: if (root == NULL) return -1;",
            "02: if (!(*isBalanced)) return -1;",
            "03: int leftHeight = checkBalanceAndHeight(...);",
            "04: if (!(*isBalanced)) return -1;",
            "05: int rightHeight = checkBalanceAndHeight(...);",
            "06: if (!(*isBalanced)) return -1;",
            "07: if (abs(left - right) > 1) {",
            "08:     *isBalanced = false;",
            "09:     return -1;",
            "10: }",
            "11: return max(left, right) + 1;"
        ]
        code = CodeLine(code_lines, font_size=24, line_spacing=0.4)
        code.set_color_by_gradient(BLUE, GREEN)
        code.move_to(LEFT * 3 + UP * 2)
        code_box = SurroundingRectangle(code, color=WHITE)
        self.play(Create(code_box))

        self.play(FadeIn(code))

        # --- Call Stack Box ---
        stack_box = Rectangle(width=4, height=5).to_corner(DR)
        stack_title = Text("Call Stack", font_size=24).next_to(stack_box, UP)
        self.play(Create(stack_box), Write(stack_title))
        stack_items = []

        # --- Simulate the call stack and traversal (manually for now) ---
        self.simulate_call(nodes[5], code, stack_box, stack_items, 5)
        self.simulate_call(nodes[4], code, stack_box, stack_items, 4)
        self.simulate_call(nodes[2], code, stack_box, stack_items, 2)
        self.simulate_call(nodes[3], code, stack_box, stack_items, 3)
        self.simulate_call(nodes[1], code, stack_box, stack_items, 1)

        self.wait(3)

    def simulate_call(self, node, code, stack_box, stack_items, label):
        # Simulate function call
        call_label = Text(f"checkBalance({label})", font_size=20).move_to(stack_box.get_top() + DOWN * (0.6 * (len(stack_items) + 1)))
        stack_items.append(call_label)
        self.play(FadeIn(call_label))

        # Highlight line 01
        self.highlight_line(code, 0, f"Node {label} not NULL")
        self.highlight_line(code, 1, "isBalanced still True")

        # If it's a leaf
        if label in [5]:
            self.highlight_line(code, 11, f"Return height 0 for node {label}")
            h_text = Text("h=0", font_size=20, color=YELLOW).next_to(node, DOWN)
            self.play(Write(h_text))
            node.height_text = h_text

        self.play(FadeOut(stack_items.pop()))

    def highlight_line(self, code_obj, line_idx, explanation=""):
        line_rect = SurroundingRectangle(code_obj.code[line_idx], color=YELLOW)
        expl = Text(explanation, font_size=24).next_to(code_obj, DOWN)
        self.play(Create(line_rect), Write(expl))
        self.wait(0.8)
        self.play(FadeOut(line_rect), FadeOut(expl))
