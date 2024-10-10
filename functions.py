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
    kernel = numpy.ones([dimension, dimension])
    suma = dimension*dimension
    kernel = kernel / suma

    return kernel


def generar_convolucion(imagen, kernel):
    """ FUNCION DE CONVOLUCION PASA BAJOS """
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
                         j - kernel.shape[0] // 2] = acumulador

    return imagen_nueva
