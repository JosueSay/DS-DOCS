# 📘 **Guía Práctica de Teledetección: NDVI y NDWI en el Lago de Atitlán usando Sentinel-2**

## 🛰️ **1. ¿Qué vamos a hacer?**

Vamos a conectarnos a un servidor que ofrece datos satelitales (Copernicus OpenEO), descargar imágenes del **Lago de Atitlán** en Guatemala y calcular **índices de vegetación (NDVI)** y **agua (NDWI)** para analizar el estado del área.

## 🧰 **2. Librerías utilizadas**

```python
import rasterio           # Para trabajar con imágenes raster
import numpy as np        # Para cálculos numéricos y matrices
import matplotlib.pyplot as plt  # Para visualizar resultados
import openeo             # Para conectarse al servidor de datos
```

## 🔐 **3. Conexión al servidor OpenEO**

```python
connection = openeo.connect("https://openeo.dataspace.copernicus.eu").authenticate_oidc()
```

> Esto permite acceder a imágenes satelitales del programa **Copernicus** de forma gratuita y segura.

## 🗺️ **4. Definir la zona de estudio**

```python
lago_atitlan = {
    "west": -91.31,
    "east": -91.08,
    "south": 14.60,
    "north": 14.74
}
```

> Estas coordenadas definen un **cuadro geográfico** sobre el Lago de Atitlán. También podrías cambiarlo para analizar otra zona (como Amatitlán).

## 📦 **5. Cargar la colección de imágenes (Sentinel-2)**

```python
atitlan_cube = connection.load_collection(
    "SENTINEL2_L2A",
    spatial_extent=lago_atitlan,
    temporal_extent=["2025-08-01", "2025-08-03"],
    bands=["B02", "B03", "B04", "B08"]
)
```

> Aquí indicamos **qué sensor usar (Sentinel-2)**, **la fecha** de observación y **las bandas** necesarias:

* **B02**: Azul
* **B03**: Verde
* **B04**: Rojo
* **B08**: Infrarrojo cercano (NIR)

Estas bandas son las más usadas para detectar **vegetación y agua**.

## 💾 **6. Descargar la imagen**

```python
result_graph = atitlan_cube.save_result(format="GTIFF")
job = connection.create_job(result_graph)
job.start_and_wait()
job.download_results("../data/GIS/Bandas_Atitlan.tif")
```

> Se guarda como un archivo `.tif`, un formato común para imágenes satelitales georreferenciadas.

## 🖼️ **7. Visualizar bandas individuales**

```python
with rasterio.open(ruta_tif) as src:
    bandas = src.read()
    nombres = src.descriptions if src.descriptions[0] else [f"Banda {i+1}" for i in range(src.count)]
    nodata = src.nodata
```

> Se abre la imagen y se obtienen las bandas cargadas.

### Luego, se visualiza cada banda

```python
for i in range(bandas.shape[0]):
    ...
```

> Esto permite **ver cómo se ve cada banda**, como si fuera una "foto" en blanco y negro.

## 🌈 **8. Composición en falso color**

¿Por qué falso color? Porque el ojo humano no ve el **infrarrojo**, pero al asignarlo a un canal visible, se pueden resaltar zonas con vegetación más fácilmente.

### Normalizar bandas

```python
def normalize(b):
    b_min, b_max = np.percentile(b[b > 0], (2, 98))
    return np.clip((b - b_min) / (b_max - b_min), 0, 1)
```

> Esto convierte los valores de reflectancia a un rango de 0 a 1, para que se vean mejor al graficarlos.

### Composición RGB

```python
rgb = np.dstack([r, g, b])
```

> Se arma una imagen apilando 3 bandas. En este caso, se hace una **composición en color real (true color)** con las bandas azul, verde y roja.

## 🌿 **9. Cálculo del NDVI**

### ¿Qué es NDVI?

$$
\text{NDVI} = \frac{B8 - B4}{B8 + B4}
$$

* **B8 (NIR)**: refleja más la vegetación sana.
* **B4 (Red)**: la vegetación la absorbe.

> Cuanto mayor sea la diferencia entre NIR y Red, mayor será el valor de NDVI.

```python
ndvi_atitlan = np.where(
    (nir_scale + red_scale) == 0,
    0,
    (nir_scale - red_scale) / (nir_scale + red_scale)
)
```

### ¿Para qué sirve?

Detecta:

* Cultivos sanos.
* Deforestación.
* Zonas sin vegetación (NDVI cercano a 0).
* Agua o sombra (NDVI negativo).

### Interpretación

| NDVI          | Interpretación                         |
| ------------- | -------------------------------------- |
| **0.6 a 1.0** | Vegetación muy densa y sana            |
| **0.4 a 0.6** | Vegetación saludable                   |
| **0.2 a 0.4** | Vegetación escasa o en estrés          |
| **0.0 a 0.2** | Suelo desnudo                          |
| **< 0.0**     | Agua, nubes o superficies artificiales |

## 💧 **10. Cálculo del NDWI**

### ¿Qué es NDWI?

$$
\text{NDWI} = \frac{B3 - B8}{B3 + B8}
$$

* **B3 (Green)**: el agua refleja más aquí.
* **B8 (NIR)**: el agua refleja poco.

> Este índice resalta cuerpos de agua como lagos, ríos o zonas inundadas.

```python
ndwi_atitlan = np.where(
    (green_scale + nir_scale) == 0,
    0,
    (green_scale - nir_scale) / (green_scale + nir_scale)
)
```

### Interpretación

| NDWI        | Interpretación                       |
| ----------- | ------------------------------------ |
| **> 0.2**   | Agua o zonas húmedas                 |
| **0 a 0.2** | Suelo húmedo o vegetación poco densa |
| **< 0**     | Vegetación o suelo seco              |

## 📊 **11. Visualización de resultados**

Ambos índices se visualizan con `matplotlib`, usando paletas de colores para facilitar su interpretación:

* **NDVI**: verde (vegetación).
* **NDWI**: azul-marrón (agua vs tierra seca).

## ✅ Conclusión

Este análisis permite:

* Detectar **vegetación saludable** alrededor del lago.
* Identificar **presencia o ausencia de cuerpos de agua**.
* Monitorear el cambio de **condiciones ambientales** con el tiempo.
