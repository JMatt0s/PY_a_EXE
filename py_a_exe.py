"""
PY a EXE - Convierte archivos .py en ejecutables usando PyInstaller.

Uso:  python py_a_exe.py
Requisitos: Python 3.8+  (PyInstaller se instala desde el propio programa)
"""

import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk


class ConvertidorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PY a EXE")
        self.geometry("680x560")
        self.minsize(600, 500)

        self.var_script = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_icono = tk.StringVar()
        self.var_salida = tk.StringVar(value=os.path.join(os.getcwd(), "dist"))
        self.var_onefile = tk.BooleanVar(value=True)
        self.var_sin_consola = tk.BooleanVar(value=False)
        self.var_limpiar = tk.BooleanVar(value=True)

        self._construir_ui()

    # ---------- Interfaz ----------
    def _construir_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)
        frm.columnconfigure(1, weight=1)

        filas = [
            ("Archivo .py:", self.var_script, self._elegir_script),
            ("Nombre del .exe:", self.var_nombre, None),
            ("Icono (.ico):", self.var_icono, self._elegir_icono),
            ("Carpeta de salida:", self.var_salida, self._elegir_salida),
        ]
        for i, (texto, var, cmd) in enumerate(filas):
            ttk.Label(frm, text=texto).grid(row=i, column=0, sticky="w", pady=4)
            ttk.Entry(frm, textvariable=var).grid(row=i, column=1, sticky="ew", padx=6)
            if cmd:
                ttk.Button(frm, text="Examinar…", command=cmd).grid(row=i, column=2)

        opciones = ttk.LabelFrame(frm, text="Opciones", padding=8)
        opciones.grid(row=4, column=0, columnspan=3, sticky="ew", pady=10)
        ttk.Checkbutton(opciones, text="Un solo archivo (--onefile)",
                        variable=self.var_onefile).pack(anchor="w")
        ttk.Checkbutton(opciones, text="Sin ventana de consola (--noconsole), ideal para apps con interfaz gráfica",
                        variable=self.var_sin_consola).pack(anchor="w")
        ttk.Checkbutton(opciones, text="Limpiar archivos temporales al terminar (build/ y .spec)",
                        variable=self.var_limpiar).pack(anchor="w")

        botones = ttk.Frame(frm)
        botones.grid(row=5, column=0, columnspan=3, sticky="ew")
        self.btn_convertir = ttk.Button(botones, text="Convertir a EXE", command=self._convertir)
        self.btn_convertir.pack(side="left")
        ttk.Button(botones, text="Abrir carpeta de salida",
                   command=self._abrir_salida).pack(side="left", padx=8)

        self.barra = ttk.Progressbar(frm, mode="indeterminate")
        self.barra.grid(row=6, column=0, columnspan=3, sticky="ew", pady=8)

        self.log = scrolledtext.ScrolledText(frm, height=14, state="disabled",
                                             font=("Consolas", 9))
        self.log.grid(row=7, column=0, columnspan=3, sticky="nsew")
        frm.rowconfigure(7, weight=1)

    # ---------- Selectores ----------
    def _elegir_script(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona el script", filetypes=[("Python", "*.py *.pyw")])
        if ruta:
            self.var_script.set(ruta)
            if not self.var_nombre.get():
                self.var_nombre.set(os.path.splitext(os.path.basename(ruta))[0])

    def _elegir_icono(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona el icono", filetypes=[("Icono", "*.ico")])
        if ruta:
            self.var_icono.set(ruta)

    def _elegir_salida(self):
        ruta = filedialog.askdirectory(title="Carpeta de salida")
        if ruta:
            self.var_salida.set(ruta)

    def _abrir_salida(self):
        ruta = self.var_salida.get()
        if not os.path.isdir(ruta):
            messagebox.showinfo("Carpeta no encontrada", "La carpeta aún no existe.")
            return
        if sys.platform.startswith("win"):
            os.startfile(ruta)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", ruta])
        else:
            subprocess.Popen(["xdg-open", ruta])

    # ---------- Log ----------
    def _escribir(self, texto):
        def _w():
            self.log.configure(state="normal")
            self.log.insert("end", texto)
            self.log.see("end")
            self.log.configure(state="disabled")
        self.after(0, _w)

    # ---------- Conversión ----------
    def _convertir(self):
        script = self.var_script.get().strip()
        if not script or not os.path.isfile(script):
            messagebox.showerror("Error", "Selecciona un archivo .py válido.")
            return
        icono = self.var_icono.get().strip()
        if icono and not os.path.isfile(icono):
            messagebox.showerror("Error", "El icono indicado no existe.")
            return

        self.btn_convertir.configure(state="disabled")
        self.barra.start(10)
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        threading.Thread(target=self._trabajo, daemon=True).start()

    def _pyinstaller_instalado(self):
        r = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"],
                           capture_output=True, text=True)
        return r.returncode == 0

    def _ejecutar(self, comando, cwd=None):
        self._escribir("> " + " ".join(f'"{c}"' if " " in c else c for c in comando) + "\n")
        flags = subprocess.CREATE_NO_WINDOW if sys.platform.startswith("win") else 0
        proc = subprocess.Popen(comando, cwd=cwd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True,
                                creationflags=flags)
        for linea in proc.stdout:
            self._escribir(linea)
        return proc.wait()

    def _trabajo(self):
        try:
            if not self._pyinstaller_instalado():
                self._escribir("PyInstaller no está instalado. Instalando…\n")
                if self._ejecutar([sys.executable, "-m", "pip", "install", "pyinstaller"]) != 0:
                    raise RuntimeError("No se pudo instalar PyInstaller.")

            script = os.path.abspath(self.var_script.get().strip())
            nombre = self.var_nombre.get().strip() or os.path.splitext(os.path.basename(script))[0]
            salida = os.path.abspath(self.var_salida.get().strip())
            trabajo = os.path.join(salida, "_build")
            os.makedirs(salida, exist_ok=True)

            cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm",
                   "--name", nombre, "--distpath", salida,
                   "--workpath", trabajo, "--specpath", trabajo]
            cmd.append("--onefile" if self.var_onefile.get() else "--onedir")
            if self.var_sin_consola.get():
                cmd.append("--noconsole")
            if self.var_icono.get().strip():
                cmd += ["--icon", os.path.abspath(self.var_icono.get().strip())]
            cmd.append(script)

            codigo = self._ejecutar(cmd, cwd=os.path.dirname(script))
            if codigo != 0:
                raise RuntimeError(f"PyInstaller terminó con código {codigo}.")

            if self.var_limpiar.get():
                import shutil
                shutil.rmtree(trabajo, ignore_errors=True)

            self._escribir(f"\n✔ Listo. Ejecutable en: {salida}\n")
            self.after(0, lambda: messagebox.showinfo("Listo", f"Ejecutable creado en:\n{salida}"))
        except Exception as e:
            self._escribir(f"\n✖ Error: {e}\n")
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.after(0, self._terminar)

    def _terminar(self):
        self.barra.stop()
        self.btn_convertir.configure(state="normal")


if __name__ == "__main__":
    ConvertidorApp().mainloop()
