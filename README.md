# 🪄 Mark Water Clean

CLI tool for removing watermarks and unwanted objects from images using OpenCV inpainting.

> **⚠️ Ethical Note:** Use this tool responsibly. Respect copyright and intellectual property rights. Only remove watermarks from images you own or have explicit permission to modify.

## Features

- 🤖 **Automatic mask generation** - Detects white/gray areas automatically
- ⚡ **Fast processing** - Uses efficient TELEA inpainting algorithm
- 🪶 **Lightweight** - Minimal dependencies, no heavy ML models required
- 🎯 **Custom mask support** - Use your own precise masks for better results
- 📦 **Batch processing** - Process entire directories of images at once

## 📸 Demo: Antes y Después

| Original (Con marca de agua) | Resultado (Procesado) |
| :---: | :---: |
| ![Antes](examples/before.jpg) | ![Después](examples/after.jpg) |

> 💡 **Nota:** Para ver el resultado, agrega tus propias imágenes de prueba en la carpeta `examples/` y actualiza las rutas.

## 🖥️ Versión Portable (Sin instalación)

Si no quieres instalar Python, puedes compilar la herramienta en un ejecutable `.exe` (Windows) o binario (Mac/Linux):

1. Instala PyInstaller: `pip install pyinstaller`
2. Genera el ejecutable: `pyinstaller --noconsole --onefile gui.py`
3. El archivo portable estará en la carpeta `dist/`.

*(Próximamente: Descarga directa del ejecutable en la sección [Releases](#))*

## Installation

```bash
git clone https://github.com/Mak01L/Mark-Water-Clean.git
cd Mark-Water-Clean
pip install -r requirements.txt
```

## Usage

### Single image (automatic mask detection)

```bash
python main.py -i input.jpg -o output.jpg
```

### Single image with custom mask

```bash
python main.py -i input.jpg -o output.jpg -m mask.png
```

### Batch processing (entire directory)

```bash
python main.py -i ./images/input -o ./images/output
```

```bash
python main.py -i ./images/input -o ./images/output -m mask.png
```

### GUI Mode (Graphical Interface)

```bash
python gui.py
```

### Arguments (CLI)

| Argument | Description | Required |
|----------|-------------|----------|
| `-i`, `--input` | Path to input image or directory | Yes |
| `-o`, `--output` | Path to save output image or directory | Yes |
| `-m`, `--mask` | Path to custom mask (white = remove) | No |

### Supported formats

- `.jpg`, `.jpeg`
- `.png`
- `.bmp`

### Creating a custom mask

For best results, create a PNG mask where:
- **White pixels (255)** = areas to remove
- **Black pixels (0)** = areas to keep

You can create masks using image editors like Photoshop, GIMP, or Paint.NET.

## Roadmap

- [ ] 🎬 Video support (process entire video files)
- [ ] 🧠 Advanced AI inpainting (LaMa, MAT)
- [x] 🖥️ GUI & Portable executable support
- [x] 📦 Batch processing for multiple images
- [ ] 🔧 Interactive mask editor

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.