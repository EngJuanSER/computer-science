"""This module contains the main Compiler for MacraScript.

It integrates the lexical, syntactic, and semantic analyzers and provides a
graphical user interface using Tkinter to write code and visualize the
generated macrame patterns.

Author: Juan Serrano
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import re
from lexical import LexicalAnalizer
from sintactic import SintacticAnalyzer
from semantic import SemanticAnalyzer

class Compiler:
    """
    This class represents the behavior of a complete and modular compiler
    for MacraScript, including a graphical user interface.
    """

    def __init__(self, root):
        """
        Initializes the Compiler, setting up the UI and internal state.
        """
        self.root = root
        self.root.title("MacraScript Compiler")
        self.pattern_visualization_canvas = None
        self.knot_visualization_canvas = None
        self.tokens_window = None  # Reference for the tokens window
        self._setup_ui()

    def _setup_ui(self):
        """
        Creates and organizes the main UI components: code editor,
        visualization canvases, and control buttons. This method is kept
        granular for clarity.
        """
        # Main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)


        # --- Code Editor Section ---
        editor_frame = self._create_section_frame(main_frame, "MacraScript Code")
        editor_frame.grid(row=0, column=0, sticky="nsew")
        self.code_editor = scrolledtext.ScrolledText(editor_frame, width=60, height=25, font=("Courier New", 10))
        self.code_editor.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        # --- Visualization Section ---
        vis_frame = tk.Frame(main_frame)
        vis_frame.grid(row=0, column=1, sticky="nsew", padx=10)
        vis_frame.grid_rowconfigure(0, weight=1)
        vis_frame.grid_rowconfigure(1, weight=1)
        vis_frame.grid_columnconfigure(0, weight=1)


        # ALPHA Pattern Canvas
        alpha_frame = self._create_section_frame(vis_frame, "ALPHA Pattern (Pixel Art)")
        alpha_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        self.pattern_visualization_canvas = tk.Canvas(alpha_frame, bg='white', width=400, height=400)
        self.pattern_visualization_canvas.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        # NORMAL Pattern Canvas
        normal_frame = self._create_section_frame(vis_frame, "NORMAL Pattern (Knots)")
        normal_frame.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        self.knot_visualization_canvas = tk.Canvas(normal_frame, bg='white', width=400, height=400)
        self.knot_visualization_canvas.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        # --- Controls Section ---
        controls_frame = tk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        compile_button = tk.Button(controls_frame, text="Compile and Visualize", command=self.compile_and_run)
        compile_button.pack(side=tk.LEFT, padx=5)
        
        load_alpha_button = tk.Button(controls_frame, text="Load Alpha Example", command=self.load_alpha_example)
        load_alpha_button.pack(side=tk.LEFT, padx=5)
        
        load_normal_button = tk.Button(controls_frame, text="Load Normal Example", command=self.load_normal_example)
        load_normal_button.pack(side=tk.LEFT, padx=5)

    def _create_section_frame(self, parent, text):
        """
        Helper method to create a labeled frame for UI sections.
        """
        frame = tk.LabelFrame(parent, text=text, padx=10, pady=10)
        return frame

    def compile_and_run(self):
        """
        Orchestrates the compilation process: gets code, runs analyzers,
        and triggers visualization.
        """
        code = self.code_editor.get("1.0", tk.END)
        if not code.strip():
            messagebox.showwarning("Warning", "Code editor is empty.")
            return

        self._clear_canvases()

        try:
            # 1. Lexical Analysis
            tokens = LexicalAnalizer.lex(code)

            # 2. Syntactic Analysis
            parser = SintacticAnalyzer(tokens)
            # The syntactic analyzer is simple and mainly for structure validation
            # We rely on the semantic analyzer for a more detailed object
            parser.parse() 

            # 3. Semantic Analysis
            semantic_analyzer = SemanticAnalyzer(tokens)
            pattern = semantic_analyzer.analyze()

            if not pattern.is_valid:
                errors = "\n".join(pattern.errors)
                messagebox.showerror("Semantic Error", f"Errors found:\n{errors}")
                return
            
            # 4. Visualization
            self.root.update_idletasks() # Ensure canvas dimensions are updated
            self._visualize_pattern(pattern)

        except Exception as e:
            messagebox.showerror("Compilation Error", str(e))

    def _visualize_pattern(self, pattern):
        """
        Directs the analyzed pattern to the correct visualization method.
        """
        if pattern.pattern_type == "ALPHA":
            self._draw_alpha_pattern(pattern)
        elif pattern.pattern_type == "NORMAL":
            self._draw_normal_pattern(pattern)

    def _draw_alpha_pattern(self, pattern):
        """
        Draws the ALPHA pattern as a pixel-art grid.
        """
        canvas = self.pattern_visualization_canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if pattern.width == 0 or pattern.height == 0: return

        pixel_width = canvas_width / pattern.width
        pixel_height = canvas_height / pattern.height

        for y, row_data in enumerate(pattern.rows):
            for x, color_index in enumerate(row_data):
                color = self._get_color_from_value(pattern.colors[color_index])
                self._draw_pixel(canvas, x, y, pixel_width, pixel_height, color)

    def _draw_pixel(self, canvas, x, y, width, height, color):
        """
        Draws a single colored rectangle (pixel) on the canvas.
        """
        x1 = x * width
        y1 = y * height
        x2 = x1 + width
        y2 = y1 + height
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def _draw_normal_pattern(self, pattern):
        """
        Draws the NORMAL pattern, visualizing threads and knots.
        """
        canvas = self.knot_visualization_canvas
        canvas_width = canvas.winfo_width()
        
        if pattern.thread_count == 0: return

        num_threads = pattern.thread_count
        thread_spacing = canvas_width / (num_threads + 1)
        
        # Initial positions of threads
        thread_positions = [(i + 1) * thread_spacing for i in range(num_threads)]
        
        self._draw_initial_threads(canvas, thread_positions, pattern.colors)

        y_step = 40  # Vertical distance for each knot
        current_y = 50

        for knot in pattern.knots:
            self._draw_knot(canvas, knot, thread_positions, current_y, y_step, pattern.colors)
            current_y += y_step

    def _draw_initial_threads(self, canvas, positions, colors):
        """
        Draws the top part of the threads before any knots.
        """
        for i, x_pos in enumerate(positions):
            color = self._get_color_from_value(colors[i % len(colors)])
            canvas.create_line(x_pos, 0, x_pos, 20, fill=color, width=2)
            canvas.create_oval(x_pos - 10, 20, x_pos + 10, 40, fill=color, outline="black")
            canvas.create_text(x_pos, 30, text=str(i + 1), fill="white")

    def _draw_knot(self, canvas, knot, thread_pos, y, step, colors):
        """
        Draws a single knot, showing direction and thread interaction.
        """
        t1_idx, t2_idx = knot['threads']
        t1_idx -= 1  # Adjust to 0-based index
        t2_idx -= 1

        x1, x2 = thread_pos[t1_idx], thread_pos[t2_idx]
        y_mid = y + step / 2

        # Determine colors
        c1 = self._get_color_from_value(colors[t1_idx % len(colors)])
        c2 = self._get_color_from_value(colors[t2_idx % len(colors)])

        # Draw lines representing the knot
        canvas.create_line(x1, y, x2, y_mid, fill=c1, width=2)
        canvas.create_line(x2, y, x1, y_mid, fill=c2, width=2)
        
        # Draw the knot center with an arrow for direction
        knot_center_x = (x1 + x2) / 2
        arrow_tip_x = knot_center_x - 10 if knot['direction'] == 'LEFT' else knot_center_x + 10
        
        canvas.create_oval(knot_center_x - 8, y_mid - 8, knot_center_x + 8, y_mid + 8, fill="yellow", outline="black")
        canvas.create_line(knot_center_x, y_mid, arrow_tip_x, y_mid, arrow=tk.LAST, width=2)

        # Draw lines continuing down
        canvas.create_line(x1, y_mid, x1, y + step, fill=c2, width=2)
        canvas.create_line(x2, y_mid, x2, y + step, fill=c1, width=2)

        # Swap thread positions for the next knot
        thread_pos[t1_idx], thread_pos[t2_idx] = thread_pos[t2_idx], thread_pos[t1_idx]


    def _get_color_from_value(self, color_value):
        """
        Converts a color name or hex string into a valid Tkinter color format.
        """
        color = color_value.strip('"')
        # Updated regex to handle optional #
        if re.match(r'^#?[A-Fa-f0-9]{6}$', color):
            return f'#{color.lstrip("#")}'
        return color # Assumes a color name like "red"

    def _clear_canvases(self):
        """
        Clears all drawings from the visualization canvases.
        """
        self.pattern_visualization_canvas.delete("all")
        self.knot_visualization_canvas.delete("all")
        
    def load_alpha_example(self):
        """
        Carga un ejemplo de patrón ALPHA en el editor de código.
        """
        try:
            file_path = "/home/juan-serrano/Documentos/Github/computer-science/Language/ejemplo_simple.txt"
            with open(file_path, "r") as f:
                example_code = f.read()
            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert("1.0", example_code)
            messagebox.showinfo("Ejemplo Cargado", "Se ha cargado un ejemplo de patrón ALPHA.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el ejemplo: {str(e)}")
            
    def load_normal_example(self):
        """
        Carga un ejemplo de patrón NORMAL en el editor de código.
        """
        try:
            file_path = "/home/juan-serrano/Documentos/Github/computer-science/Language/ejemplo_normal.txt"
            with open(file_path, "r") as f:
                example_code = f.read()
            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert("1.0", example_code)
            messagebox.showinfo("Ejemplo Cargado", "Se ha cargado un ejemplo de patrón NORMAL.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el ejemplo: {str(e)}")


if __name__ == '__main__':
    root = tk.Tk()
    app = Compiler(root)
    root.mainloop()
