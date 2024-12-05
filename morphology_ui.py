""" INTERFAZ DE PROCESAMIENTO MORFOLÓGICO """
import tkinter as tk
from tkinter import ttk, filedialog
import os.path
import imageio
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
    image_in = imageio.imread(image_in_name+extension)/255
    combobox_process['state'] = 'readonly'
    label_image_in = tk.Label(frame_image_in, image=image)
    label_image_in.grid(row=1, column=0)
    label_image_in.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def morphologic_process(type_filter, color_image=1, radio_kernel=3, type_kernel=0):
    """ APLICACION DE CONVOLUCIÓN MORFOLOGICA """
    global image_out
    image_out_name = "image_out"
    match type_filter:
        case 1:
            processed_image = functions.erosionar(image_in,
                                                  functions.generar_kernel(
                                                      radio_kernel, type_kernel),
                                                  type_kernel,
                                                  color_image)
        case 2:
            processed_image = functions.dilatar(image_in,
                                                functions.generar_kernel(
                                                    radio_kernel, type_kernel),
                                                type_kernel,
                                                color_image)
        case 3:
            processed_image = functions.apertura(image_in,
                                                 functions.generar_kernel(
                                                     radio_kernel, type_kernel),
                                                 type_kernel,
                                                 color_image)
        case 4:
            processed_image = functions.cierre(image_in,
                                               functions.generar_kernel(
                                                   radio_kernel, type_kernel),
                                               type_kernel,
                                               color_image)
        case 5:
            processed_image = functions.borde_exterior(image_in,
                                                       functions.generar_kernel(
                                                           radio_kernel, type_kernel),
                                                       type_kernel,
                                                       color_image)
        case 6:
            processed_image = functions.borde_interior(image_in,
                                                       functions.generar_kernel(
                                                           radio_kernel, type_kernel),
                                                       type_kernel,
                                                       color_image)
        case 7:
            processed_image = functions.gradiente(image_in,
                                                  functions.generar_kernel(
                                                      radio_kernel, type_kernel),
                                                  type_kernel,
                                                  color_image)
        case 8:
            processed_image = functions.mediana(image_in,
                                                functions.generar_kernel(
                                                    radio_kernel, type_kernel),
                                                color_image)
        case _:
            print("error...")

    pyplot.imsave(image_out_name+extension, processed_image)
    image_out = ImageTk.PhotoImage(Image.open(
        image_out_name+extension).convert("L"))
    label_image_out = tk.Label(frame_image_out, image=image_out)
    label_image_out.grid(row=1, column=0)
    label_image_out.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def create_frame_parameters(event):
    """ SELECCION DE PARAMETROS """
    for wid in frame_parameters.winfo_children():
        wid.destroy()
    if combobox_process.current() > 0:
        button_process['state'] = 'normal'
    label_color_image = tk.Label(frame_parameters,
                                 text="Color de imagen y fondo:",
                                 font="10",
                                 bg="#F9F9F9")
    label_color_image.grid(row=0, column=0, sticky="W")
    color_selected = tk.IntVar()
    image_white = tk.Radiobutton(frame_parameters,
                                 text="Imagen blanca, fondo negro",
                                 font="8",
                                 bg="#F9F9F9",
                                 padx=10,
                                 variable=color_selected,
                                 value=1)
    image_white.grid(row=1, column=0, sticky="W")
    image_black = tk.Radiobutton(frame_parameters,
                                 text="Imagen negra, fondo blanco",
                                 font="8",
                                 bg="#F9F9F9",
                                 padx=10,
                                 variable=color_selected,
                                 value=0)
    image_black.grid(row=2, column=0, sticky="W")
    color_selected.set(1)
    label_type_kernel = tk.Label(frame_parameters,
                                 text="Tipo de kernel:",
                                 font=10,
                                 bg="#F9F9F9")
    label_type_kernel.grid(row=3, column=0, sticky="W")
    type_selected = tk.IntVar()
    kernel_quadrate = tk.Radiobutton(frame_parameters,
                                     text="Kernel cuadrado",
                                     font="8",
                                     bg="#F9F9F9",
                                     padx=10,
                                     variable=type_selected,
                                     value=0)
    kernel_quadrate.grid(row=4, column=0, sticky="W")
    kernel_circle = tk.Radiobutton(frame_parameters,
                                   text="Kernel circular",
                                   font="8",
                                   bg="#F9F9F9",
                                   padx=10,
                                   variable=type_selected,
                                   value=1)
    kernel_circle.grid(row=5, column=0, sticky="W")
    type_selected.set(0)
    label_radio_kernel = tk.Label(frame_parameters,
                                  text="Radio del kernel:",
                                  font=10,
                                  bg="#F9F9F9")
    label_radio_kernel.grid(row=6, column=0, sticky="W")
    combobox_radio_options = ttk.Combobox(frame_parameters,
                                          state="readonly")
    combobox_radio_options['values'] = ("1",
                                        "2",
                                        "3",
                                        "4",
                                        "5",
                                        "6",
                                        "7",
                                        "8",
                                        "9",
                                        "10")
    combobox_radio_options.current(0)
    combobox_radio_options.grid(row=7, column=0)
    button_process.config(command=lambda: morphologic_process(combobox_process.current(),
                                                              color_selected.get(),
                                                              combobox_radio_options.current()+1,
                                                              type_selected.get()))


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
    button_image_in.config(width=10, command=upload_image)
    button_image_in.grid(row=1, column=1, pady=3, padx=3, sticky="W")

    label_title_process = tk.Label(frame_variables,
                                   text="Selección de proceso",
                                   font="Roboto 12", bg="#F9F9F9")
    label_title_process.grid(row=2, column=0, columnspan=2, pady=3, padx=5)
    combobox_process = ttk.Combobox(frame_variables, state="readonly")
    combobox_process['values'] = ("Selecciona un filtro",
                                  "Erosión",
                                  "Dilatación",
                                  "Apertura",
                                  "Cierre",
                                  "Borde exterior",
                                  "Borde interior",
                                  "Gradiente",
                                  "Mediana")
    combobox_process.current(0)
    combobox_process.grid(row=3, column=0, columnspan=2, pady=5)
    combobox_process['state'] = 'disabled'
    combobox_process.bind("<<ComboboxSelected>>", create_frame_parameters)
    label_title_parameters = tk.Label(frame_variables,
                                      text="Configuración de parametros",
                                      font="Roboto 12", bg="#F9F9F9")
    label_title_parameters.grid(row=4, column=0, columnspan=2, pady=3, padx=5)
    frame_parameters = tk.Frame(frame_variables, bg="#F9F9F9")
    frame_parameters.grid(row=5, column=0, columnspan=2, pady=3, padx=5)

    button_process = tk.Button(frame_variables, text="PROCESAR")
    button_process.config(width=15, font="Roboto 11 bold",
                          bg="#12A14B", fg="white")
    button_process['state'] = 'disabled'
    button_process.grid(row=15, column=0, columnspan=2, pady=10)


