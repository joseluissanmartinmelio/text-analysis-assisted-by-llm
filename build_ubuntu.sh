echo "==================================="
echo "Build Script para Ubuntu 24.04"
echo "==================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "\n${YELLOW}Verificando Python 3.12...${NC}"
if command -v python3.12 &> /dev/null; then
    echo -e "${GREEN}✓ Python 3.12 encontrado${NC}"
    PYTHON_CMD=python3.12
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [ "$PYTHON_VERSION" = "3.12" ]; then
        echo -e "${GREEN}✓ Python 3.12 encontrado${NC}"
        PYTHON_CMD=python3
    else
        echo -e "${RED}✗ Python 3.12 no encontrado. Versión actual: $PYTHON_VERSION${NC}"
        echo "Instalando Python 3.12..."
        sudo apt update
        sudo apt install -y python3.12 python3.12-venv python3.12-dev
        PYTHON_CMD=python3.12
    fi
else
    echo -e "${RED}✗ Python no encontrado${NC}"
    echo "Instalando Python 3.12..."
    sudo apt update
    sudo apt install -y python3.12 python3.12-venv python3.12-dev
    PYTHON_CMD=python3.12
fi

echo -e "\n${YELLOW}Verificando pip...${NC}"
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "Instalando pip..."
    sudo apt install -y python3-pip
fi

echo -e "\n${YELLOW}Instalando dependencias del sistema...${NC}"
sudo apt update
sudo apt install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    libmupdf-dev \
    mupdf-tools \
    libfreetype6-dev \
    libharfbuzz-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev

# Crear entorno virtual si no existe
echo -e "\n${YELLOW}Configurando entorno virtual...${NC}"
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
else
    echo -e "${GREEN}✓ Entorno virtual ya existe${NC}"
fi

source venv/bin/activate

echo -e "\n${YELLOW}Actualizando pip...${NC}"
pip install --upgrade pip

echo -e "\n${YELLOW}Instalando dependencias de Python...${NC}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencias instaladas correctamente${NC}"
else
    echo -e "${RED}✗ Error instalando dependencias${NC}"
    exit 1
fi

if [ ! -f "api_keys.txt" ]; then
    echo -e "\n${YELLOW}Creando archivo de configuración...${NC}"
    echo "OPENROUTER_API_KEY=tu_clave_aqui" > api_keys.txt
    echo -e "${GREEN}✓ Archivo api_keys.txt creado${NC}"
    echo -e "${YELLOW}⚠ Recuerda agregar tu API key de OpenRouter${NC}"
fi

echo -e "\n${YELLOW}Creando directorios necesarios...${NC}"
mkdir -p prompts
mkdir -p static
mkdir -p templates
echo -e "${GREEN}✓ Directorios creados${NC}"

echo -e "\n${YELLOW}Creando script de ejecución...${NC}"
cat > run_app.sh << 'EOF'
source venv/bin/activate
python app.py
EOF

chmod +x run_app.sh
echo -e "${GREEN}✓ Script run_app.sh creado${NC}"

echo -e "\n${YELLOW}Creando lanzador de escritorio...${NC}"
cat > text-analysis-llm.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Text Analysis LLM
Comment=Análisis de documentos con IA
Exec=$(pwd)/run_app.sh
Icon=$(pwd)/icon.png
Terminal=true
Categories=Utility;Development;
EOF

chmod +x text-analysis-llm.desktop
echo -e "${GREEN}✓ Lanzador de escritorio creado${NC}"

echo -e "\n${GREEN}==================================="
echo -e "✓ Construcción completada"
echo -e "===================================${NC}"
echo -e "\nPara ejecutar la aplicación:"
echo -e "  ${YELLOW}./run_app.sh${NC}"
echo -e "\nO activa el entorno y ejecuta manualmente:"
echo -e "  ${YELLOW}source venv/bin/activate${NC}"
echo -e "  ${YELLOW}python app.py${NC}"
echo -e "\n${YELLOW}Recuerda:${NC}"
echo -e "  1. Configurar tu API key en api_keys.txt"
echo -e "  2. La app se ejecutará en http://localhost:8000"
echo -e "  3. Para cambiar el puerto, edita app.py"
