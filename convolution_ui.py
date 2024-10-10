""" INTERFAZ DE CONVOLUCION """
import tkinter as tk
from tkinter import ttk, filedialog
import os.path
import imageio
# from cv2 import *
from matplotlib import pyplot
from PIL import Image, ImageTk
import functions


def upload_image():
    """ SELECCION Y CARGAR DE UNA IMAGEN DEL SISTEMA """
    global image, image_in, extension
    image_in_name = "image_in"
    file_name = filedialog.askopenfilename(
        title='Abrir imagen',
        initialdir='/',
        filetypes=[("images files", "*.png *.jpg *.jpeg *.gif *.bmp")])
    image_path, extension = os.path.splitext(file_name)
    image_gray = Image.open(file_name).convert("L")
    image = ImageTk.PhotoImage(image_gray)
    image_gray.save(image_in_name+extension)
    image_in = imageio.imread(image_in_name+extension)
    combobox_process['state'] = 'normal'
    label_image_in = tk.Label(frame_image_in, image=image)
    label_image_in.grid(row=1, column=0)
    label_image_in.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def convolution(type_filter, dimension_kernel):
    """ APLICACION DE CONVOLUCIÓN """
    global image_out
    image_out_name = "image_out"
    match type_filter:
        case 0:
            print("caso0")
        case 1:
            kernel = functions.generar_kernel_plano(dimension_kernel)
        case 2:
            print("caso4")
        case 3:
            print("caso4")
        case 4:
            print("caso4")
        case 5:
            print("caso5")
        case 6:
            print("caso6")

    processed_image = functions.generar_convolucion(image_in, kernel)
    pyplot.imsave(image_out_name+extension, processed_image)
    image_out = ImageTk.PhotoImage(Image.open(
        image_out_name+extension).convert("L"))
    label_image_out = tk.Label(frame_image_out, image=image_out)
    label_image_out.grid(row=1, column=0)
    label_image_out.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def create_frame_parameters(event):
    """ SELECCION DE PARAMETROS """
    global dimension_selected
    for wid in frame_parameters.winfo_children():
        wid.destroy()
    if combobox_process.current() > 0:
        button_process['state'] = 'normal'
    match combobox_process.current():
        case 0:
            print("caso0")
        case 1 | 2 | 3:
            dimension_selected = tk.IntVar()
            kernel_3x3 = tk.Radiobutton(frame_parameters,
                                        text="Kernel de 3x3",
                                        font="11",
                                        variable=dimension_selected,
                                        value=3)
            kernel_3x3.grid(row=0, column=0)
            kernel_5x5 = tk.Radiobutton(frame_parameters,
                                        text="Kernel de 5x5",
                                        font="11",
                                        variable=dimension_selected,
                                        value=5)
            kernel_5x5.grid(row=1, column=0)
            kernel_7x7 = tk.Radiobutton(frame_parameters,
                                        text="Kernel de 7x7",
                                        font="11",
                                        variable=dimension_selected,
                                        value=7)
            kernel_7x7.grid(row=2, column=0)
            dimension_selected.set(3)
        case 4:
            print("caso4")
        case 5:
            print("caso5")
        case 6:
            print("caso6")


def create_frame_variables(frame_convolution, width_frame_convolution):
    """ CREACION DE LA SECCIÓN DE VARIABLES """
    global frame_parameters, combobox_process, button_process
    frame_variables = tk.Frame(frame_convolution,
                               width=width_frame_convolution*0.2,
                               height=frame_convolution.winfo_vrootheight()*0.83,
                               bg="#F9F9F9")
    frame_variables.grid(row=0, column=0, padx=5)
    frame_variables.grid_propagate(False)

    label_title_image_in = tk.Label(frame_variables,
                                    text="Selección de imagen",
                                    font="Roboto 12", bg="#F9F9F9")
    label_title_image_in.grid(row=0, column=0, columnspan=2, pady=3, padx=5)
    label_image_in = tk.Label(frame_variables, text="Cargar imagen: ",
                              bg="#F9F9F9")
    label_image_in.grid(row=1, column=0, pady=3, padx=3, sticky="E")
    button_image_in = tk.Button(frame_variables, text="Cargar")
    button_image_in.config(
        width=10, command=upload_image)
    button_image_in.grid(row=1, column=1, pady=3, padx=3, sticky="W")

    label_title_process = tk.Label(frame_variables,
                                   text="Selección de proceso",
                                   font="Roboto 12", bg="#F9F9F9")
    label_title_process.grid(row=2, column=0, columnspan=2, pady=3, padx=5)
    combobox_process = ttk.Combobox(frame_variables, state="readonly")
    combobox_process['values'] = ("Selecciona un filtro",
                                  "Pasabajos Plano",
                                  "Pasabajos Bartlett",
                                  "Pasabajos Gaussiano",
                                  "Pasaaltos Laplaciano",
                                  "Pasaaltos Sobel",
                                  "Pasabanda DOG")
    combobox_process.current(0)
    combobox_process.grid(row=3, column=0, columnspan=2, pady=5)
    combobox_process['state'] = 'disabled'
    combobox_process.bind("<<ComboboxSelected>>", create_frame_parameters)
    label_title_parameters = tk.Label(frame_variables,
                                      text="Configuración de parametros",
                                      font="Roboto 12", bg="#F9F9F9")
    label_title_parameters.grid(row=4, column=0, columnspan=2, pady=3, padx=5)
    frame_parameters = tk.Frame(frame_variables)
    frame_parameters.grid(row=5, column=0, columnspan=2, pady=3, padx=5)

    button_process = tk.Button(frame_variables, text="PROCESAR",
                               command=lambda: convolution(combobox_process.current(), dimension_selected.get()))
    button_process.config(width=15, font="Roboto 11 bold",
                          bg="#12A14B", fg="white")
    button_process['state'] = 'disabled'
    button_process.grid(row=10, column=0, columnspan=2)


def create_frame_convolution(frame_main, screen_width):
    """ CREACION DE LA INTERFAZ DE CONVOLUCIÓN """
    global frame_image_in, frame_image_out

    frame_convolution = tk.Frame(frame_main, width=screen_width * 0.96)
    frame_convolution.pack()
    frame_convolution.config(pady=5, padx=5, bg="white")

    width_frame_convolution = frame_convolution.winfo_reqwidth()

    create_frame_variables(frame_convolution, width_frame_convolution)

    frame_image_in = tk.Frame(frame_convolution,
                              width=width_frame_convolution*0.4,
                              height=frame_convolution.winfo_vrootheight()*0.7)
    frame_image_in.grid(row=0, column=1, padx=5)
    frame_image_in.grid_propagate(False)
    label_title_in = tk.Label(frame_image_in,
                              text="Imagen original (en escala de grises)",
                              font="Roboto 12", padx=5)
    label_title_in.grid(row=0, column=0)

    frame_image_out = tk.Frame(frame_convolution,
                               width=width_frame_convolution*0.4,
                               height=frame_convolution.winfo_vrootheight()*0.7)
    frame_image_out.grid(row=0, column=2, padx=5)
    frame_image_out.grid_propagate(False)
    label_title_out = tk.Label(frame_image_out, text="Imagen procesada",
                               font="Roboto 12", padx=5)
    label_title_out.grid(row=0, column=0)
