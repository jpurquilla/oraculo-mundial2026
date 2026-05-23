cat > README.md << 'EOF'
# 🌍 Oráculo del Balón - Predicción Mundial 2026

## Configuración inicial

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/oraculo-mundial2026.git
cd oraculo-mundial2026
```

### 2. Crear entorno virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar Kaggle API (requerido)
1. Crear cuenta en https://www.kaggle.com
2. Ir a Settings → API → Generate New Token
3. Ejecutar en terminal:
```bash
mkdir -p ~/.kaggle
echo TU_API_TOKEN > ~/.kaggle/access_token
chmod 600 ~/.kaggle/access_token
```

### 4. Descargar datos
```bash
python src/download_sources.py
```

## Estructura del proyecto

oraculo-mundial2026/
├── data/
│   ├── raw/          # Datos crudos descargados
│   └── processed/    # Datos limpios y features
├── notebooks/        # Jupyter Notebooks de análisis
├── src/              # Scripts Python
├── models/           # Modelos entrenados
└── reports/          # Reporte técnico IEEE