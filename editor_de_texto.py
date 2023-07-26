import sys
import tkinter as tk
from tkinter import Menu
from tkinter.filedialog import askopenfile, asksaveasfilename


class Editor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Editor de Texto")
        #Configuracion tamaño min de la ventana
        self.rowconfigure(0, minsize=600, weight=1)
        #Configuracion tamaño minimo de la segunda columna
        self.columnconfigure(1, minsize=600, weight=1)
        #Atributo de campo texto
        self.campoTexto = tk.Text(self, wrap=tk.WORD)
        #Atributo de archivo
        self.archivo = None
        #Atributo para saber si ya se abrio un archivo anteriormente
        self.archivoAbierto = False
        self.crearMenu()
        self.crearComponentes()

    def crearComponentes(self):
        #Primera columna
        #Creamos un frame para los botones
        botonFrame = tk.Frame(self, relief=tk.RAISED, bd=2)
        botonFrame.grid(row=0, column=0, sticky="ns")

        #Creamos los botones|
        botonAbrir = tk.Button(botonFrame, text="Abrir", command=self.abrir)
        botonAbrir.grid(row=0, column=0, sticky="we", pady=5, padx=5)

        botonGuardar = tk.Button(botonFrame, text="Guardar", command=self.guardar)
        botonGuardar.grid(row=1, column=0, sticky="we", pady=5, padx=5)

        botonGuardarComo = tk.Button(botonFrame, text="Guardar Como...", command=self.guardarComo)
        botonGuardarComo.grid(row=2, column=0, sticky="we", pady=5, padx=5)

        #Campo de texto
        self.campoTexto.grid(row=0, column=1, sticky="nswe")

    def salir(self):
        self.quit()
        self.destroy()
        print(f"Salimos...")
        sys.exit()

    def abrir(self):
        #Abrimos el archivo para edicion (lectura-escritura)
        self.archivoAbierto = askopenfile(mode="r+")
        #Eliminamos el texto anterior
        self.campoTexto.delete(1.0, tk.END) #Linea 1 hasta el final
        #Revisamos si hay un archivo
        if not self.archivoAbierto:
            return
        #Abrimos el archivo en modo lectura, escritura como recurso.
        with open(self.archivoAbierto.name, "r") as self.archivo:
            #Leemos el contenido
            texto = self.archivo.read()
            #Insertamos todo este contenido en el campo de texto
            self.campoTexto.insert(1.0, texto)
            #Modificamos el titulo de la aplicacion
            self.title(f"*Editor de Texto - {self.archivo.name}")



    def guardar(self):
        #Si ya se abrio previamente este archivo, lo sobreescribimos
        if self.archivoAbierto:
            #Salvamos el archivo (lo abrimos en modo escritura)
            with open(self.archivoAbierto.name, "w") as self.archivo:
                #Leemos el contenido de la caja de texto
                texto = self.campoTexto.get(1.0, tk.END)
                #Escribimos el contenido al mismo archivo
                self.archivo.write(texto)
                #Cambiamos el nombre del titulo
                self.title(f"Editor de Texto - {self.archivo.name}")
        else:
            self.guardarComo()
    def guardarComo(self):
        #Salvamos el archivo actual como uno nuevo
        self.archivo = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Archivos de Texto", "*txt"), ("Todos los archivos", "*.*")] #Vamos a filtrar y visualizar archivos de texto
        )
        if not self.archivo:
            return
        #Abrimos el archivo en modo escritura
        with open(self.archivo, "w") as self.archivo:
            # Leemos el contenido de la caja de texto
            texto = self.campoTexto.get(1.0, tk.END)
            # Escribimos el contenido al nuevo archivo
            self.archivo.write(texto)
            # Cambiamos el nombre del titulo
            self.title(f"Editor de Texto - {self.archivo.name}")
            #Indicamos que ya hemos abierto un archivo
            self.archivoAbierto = self.archivo


    def crearMenu(self):
        #Creamos el menu principal
        menuPrincipal = Menu(self)
        menuArchivo = Menu(menuPrincipal, tearoff=False)

        #Agregamos los submenus
        menuArchivo.add_command(label="Abrir", command=self.abrir)
        menuArchivo.add_command(label="Guardar", command=self.guardar)
        menuArchivo.add_command(label="Guardar Como", command=self.guardarComo)
        menuArchivo.add_separator()
        menuArchivo.add_command(label="Salir", command=self.salir)

        #Creamos la cascada y la mostramos
        menuPrincipal.add_cascade(menu=menuArchivo, label="Archivo")
        self.config(menu=menuPrincipal)

if __name__ == "__main__":
    ventana = Editor()
    ventana.mainloop()