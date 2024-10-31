""" INTRODUCCION AL PROCESAMIENTO DIGITAL DE IMAGENES - CHURQUINA JAVIER PABLO """
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from process_yiq_ui import create_frame_process_yiq
from convolution_ui import create_frame_convolution
from morphology_ui import create_frame_mophology


def create_frame(event):
    """ SELECCION DEL TIPO DE PROCESAMIENTO A REALIZAR """
    for wid in frameMain.winfo_children():
        wid.destroy()
    match comboboxOptions.current():
        case 0:
            create_frame_home()
        case 1:
            create_frame_process_yiq(frameMain, screenWidth)
        case 2:
            frame2 = tk.Frame(frameMain, width=300, height=100, bg="blue")
            frame2.pack()
            label_message = tk.Label(frame2,
                                     text="Seccion en mantenimiento...")
            label_message.grid(row=0, column=0)
        case 3:
            frame3 = tk.Frame(frameMain, width=300, height=100, bg="green")
            frame3.pack()
            label_message = tk.Label(frame3,
                                     text="Seccion en mantenimiento...")
            label_message.grid(row=0, column=0)
        case 4:
            create_frame_convolution(frameMain, screenWidth)
        case 5:
            create_frame_mophology(frameMain, screenWidth)


def create_frame_home():
    """ CREACION DEL FRAME HOME """
    global image1, image2, image3
    frame_home = tk.Frame(frameMain, width=screenWidth * 0.96, bg="white")
    frame_home.pack()
    # IMAGENES DEL MAIN ----------------------------------------------------------------
    resize_image = frame_home.winfo_reqwidth() // 3
    image1 = ImageTk.PhotoImage(Image.open("images/paisaje.jpg")
                                .resize((resize_image, resize_image)))
    image2 = ImageTk.PhotoImage(Image.open("images/gato en flores.jpg")
                                .resize((resize_image, resize_image)))
    image3 = ImageTk.PhotoImage(Image.open("images/paisaje_nipon.jpg")
                                .resize((resize_image, resize_image)))
    label_image1 = tk.Label(frame_home, image=image1)
    label_image1.grid(row=2, column=0, padx=5, pady=5)
    label_image2 = tk.Label(frame_home, image=image2)
    label_image2.grid(row=2, column=1, padx=5, pady=5)
    label_image3 = tk.Label(frame_home, image=image3)
    label_image3.grid(row=2, column=2, padx=5, pady=5)


root = tk.Tk()
root.state("zoomed")
root.title("Procesamiento digital de imágenes")

screenWidth = root.winfo_screenwidth()

frameRoot = tk.Frame(root, width=screenWidth * 0.96)
frameRoot.pack()
frameMain = tk.Frame(root, width=screenWidth * 0.96)
frameMain.pack()

# TITULO ---------------------------------------------------------------------------
labelTitle = tk.Label(frameRoot, text="Procesamiento digital de imágenes",
                      font="Roboto 16")
labelTitle.grid(row=0, column=0, columnspan=3)
labelTitle.config(pady=10)

# SELECCION DE PROCESAMIENTO -------------------------------------------------------
comboboxOptions = ttk.Combobox(frameRoot, state="readonly")
comboboxOptions['values'] = ("Selecciona un tema",
                             "Procesamiento en YIQ (Luminancia y Cromaticidad) ",
                             "Operaciones de luminancia",
                             "Aritmetica de pixeles",
                             "Procesamiento por convolución",
                             "Procesamiento morfológico")
comboboxOptions.current(0)
comboboxOptions.grid(row=1, column=1, pady=10)
comboboxOptions.config(width=50)
comboboxOptions.bind("<<ComboboxSelected>>", create_frame)

create_frame_home()

root.mainloop()
