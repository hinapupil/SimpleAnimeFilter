# SimpleAnimeFilter

📷✨ **SimpleAnimeFilter** is a Python script that converts images into an anime-style look.  
It supports batch processing with multiple filter presets.

---

## 🚀 Features
- **Batch processing**: Converts all images in the `input/` folder and saves them in `output/`
- **Edge-preserving smoothing**: Adjustable `smooth_strength` and `edge_strength`
- **Saturation adjustment**: Control the intensity of colors with `saturation`
- **Posterization level**: Adjust the number of color levels with `level`
- **Multiple presets**: Default, realistic, anime-style, and monochrome
- **Auto-ignore `input/` and `output/` in Git**

---

## 📥 Installation

### **1. Requirements**
- **Python 3.13.2**
- `pip` (Python package manager)

### **2. Clone the repository**
```bash
git clone https://github.com/yourusername/SimpleAnimeFilter.git
cd SimpleAnimeFilter
```

### **3. Create a virtual environment**
```bash
python -m venv venv
source venv/Scripts/activate  # For Git Bash
```

### **4. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🖼 Usage

### **1. Add images to `input/`**
Place JPG, PNG, or BMP images in the `input/` folder.

### **2. Run the script**
```bash
python main.py
```

### **3. Output files**
Converted images are saved in `output/` with different styles:
```
output/
  ├── default/       # Standard settings
  ├── realistic/     # More natural look
  ├── anime_style/   # Strong anime-style shading
  ├── monochrome/    # Black-and-white effect
```

---

## ⚙️ Customization
Modify `PARAMETER_SETS` in `script.py` to add new filter presets.

Example:
```python
PARAMETER_SETS = {
    "vivid": {"saturation": 3, "level": 6, "smooth_strength": 30, "edge_strength": 0.6},
}
```

---

## 📝 License
This project is licensed under the **MIT License**.  
See [LICENSE](LICENSE) for details.

---

## 🎉 Contributing
- Report bugs or suggest features in [Issues](https://github.com/yourusername/SimpleAnimeFilter/issues)
- Pull requests are welcome!

🚀 Enjoy!
