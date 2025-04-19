#Temática 2. Calcular perímetro y áreas de figuras planas

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import numpy as np
import statistics
import random
from abc import ABC, abstractmethod


# CLASES DE FIGURAS GEOMÉTRICAS 

class Figura(ABC):
    """Clase base abstracta para todas las figuras geométricas"""
    
    def __init__(self, tipo):
        self.tipo = tipo
    
    @abstractmethod
    def calcular_area(self):
        pass
    
    @abstractmethod
    def calcular_perimetro(self):
        pass
    
    @abstractmethod
    def dibujar(self, ax):
        pass


class Cuadrado(Figura):
    """Clase que representa un cuadrado con lado igual"""
    
    def __init__(self, lado):
        super().__init__("Cuadrado")
        self.lado = lado
    
    def calcular_area(self):
        return self.lado ** 2
    
    def calcular_perimetro(self):
        return 4 * self.lado
    
    def dibujar(self, ax):
        # Dibuja un cuadrado centrado en el origen
        x = [-self.lado/2, self.lado/2, self.lado/2, -self.lado/2, -self.lado/2]
        y = [-self.lado/2, -self.lado/2, self.lado/2, self.lado/2, -self.lado/2]
        ax.plot(x, y, 'b-')
        ax.set_title(f"Cuadrado (lado = {self.lado})")
        ax.text(0, 0, f"Área: {self.calcular_area():.2f}\nPerímetro: {self.calcular_perimetro():.2f}", 
                ha='center', va='center')


class Circulo(Figura):
    """Clase que representa un círculo con radio dado"""
    
    def __init__(self, radio):
        super().__init__("Círculo")
        self.radio = radio
    
    def calcular_area(self):
        return math.pi * (self.radio ** 2)
    
    def calcular_perimetro(self):
        return 2 * math.pi * self.radio
    
    def dibujar(self, ax):
        # Dibuja un círculo centrado en el origen
        circle = plt.Circle((0, 0), self.radio, fill=False, color='r')
        ax.add_patch(circle)
        ax.set_title(f"Círculo (radio = {self.radio})")
        ax.text(0, 0, f"Área: {self.calcular_area():.2f}\nPerímetro: {self.calcular_perimetro():.2f}", 
                ha='center', va='center')


class Rectangulo(Figura):
    """Clase que representa un rectángulo con dos lados iguales y uno diferente"""
    
    def __init__(self, lado1, lado2):
        super().__init__("Rectángulo")
        self.lado1 = lado1
        self.lado2 = lado2
    
    def calcular_area(self):
        return self.lado1 * self.lado2
    
    def calcular_perimetro(self):
        return 2 * (self.lado1 + self.lado2)
    
    def dibujar(self, ax):
        # Dibuja un rectángulo centrado en el origen
        width, height = self.lado1, self.lado2
        x = [-width/2, width/2, width/2, -width/2, -width/2]
        y = [-height/2, -height/2, height/2, height/2, -height/2]
        ax.plot(x, y, 'g-')
        ax.set_title(f"Rectángulo ({self.lado1} x {self.lado2})")
        ax.text(0, 0, f"Área: {self.calcular_area():.2f}\nPerímetro: {self.calcular_perimetro():.2f}", 
                ha='center', va='center')


class Rombo(Figura):
    """Clase que representa un rombo con diagonales dadas"""
    
    def __init__(self, diagonal1, diagonal2):
        super().__init__("Rombo")
        self.diagonal1 = diagonal1
        self.diagonal2 = diagonal2
        # Calculamos el lado del rombo usando el teorema de Pitágoras
        self.lado = math.sqrt((self.diagonal1/2)**2 + (self.diagonal2/2)**2)
    
    def calcular_area(self):
        return (self.diagonal1 * self.diagonal2) / 2
    
    def calcular_perimetro(self):
        return 4 * self.lado
    
    def dibujar(self, ax):
        # Dibuja un rombo centrado en el origen
        x = [self.diagonal1/2, 0, -self.diagonal1/2, 0, self.diagonal1/2]
        y = [0, self.diagonal2/2, 0, -self.diagonal2/2, 0]
        ax.plot(x, y, 'm-')
        ax.set_title(f"Rombo (diagonales = {self.diagonal1}, {self.diagonal2})")
        ax.text(0, 0, f"Área: {self.calcular_area():.2f}\nPerímetro: {self.calcular_perimetro():.2f}", 
                ha='center', va='center')


