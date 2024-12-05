""" FUNCIONES PARA EL PROCESAMIENTO DE IMAGENES """
import numpy
from scipy import ndimage


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

# ARITMETICA DE PIXELES ---------------------------------------------------------------------------


def suma(image_a, image_b, format_selected):
    """ SUMA DE DOS IMAGENES """
    image_c = numpy.zeros(image_a.shape)
    match format_selected:
        case 1:
            image_c[:, :, 0] = numpy.clip(image_a[:, :, 0] + image_b[:, :, 0],
                                          0, 1)
            image_c[:, :, 1] = numpy.clip(image_a[:, :, 1] + image_b[:, :, 1],
                                          0, 1)
            image_c[:, :, 2] = numpy.clip(image_a[:, :, 2] + image_b[:, :, 2],
                                          0, 1)
        case 2:
            image_c[:, :, 0] = numpy.clip((image_a[:, :, 0] + image_b[:, :, 0])/2,
                                          0, 1)
            image_c[:, :, 1] = numpy.clip((image_a[:, :, 1] + image_b[:, :, 1])/2,
                                          0, 1)
            image_c[:, :, 2] = numpy.clip((image_a[:, :, 2] + image_b[:, :, 2])/2,
                                          0, 1)
        case 3:
            image_a_yiq = rgb_a_yiq(image_a)
            image_b_yiq = rgb_a_yiq(image_b)

            image_c[:, :, 0] = numpy.clip(image_a_yiq[:, :, 0] + image_b_yiq[:, :, 0],
                                          0, 1)
            image_c[:, :, 1] = (image_a_yiq[:, :, 0] * image_a_yiq[:, :, 1] + image_b_yiq[:, :, 0] *
                                image_b_yiq[:, :, 1]) / numpy.clip((image_a_yiq[:, :, 0] + image_b_yiq[:, :, 0]), 0.003922, 1)
            image_c[:, :, 2] = (image_a_yiq[:, :, 0] * image_a_yiq[:, :, 2] + image_b_yiq[:, :, 0] *
                                image_b_yiq[:, :, 2]) / numpy.clip((image_a_yiq[:, :, 0] + image_b_yiq[:, :, 0]), 0.003922, 1)

            image_c = yiq_a_rgb(image_c)
        case 4:
            image_a_yiq = rgb_a_yiq(image_a)
            image_b_yiq = rgb_a_yiq(image_b)

            image_c[:, :, 0] = numpy.clip((image_a_yiq[:, :, 0] + image_b_yiq[:, :, 0])/2,
                                          0, 1)
            image_c[:, :, 1] = (image_a_yiq[:, :, 0] * image_a_yiq[:, :, 1] + image_b_yiq[:, :, 0] *
                                image_b_yiq[:, :, 1]) / numpy.clip((image_a_yiq[:, :, 0] + image_b_yiq[:, :, 0]), 0.003922, 1)
            image_c[:, :, 2] = (image_a_yiq[:, :, 0] * image_a_yiq[:, :, 2] + image_b_yiq[:, :, 0] *
                                image_b_yiq[:, :, 2]) / numpy.clip((image_a_yiq[:, :, 0] + image_b_yiq[:, :, 0]), 0.003922, 1)

            image_c = yiq_a_rgb(image_c)
        case 5:
            image_a_yiq = rgb_a_yiq(image_a)
            image_b_yiq = rgb_a_yiq(image_b)

            for i in range(0, image_a_yiq.shape[0]):
                for j in range(0, image_a_yiq.shape[1]):
                    if image_a_yiq[i, j, 0] > image_b_yiq[i, j, 0]:
                        image_c[i, j, 0] = image_a_yiq[i, j, 0]
                        image_c[i, j, 1] = image_a_yiq[i, j, 1]
                        image_c[i, j, 2] = image_a_yiq[i, j, 2]
                    else:
                        image_c[i, j, 0] = image_b_yiq[i, j, 0]
                        image_c[i, j, 1] = image_b_yiq[i, j, 1]
                        image_c[i, j, 2] = image_b_yiq[i, j, 2]

            image_c = yiq_a_rgb(image_c)

    return image_c


