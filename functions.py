""" FUNCIONES PARA EL PROCESAMIENTO DE IMAGENES """
import numpy


def yiq_a_rgb(imagen_yiq):
    """ TRANSFORMACION DE YIQ A RGB """
    imagen_rgb = numpy.zeros(imagen_yiq.shape)
    imagen_rgb[:, :, 0] = numpy.clip(
        1*imagen_yiq[:, :, 0] + 0.9663*imagen_yiq[:, :, 1] + 0.6210*imagen_yiq[:, :, 2], 0, 1)
    imagen_rgb[:, :, 1] = numpy.clip(
        1*imagen_yiq[:, :, 0] + -0.2721*imagen_yiq[:, :, 1] + -0.6474*imagen_yiq[:, :, 2], 0, 1)
    imagen_rgb[:, :, 2] = numpy.clip(
        1*imagen_yiq[:, :, 0] + -1.1070*imagen_yiq[:, :, 1] + 1.7046*imagen_yiq[:, :, 2], 0, 1)

    return imagen_rgb


def rgb_a_yiq(imagen_rgb):
    """ TRANSFORMACION DE RGB A YIQ """
    imagen_yiq = numpy.zeros(imagen_rgb.shape)
    imagen_yiq[:, :, 0] = numpy.clip(
        0.299000*imagen_rgb[:, :, 0] + 0.587000*imagen_rgb[:, :, 1] + 0.114000*imagen_rgb[:, :, 2], 0, 1)
    imagen_yiq[:, :, 1] = numpy.clip(0.595716*imagen_rgb[:, :, 0] + -0.274453 *
                                     imagen_rgb[:, :, 1] + -0.321263*imagen_rgb[:, :, 2], -0.5957, 0.5957)
    imagen_yiq[:, :, 2] = numpy.clip(0.211456*imagen_rgb[:, :, 0] + -0.522591 *
                                     imagen_rgb[:, :, 1] + 0.311135*imagen_rgb[:, :, 2], -0.5226, 0.5226)

    return imagen_yiq


# GENERACION DE KERNELs - FILTROS PASA BAJOS

def generar_kernel_plano(dimension):
    """ GENERAR KERNEL PLANO """
    matriz_base = numpy.ones([dimension, dimension])
    kernel = matriz_base / matriz_base.sum()

    return kernel


def generar_kernel_bartlett(dimension):
    """ GENERAR KERNEL DE BARTLETT """
    base = (dimension+1)//2 - numpy.abs(numpy.arange(dimension)-dimension//2)
    matriz_base = numpy.outer(base, base.T)
    kernel = matriz_base / matriz_base.sum()

    return kernel


def generar_kernel_gaussiano(dimension):
    """ GENERAR KERNEL GAUSSIANO """
    def pascal_triangle(steps, last_layer=numpy.array([1])):
        if steps == 1:
            return last_layer
        next_layer = numpy.array([1, *(last_layer[:-1]+last_layer[1:]), 1])
        return pascal_triangle(steps-1, next_layer)

    base = pascal_triangle(dimension)
    matriz_base = numpy.outer(base, base.T)
    kernel = matriz_base / matriz_base.sum()

    return kernel


def generar_kernel_laplaciano(vecinos):
    """ GENERAR KERNEL LAPLACIANO """
    match vecinos:
        case 4:
            kernel = numpy.matrix([[0, -1, 0],
                                   [-1, 4, -1],
                                   [0, -1, 0]])
        case 8:
            kernel = numpy.matrix([[-1, -1, -1],
                                   [-1, 8, -1],
                                   [-1, -1, -1]])
        case _:
            print("error...")

    return kernel


def generar_kernel_sobel(direccion):
    """ GENERAR KERNEL SOBEL """
    match direccion:
        case 0:
            kernel = numpy.matrix([[-1, -2, -1],
                                   [0, 0, 0],
                                   [1, 2, 1]])
        case 1:
            kernel = numpy.matrix([[0, -1, -2],
                                   [1, 0, -1],
                                   [2, 1, 0]])
        case 2:
            kernel = numpy.matrix([[1, 0, -1],
                                   [2, 0, -2],
                                   [1, 0, -1]])
        case 3:
            kernel = numpy.matrix([[2, 1, 0],
                                   [1, 0, -1],
                                   [0, -1, -2]])
        case 4:
            kernel = numpy.matrix([[1, 2, 1],
                                   [0, 0, 0],
                                   [-1, -2, -1]])
        case 5:
            kernel = numpy.matrix([[0, 1, 2],
                                   [-1, 0, 1],
                                   [-2, -1, 0]])
        case 6:
            kernel = numpy.matrix([[-1, 0, 1],
                                   [-2, 0, 2],
                                   [-1, 0, 1]])
        case 7:
            kernel = numpy.matrix([[-2, -1, 0],
                                   [-1, 0, 1],
                                   [0, 1, 2]])
        case _:
            print("error...")

    return kernel


def generar_kernel_dog(dimension_a=5, dimension_b=3):
    """ GENERAR KERNEL DOG """
    kernel_a = generar_kernel_gaussiano(dimension_a)
    kernel_b = generar_kernel_gaussiano(dimension_b)
    kernel_c = numpy.zeros([dimension_a, dimension_a])
    for i in range((dimension_a-dimension_b)//2, dimension_b+1):
        for j in range((dimension_a-dimension_b)//2, dimension_b+1):
            kernel_c[i, j] = kernel_b[i - ((dimension_a-dimension_b)//2),
                                      j-((dimension_a-dimension_b)//2)]
    kernel = numpy.clip(kernel_c - kernel_a, 0, 1)

    return kernel


def generar_convolucion(imagen, kernel):
    """ FUNCION DE CONVOLUCION """
    imagen_nueva = numpy.zeros(
        [imagen.shape[0] - kernel.shape[0] + 1, imagen.shape[0] - kernel.shape[1] + 1])
    for i in range(kernel.shape[0] // 2, imagen.shape[0] - kernel.shape[0] // 2):
        for j in range(kernel.shape[1] // 2, imagen.shape[0] - kernel.shape[1] // 2):
            acumulador = 0
            for k in range(0, kernel.shape[0]):
                for l in range(0, kernel.shape[1]):
                    acumulador += imagen[i - kernel.shape[0] // 2 +
                                         k, j - kernel.shape[0] // 2 + l] * kernel[k, l]
            imagen_nueva[i - kernel.shape[0] // 2,
                         j - kernel.shape[0] // 2] = numpy.clip(acumulador, 0, 1)

    return imagen_nueva