class TrianguloEscaleno(Figura):
    """Clase que representa un triángulo escaleno con tres lados diferentes"""
    
    def __init__(self, lado1, lado2, lado3):
        super().__init__("Triángulo Escaleno")
        # Verificar si es un triángulo válido
        if lado1 + lado2 <= lado3 or lado1 + lado3 <= lado2 or lado2 + lado3 <= lado1:
            raise ValueError("Los lados no pueden formar un triángulo válido")
        self.lado1 = lado1
        self.lado2 = lado2
        self.lado3 = lado3
    
    def calcular_area(self):
        # Fórmula de Herón
        s = (self.lado1 + self.lado2 + self.lado3) / 2
        return math.sqrt(s * (s - self.lado1) * (s - self.lado2) * (s - self.lado3))
    
    def calcular_perimetro(self):
        return self.lado1 + self.lado2 + self.lado3
    
    def dibujar(self, ax):
        # Calcular coordenadas para el triángulo usando la ley de cosenos
        # Suponemos que el primer vértice está en el origen
        x1, y1 = 0, 0
        x2, y2 = self.lado1, 0
        
        # Calcular ángulo usando la ley de cosenos
        cos_angle = (self.lado1**2 + self.lado2**2 - self.lado3**2) / (2 * self.lado1 * self.lado2)
        sin_angle = math.sqrt(1 - cos_angle**2)
        
        # Tercer vértice
        x3 = self.lado2 * cos_angle
        y3 = self.lado2 * sin_angle
        
        # Centrar en el origen
        cx = (x1 + x2 + x3) / 3
        cy = (y1 + y2 + y3) / 3
        
        x1, x2, x3 = x1 - cx, x2 - cx, x3 - cx
        y1, y2, y3 = y1 - cy, y2 - cy, y3 - cy
        
        # Dibujar el triángulo
        x = [x1, x2, x3, x1]
        y = [y1, y2, y3, y1]
        ax.plot(x, y, 'c-')
        ax.set_title(f"Triángulo Escaleno ({self.lado1}, {self.lado2}, {self.lado3})")
        ax.text((x1 + x2 + x3)/3, (y1 + y2 + y3)/3, 
                f"Área: {self.calcular_area():.2f}\nPerímetro: {self.calcular_perimetro():.2f}", 
                ha='center', va='center')


class Trapecio(Figura):
    """Clase que representa un trapecio con lados dados"""
    
    def __init__(self, base_mayor, base_menor, lado1, lado2):
        super().__init__("Trapecio")
        self.base_mayor = base_mayor
        self.base_menor = base_menor
        self.lado1 = lado1
        self.lado2 = lado2
        # Calcular altura usando fórmula especial para trapecios
        s = (base_mayor - base_menor) / 2
        # Verificamos que los lados sean lo suficientemente largos para formar el trapecio
        if s > lado1 or s > lado2:
            raise ValueError("Los lados no pueden formar un trapecio válido")
        self.altura = math.sqrt(lado1**2 - s**2)
    
    def calcular_area(self):
        return ((self.base_mayor + self.base_menor) / 2) * self.altura
    
    def calcular_perimetro(self):
        return self.base_mayor + self.base_menor + self.lado1 + self.lado2
    
    def dibujar(self, ax):
        # Calcular coordenadas para el trapecio
        x = [-self.base_mayor/2, self.base_mayor/2, self.base_menor/2, -self.base_menor/2, -self.base_mayor/2]
        y = [-self.altura/2, -self.altura/2, self.altura/2, self.altura/2, -self.altura/2]
        
        ax.plot(x, y, 'y-')
        ax.set_title(f"Trapecio ({self.base_mayor}, {self.base_menor}, {self.lado1}, {self.lado2})")
        ax.text(0, 0, f"Área: {self.calcular_area():.2f}\nPerímetro: {self.calcular_perimetro():.2f}", 
                ha='center', va='center')


# ALGORITMOS DE ORDENAMIENTO Y BÚSQUEDA 

