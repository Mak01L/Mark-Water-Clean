#!/usr/bin/env python3
"""
Mark Water Clean - GUI Interface
Portable graphical interface using tkinter.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from main import remove_watermark


class MarkWaterCleanGUI:
    """Graphical user interface for Mark Water Clean."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mark Water Clean - Portable")
        self.root.resizable(False, False)
        
        self.input_path = tk.StringVar()
        self.mask_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        title_label = tk.Label(
            main_frame,
            text="🪄 Mark Water Clean",
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        self.create_input_row(main_frame, "Imagen de entrada:", self.input_path, 1)
        self.create_input_row(main_frame, "Máscara (opcional):", self.mask_path, 2)
        self.create_input_row(main_frame, "Ruta de salida:", self.output_path, 3)
        
        process_btn = tk.Button(
            main_frame,
            text="✨ Procesar",
            command=self.process_image,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 12, "bold"),
            padx=20,
            pady=10
        )
        process_btn.grid(row=4, column=0, columnspan=3, pady=30)
        
        self.status_label = tk.Label(
            main_frame,
            text="",
            font=("Helvetica", 10),
            fg="#666666"
        )
        self.status_label.grid(row=5, column=0, columnspan=3)
    
    def create_input_row(self, parent, label_text, string_var, row):
        """Create a row with label, entry field and browse button."""
        label = tk.Label(parent, text=label_text, anchor="w")
        label.grid(row=row, column=0, sticky="w", pady=5)
        
        entry = tk.Entry(parent, textvariable=string_var, width=50)
        entry.grid(row=row + 1, column=0, sticky="ew", padx=(0, 10))
        
        browse_btn = tk.Button(
            parent,
            text="Buscar",
            command=lambda: self.browse_file(string_var)
        )
        browse_btn.grid(row=row + 1, column=1, sticky="e")
        
        parent.grid_columnconfigure(0, weight=1)
    
    def browse_file(self, string_var):
        """Open file dialog and update the corresponding StringVar."""
        current_value = string_var.get()
        
        if string_var == self.output_path:
            filename = filedialog.asksaveasfilename(
                title="Guardar resultado como",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("BMP files", "*.bmp"),
                    ("All files", "*.*")
                ],
                initialfile=current_value if current_value else None
            )
        else:
            filename = filedialog.askopenfilename(
                title="Seleccionar archivo",
                filetypes=[
                    ("Image files", "*.png *.jpg *.jpeg *.bmp"),
                    ("All files", "*.*")
                ]
            )
        
        if filename:
            string_var.set(filename)
    
    def process_image(self):
        """Execute the watermark removal process."""
        if not self.input_path.get():
            messagebox.showerror("Error", "❌ Por favor selecciona una imagen de entrada.")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "❌ Por favor selecciona una ruta de salida.")
            return
        
        if not os.path.exists(self.input_path.get()):
            messagebox.showerror("Error", f"❌ La imagen de entrada no existe:\n{self.input_path.get()}")
            return
        
        mask = self.mask_path.get() if self.mask_path.get() else None
        if mask and not os.path.exists(mask):
            messagebox.showerror("Error", f"❌ El archivo de máscara no existe:\n{mask}")
            return
        
        self.status_label.config(text="⏳ Procesando...", fg="#FF9800")
        self.root.update()
        
        success = remove_watermark(self.input_path.get(), self.output_path.get(), mask)
        
        if success:
            self.status_label.config(text="✅ Éxito - Imagen procesada correctamente", fg="#4CAF50")
            messagebox.showinfo("Éxito", "✨ ¡Imagen procesada correctamente!\n\nLa salida se guardó en:\n" + self.output_path.get())
        else:
            self.status_label.config(text="❌ Error - Procesamiento fallido", fg="#F44336")
            messagebox.showerror("Error", "❌ El procesamiento falló. Revisa la consola para más detalles.")


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = MarkWaterCleanGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()