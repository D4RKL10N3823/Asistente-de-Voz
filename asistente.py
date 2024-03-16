<<<<<<< HEAD
import pyttsx3
import speech_recognition as sr
import pywhatkit
import webbrowser
import datetime
import pyautogui
import time

# opciones de voz / idioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'

# escuchar nuestro microfono y devolver el audio comotexto
def trasformar_audio_en_texto():
    # almacenar recognizer en variable
    microfono = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:
        # tiempo de espera
        microfono.pause_threshold = 0.8
        # informar que comenzo la grabacion
        print("ya puedes hablar")
        # guardar lo que escuche como audio
        audio =microfono.listen(origen)

        try:
            # buscar en google
            pedido = microfono.recognize_google(audio, language="es-mx")
            # prueba de que pudo ingresar
            print(f"Dijiste: {pedido}")
            # devolver pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:
            # prueba de que no comprendio el audio
            print("ups, no entendi")
            # devolver error
            return "sigo esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:
            # prueba de que no comprendio el audio
            print("ups, no hay servicio")
            # devolver error
            return "sigo esperando"

        # error inesperado
        except:
            # prueba de que no comprendio el audio
            print("ups, algo ha salido mal")
            # devolver error
            return "sigo esperando"


# Inicializar el motor de texto a voz (pyttsx3) una sola vez al comienzo del programa
engine = pyttsx3.init()
engine.setProperty('voice', id1)
# Función para que el asistente pueda ser escuchado
def hablar(mensaje):
    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dia de la semana
def pedir_dia():
    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)
    # crear variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)
    # diccionario con nombres de dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}
    # decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar que hora es
def pedir_hora():
    # crear una variab;e con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)
    # decir la hora
    hablar(hora)

def pedir_nombre():
    hablar("¡Hola! Soy Yotsuba. Antes de continuar, ¿cuál es tu nombre?")
    nombre = trasformar_audio_en_texto()
    return nombre


# funcion saludo inicial
def saludo_inicial():
    nombre = pedir_nombre()

    # crear variable condatos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'
    # decir el saludo
    hablar(f'{momento} {nombre}, dime en qué te puedo ayudar')


def escribir(texto):  
    pyautogui.press('win')
    pyautogui.write('block de notas')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.write(texto)


def controlar_video(accion):
    if accion == 'pausar':
        pyautogui.press('space')
    elif accion == 'mutear':
        pyautogui.press('m')
    elif accion == 'adelantar':
        pyautogui.press('l')
    elif accion == 'regresar':
        pyautogui.press('j')
    elif accion == 'subir':
        pyautogui.press('up')
    elif accion == 'bajar':
        pyautogui.press('down')
    elif accion == 'pantalla_completa':
        pyautogui.press('f')
    elif accion == 'minimizar':
        pyautogui.press('i')
    

def abrir(programa):
    if programa == 'word':
        pyautogui.press('win')
        pyautogui.write('word')
        pyautogui.press('enter')
    elif programa == 'excel':
        pyautogui.press('win')
        pyautogui.write('excel')
        pyautogui.press('enter')
    elif programa == 'pp':
        pyautogui.press('win')
        pyautogui.write('power point')
        pyautogui.press('enter')

def buscar_en_internet(pedido):
    hablar('Ya mismo estoy en eso')
    consulta = pedido.replace('busca en internet', '')
    pywhatkit.search(consulta)
    hablar('Esto es lo que he encontrado')

def buscar_en_youtube(pedido):
    hablar('Buscando')
    pywhatkit.playonyt(pedido.replace('busca en youtube', ''))

def escribir_nota():
    hablar('Claro, ¿qué texto deseas escribir en el bloc de notas?')
    texto_a_escribir = trasformar_audio_en_texto()
    escribir(texto_a_escribir)

def abrir_sitio_web(url, mensaje):
    hablar(mensaje)
    webbrowser.open(url)


# funcion central del asistente
def pedir_cosas():
    saludo_inicial()

    while True:
        pedido = trasformar_audio_en_texto().lower()

        if 'adiós' in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            break

        # Utilizar un diccionario para mapear comandos a funciones podría simplificar esta estructura
        acciones = {
            'abrir youtube': lambda: abrir_sitio_web('https://www.youtube.com', 'Con gusto, estoy abriendo YouTube'),
            'busca en internet': lambda pedido=pedido: buscar_en_internet(pedido),
            'busca en youtube': lambda pedido=pedido: buscar_en_youtube(pedido),
            'escribir': escribir_nota,
            'abre el navegador': lambda: abrir_sitio_web('https://www.google.com', 'Claro, estoy en eso'),
            'qué día es hoy': pedir_dia,
            'qué hora es': pedir_hora,
            'pausa el video': lambda: controlar_video('pausar'),
            'continúa': lambda: controlar_video('pausar'),
            'adelanta el video': lambda: controlar_video('adelantar'),
            'regresa el video': lambda: controlar_video('regresar'),
            'silencia el video': lambda: controlar_video('mutear'),
            'desmutea el video': lambda: controlar_video('mutear'),
            'pantalla completa': lambda: controlar_video('pantalla_completa'),
            'achica la pantalla': lambda: controlar_video('pantalla_completa'),
            'abre word': lambda: abrir('word'),
            'abre excel': lambda: abrir('excel'),
            'abre power point': lambda: abrir('pp')
        }

        for comando, accion in acciones.items():
            if comando in pedido:
                if comando in ['busca en internet', 'busca en youtube']:
                    accion(pedido)
                else:
                    accion()
                break
        else:
            hablar('No entendí el comando, por favor intenta de nuevo')