def resta(image_a, image_b, format_selected):
    """ RESTA DE DOS IMAGENES """
    image_c = numpy.zeros(image_a.shape)
    match format_selected:
        case 1:
            image_c[:, :, 0] = numpy.clip(image_a[:, :, 0] - image_b[:, :, 0],
                                          0, 1)
            image_c[:, :, 1] = numpy.clip(image_a[:, :, 1] - image_b[:, :, 1],
                                          0, 1)
            image_c[:, :, 2] = numpy.clip(image_a[:, :, 2] - image_b[:, :, 2],
                                          0, 1)
        case 2:
            image_c[:, :, 0] = numpy.clip((image_a[:, :, 0] - image_b[:, :, 0])/2,
                                          0, 1)
            image_c[:, :, 1] = numpy.clip((image_a[:, :, 1] - image_b[:, :, 1])/2,
                                          0, 1)
            image_c[:, :, 2] = numpy.clip((image_a[:, :, 2] - image_b[:, :, 2])/2,
                                          0, 1)
        case 3:
            image_a_yiq = rgb_a_yiq(image_a)
            image_b_yiq = rgb_a_yiq(image_b)

            image_c[:, :, 0] = numpy.clip(image_a_yiq[:, :, 0] - image_b_yiq[:, :, 0],
                                          0, 1)
            image_c[:, :, 1] = (image_a_yiq[:, :, 0] * image_a_yiq[:, :, 1] + image_b_yiq[:, :, 0] *
                                image_b_yiq[:, :, 1]) / numpy.clip((image_a_yiq[:, :, 0] + image_b_yiq[:, :, 0]), 0.003922, 1)
            image_c[:, :, 2] = (image_a_yiq[:, :, 0] * image_a_yiq[:, :, 2] + image_b_yiq[:, :, 0] *
                                image_b_yiq[:, :, 2]) / numpy.clip((image_a_yiq[:, :, 0] + image_b_yiq[:, :, 0]), 0.003922, 1)

            image_c = yiq_a_rgb(image_c)
        case 4:
            image_a_yiq = rgb_a_yiq(image_a)
            image_b_yiq = rgb_a_yiq(image_b)

            image_c[:, :, 0] = numpy.clip((image_a_yiq[:, :, 0] - image_b_yiq[:, :, 0])/2,
                                          0, 1)
            image_c[:, :, 1] = (image_a_yiq[:, :, 0] * image_a_yiq[:, :, 1] + image_b_yiq[:, :, 0] *
                                image_b_yiq[:, :, 1]) / numpy.clip((image_a_yiq[:, :, 0] + image_b_yiq[:, :, 0]), 0.003922, 1)
            image_c[:, :, 2] = (image_a_yiq[:, :, 0] * image_a_yiq[:, :, 2] + image_b_yiq[:, :, 0] *
                                image_b_yiq[:, :, 2]) / numpy.clip((image_a_yiq[:, :, 0] + image_b_yiq[:, :, 0]), 0.003922, 1)

            image_c = yiq_a_rgb(image_c)
        case 5:
            image_a_yiq = rgb_a_yiq(image_a)
            image_b_yiq = rgb_a_yiq(image_b)

            for i in range(0, image_a_yiq.shape[0]):
                for j in range(0, image_a_yiq.shape[1]):
                    if image_a_yiq[i, j, 0] < image_b_yiq[i, j, 0]:
                        image_c[i, j, 0] = image_a_yiq[i, j, 0]
                        image_c[i, j, 1] = image_a_yiq[i, j, 1]
                        image_c[i, j, 2] = image_a_yiq[i, j, 2]
                    else:
                        image_c[i, j, 0] = image_b_yiq[i, j, 0]
                        image_c[i, j, 1] = image_b_yiq[i, j, 1]
                        image_c[i, j, 2] = image_b_yiq[i, j, 2]

            image_c = yiq_a_rgb(image_c)

    return image_c


# CONVOLUCION -------------------------------------------------------------------------------------


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


# MORFOLOGIA --------------------------------------------------------------------------------------

def dilatar(imagen, kernel, tipo_kernel, color_objetivo=1):
    """ DILATACION DE LA IMAGEN """
    imagen_dilatada = numpy.zeros(imagen.shape)
    if color_objetivo == 0:
        imagen = abs(imagen-1)
    match tipo_kernel:
        case 0:
            imagen_dilatada = ndimage.grey_dilation(imagen, size=kernel.shape)
        case 1:
            imagen_dilatada = ndimage.grey_dilation(imagen, footprint=kernel)
        case _:
            print("error...")
    if color_objetivo == 0:
        imagen_dilatada = abs(imagen_dilatada-1)

    return imagen_dilatada


def erosionar(imagen, kernel, tipo_kernel, color_objetivo=1):
    """ EROSION DE LA IMAGEN """
    imagen_erosionada = numpy.zeros(imagen.shape)
    if color_objetivo == 0:
        imagen = abs(imagen-1)
    match tipo_kernel:
        case 0:
            imagen_erosionada = ndimage.grey_erosion(imagen, size=kernel.shape)
        case 1:
            imagen_erosionada = ndimage.grey_erosion(imagen, footprint=kernel)
        case _:
            print("error...")
    if color_objetivo == 0:
        imagen_erosionada = abs(imagen_erosionada-1)

    return imagen_erosionada


