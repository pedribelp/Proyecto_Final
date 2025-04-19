
Creado por Pedribel Pión Rijo, 24-0429

---

```markdown
# Sistema de Procesamiento de Figuras Geométricas

## Project Overview
El "Sistema de Procesamiento de Figuras Geométricas" es una aplicación que permite a los usuarios introducir ternas de números y generar representaciones gráficas de figuras geométricas. A través de una interfaz gráfica, los usuarios pueden visualizar las figuras, calcular su área y perímetro, ordenar figuras y buscar por área. La aplicación se basa en el uso de clases de figuras geométricas y algoritmos de ordenamiento y búsqueda.

## Installation

Para ejecutar esta aplicación, necesitas tener Python y algunos paquetes instalados. Sigue estos pasos:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/sistema_figuras.git
   ```

2. Cambia al directorio del proyecto:
   ```bash
   cd sistema_figuras
   ```

3. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   ```

4. Activa el entorno virtual:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En Unix o MacOS:
     ```bash
     source venv/bin/activate
     ```

5. Instala los requisitos necesarios:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Para ejecutar la aplicación, simplemente utiliza:
```bash
python app.py
```

Luego, abre tu navegador y ve a `http://127.0.0.1:8000/` para acceder a la interfaz de usuario.

## Features

- Ingreso de ternas de números para generar diferentes figuras geométricas.
- Cálculo y visualización del área y perímetro de las figuras.
- Ordenar las figuras por área y perímetro.
- Búsquedas por área.
- Visualización de estadísticas sobre las figuras y ternas generadas.
- Interfaz gráfica intuitiva construida con Tkinter.

## Dependencies

La aplicación utiliza varias bibliotecas, las cuales se encuentran listadas en el archivo `requirements.txt`. Las principales dependencias son:
- tkinter: Para la interfaz gráfica.
- matplotlib: Para la visualización gráfica de las figuras.
- NumPy: Para cálculos numéricos.
- estadísticas: Para calcular estadísticas como la mediana.

## Project Structure

```
sistema_figuras/
│
├── app.py                  # Archivo principal para ejecutar la aplicación Flask
├── PionPedribel_PF.py      # Archivo que contiene la lógica del sistema de procesamiento de figuras
├── complete_sistema_figuras.py   # Versión completa del sistema de procesamiento de figuras
├── sistema_figuras.py      # Definiciones de clases para figuras geométricas
├── requirements.txt        # Lista de dependencias del proyecto
```

### Clases definidas:
- **Figura**: Clase base abstracta para todas las figuras geométricas.
- **Cuadrado**: Representación de un cuadrado.
- **Circulo**: Representación de un círculo.
- **Rectangulo**: Representación de un rectángulo.
- **Rombo**: Representación de un rombo.
- **TrianguloEscaleno**: Representación de un triángulo escaleno.
- **Trapecio**: Representación de un trapecio.

### Algoritmos:
- **Algoritmo de Bubble Sort**: Implementado tanto iterativa como recursivamente.
- **Búsqueda Lineal y Binaria**: Métodos para buscar un valor en una lista de figuras.

## Contribuciones

Si quieres contribuir a este proyecto, por favor abre un "issue" o envía una "pull request". Cualquier tipo de mejora, corrección de errores o sugerencia es bienvenida.

---
