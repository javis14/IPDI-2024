""" INTERFAZ DE ARITMETICA DE PIXELES """
import tkinter as tk
from tkinter import ttk, filedialog
import os.path
import imageio
from matplotlib import pyplot
from PIL import Image, ImageTk
import functions


def search_image():
    """ BUSQUEDA Y SELECCION DE IMAGEN """
    file_name = filedialog.askopenfilename(
        title='Abrir imagen',
        initialdir='/',
        filetypes=[("images files", "*.png *.jpg *.jpeg *.gif *.bmp")])
    return file_name


def upload_image_a():
    """ CARGAR IMAGEN A """
    global image_a, image_a_normalized, extension
    file_name = search_image()
    image_path, extension = os.path.splitext(file_name)
    image_a = ImageTk.PhotoImage(Image.open(file_name).resize((frame_image_a.winfo_reqwidth(),
                                                               frame_image_a.winfo_reqwidth())))
    image_a_normalized = imageio.imread(file_name)/255
    button_image_b['state'] = 'normal'
    label_image_a = tk.Label(frame_image_a, image=image_a)
    label_image_a.grid(row=1, column=0)
    label_image_a.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def upload_image_b():
    """ CARGAR IMAGEN B """
    global image_b, image_b_normalized, extension
    file_name = search_image()
    image_path, extension = os.path.splitext(file_name)
    image_b = ImageTk.PhotoImage(Image.open(file_name).resize((frame_image_b.winfo_reqwidth(),
                                                               frame_image_b.winfo_reqwidth())))
    image_b_normalized = imageio.imread(file_name)/255
    combobox_process['state'] = 'readonly'
    label_image_b = tk.Label(frame_image_b, image=image_b)
    label_image_b.grid(row=1, column=0)
    label_image_b.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def process_operation(operation, format_selected):
    """ APLICACION DE OPERACIÓN SELECCIONADA """
    global image_out
    image_out_name = "image_out"
    match operation:
        case 1:
            processed_image = functions.suma(image_a_normalized,
                                             image_b_normalized,
                                             format_selected)
        case 2:
            processed_image = functions.resta(image_a_normalized,
                                              image_b_normalized,
                                              format_selected)
        case _:
            print("error...")

    pyplot.imsave(image_out_name+extension, processed_image)
    image_out = ImageTk.PhotoImage(Image.open(image_out_name+extension).resize((frame_image_out.winfo_reqwidth(),
                                                                                frame_image_out.winfo_reqwidth())))
    label_image_out = tk.Label(frame_image_out, image=image_out)
    label_image_out.grid(row=1, column=0)
    label_image_out.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def create_frame_formats(event):
    """ SELECCION DE FORMATO """
    for wid in frame_formats.winfo_children():
        wid.destroy()
    if combobox_process.current() > 0:
        button_process['state'] = 'normal'
    match combobox_process.current():
        case 1:
            format_selected = tk.IntVar()
            rgb_clamped = tk.Radiobutton(frame_formats,
                                         text="RGB clampeado",
                                         font="10",
                                         variable=format_selected,
                                         value=1)
            rgb_clamped.grid(row=0, column=0, sticky="W")
            rgb_mean = tk.Radiobutton(frame_formats,
                                      text="RGB promediado",
                                      font="10",
                                      variable=format_selected,
                                      value=2)
            rgb_mean.grid(row=1, column=0, sticky="W")
            yiq_clamped = tk.Radiobutton(frame_formats,
                                         text="YIQ clampeado",
                                         font="10",
                                         variable=format_selected,
                                         value=3)
            yiq_clamped.grid(row=2, column=0, sticky="W")
            yiq_mean = tk.Radiobutton(frame_formats,
                                      text="YIQ promediado",
                                      font="10",
                                      variable=format_selected,
                                      value=4)
            yiq_mean.grid(row=3, column=0, sticky="W")
            yiq_if_ligther = tk.Radiobutton(frame_formats,
                                            text="If lighter",
                                            font="10",
                                            variable=format_selected,
                                            value=5)
            yiq_if_ligther.grid(row=4, column=0, sticky="W")
            format_selected.set(1)
            button_process.config(command=lambda: process_operation(combobox_process.current(),
                                                                    format_selected.get()))
        case 2:
            format_selected = tk.IntVar()
            rgb_clamped = tk.Radiobutton(frame_formats,
                                         text="RGB clampeado",
                                         font="10",
                                         variable=format_selected,
                                         value=1)
            rgb_clamped.grid(row=0, column=0, sticky="W")
            rgb_mean = tk.Radiobutton(frame_formats,
                                      text="RGB promediado",
                                      font="10",
                                      variable=format_selected,
                                      value=2)
            rgb_mean.grid(row=1, column=0, sticky="W")
            yiq_clamped = tk.Radiobutton(frame_formats,
                                         text="YIQ clampeado",
                                         font="10",
                                         variable=format_selected,
                                         value=3)
            yiq_clamped.grid(row=2, column=0, sticky="W")
            yiq_mean = tk.Radiobutton(frame_formats,
                                      text="YIQ promediado",
                                      font="10",
                                      variable=format_selected,
                                      value=4)
            yiq_mean.grid(row=3, column=0, sticky="W")
            yiq_if_darker = tk.Radiobutton(frame_formats,
                                           text="If darker",
                                           font="10",
                                           variable=format_selected,
                                           value=5)
            yiq_if_darker.grid(row=4, column=0, sticky="W")
            format_selected.set(1)
            button_process.config(command=lambda: process_operation(combobox_process.current(),
                                                                    format_selected.get()))


