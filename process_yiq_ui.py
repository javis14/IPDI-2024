""" INTERFAZ DE PROCESAMIENTO EN EL ESPACIO YIQ """
import tkinter as tk
from tkinter import ttk, filedialog
import os.path
import imageio
import numpy
from matplotlib import pyplot
from PIL import Image, ImageTk
import functions


def upload_image():
    """ SELECCION Y CARGAR DE UNA IMAGEN DEL SISTEMA """
    global image, image_in, extension
    file_name = filedialog.askopenfilename(
        title='Abrir imagen',
        initialdir='/',
        filetypes=[("images files", "*.png *.jpg *.gif *.bmp")])
    image_path, extension = os.path.splitext(file_name)
    image_in = imageio.imread(file_name)/255

    image = ImageTk.PhotoImage(file=file_name)
    label_image_in = tk.Label(frame_image_in, image=image)
    label_image_in.grid(row=1, column=0)
    label_image_in.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    button_process['state'] = 'normal'


def process_image(luminancia=1, saturacion=1):
    """ MODIFICAR LUMINANCIA Y/O SATURACION DE LA IMAGEN """
    global image_out
    image_out_name = "image_out"
    new_image_yiq = numpy.zeros(image_in.shape)

    image_yiq = functions.rgb_a_yiq(image_in)
    new_image_yiq[:, :, 0] = numpy.clip(luminancia * image_yiq[:, :, 0], 0, 1)
    new_image_yiq[:, :, 1] = numpy.clip(saturacion * image_yiq[:, :, 1],
                                        -0.5957, 0.5957)
    new_image_yiq[:, :, 2] = numpy.clip(saturacion * image_yiq[:, :, 2],
                                        -0.5226, 0.5226)
    image_rgb = functions.yiq_a_rgb(new_image_yiq)
    image_rgb = numpy.clip(image_rgb*255, 0, 255).astype(numpy.uint8)

    pyplot.imsave(image_out_name+extension, image_rgb)
    image_out = ImageTk.PhotoImage(Image.open(image_out_name+extension))
    label_image_out = tk.Label(frame_image_out, image=image_out)
    label_image_out.grid(row=1, column=0)
    label_image_out.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def validate_entry(text):
    """ VALIDAR ENTRADA NUMERICA """
    return text in "0123456789."


def create_frame_variables(frame_convolution, width_frame_convolution):
    """ CREACION DE LA SECCIÓN DE VARIABLES """
    global frame_parameters, button_process
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
    button_image_in.config(width=10, command=upload_image)
    button_image_in.grid(row=1, column=1, pady=3, padx=3, sticky="W")

    label_title_parameters = tk.Label(frame_variables,
                                      text="Configuración de parametros",
                                      font="Roboto 12", bg="#F9F9F9")
    label_title_parameters.grid(row=4, column=0, columnspan=2, pady=3, padx=5)
    frame_parameters = tk.Frame(frame_variables, bg="#F9F9F9")
    frame_parameters.grid(row=5, column=0, columnspan=2, pady=3, padx=5)
    label_luminancia = tk.Label(frame_parameters, text="Valor de Luminancia:",
                                bg="#F9F9F9")
    label_luminancia.grid(row=6, column=0, pady=3)
    entry_luminancia = tk.Entry(frame_parameters, validate="key",
                                validatecommand=(frame_parameters.register(validate_entry), "%S"))
    entry_luminancia.grid(row=6, column=1, pady=3)
    label_saturacion = tk.Label(frame_parameters, text="Valor de Saturación:",
                                bg="#F9F9F9")
    label_saturacion.grid(row=7, column=0, pady=3)
    entry_saturacion = tk.Entry(frame_parameters, validate="key",
                                validatecommand=(frame_parameters.register(validate_entry), "%S"))
    entry_saturacion.grid(row=7, column=1, pady=3)

    button_process = tk.Button(frame_variables,
                               text="PROCESAR",
                               command=lambda: process_image(float(entry_luminancia.get()),
                                                             float(entry_saturacion.get())))
    button_process.config(width=15,
                          font="Roboto 11 bold",
                          bg="#12A14B",
                          fg="white")
    button_process['state'] = 'disabled'
    button_process.grid(row=15, column=0, columnspan=2, pady=10)


def create_frame_process_yiq(frame_main, screen_width):
    """ CREACION DE LA INTERFAZ PARA PROCESAMIENTO EN YIQ """
    global frame_image_in, frame_image_out

    frame_yiq = tk.Frame(frame_main, width=screen_width * 0.96)
    frame_yiq.pack()
    frame_yiq.config(pady=5, padx=5, bg="white")

    width_frame_yiq = frame_yiq.winfo_reqwidth()

    create_frame_variables(frame_yiq, width_frame_yiq)

    frame_image_in = tk.Frame(frame_yiq,
                              width=width_frame_yiq*0.4,
                              height=frame_yiq.winfo_vrootheight()*0.7)
    frame_image_in.grid(row=0, column=1, padx=5)
    frame_image_in.grid_propagate(False)
    label_title_in = tk.Label(frame_image_in,
                              text="Imagen original",
                              font="Roboto 12", padx=5)
    label_title_in.grid(row=0, column=0)

    frame_image_out = tk.Frame(frame_yiq,
                               width=width_frame_yiq*0.4,
                               height=frame_yiq.winfo_vrootheight()*0.7)
    frame_image_out.grid(row=0, column=2, padx=5)
    frame_image_out.grid_propagate(False)
    label_title_out = tk.Label(frame_image_out, text="Imagen procesada",
                               font="Roboto 12", padx=5)
    label_title_out.grid(row=0, column=0)
