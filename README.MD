# olympic-games-datamart

Desarrollo de datamart sobre como la calidad de vida afecta el rendimiento atlético de cada país en los juegos olimpicos. **UNAP IN 2024.**

Disponible en <https://datamart-data.streamlit.app/>

## Instalación

Instala las dependencias del proyecto con pip:

```shell
pip install -r requirements.txt
```

## Uso

```shell
streamlit run app.py
```

## Estructura

- `app.py`: Este es el punto de entrada principal de la aplicación.
- `charts/`: Este directorio contiene scripts para generar varios gráficos:
  - `hdi.py`: Genera gráficos relacionados con el Índice de Desarrollo Humano.
  - `income.py`: Genera gráficos relacionados con los ingresos.
  - `olympics.py`: Genera gráficos relacionados con los Juegos Olímpicos.
  - `schooling.py`: Genera gráficos relacionados con la educación.
- `datasets/`: Este directorio contiene varios conjuntos de datos CSV utilizados en el proyecto.
- `descriptors/`: Este directorio contiene archivos de descriptor.
- `*.ipynb`: Estos son cuadernos Jupyter utilizados para el análisis y exploración de datos.
- `statistics_calc.py`: Este script contiene varios cálculos estadísticos utilizados en el proyecto.