def create_frame_variables(frame_pixel_arithmetic, width_frame_pixel_arithmetic):
    """ CREACION DE LA SECCIÓN DE VARIABLES """
    global frame_formats, combobox_process, button_process, button_image_b
    frame_variables = tk.Frame(frame_pixel_arithmetic,
                               width=width_frame_pixel_arithmetic*0.15,
                               height=frame_pixel_arithmetic.winfo_vrootheight()*0.83,
                               bg="#F9F9F9")
    frame_variables.grid(row=0, column=0, padx=5)
    frame_variables.grid_propagate(False)

    label_title_image_in = tk.Label(frame_variables,
                                    text="Selección de imagen",
                                    font="Roboto 12", bg="#F9F9F9")
    label_title_image_in.grid(row=0, column=0, columnspan=2, pady=3, padx=5)

    label_image_a = tk.Label(frame_variables, text="Cargar imagen A: ",
                             bg="#F9F9F9")
    label_image_a.grid(row=1, column=0, pady=3, padx=3, sticky="E")
    button_image_a = tk.Button(frame_variables, text="Cargar")
    button_image_a.config(width=10, command=upload_image_a)
    button_image_a.grid(row=1, column=1, pady=3, padx=3, sticky="W")

    label_image_b = tk.Label(frame_variables, text="Cargar imagen B: ",
                             bg="#F9F9F9")
    label_image_b.grid(row=2, column=0, pady=3, padx=3, sticky="E")
    button_image_b = tk.Button(frame_variables, text="Cargar")
    button_image_b.config(width=10, command=upload_image_b)
    button_image_b.grid(row=2, column=1, pady=3, padx=3, sticky="W")
    button_image_b['state'] = 'disabled'

    label_title_process = tk.Label(frame_variables,
                                   text="Selección de proceso",
                                   font="Roboto 12", bg="#F9F9F9")
    label_title_process.grid(row=3, column=0, columnspan=2, pady=3, padx=5)
    combobox_process = ttk.Combobox(frame_variables, state="readonly",
                                    width=25)
    combobox_process['values'] = ("Selecciona una operación",
                                  "Suma",
                                  "Resta")
    combobox_process.current(0)
    combobox_process.grid(row=4, column=0, columnspan=2, pady=5)
    combobox_process['state'] = 'disabled'
    combobox_process.bind("<<ComboboxSelected>>", create_frame_formats)

    label_title_format = tk.Label(frame_variables,
                                  text="Selección de formato",
                                  font="Roboto 12", bg="#F9F9F9")
    label_title_format.grid(row=5, column=0, columnspan=2, pady=3, padx=5)
    frame_formats = tk.Frame(frame_variables)
    frame_formats.grid(row=6, column=0, columnspan=2, pady=3, padx=5)

    button_process = tk.Button(frame_variables, text="PROCESAR")
    button_process.config(width=15, font="Roboto 11 bold",
                          bg="#12A14B", fg="white")
    button_process['state'] = 'disabled'
    button_process.grid(row=10, column=0, columnspan=2, pady=15)


def create_frame_pixel_arithmetic(frame_main, screen_width):
    """ CREACION DE LA INTERFAZ ARITMETICA DE PIXELES """
    global frame_image_a, frame_image_b, frame_image_out

    frame_pixel_arithmetic = tk.Frame(frame_main, width=screen_width * 0.96)
    frame_pixel_arithmetic.pack()
    frame_pixel_arithmetic.config(pady=5, padx=5, bg="white")

    width_frame_pixel_arithmetic = frame_pixel_arithmetic.winfo_reqwidth()

    create_frame_variables(frame_pixel_arithmetic,
                           width_frame_pixel_arithmetic)

    frame_image_a = tk.Frame(frame_pixel_arithmetic,
                             width=width_frame_pixel_arithmetic*0.28,
                             height=frame_pixel_arithmetic.winfo_vrootheight()*0.7)
    frame_image_a.grid(row=0, column=1, padx=5)
    frame_image_a.grid_propagate(False)
    label_title_a = tk.Label(frame_image_a,
                             text="Imagen A",
                             font="Roboto 12", padx=5)
    label_title_a.grid(row=0, column=0)

    frame_image_b = tk.Frame(frame_pixel_arithmetic,
                             width=width_frame_pixel_arithmetic*0.28,
                             height=frame_pixel_arithmetic.winfo_vrootheight()*0.7)
    frame_image_b.grid(row=0, column=2, padx=5)
    frame_image_b.grid_propagate(False)
    label_title_b = tk.Label(frame_image_b,
                             text="Imagen B",
                             font="Roboto 12", padx=5)
    label_title_b.grid(row=0, column=0)

    frame_image_out = tk.Frame(frame_pixel_arithmetic,
                               width=width_frame_pixel_arithmetic*0.28,
                               height=frame_pixel_arithmetic.winfo_vrootheight()*0.7)
    frame_image_out.grid(row=0, column=3, padx=5)
    frame_image_out.grid_propagate(False)
    label_title_out = tk.Label(frame_image_out,
                               text="Imagen procesada",
                               font="Roboto 12", padx=5)
    label_title_out.grid(row=0, column=0)
