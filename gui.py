#!/usr/bin/env python3
"""
Mark Water Clean - Interactive GUI Editor
Allows users to manually paint over watermarks for precise removal.
"""

import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from main import remove_watermark


class InteractiveCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mark Water Clean - Editor Interactivo")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        self.original_image = None
        self.mask = None
        self.input_path = ""
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.last_x = None
        self.last_y = None
        self.brush_size = 15
        
        self.setup_ui()

    def setup_ui(self):
        control_frame = tk.Frame(self.root, pady=10, padx=10)
        control_frame.pack(fill="x")
        
        tk.Button(
            control_frame,
            text="📂 Cargar Imagen",
            command=self.load_image,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="🪄 Procesar",
            command=self.process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="🗑️ Limpiar Dibujo",
            command=self.clear_mask,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(side="left", padx=5)
        
        brush_frame = tk.Frame(control_frame)
        brush_frame.pack(side="right", padx=10)
        tk.Label(brush_frame, text="Tamaño del pincel:", font=("Arial", 10)).pack(side="left", padx=5)
        self.brush_slider = tk.Scale(
            brush_frame,
            from_=5,
            to=50,
            orient="horizontal",
            length=150,
            command=self.update_brush
        )
        self.brush_slider.set(self.brush_size)
        self.brush_slider.pack(side="left")

        self.canvas_frame = tk.Frame(self.root, bd=2, relief="sunken", bg="gray")
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="gray", cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)
        
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.status_label = tk.Label(
            self.root,
            text="Carga una imagen para comenzar. Dibuja con el mouse sobre la marca de agua.",
            fg="#666",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=5)

    def on_canvas_resize(self, event):
        if self.original_image is not None:
            self.display_image()

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")]
        )
        if not path:
            return
        
        self.input_path = path
        self.original_image = cv2.imread(path)
        if self.original_image is None:
            messagebox.showerror("Error", "No se pudo cargar la imagen.")
            return

        self.mask = np.zeros_like(self.original_image[:, :, 0])
        
        self.display_image()
        self.status_label.config(
            text="🖌️ Dibuja con el clic izquierdo sobre la marca de agua. Luego presiona 'Procesar'.",
            fg="#2196F3"
        )

    def display_image(self):
        if self.original_image is None:
            return
        
        rgb_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        h, w = rgb_image.shape[:2]
        
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 100:
            canvas_w = 800
        if canvas_h < 100:
            canvas_h = 600
        
        scale = min(canvas_w / w, canvas_h / h, 1.0)
        new_w, new_h = int(w * scale), int(h * scale)
        
        self.scale_x = w / new_w
        self.scale_y = h / new_h
        
        resized = cv2.resize(rgb_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        self.tk_image = ImageTk.PhotoImage(Image.fromarray(resized))
        
        self.canvas.delete("all")
        self.canvas.create_image(canvas_w // 2, canvas_h // 2, anchor="center", image=self.tk_image)

    def start_draw(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.last_x is None or self.original_image is None:
            return
        
        self.canvas.create_line(
            self.last_x, self.last_y, event.x, event.y,
            fill="red", width=self.brush_size, capstyle="round"
        )
        
        orig_x1, orig_y1 = int(self.last_x * self.scale_x), int(self.last_y * self.scale_y)
        orig_x2, orig_y2 = int(event.x * self.scale_x), int(event.y * self.scale_y)
        
        thickness = max(1, int(self.brush_size * min(self.scale_x, self.scale_y)))
        
        cv2.line(self.mask, (orig_x1, orig_y1), (orig_x2, orig_y2), 255, thickness)
        
        self.last_x = event.x
        self.last_y = event.y

    def stop_draw(self, event):
        self.last_x = None
        self.last_y = None

    def update_brush(self, val):
        self.brush_size = int(val)

    def clear_mask(self):
        if self.original_image is not None:
            self.mask = np.zeros_like(self.original_image[:, :, 0])
            self.display_image()
            self.status_label.config(
                text="🗑️ Dibujo limpiado. Vuelve a marcar la zona.",
                fg="#FF9800"
            )

    def process(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Primero carga una imagen.")
            return
        
        self.status_label.config(text="⏳ Procesando...", fg="#FF9800")
        self.root.update()
        
        temp_mask = "temp_interactive_mask.png"
        cv2.imwrite(temp_mask, self.mask)
        
        base, ext = os.path.splitext(self.input_path)
        output_path = f"{base}_cleaned{ext}"
        
        success = remove_watermark(self.input_path, output_path, temp_mask)
        
        if os.path.exists(temp_mask):
            os.remove(temp_mask)
            
        if success:
            self.status_label.config(
                text=f"✅ ¡Éxito! Guardado en: {output_path}",
                fg="#4CAF50"
            )
            messagebox.showinfo(
                "Éxito",
                f"Imagen procesada correctamente.\nGuardada en:\n{output_path}"
            )
            
            self.original_image = cv2.imread(output_path)
            self.display_image()
            self.mask = np.zeros_like(self.original_image[:, :, 0])
        else:
            self.status_label.config(text="❌ Error en el procesamiento.", fg="#F44336")
            messagebox.showerror("Error", "No se pudo procesar la imagen.")


def main():
    root = tk.Tk()
    app = InteractiveCleanerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()