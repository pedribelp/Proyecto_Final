from flask import Flask, render_template_string, request, redirect, url_for, flash
import math
import matplotlib.pyplot as plt
import io
import base64
import statistics

app = Flask(__name__)
app.secret_key = 'secret-key-for-session'

class Figura:
    def __init__(self, tipo):
        self.tipo = tipo
    def calcular_area(self):
        pass
    def calcular_perimetro(self):
        pass

class Cuadrado(Figura):
    def __init__(self, lado):
        super().__init__("Cuadrado")
        self.lado = lado
    def calcular_area(self):
        return self.lado ** 2
    def calcular_perimetro(self):
        return 4 * self.lado

class Circulo(Figura):
    def __init__(self, radio):
        super().__init__("Círculo")
        self.radio = radio
    def calcular_area(self):
        return math.pi * (self.radio ** 2)
    def calcular_perimetro(self):
        return 2 * math.pi * self.radio

class Rectangulo(Figura):
    def __init__(self, lado1, lado2):
        super().__init__("Rectángulo")
        self.lado1 = lado1
        self.lado2 = lado2
    def calcular_area(self):
        return self.lado1 * self.lado2
    def calcular_perimetro(self):
        return 2 * (self.lado1 + self.lado2)

class Rombo(Figura):
    def __init__(self, diagonal1, diagonal2):
        super().__init__("Rombo")
        self.diagonal1 = diagonal1
        self.diagonal2 = diagonal2
        self.lado = math.sqrt((self.diagonal1/2)**2 + (self.diagonal2/2)**2)
    def calcular_area(self):
        return (self.diagonal1 * self.diagonal2) / 2
    def calcular_perimetro(self):
        return 4 * self.lado

class TrianguloEscaleno(Figura):
    def __init__(self, lado1, lado2, lado3):
        super().__init__("Triángulo Escaleno")
        if lado1 + lado2 <= lado3 or lado1 + lado3 <= lado2 or lado2 + lado3 <= lado1:
            raise ValueError("Lados no forman un triángulo válido")
        self.lado1 = lado1
        self.lado2 = lado2
        self.lado3 = lado3
    def calcular_area(self):
        s = (self.lado1 + self.lado2 + self.lado3) / 2
        return math.sqrt(s * (s - self.lado1) * (s - self.lado2) * (s - self.lado3))
    def calcular_perimetro(self):
        return self.lado1 + self.lado2 + self.lado3

class Trapecio(Figura):
    def __init__(self, base_mayor, base_menor, lado1, lado2):
        super().__init__("Trapecio")
        self.base_mayor = base_mayor
        self.base_menor = base_menor
        self.lado1 = lado1
        self.lado2 = lado2
        s = (base_mayor - base_menor) / 2
        if s > lado1 or s > lado2:
            raise ValueError("Lados no forman un trapecio válido")
        self.altura = math.sqrt(lado1**2 - s**2)
    def calcular_area(self):
        return ((self.base_mayor + self.base_menor) / 2) * self.altura
    def calcular_perimetro(self):
        return self.base_mayor + self.base_menor + self.lado1 + self.lado2

# Bubble sort iterative and recursive implementations

def bubble_sort_iterative(arr, key=lambda x: x, reverse=False):
    n = len(arr)
    resultado = arr.copy()
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            condicion = key(resultado[j]) > key(resultado[j + 1])
            if reverse:
                condicion = not condicion
            if condicion:
                resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
                swapped = True
        if not swapped:
            break
    return resultado

def bubble_sort_recursive(arr, key=lambda x: x, reverse=False):
    resultado = arr.copy()
    def recursive_sort(n):
        if n == 1:
            return
        swapped = False
        for i in range(n - 1):
            condicion = key(resultado[i]) > key(resultado[i + 1])
            if reverse:
                condicion = not condicion
            if condicion:
                resultado[i], resultado[i + 1] = resultado[i + 1], resultado[i]
                swapped = True
        if not swapped:
            return
        recursive_sort(n - 1)
    recursive_sort(len(resultado))
    return resultado

# Processing ternas to generate figures