def apertura(imagen, kernel, tipo_kernel, color_objetivo=1):
    """ APERTURA DE IMAGEN """
    imagen_abierta = numpy.zeros(imagen.shape)
    if color_objetivo == 0:
        imagen = abs(imagen-1)
    match tipo_kernel:
        case 0:
            imagen_abierta = ndimage.grey_opening(imagen, size=kernel.shape)
        case 1:
            imagen_abierta = ndimage.grey_opening(imagen, footprint=kernel)
        case _:
            print("error...")
    if color_objetivo == 0:
        imagen_abierta = abs(imagen_abierta-1)

    return imagen_abierta


def cierre(imagen, kernel, tipo_kernel, color_objetivo=1):
    """ CIERRE DE IMAGEN """
    imagen_cerrada = numpy.zeros(imagen.shape)
    if color_objetivo == 0:
        imagen = abs(imagen-1)
    match tipo_kernel:
        case 0:
            imagen_cerrada = ndimage.grey_closing(imagen, size=kernel.shape)
        case 1:
            imagen_cerrada = ndimage.grey_closing(imagen, footprint=kernel)
        case _:
            print("error...")
    if color_objetivo == 0:
        imagen_cerrada = abs(imagen_cerrada-1)

    return imagen_cerrada


def borde_exterior(imagen, kernel, tipo_kernel, color_objetivo):
    """ OBTENCION DEL BORDE EXTERIOR DE LA IMAGEN """
    imagen_b_e = numpy.zeros(imagen.shape)
    if color_objetivo == 0:
        imagen = abs(imagen-1)
    match tipo_kernel:
        case 0:
            imagen_b_e = ndimage.grey_dilation(imagen,
                                               size=kernel.shape)-imagen
        case 1:
            imagen_b_e = ndimage.grey_dilation(imagen,
                                               footprint=kernel)-imagen
        case _:
            print("error...")
    if color_objetivo == 0:
        imagen_b_e = abs(imagen_b_e-1)

    return imagen_b_e


def borde_interior(imagen, kernel, tipo_kernel, color_objetivo):
    """ OBTENCION DEL BORDE INTERIOR DE LA IMAGEN """
    imagen_b_i = numpy.zeros(imagen.shape)
    if color_objetivo == 0:
        imagen = abs(imagen-1)
    match tipo_kernel:
        case 0:
            imagen_b_i = imagen - ndimage.grey_erosion(imagen,
                                                       size=kernel.shape)
        case 1:
            imagen_b_i = imagen - ndimage.grey_erosion(imagen,
                                                       footprint=kernel)
        case _:
            print("error...")
    if color_objetivo == 0:
        imagen_b_i = abs(imagen_b_i-1)

    return imagen_b_i


def gradiente(imagen, kernel, tipo_kernel, color_objetivo):
    """ OBTENCION GRADIENTE DE LA IMAGEN """
    imagen_gradiente = numpy.zeros(imagen.shape)
    if color_objetivo == 0:
        imagen = abs(imagen-1)
    match tipo_kernel:
        case 0:
            imagen_dilatada = ndimage.grey_dilation(imagen, size=kernel.shape)
            imagen_erosionada = ndimage.grey_erosion(imagen, size=kernel.shape)
            imagen_gradiente = imagen_dilatada - imagen_erosionada
        case 1:
            imagen_dilatada = ndimage.grey_dilation(imagen, footprint=kernel)
            imagen_erosionada = ndimage.grey_erosion(imagen, footprint=kernel)
            imagen_gradiente = imagen_dilatada - imagen_erosionada
        case _:
            print("error...")
    if color_objetivo == 0:
        imagen_gradiente = abs(imagen_gradiente-1)

    return imagen_gradiente


def mediana(imagen, kernel, color_objetivo):
    """ CALCULO DE MEDIANA DE LA IMAGEN """
    imagen_mediana = numpy.zeros(
        (numpy.array(imagen.shape)-numpy.array(kernel.shape)+1))
    if color_objetivo == 0:
        imagen = abs(imagen-1)
    for x in range(imagen_mediana.shape[0]):
        for y in range(imagen_mediana.shape[1]):
            imagen_mediana[x, y] = numpy.median(
                imagen[x:x+kernel.shape[0], y:y+kernel.shape[1]]*kernel)
    if color_objetivo == 0:
        imagen_mediana = abs(imagen_mediana-1)

    return imagen_mediana


def generar_kernel(radio, tipo, umbral=0.3):
    """ GENERACION DE KERNEL PARA MORFOLOGIA """
    match tipo:
        case 0:
            kernel_cuadrado = numpy.ones(
                (radio*2+1, radio*2+1), dtype=numpy.bool_)
            return kernel_cuadrado
        case 1:
            vector = numpy.linspace(-radio, radio, radio*2+1)
            [x, y] = numpy.meshgrid(vector, vector)
            kernel_circular = (x**2 + y**2)**0.5 < (radio + umbral)
            return kernel_circular
        case _:
            print("error...")