pedir_cosas()
=======
import pyttsx3
import speech_recognition as sr
import pywhatkit
import pyjokes
import webbrowser
import datetime
import wikipedia
import pyautogui
import time

# opciones de voz / idioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'

# escuchar nuestro microfono y devolver el audio comotexto
def trasformar_audio_en_texto():
    # almacenar recognizer en variable
    microfono = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:
        # tiempo de espera
        microfono.pause_threshold = 0.8
        # informar que comenzo la grabacion
        print("ya puedes hablar")
        # guardar lo que escuche como audio
        audio =microfono.listen(origen)

        try:
            # buscar en google
            pedido = microfono.recognize_google(audio, language="es-mx")
            # prueba de que pudo ingresar
            print(f"Dijiste: {pedido}")
            # devolver pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:
            # prueba de que no comprendio el audio
            print("ups, no entendi")
            # devolver error
            return "sigo esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:
            # prueba de que no comprendio el audio
            print("ups, no hay servicio")
            # devolver error
            return "sigo esperando"

        # error inesperado
        except:
            # prueba de que no comprendio el audio
            print("ups, algo ha salido mal")
            # devolver error
            return "sigo esperando"


# Inicializar el motor de texto a voz (pyttsx3) una sola vez al comienzo del programa
engine = pyttsx3.init()
engine.setProperty('voice', id1)
# Función para que el asistente pueda ser escuchado
def hablar(mensaje):
    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dia de la semana
def pedir_dia():
    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)
    # crear variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)
    # diccionario con nombres de dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}
    # decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar que hora es
def pedir_hora():
    # crear una variab;e con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)
    # decir la hora
    hablar(hora)

def pedir_nombre():
    hablar("¡Hola! Soy Yotsuba. Antes de continuar, ¿cuál es tu nombre?")
    nombre = trasformar_audio_en_texto()
    return nombre


# funcion saludo inicial
def saludo_inicial():
    nombre = pedir_nombre()

    # crear variable condatos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'
    # decir el saludo
    hablar(f'{momento} {nombre}, dime en qué te puedo ayudar')


def escribir(texto):  # Agrega el argumento 'texto' para que la función reciba el texto a escribir
    pyautogui.press('win')
    pyautogui.write('block de notas')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.write(texto)


def controlar_video(accion):
    if accion == 'pausar':
        pyautogui.press('space')
    elif accion == 'mutear':
        pyautogui.press('m')
    elif accion == 'adelantar':
        pyautogui.press('l')
    elif accion == 'regresar':
        pyautogui.press('j')
    elif accion == 'subir':
        pyautogui.press('up')
    elif accion == 'bajar':
        pyautogui.press('down')
    elif accion == 'pantalla_completa':
        pyautogui.press('f')
    elif accion == 'minimizar':
        pyautogui.press('i')
    

def mover_mouse(accion):
    if accion == 'bajar_mouse':
        # Obtiene las coordenadas actuales del mouse
        x_actual, y_actual = pyautogui.position()
        # Cuántos píxeles hacia abajo deseas mover el mouse
        desplazamiento_abajo = 100
        # Calcula las nuevas coordenadas en el eje y para mover el mouse hacia abajo
        y_destino = y_actual + desplazamiento_abajo
        # Mueve el mouse hacia abajo a la nueva posición
        pyautogui.moveTo(x_actual, y_destino)
    
    elif accion == 'subir_mouse':
        # Obtiene las coordenadas actuales del mouse
        x_actual, y_actual = pyautogui.position()
        # Cuántos píxeles hacia abajo deseas mover el mouse
        desplazamiento_arriba = 100
        # Calcula las nuevas coordenadas en el eje y para mover el mouse hacia abajo
        y_destino = y_actual - desplazamiento_arriba
        # Mueve el mouse hacia abajo a la nueva posición
        pyautogui.moveTo(x_actual, y_destino)
    elif accion == 'derecha_mouse':
        # Obtiene las coordenadas actuales del mouse
        x_actual, y_actual = pyautogui.position()
        # Cuántos píxeles hacia abajo deseas mover el mouse
        desplazamiento_derecha = 100
        # Calcula las nuevas coordenadas en el eje y para mover el mouse hacia abajo
        x_destino = x_actual + desplazamiento_derecha
        # Mueve el mouse hacia abajo a la nueva posición
        pyautogui.moveTo(x_destino, y_actual)
    elif accion == 'izq_mouse':
        # Obtiene las coordenadas actuales del mouse
        x_actual, y_actual = pyautogui.position()
        # Cuántos píxeles hacia abajo deseas mover el mouse
        desplazamiento_izq = 100
        # Calcula las nuevas coordenadas en el eje y para mover el mouse hacia abajo
        x_destino = x_actual - desplazamiento_izq
        # Mueve el mouse hacia abajo a la nueva posición
        pyautogui.moveTo(x_destino, y_actual)
    elif accion == 'video':
        pyautogui.moveTo(980,260)
    elif accion == 'like':
        pyautogui.moveTo(560,700)
    elif accion == 'imagenes':
        pyautogui.moveTo(180,170)
    elif accion == 'presionar':
        pyautogui.click()


