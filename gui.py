#!/usr/bin/env python3
"""
Mark Water Clean - GUI Interface
Portable graphical interface using tkinter with single and batch mode support.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from main import remove_watermark, process_batch


class MarkWaterCleanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mark Water Clean - Portable")
        self.root.geometry("550x420")
        self.root.resizable(False, False)
        
        self.is_batch_mode = tk.BooleanVar(value=False)
        self.input_path = tk.StringVar()
        self.mask_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        title_label = tk.Label(main_frame, text="🪄 Mark Water Clean", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        batch_check = tk.Checkbutton(
            main_frame, 
            text="📦 Modo Lote (Procesar carpeta completa)", 
            variable=self.is_batch_mode,
            command=self.toggle_mode,
            font=("Helvetica", 10)
        )
        batch_check.pack(anchor="w", pady=(0, 15))
        
        self.create_input_row(main_frame, "Entrada:", self.input_path, self.browse_input)
        self.create_input_row(main_frame, "Máscara (Opc.):", self.mask_path, self.browse_mask)
        self.create_input_row(main_frame, "Salida:", self.output_path, self.browse_output)
        
        process_btn = tk.Button(
            main_frame,
            text="✨ Procesar",
            command=self.process,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=20,
            height=2
        )
        process_btn.pack(pady=25)
        
        self.status_label = tk.Label(main_frame, text="Listo para usar", font=("Helvetica", 10), fg="#666666")
        self.status_label.pack(side="bottom", pady=10)

    def create_input_row(self, parent, label_text, string_var, browse_command):
        frame = tk.Frame(parent)
        frame.pack(fill="x", pady=8)
        
        label = tk.Label(frame, text=label_text, width=15, anchor="w", font=("Helvetica", 10, "bold"))
        label.pack(side="left")
        
        entry = tk.Entry(frame, textvariable=string_var, font=("Helvetica", 10))
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn = tk.Button(frame, text="Buscar", command=browse_command, width=10)
        btn.pack(side="right")

    def toggle_mode(self):
        self.input_path.set("")
        self.mask_path.set("")
        self.output_path.set("")
        self.status_label.config(text="Modo cambiado. Selecciona las rutas nuevamente.", fg="#2196F3")

    def browse_input(self):
        if self.is_batch_mode.get():
            path = filedialog.askdirectory(title="Seleccionar carpeta de entrada")
        else:
            path = filedialog.askopenfilename(
                title="Seleccionar imagen de entrada",
                filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")]
            )
            if path:
                base, ext = os.path.splitext(path)
                self.output_path.set(f"{base}_cleaned{ext}")
                
        if path:
            self.input_path.set(path)

    def browse_mask(self):
        path = filedialog.askopenfilename(
            title="Seleccionar máscara (opcional)",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")]
        )
        if path:
            self.mask_path.set(path)

    def browse_output(self):
        if self.is_batch_mode.get():
            path = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        else:
            path = filedialog.asksaveasfilename(
                title="Guardar resultado como",
                filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg"), ("BMP", "*.bmp")],
                initialfile=self.output_path.get() or "output_cleaned.png"
            )
        if path:
            self.output_path.set(path)

    def process(self):
        inp = self.input_path.get()
        out = self.output_path.get()
        mask = self.mask_path.get() or None
        
        if not inp or not out:
            messagebox.showerror("Error", "❌ Por favor selecciona las rutas de entrada y salida.")
            return
            
        if not os.path.exists(inp):
            messagebox.showerror("Error", f"❌ La ruta de entrada no existe:\n{inp}")
            return

        self.status_label.config(text="⏳ Procesando...", fg="#FF9800")
        self.root.update()
        
        try:
            if self.is_batch_mode.get():
                if not os.path.isdir(inp) or not os.path.isdir(out):
                    messagebox.showerror("Error", "❌ En modo lote, entrada y salida deben ser carpetas.")
                    self.status_label.config(text="❌ Error de configuración", fg="#F44336")
                    return
                
                successful, failed = process_batch(inp, out, mask)
                total = successful + failed
                if failed == 0:
                    self.status_label.config(text=f"✅ Éxito: {successful} imágenes procesadas", fg="#4CAF50")
                    messagebox.showinfo("Éxito", f"✨ ¡Procesamiento por lotes completado!\n✅ Exitosas: {successful}\n❌ Fallidas: {failed}")
                else:
                    self.status_label.config(text=f"⚠️ Completado con {failed} errores", fg="#FF9800")
                    messagebox.showwarning("Advertencia", f"Procesamiento completado.\n✅ Exitosas: {successful}\n❌ Fallidas: {failed}")
            else:
                success = remove_watermark(inp, out, mask)
                if success:
                    self.status_label.config(text="✅ Éxito - Imagen procesada", fg="#4CAF50")
                    messagebox.showinfo("Éxito", f"✨ ¡Imagen procesada correctamente!\nGuardada en:\n{out}")
                else:
                    self.status_label.config(text="❌ Error en el proceso", fg="#F44336")
                    messagebox.showerror("Error", "❌ El procesamiento falló.")
        except Exception as e:
            self.status_label.config(text="❌ Error inesperado", fg="#F44336")
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")


def main():
    root = tk.Tk()
    app = MarkWaterCleanGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()