def procesar_terna(terna):
    terna_ordenada = sorted(terna)
    figuras = {}
    if terna_ordenada[0] == terna_ordenada[1] == terna_ordenada[2]:
        lado = terna_ordenada[0]
        figuras["cuadrado"] = Cuadrado(lado)
        figuras["circulo"] = Circulo(lado)
    elif terna_ordenada[0] == terna_ordenada[1] or terna_ordenada[1] == terna_ordenada[2]:
        if terna_ordenada[0] == terna_ordenada[1]:
            lado_igual = terna_ordenada[0]
            lado_distinto = terna_ordenada[2]
        else:
            lado_igual = terna_ordenada[1]
            lado_distinto = terna_ordenada[0]
        figuras["rectangulo"] = Rectangulo(lado_igual, lado_distinto)
        figuras["rombo"] = Rombo(lado_igual, lado_distinto)
    else:
        try:
            figuras["triangulo"] = TrianguloEscaleno(terna_ordenada[0], terna_ordenada[1], terna_ordenada[2])
        except ValueError:
            pass
        base_mayor = max(terna)
        base_menor = min(terna)
        lado_medio = sum(terna) - base_mayor - base_menor
        delta = (base_mayor - base_menor) / 2
        try:
            lado2 = math.sqrt(lado_medio**2 - delta**2)
            figuras["trapecio"] = Trapecio(base_mayor, base_menor, lado_medio, lado2)
        except ValueError:
            pass
    return figuras

# Global data storage

ternas = []
figuras = []

def generar_datos_prueba():
    return [
        [5, 5, 5],
        [10, 10, 10],
        [4, 4, 8],
        [7, 3, 7],
        [3, 4, 5],
        [7, 9, 12],
        [6, 6, 6],
        [8, 8, 12],
        [5, 7, 10]
    ]

# Load test data on startup
for terna in generar_datos_prueba():
    figuras_terna = procesar_terna(terna)
    if figuras_terna:
        ternas.append(terna)
        for f in figuras_terna.values():
            figuras.append(f)

# Helper to generate matplotlib plot as base64 image

def plot_figura(figura):
    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    # Draw figure shape
    if figura.tipo == "Cuadrado":
        lado = figura.lado
        x = [-lado/2, lado/2, lado/2, -lado/2, -lado/2]
        y = [-lado/2, -lado/2, lado/2, lado/2, -lado/2]
        ax.plot(x, y, 'b-')
    elif figura.tipo == "Círculo":
        circle = plt.Circle((0,0), figura.radio, fill=False, color='r')
        ax.add_patch(circle)
    elif figura.tipo == "Rectángulo":
        w, h = figura.lado1, figura.lado2
        x = [-w/2, w/2, w/2, -w/2, -w/2]
        y = [-h/2, -h/2, h/2, h/2, -h/2]
        ax.plot(x, y, 'g-')
    elif figura.tipo == "Rombo":
        d1, d2 = figura.diagonal1, figura.diagonal2
        x = [d1/2, 0, -d1/2, 0, d1/2]
        y = [0, d2/2, 0, -d2/2, 0]
        ax.plot(x, y, 'm-')
    elif figura.tipo == "Triángulo Escaleno":
        x1, y1 = 0, 0
        x2, y2 = figura.lado1, 0
        cos_angle = (figura.lado1**2 + figura.lado2**2 - figura.lado3**2) / (2 * figura.lado1 * figura.lado2)
        sin_angle = math.sqrt(1 - cos_angle**2)
        x3 = figura.lado2 * cos_angle
        y3 = figura.lado2 * sin_angle
        cx = (x1 + x2 + x3) / 3
        cy = (y1 + y2 + y3) / 3
        x1, x2, x3 = x1 - cx, x2 - cx, x3 - cx
        y1, y2, y3 = y1 - cy, y2 - cy, y3 - cy
        x = [x1, x2, x3, x1]
        y = [y1, y2, y3, y1]
        ax.plot(x, y, 'c-')
    elif figura.tipo == "Trapecio":
        bm, bn, l1, l2 = figura.base_mayor, figura.base_menor, figura.lado1, figura.lado2
        s = (bm - bn) / 2
        h = figura.altura
        x = [-bm/2, bm/2, bn/2, -bn/2, -bm/2]
        y = [-h/2, -h/2, h/2, h/2, -h/2]
        ax.plot(x, y, 'y-')
    area = figura.calcular_area()
    perim = figura.calcular_perimetro()
    ax.set_title(f"{figura.tipo}\nÁrea: {area:.2f}\nPerímetro: {perim:.2f}")
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

