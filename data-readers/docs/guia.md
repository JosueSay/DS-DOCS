# 📘 Guía: Análisis de Importación de Vehículos desde el Portal SAT

En la página del **[Portal SAT - Importación de Vehículos](https://www.sat.gob.gt)** se encuentran disponibles los datos mensuales de importación de vehículos por año en formato `.zip`.

## 🎯 Objetivo

Automatizar la descarga, procesamiento y análisis de los datos de importación de vehículos correspondientes a:

- Todo el año **2024** (12 meses).
- Los primeros **5 meses de 2025**.

## 🧩 Parte 1: Automatización de Descarga y Preparación de Datos

### 🛠️ Script Automatizado

El script deberá realizar lo siguiente:

1. **Descargar automáticamente** los archivos `.zip` desde el sitio del SAT correspondientes a cada mes del 2024 y hasta mayo de 2025.
2. **Descomprimir** los archivos descargados.
3. **Guardar los archivos de texto** descomprimidos en una carpeta llamada `Datos`.
4. **Leer** todos los archivos de texto para crear un **conjunto de datos unificado** con información de los:
   - 12 meses de 2024
   - 5 meses de 2025
5. **Guardar** el conjunto de datos final como un archivo `.csv`.

## 🔍 Parte 2: Exploración de Datos

Una vez generado el `data.frame` unificado, se debe realizar una pequeña exploración con base en las siguientes preguntas:

### 📊 Análisis para el año 2024

- ¿Cuántos **vehículos livianos** de **cada tipo** se importaron en 2024?
- ¿Cuál es la **distribución de modelos** de **carros**, **pickups** y **SUV** importados en ese año?
- ¿Cuál es el **tipo de vehículo** que más se importó durante el 2024?
- ¿Cuáles fueron los **meses con mayor importación** de vehículos livianos?

### 📈 Comparativo 2024 vs 2025 (hasta mayo)

- ¿Cómo vamos con la importación de **cada tipo de vehículo** en los primeros meses de 2025 comparado con los mismos meses de 2024?

## 📝 Recomendaciones

- Asegúrate de tener una conexión estable para descargar múltiples archivos.
- Utiliza librerías como `requests`, `zipfile`, `pandas`, `os`, y `glob` para automatizar el flujo.
- Guarda todos los datos intermedios y resultados finales en carpetas bien organizadas.

## 📂 Estructura Sugerida de Carpetas

```bash
pendiente
```
