from django.shortcuts import render

# Create your views here.
def ejercicios(request):

    formulas = [
            {
                "name": "Integral Definida",
                "description": "Cálculo del área bajo una curva en un intervalo cerrado",
                "latex": r"\int_{a}^{b} f(x) \, dx = F(b) - F(a)",
                "category": "Cálculo Integral"
            },
            {
                "name": "Serie de Taylor",
                "description": "Representación de una función como suma infinita de términos",
                "latex": r"f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n",
                "category": "Análisis Matemático"
            },
            {
                "name": "Derivada del Producto",
                "description": "Regla para derivar el producto de dos funciones",
                "latex": r"\frac{d}{dx}[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)",
                "category": "Cálculo Diferencial"
            },
            {
                "name": "Determinante de Matriz 3x3",
                "description": "Cálculo del determinante de una matriz de orden 3",
                "latex": r"\det(A) = \begin{vmatrix} a_{11} & a_{12} & a_{13} \\ a_{21} & a_{22} & a_{23} \\ a_{31} & a_{32} & a_{33} \end{vmatrix} = a_{11}(a_{22}a_{33} - a_{23}a_{32}) - a_{12}(a_{21}a_{33} - a_{23}a_{31}) + a_{13}(a_{21}a_{32} - a_{22}a_{31})",
                "category": "Álgebra Lineal"
            },
            {
                "name": "Fórmula Cuadrática",
                "description": "Solución de ecuaciones cuadráticas de segundo grado",
                "latex": r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
                "category": "Álgebra"
            },
            {
                "name": "Producto Escalar de Vectores",
                "description": "Producto interno entre dos vectores en el espacio (Para R^3)",
                "latex": r"\vec{u} \cdot \vec{v} = |\vec{u}||\vec{v}|\cos\theta = u_1v_1 + u_2v_2 + u_3v_3",
                "category": "Álgebra Lineal"
            },
            {
                "name": "Límite Fundamental",
                "description": "Número de Euler por definición",
                "latex": r"\lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n = e",
                "category": "Análisis Matemático"
            },
            {
                "name": "Transformada de Laplace",
                "description": "Transformada integral para resolver ecuaciones diferenciales",
                "latex": r"\mathcal{L}\{f(t)\} = F(s) = \int_{0}^{\infty} f(t)e^{-st} \, dt",
                "category": "Ecuaciones Diferenciales"
            },
            {
                "name": "Eigenvalores y Eigenvectores",
                "description": "Ecuación característica para encontrar valores y vectores propios",
                "latex": r"A\vec{v} = \lambda\vec{v} \quad \Rightarrow \quad \det(A - \lambda I) = 0",
                "category": "Álgebra Lineal"
            },
            {
                "name": "Teorema Fundamental del Cálculo",
                "description": "Conexión entre derivación e integración",
                "latex": r"\frac{d}{dx}\int_{a}^{x} f(t) \, dt = f(x)",
                "category": "Cálculo Integral"
            },
            {
                "name": "Regla de la Cadena",
                "description": "Derivada de una función compuesta",
                "latex": r"\frac{d}{dx}[f(g(x))] = f'(g(x))g'(x)",
                "category": "Cálculo Diferencial"
            },
            {
                "name": "Regla de la Potencia",
                "description": "Derivada de un polinomio",
                "latex": r"\frac{d}{dx}[x^n] = nx^{n-1}",
                "category": "Cálculo Diferencial"
            }            
        ]
    
    contexto = {
        'formulas': formulas
    }

    return render(request, 'ejercicios.html', contexto)