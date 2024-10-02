""" INTRODUCCION AL PROCESAMIENTO DIGITAL DE IMAGENES - CHURQUINA JAVIER PABLO """
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()
root.state("zoomed")
root.title("Procesamiento digital de imágenes")

screenWidth = root.winfo_screenwidth()

frameRoot = tk.Frame(root, width=screenWidth * 0.96)
frameRoot.pack()

# TITULO ---------------------------------------------------------------------------
labelTitle = tk.Label(frameRoot, text="Procesamiento digital de imágenes",
                      font="Roboto 16")
labelTitle.grid(row=0, column=0, columnspan=3)
labelTitle.config(pady=10)

# SELECCION DE PROCESAMIENTO -------------------------------------------------------
labelOptions = tk.Label(frameRoot, text="Selecciona un proceso: ",
                        font="Roboto 12")
labelOptions.config(pady=5)
labelOptions.grid(row=1, column=1)
comboboxOptions = ttk.Combobox(frameRoot, state="readonly")
comboboxOptions['values'] = ("Selecciona un tema",
                             "Procesamiento en YIQ (Luminancia y Cromaticidad) ",
                             "Operaciones de luminancia",
                             "Aritmetica de pixeles",
                             "Procesamiento por convolución")
comboboxOptions.current(0)
comboboxOptions.grid(row=1, column=1)
comboboxOptions.config(width=50)

# IMAGENES DEL MAIN ----------------------------------------------------------------
reSizeImage = frameRoot.winfo_reqwidth() // 3
image1 = ImageTk.PhotoImage(Image.open("images/paisaje.jpg")
                            .resize((reSizeImage, reSizeImage)))
image2 = ImageTk.PhotoImage(Image.open("images/gato en flores.jpg")
                            .resize((reSizeImage, reSizeImage)))
image3 = ImageTk.PhotoImage(Image.open("images/paisaje_nipon.jpg")
                            .resize((reSizeImage, reSizeImage)))
labelImage1 = tk.Label(frameRoot, image=image1)
labelImage1.grid(row=2, column=0, padx=5, pady=5)
labelImage2 = tk.Label(frameRoot, image=image2)
labelImage2.grid(row=2, column=1, padx=5, pady=5)
labelImage3 = tk.Label(frameRoot, image=image3)
labelImage3.grid(row=2, column=2, padx=5, pady=5)


root.mainloop()