def abrir(programa):
    if programa == 'word':
        pyautogui.press('win')
        pyautogui.write('word')
        pyautogui.press('enter')
    elif programa == 'excel':
        pyautogui.press('win')
        pyautogui.write('excel')
        pyautogui.press('enter')
    elif programa == 'pp':
        pyautogui.press('win')
        pyautogui.write('power point')
        pyautogui.press('enter')


def abrir_sitio_web(url, mensaje):
    hablar(mensaje)
    webbrowser.open(url)


# funcion central del asistente
def pedir_cosas():
    # activar saludo inicial
    saludo_inicial()
    # variable de corte
    comenzar = True
    # loop central
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = trasformar_audio_en_texto().lower()  # Agregar esta línea para obtener el valor actualizado de pedido

        # activar el micro y guardar el pedido en un string
        if 'abrir youtube' in pedido:
            abrir_sitio_web('https://www.youtube.com', 'Con gusto, estoy abriendo YouTube')
            continue
        elif 'abre el navegador' in pedido:
            abrir_sitio_web('https://www.google.com', 'Claro, estoy en eso')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'busca en youtube' in pedido: 
            hablar('Buscando')
            pywhatkit.playonyt(pedido)
            continue
        elif 'pausa el video' in pedido:
            controlar_video('pausar')
            hablar('Video pausado')
            continue
        elif 'continúa' in pedido:
            controlar_video('pausar')
            hablar('Video despausado')
            continue
        elif 'adelanta el video' in pedido:
            controlar_video('adelantar')
            hablar('Video adelantado 5 segundos')
            continue
        elif 'regresa el video' in pedido:
            controlar_video('regresar')
            hablar('Regresando el video')
            continue
        elif 'sube el volumen' in pedido:
            for _ in range(4):
                controlar_video('subir')
            hablar('Subiendo el volumen')
            continue
        elif 'baja el volumen' in pedido:
            for _ in range(4):
                controlar_video('bajar')
            hablar('Bajando el volumen')
            continue
        elif 'silencia el video' in pedido:
            controlar_video('mutear')
            hablar('Video silenciado')
            continue
        elif 'desmutea el video' in pedido:
            controlar_video('mutear')
            hablar('Video desmuteado')
            continue
        elif 'pantalla completa' in pedido:
            controlar_video('pantalla_completa')
            hablar('Poniendo el video en pantalla completa')
            continue
        elif 'achica la pantalla' in pedido:
            controlar_video('pantalla_completa')
            hablar('Quitando el video de pantalla completa')
            continue
        elif 'minimiza el video' in pedido:
            controlar_video('minimizar')
            hablar('Video minimizado')
            continue
        elif 'mouse abajo' in pedido:
            mover_mouse('bajar_mouse')
            hablar('Moviendo mouse hacia abajo')
            continue
        elif 'subir mouse' in pedido:
            mover_mouse('subir_mouse')
            hablar('Moviendo mouse hacia arriba')
            continue
        elif 'mover mouse derecha' in pedido:
            mover_mouse('derecha_mouse')
            hablar('Moviendo mouse hacia la derecha')
            continue
        elif 'mover mouse izquierda' in pedido:
            mover_mouse('izq_mouse')
            hablar('Moviendo mouse hacia la izquierda')
            continue
        elif 'presionar' in pedido:
            mover_mouse('presionar')
            hablar('Presionadno')
            continue
        elif 'video' in pedido:
            mover_mouse('video')
            hablar('moviendo mouse')
            continue
        elif 'like' in pedido:
            mover_mouse('like')
            hablar('Dando like')
        elif 'imágenes' in pedido:
            mover_mouse('imagenes')
            hablar('Abriendo imagenes')
        elif 'abre word' in pedido:
            abrir('word')
            hablar('Abriendo Word')
            continue
        elif 'abre excel' in pedido:
            abrir('excel')
            hablar('Abriendo Excel')
            continue
        elif 'abre power point' in pedido:
            abrir('pp')
            hablar('Abriendo Power Point')
            continue
        elif 'baja' in pedido:
            for _ in range(29):
                controlar_video('bajar')
            hablar('Bajando')
            continue
        elif 'escribir' in pedido:
            hablar('Claro, ¿qué texto deseas escribir en el bloc de notas?')
            texto_a_escribir = trasformar_audio_en_texto()  # Escucha el texto que deseas escribir
            escribir(texto_a_escribir) 
        elif 'Dime un chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'adiós' in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            break

pedir_cosas()
>>>>>>> 9f5f3225688f8c5b5b8de0dbe325e283324aed14