def create_frame_mophology(frame_main, screen_width):
    """ CREACION DE LA INTERFAZ DE PROCESAMIENTO MORFOLÓGICO """
    global frame_image_in, frame_image_out

    frame_morphology = tk.Frame(frame_main, width=screen_width * 0.96)
    frame_morphology.pack()
    frame_morphology.config(pady=5, padx=5, bg="white")

    width_frame_morphology = frame_morphology.winfo_reqwidth()

    create_frame_variables(frame_morphology, width_frame_morphology)

    frame_image_in = tk.Frame(frame_morphology,
                              width=width_frame_morphology*0.4,
                              height=frame_morphology.winfo_vrootheight()*0.7)
    frame_image_in.grid(row=0, column=1, padx=5)
    frame_image_in.grid_propagate(False)
    label_title_in = tk.Label(frame_image_in,
                              text="Imagen original (en escala de grises)",
                              font="Roboto 12", padx=5)
    label_title_in.grid(row=0, column=0)

    frame_image_out = tk.Frame(frame_morphology,
                               width=width_frame_morphology*0.4,
                               height=frame_morphology.winfo_vrootheight()*0.7)
    frame_image_out.grid(row=0, column=2, padx=5)
    frame_image_out.grid_propagate(False)
    label_title_out = tk.Label(frame_image_out, text="Imagen procesada",
                               font="Roboto 12", padx=5)
    label_title_out.grid(row=0, column=0)
