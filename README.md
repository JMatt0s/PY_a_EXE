# PY a EXE

Aplicación de escritorio con interfaz gráfica que convierte archivos de Python (`.py`) en ejecutables (`.exe`) usando [PyInstaller](https://pyinstaller.org/). No necesitas escribir comandos: eliges tu script, marcas las opciones y presionas un botón.

## Características

- Interfaz gráfica sencilla hecha con **Tkinter** (sin dependencias externas para la app).
- Instala **PyInstaller automáticamente** si todavía no lo tienes.
- Opción de generar **un solo archivo** (`--onefile`) o una carpeta (`--onedir`).
- Opción de **ocultar la consola** (`--noconsole`), ideal para programas con interfaz gráfica.
- Permite asignar un **nombre personalizado** y un **icono** (`.ico`) al ejecutable.
- Elección de la **carpeta de salida**, con botón para abrirla al terminar.
- **Registro en vivo** de lo que hace PyInstaller dentro de la ventana.
- **Limpieza automática** de los archivos temporales de compilación.
- La conversión corre en un hilo aparte, así que la ventana no se congela.

## Requisitos

- Python **3.8 o superior**
- Tkinter (viene incluido con Python en Windows y macOS; en Linux puede requerir `sudo apt install python3-tk`)
- Conexión a internet la primera vez, solo si PyInstaller no está instalado

> PyInstaller **no compila de forma cruzada**: el ejecutable se genera para el sistema operativo en el que corres el programa. Para obtener un `.exe` de Windows, debes ejecutarlo en Windows.

## Instalación

1. Descarga o clona este repositorio.
2. Asegúrate de tener Python instalado:

   ```bash
   python --version
   ```

3. (Opcional) Instala PyInstaller de antemano:

   ```bash
   pip install pyinstaller
   ```

   Si no lo haces, la aplicación lo instalará por ti al convertir.

## Uso

Ejecuta el programa:

```bash
python py_a_exe.py
```

Luego, en la ventana:

1. **Archivo .py:** pulsa *Examinar…* y selecciona el script que quieres convertir. El nombre del `.exe` se completa solo.
2. **Nombre del .exe:** cámbialo si quieres otro nombre (opcional).
3. **Icono (.ico):** selecciona un icono para el ejecutable (opcional).
4. **Carpeta de salida:** por defecto es `dist/` dentro de la carpeta actual; puedes cambiarla.
5. Marca las **opciones** que necesites.
6. Presiona **Convertir a EXE** y espera. Verás el progreso en el registro.
7. Al terminar, usa **Abrir carpeta de salida** para encontrar tu ejecutable.

## Opciones

| Opción | Equivale a | Cuándo usarla |
|---|---|---|
| Un solo archivo | `--onefile` | Para distribuir un único `.exe`. Si la desmarcas, se genera una carpeta (`--onedir`), que arranca más rápido. |
| Sin ventana de consola | `--noconsole` | Para aplicaciones con interfaz gráfica (Tkinter, PyQt, etc.). Si tu programa usa `print()` o `input()`, déjala desmarcada. |
| Limpiar archivos temporales | Elimina la carpeta `_build` | Recomendado. Borra los archivos de trabajo y el `.spec` al finalizar. |

## Cómo funciona

Internamente, el programa arma y ejecuta un comando como este:

```bash
python -m PyInstaller --noconfirm --name MiApp --distpath <salida> \
    --workpath <salida>/_build --specpath <salida>/_build \
    --onefile --noconsole --icon icono.ico mi_script.py
```

Los archivos temporales (`build` y `.spec`) se guardan en `<salida>/_build`, de modo que no ensucian la carpeta de tu proyecto. Si activas la limpieza, esa carpeta se elimina al terminar.

## Estructura del proyecto

```
.
├── py_a_exe.py   # Aplicación completa (interfaz + lógica de conversión)
└── README.md
```

## Solución de problemas

**"PyInstaller terminó con código 1"**
Revisa el registro: casi siempre indica un módulo que falta o un error en tu script. Prueba primero que tu script funcione con `python mi_script.py`.

**El `.exe` se cierra al abrirlo o no muestra errores**
Si lo creaste con *Sin ventana de consola*, los errores quedan ocultos. Vuelve a generarlo con la consola activada para ver el mensaje.

**El antivirus marca el `.exe` como sospechoso**
Es un falso positivo frecuente en ejecutables creados con PyInstaller, sobre todo con `--onefile`. Puedes agregar una excepción o usar el modo `--onedir`.

**El ejecutable no encuentra imágenes, bases de datos u otros archivos**
Esta herramienta no incluye archivos de datos adicionales. Si tu programa los necesita, deberás agregarlos con la opción `--add-data` de PyInstaller desde la línea de comandos.

**No se pudo instalar PyInstaller**
Verifica tu conexión a internet o instálalo manualmente con `pip install pyinstaller`.

**En Linux aparece un error de `tkinter`**
Instala el paquete con `sudo apt install python3-tk`.

## Limitaciones

- No incluye archivos de datos adicionales (`--add-data`) ni módulos ocultos (`--hidden-import`).
- Genera ejecutables solo para el sistema operativo desde el que se ejecuta.
- El primer arranque de un `.exe` en modo un solo archivo puede tardar unos segundos mientras se descomprime.

## Tecnologías

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller](https://pyinstaller.org/)
