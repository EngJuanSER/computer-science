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

        # --- Pixel Visualization with Scrollbars ---
        pixel_container = self._create_section_frame(vis_frame, "Pattern (Pixel Art)")
        pixel_container.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        pixel_container.grid_rowconfigure(0, weight=1)
        pixel_container.grid_columnconfigure(0, weight=1)
        
        self.pattern_visualization_canvas = tk.Canvas(pixel_container, bg='white')
        px_h_scroll = tk.Scrollbar(pixel_container, orient=tk.HORIZONTAL, command=self.pattern_visualization_canvas.xview)
        px_v_scroll = tk.Scrollbar(pixel_container, orient=tk.VERTICAL, command=self.pattern_visualization_canvas.yview)
        self.pattern_visualization_canvas.configure(xscrollcommand=px_h_scroll.set, yscrollcommand=px_v_scroll.set)
        
        self.pattern_visualization_canvas.grid(row=0, column=0, sticky="nsew")
        px_h_scroll.grid(row=1, column=0, sticky="ew")
        px_v_scroll.grid(row=0, column=1, sticky="ns")

        # --- Knot Flow Visualization with Scrollbars ---
        knot_container = self._create_section_frame(vis_frame, "Knot Flow Diagram")
        knot_container.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        knot_container.grid_rowconfigure(0, weight=1)
        knot_container.grid_columnconfigure(0, weight=1)

        self.knot_visualization_canvas = tk.Canvas(knot_container, bg='white')
        kn_h_scroll = tk.Scrollbar(knot_container, orient=tk.HORIZONTAL, command=self.knot_visualization_canvas.xview)
        kn_v_scroll = tk.Scrollbar(knot_container, orient=tk.VERTICAL, command=self.knot_visualization_canvas.yview)
        self.knot_visualization_canvas.configure(xscrollcommand=kn_h_scroll.set, yscrollcommand=kn_v_scroll.set)

        self.knot_visualization_canvas.grid(row=0, column=0, sticky="nsew")
        kn_h_scroll.grid(row=1, column=0, sticky="ew")
        kn_v_scroll.grid(row=0, column=1, sticky="ns")

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
            # 1. Lexical Analysis
            print("--- 1. Lexical Analysis ---")
            tokens = LexicalAnalizer.lex(code)
            for token in tokens:
                print(token)
            print("-" * 27 + "\n")

            # 2. Syntactic Analysis
            print("--- 2. Syntactic Analysis ---")
            parser = SintacticAnalyzer(tokens)
            parsed_structure = parser.parse()
            print("Parsed Structure:", parsed_structure)
            print("-" * 29 + "\n")

            # 3. Semantic Analysis
            print("--- 3. Semantic Analysis ---")
            semantic_analyzer = SemanticAnalyzer(tokens)
            pattern = semantic_analyzer.analyze()
            print(pattern)
            print("-" * 28 + "\n")

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
        Directs the analyzed pattern to the correct visualization methods.
        This now draws a pixel pattern for all types, and a specific knot
        flow diagram below it.
        """
        # 1. Draw the pixel-art pattern on the top canvas for both types
        self._draw_pixel_pattern(pattern)

        # 2. Draw the specific knot flow diagram on the bottom canvas
        if pattern.pattern_type == "ALPHA":
            self._draw_alpha_knot_flow(pattern)
        elif pattern.pattern_type == "NORMAL":
            self._draw_normal_knot_diagram(pattern)
        
        # 3. Update scrollregions for both canvases
        self.pattern_visualization_canvas.configure(scrollregion=self.pattern_visualization_canvas.bbox("all"))
        self.knot_visualization_canvas.configure(scrollregion=self.knot_visualization_canvas.bbox("all"))

    def _draw_pixel_pattern(self, pattern):
        """Draws a pixel-art grid. Squares for ALPHA, Diamonds for NORMAL."""
        canvas = self.pattern_visualization_canvas
        
        if pattern.pattern_type == "ALPHA":
            pixel_size = 20
            if not pattern.rows or pattern.width == 0: return
            for y, row_data in enumerate(pattern.rows):
                for x, color_index in enumerate(row_data):
                    color = self._get_color_from_value(pattern.colors[color_index])
                    self._draw_pixel(canvas, x, y, pixel_size, pixel_size, color)
        
        elif pattern.pattern_type == "NORMAL":
            if not pattern.knots or pattern.thread_count < 2: return
            diamond_w, diamond_h = 24, 24
            x_margin, y_margin = 20, 20
            
            thread_colors = [pattern.colors[i % len(pattern.colors)] for i in range(pattern.thread_count)]
            knots_per_row = pattern.thread_count // 2
            
            row_idx = 0
            col_idx = 0

            for knot in pattern.knots:
                t1_idx, t2_idx = knot['threads']
                t1_idx -= 1
                t2_idx -= 1

                active_thread_idx = t1_idx if knot['direction'] == 'RIGHT' else t2_idx
                knot_color = thread_colors[active_thread_idx]

                cx = (col_idx * diamond_w) + ((row_idx % 2) * diamond_w / 2) + x_margin
                cy = (row_idx * diamond_h / 2) + y_margin

                self._draw_diamond(canvas, cx, cy, diamond_w, diamond_h, self._get_color_from_value(knot_color))
                
                thread_colors[t1_idx], thread_colors[t2_idx] = thread_colors[t2_idx], thread_colors[t1_idx]
                
                col_idx += 1
                if col_idx >= knots_per_row - (row_idx % 2):
                    col_idx = 0
                    row_idx += 1

    def _draw_pixel(self, canvas, x, y, width, height, color):
        """Draws a single colored rectangle (pixel) on the canvas."""
        x1, y1 = x * width + 5, y * height + 5 # Add margin
        x2, y2 = x1 + width, y1 + height
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="grey50")

    def _draw_diamond(self, canvas, cx, cy, w, h, color):
        """Draws a single colored diamond on the canvas."""
        points = [cx, cy - h/2, cx + w/2, cy, cx, cy + h/2, cx - w/2, cy]
        canvas.create_polygon(points, fill=color, outline="black")

    def _draw_alpha_knot_flow(self, pattern):
        """Draws the ALPHA pattern as a snake-like knot flow diagram."""
        canvas = self.knot_visualization_canvas
        if not pattern.rows or pattern.width == 0: return

        node_size, x_spacing, y_spacing = 25, 40, 40

        for y, row_data in enumerate(pattern.rows):
            direction = 1 if y % 2 == 0 else -1
            for x_idx in range(pattern.width):
                visual_x = x_idx if direction == 1 else pattern.width - 1 - x_idx
                cx = (visual_x + 1) * x_spacing
                cy = (y + 1) * y_spacing
                
                color_index = row_data[visual_x]
                color = self._get_color_from_value(pattern.colors[color_index])

                if x_idx < pattern.width - 1:
                    next_cx = (visual_x + direction + 1) * x_spacing
                    canvas.create_line(cx, cy, next_cx, cy, fill=color, width=2)
                elif y < pattern.height - 1:
                    next_cy = (y + 2) * y_spacing
                    canvas.create_line(cx, cy, cx, next_cy, fill=color, width=2)

        for y, row_data in enumerate(pattern.rows):
            direction = 1 if y % 2 == 0 else -1
            for x_idx in range(pattern.width):
                visual_x = x_idx if direction == 1 else pattern.width - 1 - x_idx
                cx = (visual_x + 1) * x_spacing
                cy = (y + 1) * y_spacing
                
                color_index = row_data[visual_x]
                color = self._get_color_from_value(pattern.colors[color_index])
                
                canvas.create_oval(cx - node_size/2, cy - node_size/2, cx + node_size/2, cy + node_size/2, fill=color, outline="black")
                arrow_start = cx - node_size * 0.2 * direction
                arrow_end = cx + node_size * 0.2 * direction
                canvas.create_line(arrow_start, cy, arrow_end, cy, arrow=tk.LAST, fill="white", width=2)

    def _draw_normal_knot_diagram(self, pattern):
        """Draws the NORMAL pattern with a clear, lattice-style knot diagram."""
        canvas = self.knot_visualization_canvas
        if pattern.thread_count == 0 or not pattern.knots: return

        thread_spacing, y_step = 50, 60
        y_margin, x_margin = 40, 30
        node_radius = 12

        # Initial state
        thread_x = [(i * thread_spacing) + x_margin for i in range(pattern.thread_count)]
        thread_colors = [pattern.colors[i % len(pattern.colors)] for i in range(pattern.thread_count)]
        
        # Draw initial thread markers
        for i, x_pos in enumerate(thread_x):
            color = self._get_color_from_value(thread_colors[i])
            canvas.create_oval(x_pos - 15, y_margin - 15, x_pos + 15, y_margin + 15, fill=color, outline="black")
            canvas.create_text(x_pos, y_margin, text=chr(ord('A') + i), fill="white", font=("Arial", 10, "bold"))

        current_y = y_margin
        row_idx = 0
        knots_in_row = (pattern.thread_count - (row_idx % 2)) // 2
        knot_count_in_row = 0

        # Store the y-positions for each thread to draw lines correctly
        thread_y_positions = [current_y] * pattern.thread_count

        for knot in pattern.knots:
            t1_idx, t2_idx = knot['threads']
            t1_idx -= 1
            t2_idx -= 1

            # --- Draw connecting lines from previous state ---
            # Active thread
            canvas.create_line(thread_x[t1_idx], thread_y_positions[t1_idx], thread_x[t2_idx], current_y + y_step, fill=self._get_color_from_value(thread_colors[t1_idx]), width=4)
            # Passive thread
            canvas.create_line(thread_x[t2_idx], thread_y_positions[t2_idx], thread_x[t1_idx], current_y + y_step, fill=self._get_color_from_value(thread_colors[t2_idx]), width=4)

            # --- Draw the knot node ---
            knot_cx = (thread_x[t1_idx] + thread_x[t2_idx]) / 2
            knot_cy = current_y + y_step / 2
            
            # Determine knot color based on active thread
            active_thread_idx = t1_idx if knot['direction'] == 'RIGHT' else t2_idx
            knot_color = self._get_color_from_value(thread_colors[active_thread_idx])
            
            canvas.create_oval(knot_cx - node_radius, knot_cy - node_radius, knot_cx + node_radius, knot_cy + node_radius, fill=knot_color, outline="black", width=1)
            arrow_dir = -1 if knot['direction'] == 'LEFT' else 1
            canvas.create_line(knot_cx, knot_cy, knot_cx + 6 * arrow_dir, knot_cy, arrow=tk.LAST, fill="white", width=2)

            # Update y-positions for the threads involved in the knot
            thread_y_positions[t1_idx] = current_y + y_step
            thread_y_positions[t2_idx] = current_y + y_step

            # Swap colors for the next state
            thread_colors[t1_idx], thread_colors[t2_idx] = thread_colors[t2_idx], thread_colors[t1_idx]
            
            knot_count_in_row += 1
            if knot_count_in_row >= knots_in_row:
                # End of a visual row, update all thread y-positions and reset counters
                for i in range(pattern.thread_count):
                    if thread_y_positions[i] < current_y + y_step:
                         canvas.create_line(thread_x[i], thread_y_positions[i], thread_x[i], current_y + y_step, fill=self._get_color_from_value(thread_colors[i]), width=4)
                         thread_y_positions[i] = current_y + y_step

                current_y += y_step
                row_idx += 1
                knots_in_row = (pattern.thread_count - (row_idx % 2)) // 2
                knot_count_in_row = 0


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
