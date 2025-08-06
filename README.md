# Text analysis assisted by llm (José San Martín Melio)

Una aplicación web para analizar documentos usando inteligencia artificial (otra más!). Permite procesar archivos pdf, docx y txt usando diferentes modelos de ia como claude, deepseek, openai y otros.

## Qué hace esta aplicación

- Analiza documentos individuales (pdf, docx, txt)
- Procesa múltiples documentos en lotes
- Extrae texto y lo analiza usando prompts personalizados
- Genera reportes en formato markdown
- Cuenta estadísticas de palabras
- Unifica múltiples análisis en un solo documento
- Permite modificar parámetros de decodificación y trabajar con los modelos de manera algo más personalizada que los chatbots tradicionales.

## Requisitos del sistema

- python 3.12
- conexión a internet
- cuenta en openrouter.ai para usar los modelos de ia, algunos son gratuitos y otros de pago.

## Instalación paso a paso

### 1. Descargar el proyecto

```bash
git clone https://github.com/joseluissanmartinmelio/text-analysis-assisted-by-llm.git
cd text-analysis-assisted-by-llm
```

### 2. instalar python

**en windows:**
- descarga python desde https://python.org
- durante la instalación marca "add python to path"


**en linux (ubuntu/debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 3. instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. obtener clave de api

1. ve a https://openrouter.ai
2. crea una cuenta gratuita
3. ve a la sección "keys"
4. crea una nueva api key
5. copia la clave

### 5. configurar la clave de api

**opción 1: variable de entorno (recomendado)**

**en windows:**
```bash
set OPENROUTER_API_KEY=tu_clave_aqui
```

**opción 2: archivo de configuración**

crea un archivo llamado `api_keys.txt` en la carpeta principal y escribe:
```
OPENROUTER_API_KEY=tu_clave_aqui
```

## cómo usar la aplicación

### iniciar la aplicación

```bash
python app.py
```

la aplicación se abrirá en http://localhost:5000

### análisis de un documento individual

1. abre tu navegador en http://localhost:5000
2. selecciona un archivo (pdf, docx o txt)
3. elige un prompt de análisis
4. selecciona el modelo de ia
5. haz clic en "analizar documento"
6. espera los resultados

### procesamiento en lote

1. ve a http://localhost:5000/batch
2. ingresa la ruta de la carpeta con documentos
3. ingresa la ruta donde guardar resultados
4. selecciona el tipo de archivo (.pdf, .docx, .txt)
5. elige un prompt
6. selecciona el modelo de ia
7. inicia el proceso

## prompts disponibles

la aplicación incluye varios prompts predefinidos:

- `1_systematic_conceptual_definitions_extraction.txt`: extrae definiciones conceptuales
- `2_systemic_resume.txt`: genera resúmenes sistemáticos de artículos
- `3_systemic_theory_frame.txt`: construye marcos teóricos en base a los resumenes.

puedes crear tus propios prompts agregando archivos .txt en la carpeta `prompts/` y siempre incorporando {context} al final del prompt para incorporar el texto del articulo de interés.

## modelos de ia disponibles

- **claude**: anthropic claude sonnet 4
- **deepseek**: deepseek r1 (gratuito)
- **openai_o3**: openai o3
- **openai_o4_mini**: openai o4 mini

cada modelo tiene diferentes costos y capacidades. deepseek r1 es gratuito y recomendado para empezar.

## estructura de carpetas

```
text-analysis-assisted-by-llm/
├── app.py                  # aplicación principal
├── requirements.txt        # dependencias
├── prompts/               # plantillas de análisis
├── src/                   # código fuente
├── templates/             # interfaz web
└── README.md              # este archivo
```

## Solución de problemas comunes

### error: "no module named 'fitz'"

```bash
pip install PyMuPDF
```

### error: "openrouter api key not found"

verifica que hayas configurado correctamente la clave de api siguiendo el paso 5.

### error: "port already in use"

cambia el puerto en `app.py`:
```python
app.run(debug=True, port=5001)
```

### el análisis es muy lento

- usa deepseek r1 (más rápido y gratuito)
- divide documentos grandes en archivos más pequeños
- verifica tu conexión a internet

### Errores al leer pdf

algunos pdf pueden tener protección o formato complejo. prueba:
- convertir el pdf a txt primero
- usar un pdf sin protección por contraseña
- verificar que el pdf contenga texto seleccionable
- Puedes implementar OCR con Tesseract si el pdf es una imagen escaneada [Link aquí](https://pypi.org/project/pytesseract/)

## Uso avanzado

### crear prompts personalizados

1. crea un archivo .txt en la carpeta `prompts/`
2. usa `{context}` donde quieres que aparezca el texto del documento
3. escribe las instrucciones para la ia

ejemplo:
```
analiza el siguiente texto y extrae las ideas principales.

texto a analizar:
{context}

formato de salida:
- idea 1
- idea 2
- idea 3
```

### procesamiento por lotes grandes

para procesar muchos documentos:
1. organiza los archivos en una carpeta
2. usa nombres descriptivos
3. crea una carpeta de salida vacía
4. ejecuta el procesamiento por lotes
5. revisa los resultados en la carpeta de salida

### unificar resultados

usa el script `unify_markdowns.py` para combinar múltiples análisis:

```bash
cd src
python unify_markdowns.py
```

edita las rutas en el archivo antes de ejecutar.

## limitaciones

- requiere conexión a internet
- los modelos de ia tienen límites de uso
- archivos muy grandes pueden causar errores
- algunos pdf complejos pueden no procesarse correctamente
- [la mayoría de los modelos de código abierto muestran una longitud de contexto efectiva inferior al 50% de su longitud de entrenamiento](https://arxiv.org/html/2410.18745v1), revisa la longitud máxima del modelo que uses y trata de no excederla en un 50-60% (si tiene 64k, no utilices más de 38k), para saber cuantos tokens tiene tu texto utiliza el tokenizador de Openai [Link aquí](https://platform.openai.com/tokenizer)

## Créditos

desarrollado por josé san martin melio para análisis asistido por inteligencia artificial. Copiloto de codificación: [Ollama - deepseek-r1:14b](https://ollama.com/library/deepseek-r1:14b) soportado por una RTX 4070 Ti Super.

## licencia

este proyecto es de código abierto. puedes usarlo y modificarlo libremente.

## soporte

El programa es sencillo, pero si tienes problemas:
1. revisa esta guía completamente
2. verifica que todos los requisitos estén instalados
3. comprueba tu conexión a internet
4. asegúrate de que la api key sea válida
