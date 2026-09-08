<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.md">English</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/schumann-surface/readme.png" alt="Schumann Surface" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/schumann-surface/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/schumann-surface/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT"></a>
  <a href="https://mcp-tool-shop-org.github.io/schumann-surface/"><img src="https://img.shields.io/badge/landing-page-0ea5e9" alt="Landing page"></a>
  <a href="https://huggingface.co/datasets/mcp-tool-shop/schumann-sierra-nevada"><img src="https://img.shields.io/badge/dataset-Hugging%20Face-ffcc4d" alt="Dataset"></a>
</p>

<p align="center"><a href="README.md">English</a> · <a href="README.ja.md">日本語</a> · <a href="README.zh.md">中文</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (BR)</a></p>

# schumann-surface

Resonancia de Schumann como una superficie 3D de tiempo-frecuencia con carriles de eventos y un panel de correlación cruzada honesto y con cierto retraso. Se muestra un mes de datos reales de una estación ELF, de modo que se pueda observar el ritmo diario de los relámpagos, las bandas de modo y el efecto de una tormenta geomagnética, así como lo que no hace.

Estado: v1.0.0. Octubre y junio de 2013, de la estación ELF de Sierra Nevada (Universidad de Granada), reproducido en comparación con los espectros y ajustes de modo publicados por la estación, paso a paso; los diez meses restantes del archivo original se están procesando a través de la misma cadena de procesamiento. El visor es un único archivo HTML autocontenido con cuatro modos; está disponible en [la página de inicio](https://mcp-tool-shop-org.github.io/schumann-surface/viewer/).

## Qué muestra

- **Superficie**: tiempo (un mes, columnas de 30 minutos) × frecuencia (6–25 Hz, filas de 0,125 Hz) × amplitud magnética en dB con respecto a 1 pT/√Hz. Sensores NS y EW como dos hojas apilables.
- **Bandas de modo**: frecuencia central ajustada de los modos 1–3 sobre la superficie.
- **Carriles de eventos** frente a la superficie: índice geomagnético Kp (cada 3 horas, GFZ), hora local en la estación (calculada a partir de la marca de tiempo), terremotos M6+ (USGS).
- **Panel de correlación**: correlación de Pearson r frente al retraso (±24 h) entre cualquier serie de la superficie (amplitud del modo, frecuencia del modo, potencia de la banda) y cualquier serie de eventos, con una banda nula del 95 %, cuyo tamaño de muestra efectivo se corrige para la autocorrelación en ambas series (Bartlett). Una curva dentro de la banda es un resultado nulo y se muestra como tal.

## Por qué la banda es de 6–25 Hz

La bobina de la estación es un sensor RLC con resonancia cercana a 33 Hz y calibrado por sus autores solo para 6–25 Hz. Por encima de 25 Hz, el espectro original está dominado por la resonancia del sensor, no por la cavidad, por lo que los modos 4 y superiores no se pueden resolver con este instrumento. Se necesita una estación de banda más amplia para ellos.

## Verificación (octubre de 2013, 4464 intervalos por sensor)

| Comprobar con el archivo npz publicado por la estación | NS | EW |
|---|---|---|
| Relación del espectro de amplitud, la nuestra/la de la estación, 6–25 Hz (mediana, percentil 5, percentil 95) | 1.0000 / 1.0000 / 1.0000 | 1.0000 / 1.0000 / 1.0000 |
| Fracción de saturación por intervalo, correlación | 1.000 | 1.000 |
| Frecuencia central del modo 1, diferencia de la mediana | +0,004 Hz | +0,008 Hz |
| Frecuencia central del modo 2, diferencia de la mediana | +0,000 Hz | +0,002 Hz |
| Frecuencia central del modo 3, diferencia de la mediana | -0,000 Hz | +0,001 Hz |
| Relación de la amplitud máxima del modo, mediana | 1.001 / 1.000 / 1.000 | 1.001 / 1.000 / 1.000 |

La dispersión residual de la frecuencia se debe a que las dos implementaciones de Levenberg-Marquardt (lmfit en la estación, SciPy aquí) convergen en mínimos locales diferentes para un pequeño porcentaje de intervalos; el visor enmascara los ajustes que dejan los intervalos por modo documentados.

El verificador es una puerta: sale con un valor distinto de cero a menos que al menos el 95 % de los intervalos coincidan en un plazo de 30 segundos, los percentiles 5 y 95 de la relación del espectro estén dentro de 1 ± 0,005, la diferencia de la frecuencia mediana de cada modo sea inferior a 0,02 Hz y las series de saturación tengan una correlación superior a 0,99.

## Carril de relámpagos: modelo, no medición

No existe ninguna serie global de relámpagos medida y de descarga pública para 2013 (WWLLN requiere suscripción, el archivo de Blitzortung necesita que el participante inicie sesión, la climatología LIS/OTD de la NASA está detrás de Earthdata). Por lo tanto, el visor incluye un **calendario de chimeneas** como un carril de modelo: tres gaussianas en la hora UTC para el sudeste asiático, África y América, según Whipple 1929, la curva de Carnegie (Harrison 2013) y la climatología diurna LIS/OTD (Blakeslee et al. 2014). Se etiqueta como un modelo dondequiera que se muestre. El equivalente medido también está incluido: la media por hora UTC de la amplitud de cada modo durante el mes. Consulte `docs/data-contract.md`.

## Datos y licencias

| Fuente | Qué | Licencia | Uso aquí |
|---|---|---|---|
| Salinas et al., Zenodo [10.5281/zenodo.6348930](https://zenodo.org/records/6348930) | serie temporal original de 256 Hz, marzo-diciembre de 2013 y enero-febrero de 2017 | CC BY 4.0 | entrada; los productos derivados son nuestros y los publicamos con la atribución adecuada |
| Salinas et al., Digibug [10481/71563](https://digibug.ugr.es/handle/10481/71563) | espectros de 10 minutos procesados por la estación + ajustes de Lorentz | CC BY-NC-ND 3.0 | solo para el verificador, nunca se redistribuye |
| Salinas et al. 2022, *Computers & Geosciences* 165:105148; código [asalinas62/Sierra_Nevada_SR](https://github.com/asalinas62/Sierra_Nevada_SR) | fórmula de calibración y cadena de procesamiento | el artículo tiene licencia CC BY-NC-ND; el código tiene la licencia de su repositorio | método reproducido en `scripts/process_month.py` |
| Índice Kp de GFZ Potsdam, Matzka et al. 2021 | Kp cada 3 horas | CC BY 4.0 | carril de eventos |
| Servicio de eventos FDSN de USGS | terremotos | dominio público | carril de eventos |

Nada de `data/` se incluye. El archivo de Zenodo es un archivo zip de 26,5 GB; el script de descarga lee su directorio central a través de solicitudes de rango HTTP y transmite solo el mes solicitado.

## Cadena de procesamiento

```bash
python scripts/fetch_zenodo_month.py 1310          # ~2.4 GB, one month, both sensors
python scripts/process_month.py 1310 0             # NS  -> data/derived/SN_1310_0.npz
python scripts/process_month.py 1310 1             # EW  -> data/derived/SN_1310_1.npz
python scripts/verify_against_granada.py 1310 0    # optional, needs the Digibug npz in data/granada/
python scripts/build_viewer.py 1310                # -> viewer/index.html (+ viewer/artifact.html)
python -m pytest -q tests                          # synthetic checks on the chain
```

Método fijado (refleja la cadena de la estación para que se pueda verificar): ventanas Hann de 10 segundos, 50 % de superposición, FFT con relleno cero a 8192 (31,25 mHz), ventanas saturadas descartadas, calibración RLC `Scal(f) = 1e12/(2500·1.9e6) · sqrt((1-(f/f0)²)² + (2δf/f0)²) / f` con L = 298 kH, C = 77,75 pF, R = 320 kΩ, filtro de línea recta de la banda antropogénica, tres funciones de Lorentz más un término lineal ajustado en el dominio de la amplitud en el rango de 6,35–23,75 Hz.

## Cumplimiento de los estándares

Puntuación de 0 a 3 en comparación con los seis estándares de flujo de trabajo del estudio.

| Estándar | Puntuación | Evidencia |
|---|---|---|
| PIN_PER_STEP | 2 | Cada opción numérica (ventana, superposición, tamaño de la FFT, constantes de calibración, banda de ajuste, semillas) es una constante con nombre en la parte superior de `process_month.py` y se escribe en el campo npz `method`. Aún no se puede replicar en diferentes versiones de NumPy; no se registra la versión de la biblioteca. |
| AUTORIDAD_ANDON | 2 | `verify_against_granada.py` es el punto de parada en caso de discrepancia con los ajustes publicados de la estación; el script de descarga verifica el tamaño descomprimido de cada entrada zip antes de escribir. |
| COMPENSADORES_NOMBRADOS | 2 | No hay llamadas externas irreversibles en la cadena de procesamiento. La única forma de publicación es un "git push" del código fuente; `data/` se ignora. Compensador para un `viewer/index.html` defectuoso: reconstruir a partir del archivo npz. |
| DESCOMPOSICIÓN_POR_SECRETOS | 2 | Descarga, procesamiento, verificación y construcción son cuatro scripts, cada uno con una tarea. La plantilla del visor no conoce nada sobre la estación y consume un bloque JSON independiente de la estación. |
| HUMANOS_CON_CONTROL_DE_INCERTIDUMBRE | 1 | El panel de correlación muestra la banda nula, que es el control de incertidumbre para el visor. No hay ningún punto de control humano en la propia cadena de procesamiento. Solución: hacer que el verificador emita un resultado de aprobación/rechazo en función de una tolerancia establecida (responsable: próxima sesión). |
| VERIFICADOR_EXTERNO | 3 | El verificador es la salida producida de forma independiente por la propia estación (código diferente, autores diferentes, lmfit frente a SciPy). Números en la tabla anterior. |

## Confianza y datos

La cadena de procesamiento se ejecuta localmente a partir de una copia del código. Solo lee y escribe en `data/` y `viewer/`.
El acceso a la red solo se produce cuando se solicita a un script que descargue: Zenodo (archivo sin procesar), Digibug (los archivos de verificación de la estación), GFZ (Kp), USGS (terremotos). La carga del conjunto de datos utiliza su propio inicio de sesión de Hugging Face fuera de estos scripts. No se leen ni almacenan credenciales, no se envía ninguna telemetría y el visor es una página estática que carga Three.js y dos fuentes de CDN públicas, y nada más.
Requisitos: Python 3.11 o posterior con NumPy, SciPy y PyArrow, en cualquier sistema operativo; Node solo es necesario para la página de destino opcional.

## Licencia

Licencia MIT para el código. Los productos de datos derivados llevan la atribución requerida por sus fuentes.

---

<p align="center">Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a></p>
