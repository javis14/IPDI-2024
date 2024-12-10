""" INTERFAZ DE OPERACIONES DE LUMINANCIA """
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
    image = ImageTk.PhotoImage(Image.open(file_name))
    image_in = imageio.imread(file_name)/255
    combobox_process['state'] = 'readonly'
    label_image_in = tk.Label(frame_image_in, image=image)
    label_image_in.grid(row=1, column=0)
    label_image_in.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def process_image(process_selected, function_selected):
    """ APLICACION DE OPERACION DE LUMINANCIA """
    global image_out
    image_out_name = "image_out"
    match process_selected:
        case 1:
            processed_image = functions.aumentar_luminancia(image_in,
                                                            function_selected)
        case 2:
            processed_image = functions.disminuir_luminancia(image_in,
                                                             function_selected)
        case _:
            print("error...")

    pyplot.imsave(image_out_name+extension, processed_image)
    image_out = ImageTk.PhotoImage(Image.open(image_out_name+extension))
    label_image_out = tk.Label(frame_image_out, image=image_out)
    label_image_out.grid(row=1, column=0)
    label_image_out.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def process_image_contrast(y_min, y_max):
    """ APLICACION DE OPERACION DE LUMINANCIA """
    global image_out
    image_out_name = "image_out"
    processed_image = functions.mejorar_contraste(image_in, y_min, y_max)

    pyplot.imsave(image_out_name+extension, processed_image)
    image_out = ImageTk.PhotoImage(Image.open(image_out_name+extension))
    label_image_out = tk.Label(frame_image_out, image=image_out)
    label_image_out.grid(row=1, column=0)
    label_image_out.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def validate_entry(text):
    """ VALIDAR ENTRADA NUMERICA """
    return text in "0123456789."


def create_frame_parameters(event):
    """ SELECCION DE PARAMETROS """
    for wid in frame_parameters.winfo_children():
        wid.destroy()
    if combobox_process.current() > 0:
        button_process['state'] = 'normal'
    match combobox_process.current():
        case 1:
            function_selected = tk.IntVar()
            square_root = tk.Radiobutton(frame_parameters,
                                         text="Raíz cuadrada",
                                         font="10",
                                         variable=function_selected,
                                         value=1)
            square_root.grid(row=0, column=0)
            function_selected.set(1)
            button_process.config(command=lambda: process_image(combobox_process.current(),
                                                                function_selected.get()))
        case 2:
            function_selected = tk.IntVar()
            quadratic = tk.Radiobutton(frame_parameters,
                                       text="Potencia al cuadrado",
                                       font="10",
                                       variable=function_selected,
                                       value=1)
            quadratic.grid(row=0, column=0)
            function_selected.set(1)
            button_process.config(command=lambda: process_image(combobox_process.current(),
                                                                function_selected.get()))
        case 3:
            label_y_minimo = tk.Label(frame_parameters, text="Luminancia mínima:",
                                      bg="#F9F9F9")
            label_y_minimo.grid(row=0, column=0, pady=3)
            entry_y_minimo = tk.Entry(frame_parameters, validate="key",
                                      validatecommand=(frame_parameters.register(validate_entry), "%S"))
            entry_y_minimo.grid(row=0, column=1, pady=3)
            label_y_maximo = tk.Label(frame_parameters, text="Luminancia máxima:",
                                      bg="#F9F9F9")
            label_y_maximo.grid(row=1, column=0, pady=3)
            entry_y_maximo = tk.Entry(frame_parameters, validate="key",
                                      validatecommand=(frame_parameters.register(validate_entry), "%S"))
            entry_y_maximo.grid(row=1, column=1, pady=3)
            button_process.config(command=lambda: process_image_contrast(float(entry_y_minimo.get()),
                                                                         float(entry_y_maximo.get())))


def create_frame_variables(frame_luminancia, width_frame_luminancia):
    """ CREACION DE LA SECCIÓN DE VARIABLES """
    global frame_parameters, combobox_process, button_process
    frame_variables = tk.Frame(frame_luminancia,
                               width=width_frame_luminancia*0.2,
                               height=frame_luminancia.winfo_vrootheight()*0.83,
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
    combobox_process['values'] = ("Selecciona un proceso",
                                  "Aumentar luminancia",
                                  "Disminuir luminancia",
                                  "Mejorar contraste")
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

    button_process = tk.Button(frame_variables, text="PROCESAR")
    button_process.config(width=15, font="Roboto 11 bold",
                          bg="#12A14B", fg="white")
    button_process['state'] = 'disabled'
    button_process.grid(row=10, column=0, columnspan=2, pady=15)


def create_frame_luminance_operations(frame_main, screen_width):
    """ CREACION DE LA INTERFAZ OPERACIONES DE LUMINANCIA """
    global frame_image_in, frame_image_out

    frame_luminancia = tk.Frame(frame_main, width=screen_width * 0.96)
    frame_luminancia.pack()
    frame_luminancia.config(pady=5, padx=5, bg="white")

    width_frame_luminancia = frame_luminancia.winfo_reqwidth()

    create_frame_variables(frame_luminancia, width_frame_luminancia)

    frame_image_in = tk.Frame(frame_luminancia,
                              width=width_frame_luminancia*0.4,
                              height=frame_luminancia.winfo_vrootheight()*0.7)
    frame_image_in.grid(row=0, column=1, padx=5)
    frame_image_in.grid_propagate(False)
    label_title_in = tk.Label(frame_image_in,
                              text="Imagen original",
                              font="Roboto 12", padx=5)
    label_title_in.grid(row=0, column=0)

    frame_image_out = tk.Frame(frame_luminancia,
                               width=width_frame_luminancia*0.4,
                               height=frame_luminancia.winfo_vrootheight()*0.7)
    frame_image_out.grid(row=0, column=2, padx=5)
    frame_image_out.grid_propagate(False)
    label_title_out = tk.Label(frame_image_out, text="Imagen procesada",
                               font="Roboto 12", padx=5)
    label_title_out.grid(row=0, column=0)
