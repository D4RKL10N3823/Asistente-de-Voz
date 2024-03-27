import pyttsx3
import speech_recognition as sr
import pywhatkit
import webbrowser
import datetime
import pyautogui
import time

id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'

def trasformar_audio_en_texto():
    microfono = sr.Recognizer()

    with sr.Microphone() as origen:
        microfono.pause_threshold = 0.8
        print("ya puedes hablar")
        audio =microfono.listen(origen)

        try:
            pedido = microfono.recognize_google(audio, language="es-mx")
            print(f"Dijiste: {pedido}")
            return pedido

        except sr.UnknownValueError:
            print("ups, no entendi")
            return "sigo esperando"

        except sr.RequestError:
            print("ups, no hay servicio")
            return "sigo esperando"

        except:
            print("ups, algo ha salido mal")
            return "sigo esperando"


engine = pyttsx3.init()
engine.setProperty('voice', id1)

def hablar(mensaje):
    engine.say(mensaje)
    engine.runAndWait()


def pedir_dia():
    dia = datetime.date.today()
    print(dia)
    dia_semana = dia.weekday()
    print(dia_semana)
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}
    hablar(f'Hoy es {calendario[dia_semana]}')


def pedir_hora():
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)
    
    hablar(hora)

def pedir_nombre():
    hablar("¡Hola! Soy Yotsuba. Antes de continuar, ¿cuál es tu nombre?")
    nombre = trasformar_audio_en_texto()
    return nombre


def saludo_inicial():
    nombre = pedir_nombre()

    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'
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
    
def pedir_cosas():
    saludo_inicial()

    while True:
        pedido = trasformar_audio_en_texto().lower()

        if 'adiós' in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            break

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