# Routes and views

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            num1 = float(request.form.get('num1'))
            num2 = float(request.form.get('num2'))
            num3 = float(request.form.get('num3'))
            terna = [num1, num2, num3]
            figuras_terna = procesar_terna(terna)
            if figuras_terna:
                ternas.append(terna)
                for f in figuras_terna.values():
                    figuras.append(f)
                flash(f"Terna procesada: {len(figuras_terna)} figuras generadas", "success")
            else:
                flash("No se pudieron generar figuras con esta terna", "warning")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        return redirect(url_for('index'))
    return render_template_string(TEMPLATE, ternas=ternas, figuras=figuras, plot_figura=plot_figura)

@app.route('/ordenar_area')
def ordenar_area():
    global figuras
    figuras = bubble_sort_iterative(figuras, key=lambda x: x.calcular_area())
    flash("Figuras ordenadas por área (ascendente)", "info")
    return redirect(url_for('index'))

@app.route('/ordenar_perimetro')
def ordenar_perimetro():
    global figuras
    figuras = bubble_sort_recursive(figuras, key=lambda x: x.calcular_perimetro(), reverse=True)
    flash("Figuras ordenadas por perímetro (descendente)", "info")
    return redirect(url_for('index'))

@app.route('/buscar_area', methods=['GET', 'POST'])
def buscar_area():
    if request.method == 'POST':
        try:
            area_buscar = float(request.form.get('area'))
            figuras_ordenadas = bubble_sort_iterative(figuras, key=lambda x: x.calcular_area())
            areas_ordenadas = [f.calcular_area() for f in figuras_ordenadas]
            # Búsqueda binaria
            izquierda, derecha = 0, len(areas_ordenadas) - 1
            indice = -1
            while izquierda <= derecha:
                medio = (izquierda + derecha) // 2
                if abs(areas_ordenadas[medio] - area_buscar) < 0.001:
                    indice = medio
                    break
                elif areas_ordenadas[medio] < area_buscar:
                    izquierda = medio + 1
                else:
                    derecha = medio - 1
            if indice == -1:
                flash(f"No se encontró figura con área aproximada a {area_buscar}", "warning")
            else:
                figura = figuras_ordenadas[indice]
                flash(f"Figura encontrada: {figura.tipo} con área {figura.calcular_area():.2f}", "success")
        except Exception as e:
            flash(f"Error en búsqueda: {e}", "danger")
        return redirect(url_for('index'))
    return render_template_string(SEARCH_TEMPLATE)

@app.route('/estadisticas')
def estadisticas():
    if not figuras:
        flash("No hay figuras para mostrar estadísticas", "warning")
        return redirect(url_for('index'))
    total_ternas = len(ternas)
    ternas_tres_iguales = sum(1 for t in ternas if len(set(t)) == 1)
    ternas_dos_iguales = sum(1 for t in ternas if len(set(t)) == 2)
    total_figuras = len(figuras)
    tipos_figura = {}
    for f in figuras:
        tipos_figura[f.tipo] = tipos_figura.get(f.tipo, 0) + 1
    areas = [f.calcular_area() for f in figuras]
    perimetros = [f.calcular_perimetro() for f in figuras]
    promedio_areas = sum(areas) / len(areas) if areas else 0
    mediana_perimetros = statistics.median(perimetros) if perimetros else 0
    return render_template_string(STATS_TEMPLATE,
                                  total_ternas=total_ternas,
                                  ternas_tres_iguales=ternas_tres_iguales,
                                  ternas_dos_iguales=ternas_dos_iguales,
                                  total_figuras=total_figuras,
                                  tipos_figura=tipos_figura,
                                  promedio_areas=promedio_areas,
                                  mediana_perimetros=mediana_perimetros)

# HTML Templates

TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Sistema de Figuras Geométricas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-4">
    <h1 class="mb-4">Sistema de Procesamiento de Figuras Geométricas</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert alert-{{category}} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    <form method="post" class="row g-3 mb-4">
        <div class="col-auto">
            <input type="number" step="any" name="num1" class="form-control" placeholder="Número 1" required>
        </div>
        <div class="col-auto">
            <input type="number" step="any" name="num2" class="form-control" placeholder="Número 2" required>
        </div>
        <div class="col-auto">
            <input type="number" step="any" name="num3" class="form-control" placeholder="Número 3" required>
        </div>
        <div class="col-auto">
            <button type="submit" class="btn btn-primary mb-3">Agregar Terna</button>
        </div>
    </form>
    <div class="mb-3">
        <a href="{{ url_for('ordenar_area') }}" class="btn btn-success me-2">Ordenar por Área (Iterativo)</a>
        <a href="{{ url_for('ordenar_perimetro') }}" class="btn btn-warning me-2">Ordenar por Perímetro (Recursivo)</a>
        <a href="{{ url_for('buscar_area') }}" class="btn btn-info me-2">Buscar por Área</a>
        <a href="{{ url_for('estadisticas') }}" class="btn btn-secondary">Ver Estadísticas</a>
    </div>
    <h2>Figuras Generadas</h2>
    {% if figuras %}
    <div class="row row-cols-1 row-cols-md-3 g-4">
        {% for figura in figuras %}
        <div class="col">
            <div class="card h-100">
                <img src="data:image/png;base64,{{ plot_figura(figura) }}" class="card-img-top" alt="{{ figura.tipo }}">
                <div class="card-body">
                    <h5 class="card-title">{{ figura.tipo }}</h5>
                    <p class="card-text">
                        Área: {{ "%.2f"|format(figura.calcular_area()) }}<br>
                        Perímetro: {{ "%.2f"|format(figura.calcular_perimetro()) }}<br>
                        {% if figura.tipo == "Cuadrado" %}
                            Lado: {{ "%.2f"|format(figura.lado) }}
                        {% elif figura.tipo == "Círculo" %}
                            Radio: {{ "%.2f"|format(figura.radio) }}
                        {% elif figura.tipo == "Rectángulo" %}
                            Lados: {{ "%.2f"|format(figura.lado1) }} x {{ "%.2f"|format(figura.lado2) }}
                        {% elif figura.tipo == "Rombo" %}
                            Diagonales: {{ "%.2f"|format(figura.diagonal1) }}, {{ "%.2f"|format(figura.diagonal2) }}
                        {% elif figura.tipo == "Triángulo Escaleno" %}
                            Lados: {{ "%.2f"|format(figura.lado1) }}, {{ "%.2f"|format(figura.lado2) }}, {{ "%.2f"|format(figura.lado3) }}
                        {% elif figura.tipo == "Trapecio" %}
                            Bases: {{ "%.2f"|format(figura.base_mayor) }}, {{ "%.2f"|format(figura.base_menor) }}<br>
                            Lados: {{ "%.2f"|format(figura.lado1) }}, {{ "%.2f"|format(figura.lado2) }}
                        {% endif %}
                    </p>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p>No hay figuras generadas aún.</p>
    {% endif %}
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

SEARCH_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Buscar por Área</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-4">
    <h1>Buscar Figura por Área</h1>
    <form method="post" class="mb-3">
        <div class="mb-3">
            <label for="area" class="form-label">Área a buscar:</label>
            <input type="number" step="any" name="area" id="area" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">Buscar</button>
        <a href="{{ url_for('index') }}" class="btn btn-secondary">Volver</a>
    </form>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

STATS_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estadísticas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-4">
    <h1>Estadísticas de Figuras</h1>
    <ul class="list-group mb-3">
        <li class="list-group-item">Total de ternas procesadas: {{ total_ternas }}</li>
        <li class="list-group-item">Ternas con tres números iguales: {{ ternas_tres_iguales }}</li>
        <li class="list-group-item">Ternas con dos números iguales: {{ ternas_dos_iguales }}</li>
        <li class="list-group-item">Ternas con tres números diferentes: {{ total_ternas - ternas_tres_iguales - ternas_dos_iguales }}</li>
        <li class="list-group-item">Total de figuras generadas: {{ total_figuras }}</li>
    </ul>
    <h2>Figuras por Tipo</h2>
    <ul class="list-group mb-3">
        {% for tipo, cantidad in tipos_figura.items() %}
        <li class="list-group-item d-flex justify-content-between align-items-center">
            {{ tipo }}
            <span class="badge bg-primary rounded-pill">{{ cantidad }}</span>
        </li>
        {% endfor %}
    </ul>
    <ul class="list-group mb-3">
        <li class="list-group-item">Promedio de áreas: {{ "%.2f"|format(promedio_areas) }}</li>
        <li class="list-group-item">Mediana de perímetros: {{ "%.2f"|format(mediana_perimetros) }}</li>
    </ul>
    <a href="{{ url_for('index') }}" class="btn btn-secondary">Volver</a>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