def bubble_sort(arr, key=lambda x: x, reverse=False, metodo='iterativo'):
    comparaciones = 0
    intercambios = 0

    def bubble_sort_iterativo(arr):
        nonlocal comparaciones, intercambios
        n = len(arr)
        resultado = arr.copy()
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                comparaciones += 1
                condicion = key(resultado[j]) > key(resultado[j + 1])
                if reverse:
                    condicion = not condicion
                if condicion:
                    resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
                    swapped = True
                    intercambios += 1
            if not swapped:
                break
        return resultado

    def bubble_sort_recursivo(arr, n):
        nonlocal comparaciones, intercambios
        if n == 1:
            return arr
        for i in range(n - 1):
            comparaciones += 1
            condicion = key(arr[i]) > key(arr[i + 1])
            if reverse:
                condicion = not condicion
            if condicion:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                intercambios += 1
        return bubble_sort_recursivo(arr, n - 1)

    # Lógica para elegir método
    resultado = arr.copy()
    if metodo == 'iterativo':
        resultado = bubble_sort_iterativo(resultado)
        print(f"Bubble Sort (Iterativo): {comparaciones} comparaciones, {intercambios} intercambios")
    elif metodo == 'recursivo':
        resultado = bubble_sort_recursivo(resultado, len(resultado))
        print(f"Bubble Sort (Recursivo): {comparaciones} comparaciones, {intercambios} intercambios")
    else:
        raise ValueError("Método inválido. Usa 'iterativo' o 'recursivo'.")

    return resultado



def busqueda_lineal(arr, valor, key=lambda x: x):
    comparaciones = 0
    for i, item in enumerate(arr):
        comparaciones += 1
        if abs(key(item) - valor) < 0.001:  # Comparación con tolerancia para valores flotantes
            print(f"Búsqueda Lineal: {comparaciones} comparaciones")
            return i
    
    print(f"Búsqueda Lineal: {comparaciones} comparaciones")
    return -1


def busqueda_binaria(arr, valor, key=lambda x: x):
    izquierda, derecha = 0, len(arr) - 1
    comparaciones = 0
    
    while izquierda <= derecha:
        comparaciones += 1
        medio = (izquierda + derecha) // 2
        valor_medio = key(arr[medio])
        
        # Comparación con tolerancia para valores flotantes
        if abs(valor_medio - valor) < 0.001:
            print(f"Búsqueda Binaria: {comparaciones} comparaciones")
            return medio
        elif valor_medio < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1  
    
    print(f"Búsqueda Binaria: {comparaciones} comparaciones")
    return -1


# FUNCIONES DE PROCESAMIENTO DE TERNAS 

def procesar_terna(terna):
    # Ordenamos la terna para facilitar el análisis
    terna_ordenada = sorted(terna)
    
    figuras = {}
    
    # Caso 1: Tres números iguales -> Cuadrado y Círculo
    if terna_ordenada[0] == terna_ordenada[1] == terna_ordenada[2]:
        lado = terna_ordenada[0]
        try:
            cuadrado = Cuadrado(lado)
            figuras["cuadrado"] = cuadrado
        except Exception as e:
            print(f"Error al crear cuadrado: {e}")
        
        try:
            circulo = Circulo(lado)
            figuras["circulo"] = circulo
        except Exception as e:
            print(f"Error al crear círculo: {e}")
    
    # Caso 2: Dos números iguales -> Rectángulo y Rombo
    elif terna_ordenada[0] == terna_ordenada[1] or terna_ordenada[1] == terna_ordenada[2]:
        if terna_ordenada[0] == terna_ordenada[1]:
            lado_igual = terna_ordenada[0]
            lado_distinto = terna_ordenada[2]
        else:
            lado_igual = terna_ordenada[1]
            lado_distinto = terna_ordenada[0]
        
        try:
            rectangulo = Rectangulo(lado_igual, lado_distinto)
            figuras["rectangulo"] = rectangulo
        except Exception as e:
            print(f"Error al crear rectángulo: {e}")
        
        try:
            rombo = Rombo(lado_igual, lado_distinto)
            figuras["rombo"] = rombo
        except Exception as e:
            print(f"Error al crear rombo: {e}")
    
    # Caso 3: Tres números diferentes -> Triángulo Escaleno y Trapecio
    else:
        # Verificar si los lados pueden formar un triángulo
        try:
            triangulo = TrianguloEscaleno(terna_ordenada[0], terna_ordenada[1], terna_ordenada[2])
            figuras["triangulo"] = triangulo
        except ValueError as e:
            print(f"Error al crear triángulo: {e}")
        
        # Para el trapecio, usamos los tres valores como base_mayor, base_menor y lados
        base_mayor = max(terna)
        base_menor = min(terna)
        # El tercer valor lo usamos como lado1 y calculamos lado2
        lado_medio = sum(terna) - base_mayor - base_menor
        
        # Calculamos lado2 para que el trapecio sea válido
        delta = (base_mayor - base_menor) / 2
        lado2 = math.sqrt(lado_medio**2 - delta**2)
        
        try:
            trapecio = Trapecio(base_mayor, base_menor, lado_medio, lado2)
            figuras["trapecio"] = trapecio
        except ValueError as e:
            print(f"Error al crear trapecio: {e}")
    
    return figuras


