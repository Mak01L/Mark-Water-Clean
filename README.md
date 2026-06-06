# 🪄 Mark Water Clean

CLI tool for removing watermarks and unwanted objects from images using OpenCV inpainting.

> **⚠️ Ethical Note:** Use this tool responsibly. Respect copyright and intellectual property rights. Only remove watermarks from images you own or have explicit permission to modify.

## Features

- 🤖 **Automatic mask generation** - Detects white/gray areas automatically
- ⚡ **Fast processing** - Uses efficient TELEA inpainting algorithm
- 🪶 **Lightweight** - Minimal dependencies, no heavy ML models required
- 🎯 **Custom mask support** - Use your own precise masks for better results

## Installation

```bash
git clone https://github.com/Mak01L/Mark-Water-Clean.git
cd Mark-Water-Clean
pip install -r requirements.txt
```

## Usage

### Basic usage (automatic mask detection)

```bash
python main.py -i input.jpg -o output.jpg
```

### With custom mask

```bash
python main.py -i input.jpg -o output.jpg -m mask.png
```

### Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `-i`, `--input` | Path to input image | Yes |
| `-o`, `--output` | Path to save output image | Yes |
| `-m`, `--mask` | Path to custom mask (white = remove) | No |

### Creating a custom mask

For best results, create a PNG mask where:
- **White pixels (255)** = areas to remove
- **Black pixels (0)** = areas to keep

You can create masks using image editors like Photoshop, GIMP, or Paint.NET.

## Roadmap

- [ ] 🎬 Video support (process entire video files)
- [ ] 🧠 Advanced AI inpainting (LaMa, MAT)
- [ ] 🎨 GUI interface for non-technical users
- [ ] 📦 Batch processing for multiple images
- [ ] 🔧 Interactive mask editor

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.