def generar_datos_prueba():
    ternas = [
        # Tres números iguales
        [5, 5, 5],
        [10, 10, 10],
        # Dos números iguales
        [4, 4, 8],
        [7, 3, 7],
        # Tres números diferentes válidos para un triángulo
        [3, 4, 5],
        [7, 9, 12],
        # Ternas adicionales
        [6, 6, 6],
        [8, 8, 12],
        [5, 7, 10]
    ]
    return ternas


# APLICACIÓN PRINCIPAL 

class SistemaFigurasApp:
    """Clase principal que implementa la interfaz gráfica del sistema"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Procesamiento de Figuras Geométricas")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Inicializar variables
        self.ternas = []
        self.figuras = []
        self.terna_actual = []
        
        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="black")
        self.style.configure("TLabel", background="#f0f0f0", font=('Arial', 12))
        self.style.configure("Header.TLabel", font=('Arial', 14, 'bold'))
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Cargar datos de prueba
        self.cargar_datos_prueba()
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica del sistema"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame superior para entrada de datos
        input_frame = ttk.Frame(main_frame, padding="10", style="TFrame")
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Sistema de Procesamiento de Figuras Geométricas", 
                 style="Header.TLabel").pack(pady=5)
        
        # Frame para ingresar ternas
        terna_frame = ttk.Frame(input_frame, padding="5")
        terna_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(terna_frame, text="Ingrese números para la terna:").pack(side=tk.LEFT, padx=5)
        
        self.num_entry = ttk.Entry(terna_frame, width=10)
        self.num_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(terna_frame, text="Agregar Número", command=self.agregar_numero).pack(side=tk.LEFT, padx=5)
        ttk.Button(terna_frame, text="Completar Terna", command=self.completar_terna).pack(side=tk.LEFT, padx=5)
        
        # Frame para mostrar la terna actual
        self.terna_actual_var = tk.StringVar(value="Terna actual: []")
        ttk.Label(input_frame, textvariable=self.terna_actual_var).pack(pady=7)
        
        # Frame para botones de acción
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Ver Estadísticas", command=self.mostrar_estadisticas).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ordenar por Área (Asc)", command=self.ordenar_por_area).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ordenar por Perímetro (Desc)", command=self.ordenar_por_perimetro).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Buscar por Área", command=self.buscar_por_area).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Mostrar Todas las Figuras", command=self.mostrar_todas_figuras).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Datos de Prueba", command=self.cargar_datos_prueba).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salir", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        # Crear paneles para mostrar información y gráficas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Panel de visualización de figuras
        self.visualizacion_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.visualizacion_frame, text="Visualización")
        
        # Panel de listado de figuras
        self.listado_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.listado_frame, text="Listado de Figuras")
        
        # Panel de estadísticas
        self.estadisticas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.estadisticas_frame, text="Estadísticas")
        
        # Crear Treeview para listado de figuras
        self.crear_tabla_figuras()
    
    def crear_tabla_figuras(self):
        """Crea la tabla para mostrar el listado de figuras"""
        columns = ('id', 'tipo', 'area', 'perimetro', 'detalles')
        self.tabla_figuras = ttk.Treeview(self.listado_frame, columns=columns, show='headings')
        
        # Definir encabezados
        self.tabla_figuras.heading('id', text='ID')
        self.tabla_figuras.heading('tipo', text='Tipo de Figura')
        self.tabla_figuras.heading('area', text='Área')
        self.tabla_figuras.heading('perimetro', text='Perímetro')
        self.tabla_figuras.heading('detalles', text='Detalles')
        
        # Definir ancho de columnas
        self.tabla_figuras.column('id', width=50, anchor=tk.CENTER)
        self.tabla_figuras.column('tipo', width=150)
        self.tabla_figuras.column('area', width=100, anchor=tk.CENTER)
        self.tabla_figuras.column('perimetro', width=100, anchor=tk.CENTER)
        self.tabla_figuras.column('detalles', width=300)
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(self.listado_frame, orient=tk.VERTICAL, command=self.tabla_figuras.yview)
        self.tabla_figuras.configure(yscroll=scrollbar.set)
        
        # Empaquetar la tabla y scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla_figuras.pack(fill=tk.BOTH, expand=True)
        
        # Agregar evento de doble clic para visualizar la figura
        self.tabla_figuras.bind("<Double-1>", self.visualizar_figura_seleccionada)
    
    def agregar_numero(self):
        """Agrega un número a la terna actual"""
        try:
            num = float(self.num_entry.get())
            if len(self.terna_actual) < 3:
                self.terna_actual.append(num)
                self.actualizar_terna_actual()
                self.num_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Información", "Ya hay 3 números en la terna. Complete la terna actual.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")
    
    def actualizar_terna_actual(self):
        """Actualiza la visualización de la terna actual"""
        self.terna_actual_var.set(f"Terna actual: {self.terna_actual}")
    
    def completar_terna(self):
        """Procesa la terna actual y genera las figuras correspondientes"""
        if len(self.terna_actual) != 3:
            messagebox.showinfo("Información", "Debe ingresar exactamente 3 números para completar una terna")
            return
        
        # Procesar la terna
        figuras_terna = procesar_terna(self.terna_actual)
        
        # Si se generaron figuras, agregarlas a la lista
        if figuras_terna:
            # Guardar la terna
            self.ternas.append(self.terna_actual.copy())
            
            # Guardar las figuras
            for figura in figuras_terna.values():
                self.figuras.append(figura)
            
            # Actualizar la tabla de figuras
            self.actualizar_tabla_figuras()
            
            # Visualizar las figuras generadas
            self.visualizar_figuras(list(figuras_terna.values()))
            
            # Limpiar la terna actual
            self.terna_actual = []
            self.actualizar_terna_actual()
            
            messagebox.showinfo("Éxito", f"Terna procesada: {len(figuras_terna)} figuras generadas")
        else:
            messagebox.showwarning("Advertencia", "No se pudieron generar figuras con esta terna")
    
    def actualizar_tabla_figuras(self):
        """Actualiza la tabla de listado de figuras"""
        # Limpiar tabla
        for item in self.tabla_figuras.get_children():
            self.tabla_figuras.delete(item)
        
        # Agregar figuras a la tabla
        for i, figura in enumerate(self.figuras):
            area = figura.calcular_area()
            perimetro = figura.calcular_perimetro()
            
            # Generar detalles según el tipo de figura
            detalles = self.generar_detalles_figura(figura)
            
            self.tabla_figuras.insert('', tk.END, values=(
                i+1, figura.tipo, f"{area:.2f}", f"{perimetro:.2f}", detalles
            ))
    
 
        
    def generar_detalles_figura(self, figura):
        """Genera una descripción detallada de la figura para mostrar en la tabla"""
        if isinstance(figura, Cuadrado):
            return f"Lado: {figura.lado:.2f}"
        elif isinstance(figura, Circulo):
            return f"Radio: {figura.radio:.2f}"
        elif isinstance(figura, Rectangulo):
            return f"Lados: {figura.lado1:.2f} x {figura.lado2:.2f}"
        elif isinstance(figura, Rombo):
            return f"Diagonales: {figura.diagonal1:.2f} y {figura.diagonal2:.2f}"
        elif isinstance(figura, TrianguloEscaleno):
            return f"Lados: {figura.lado1:.2f}, {figura.lado2:.2f}, {figura.lado3:.2f}"
        elif isinstance(figura, Trapecio):
            return f"Bases: {figura.base_mayor:.2f}, {figura.base_menor:.2f}, Lados: {figura.lado1:.2f}, {figura.lado2:.2f}"
        return ""
    
    def visualizar_figuras(self, figuras_a_mostrar=None):
        """Visualiza las figuras en el panel de visualización"""
        # Limpiar el frame de visualización
        for widget in self.visualizacion_frame.winfo_children():
            widget.destroy()
        
        if not figuras_a_mostrar:
            if not self.figuras:
                ttk.Label(self.visualizacion_frame, text="No hay figuras para visualizar").pack(pady=20)
                return
            figuras_a_mostrar = self.figuras
    
    # Crear una figura de matplotlib
        num_figuras = len(figuras_a_mostrar)
        
        # Ajustar la distribución para mostrar todas las figuras
        # Usar 4 columnas en lugar de 2
        cols = 4  # 4 figuras por fila
        filas = (num_figuras + cols - 1) // cols  # Calcular filas necesarias
        
        # Crear subplots para cada figura con un tamaño adecuado
        fig, axs = plt.subplots(filas, cols, figsize=(16, 4 * filas))
        fig.suptitle('Visualización de Figuras Geométricas', fontsize=16)
        
        # Asegurarse de que axs sea un array
        axs = np.array(axs).reshape(filas, cols)
        
        # Aplanar el array de axs para facilitar la iteración
        axs_flat = axs.flatten()
        
        # Dibujar cada figura en su subplot correspondiente
        for i, figura in enumerate(figuras_a_mostrar):
            if i < len(axs_flat):
                ax = axs_flat[i]
                # Limpiar ejes
                ax.clear()
                # Configurar límites y aspecto
                ax.set_xlim(-10, 10)
                ax.set_ylim(-10, 10)
                ax.set_aspect('equal')
                # Dibujar ejes
                ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
                ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
                # Dibujar la figura
                figura.dibujar(ax)
                
                # Añadir título al subplot con el tipo de figura
                ax.set_title(figura.tipo, fontsize=10)
                
                # Remover los ticks para una apariencia más limpia
                ax.set_xticks([])
                ax.set_yticks([])
        
        # Ocultar los ejes no utilizados
        for j in range(i + 1, len(axs_flat)):
            axs_flat[j].axis('off')
        
        # Ajustar los espacios para evitar superposiciones
        plt.tight_layout(rect=[0, 0, 1, 0.95], h_pad=2.0, w_pad=2.0)
        
        # Crear un canvas de matplotlib para Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.visualizacion_frame)
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)
        
        # Añadir una barra de desplazamiento vertical para poder ver todas las figuras
        scrollbar = ttk.Scrollbar(self.visualizacion_frame, orient='vertical')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=widget.yview)
        
        canvas.draw()
    
    def mostrar_mas_figuras(self, todas_figuras):
        """Muestra el siguiente conjunto de figuras"""
    # Implementar lógica para mostrar las siguientes figuras
    # Esta es una implementación simple - en una aplicación real
    # querrías mantener un índice de la página actual
    messagebox.showinfo("Información", "Esta función mostraría el siguiente conjunto de figuras")
    # Aquí implementarías la lógica para mostrar las siguientes 6 figuras

    def visualizar_figura_seleccionada(self, event):
        """Visualiza la figura seleccionada en la tabla"""
        seleccion = self.tabla_figuras.selection()
        if seleccion:
            idx = int(self.tabla_figuras.item(seleccion[0])['values'][0]) - 1
            if 0 <= idx < len(self.figuras):
                self.visualizar_figuras([self.figuras[idx]])
                self.notebook.select(0)  # Cambiar al panel de visualización
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas sobre las figuras procesadas"""
        # Limpiar el frame de estadísticas
        for widget in self.estadisticas_frame.winfo_children():
            widget.destroy()
        
        if not self.figuras:
            ttk.Label(self.estadisticas_frame, text="No hay datos para calcular estadísticas").pack(pady=20)
            return
        
        # Frame para las estadísticas
        stats_frame = ttk.Frame(self.estadisticas_frame, padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Total de ternas
        ttk.Label(stats_frame, text=f"Total de ternas procesadas: {len(self.ternas)}", 
                  style="Header.TLabel").pack(anchor=tk.W, pady=5)
        
        # Contar ternas con tres números iguales y dos números iguales
        ternas_tres_iguales = sum(1 for terna in self.ternas if len(set(terna)) == 1)
        ternas_dos_iguales = sum(1 for terna in self.ternas if len(set(terna)) == 2)
        
        ttk.Label(stats_frame, text=f"Ternas con tres números iguales: {ternas_tres_iguales}").pack(anchor=tk.W)
        ttk.Label(stats_frame, text=f"Ternas con dos números iguales: {ternas_dos_iguales}").pack(anchor=tk.W)
        ttk.Label(stats_frame, text=f"Ternas con tres números diferentes: {len(self.ternas) - ternas_tres_iguales - ternas_dos_iguales}").pack(anchor=tk.W)
        
        # Total de figuras
        ttk.Label(stats_frame, text=f"\nTotal de figuras generadas: {len(self.figuras)}", 
                  style="Header.TLabel").pack(anchor=tk.W, pady=5)
        
        # Contar figuras por tipo
        tipos_figura = {}
        for figura in self.figuras:
            tipo = figura.tipo
            tipos_figura[tipo] = tipos_figura.get(tipo, 0) + 1
        
        for tipo, cantidad in tipos_figura.items():
            ttk.Label(stats_frame, text=f"{tipo}: {cantidad}").pack(anchor=tk.W)
        
        # Calcular estadísticas de áreas y perímetros
        areas = [figura.calcular_area() for figura in self.figuras]
        perimetros = [figura.calcular_perimetro() for figura in self.figuras]
        
        # Promedio de áreas
        promedio_areas = sum(areas) / len(areas) if areas else 0
        ttk.Label(stats_frame, text=f"\nPromedio de áreas: {promedio_areas:.2f}", 
                  style="Header.TLabel").pack(anchor=tk.W, pady=5)
        
        # Mediana de perímetros
        mediana_perimetros = statistics.median(perimetros) if perimetros else 0
        ttk.Label(stats_frame, text=f"Mediana de perímetros: {mediana_perimetros:.2f}", 
                  style="Header.TLabel").pack(anchor=tk.W, pady=5)
        
        # Mostrar áreas ordenadas
        ttk.Label(stats_frame, text="\nÁreas ordenadas (ascendente):", 
                  style="Header.TLabel").pack(anchor=tk.W, pady=5)
        areas_ordenadas = sorted(enumerate(areas), key=lambda x: x[1])
        for idx, (i, area) in enumerate(areas_ordenadas):
            if idx < 10:  # Mostrar solo las primeras 10 para no sobrecargar la interfaz
                ttk.Label(stats_frame, text=f"{idx+1}. {self.figuras[i].tipo}: {area:.2f}").pack(anchor=tk.W)
        
        # Mostrar perímetros ordenados
        ttk.Label(stats_frame, text="\nPerímetros ordenados (descendente):", 
                  style="Header.TLabel").pack(anchor=tk.W, pady=5)
        perimetros_ordenados = sorted(enumerate(perimetros), key=lambda x: x[1], reverse=True)
        for idx, (i, perimetro) in enumerate(perimetros_ordenados):
            if idx < 10:  # Mostrar solo los primeros 10
                ttk.Label(stats_frame, text=f"{idx+1}. {self.figuras[i].tipo}: {perimetro:.2f}").pack(anchor=tk.W)
        
        # Cambiar al panel de estadísticas
        self.notebook.select(2)
    
    def ordenar_por_area(self):
        """Ordena las figuras por área en orden ascendente"""
        if not self.figuras:
            messagebox.showinfo("Información", "No hay figuras para ordenar")
            return
        
        # Usar el algoritmo de ordenamiento bubble sort
        self.figuras = bubble_sort(self.figuras, key=lambda x: x.calcular_area())
        
        # Actualizar la tabla y mostrar mensaje
        self.actualizar_tabla_figuras()
        messagebox.showinfo("Información", "Figuras ordenadas por área (ascendente)")
    
    def ordenar_por_perimetro(self):
        """Ordena las figuras por perímetro en orden descendente"""
        if not self.figuras:
            messagebox.showinfo("Información", "No hay figuras para ordenar")
            return
        
        # Usar el algoritmo de ordenamiento bubble sort
        self.figuras = bubble_sort(self.figuras, key=lambda x: x.calcular_perimetro(), reverse=True)
        
        # Actualizar la tabla y mostrar mensaje
        self.actualizar_tabla_figuras()
        messagebox.showinfo("Información", "Figuras ordenadas por perímetro (descendente)")
    
    def buscar_por_area(self):
        """Busca una figura por su área"""
        if not self.figuras:
            messagebox.showinfo("Información", "No hay figuras para buscar")
            return
        
        try:
            # Pedir al usuario el área a buscar
            area_buscar = simpledialog.askfloat("Buscar por Área", "Ingrese el área a buscar:")
            if area_buscar is None:
                return

            # Ordenar las figuras por área para poder usar búsqueda binaria
            figuras_ordenadas = bubble_sort(self.figuras, key=lambda x: x.calcular_area(), metodo='iterativo')
            figuras_ordenadas = bubble_sort(self.figuras, key=lambda x: x.calcular_area(), metodo='recursivo')
            areas_ordenadas = [figura.calcular_area() for figura in figuras_ordenadas]
            
            # Primero intentamos con búsqueda binaria (más eficiente, pero requiere lista ordenada)
            indice = busqueda_binaria(figuras_ordenadas, area_buscar, key=lambda x: x.calcular_area())
            
            if indice == -1:
                # Si no se encuentra, intentamos con búsqueda lineal (más tolerante con valores aproximados)
                indice = busqueda_lineal(self.figuras, area_buscar, key=lambda x: x.calcular_area())
            
            if indice != -1:
                figura = self.figuras[indice] if indice < len(self.figuras) else None
                if figura:
                    messagebox.showinfo("Búsqueda exitosa", 
                                        f"Figura encontrada:\nTipo: {figura.tipo}\n" + 
                                        f"Área: {figura.calcular_area():.2f}\n" + 
                                        f"Perímetro: {figura.calcular_perimetro():.2f}")
                    # Visualizar la figura encontrada
                    self.visualizar_figuras([figura])
                    # Seleccionar la figura en la tabla
                    for item in self.tabla_figuras.get_children():
                        valores = self.tabla_figuras.item(item, 'values')
                        if int(valores[0]) == indice + 1:
                            self.tabla_figuras.selection_set(item)
                            self.tabla_figuras.see(item)
                            break
                    return
            
            messagebox.showinfo("Búsqueda", f"No se encontró ninguna figura con área aproximada a {area_buscar:.2f}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {e}")
    
    def mostrar_todas_figuras(self):
        """Muestra todas las figuras en la visualización"""
        if not self.figuras:
            messagebox.showinfo("Información", "No hay figuras para mostrar")
            return
        
        self.visualizar_figuras()
        self.notebook.select(0)  # Cambiar al panel de visualización
    
    def cargar_datos_prueba(self):
        """Carga datos de prueba para demostrar el funcionamiento del sistema"""
        # Limpiar datos actuales
        self.ternas = []
        self.figuras = []
        self.terna_actual = []
        self.actualizar_terna_actual()
        
        # Generar ternas de prueba
        ternas_prueba = generar_datos_prueba()
        
        # Procesar cada terna
        for terna in ternas_prueba:
            figuras_terna = procesar_terna(terna)
            if figuras_terna:
                self.ternas.append(terna)
                for figura in figuras_terna.values():
                    self.figuras.append(figura)
        
        # Actualizar la interfaz
        self.actualizar_tabla_figuras()
        self.visualizar_figuras()
        
        messagebox.showinfo("Datos de Prueba", f"Se han cargado {len(self.ternas)} ternas y {len(self.figuras)} figuras de prueba")


# FUNCIÓN PRINCIPAL 

def main():
    """Función principal para iniciar la aplicación"""
    try:
        # Necesario para matplotlib
        import numpy as np
        
        # Crear la ventana principal
        root = tk.Tk()
        app = SistemaFigurasApp(root)
        
        # Iniciar el bucle principal
        root.mainloop()
    
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()