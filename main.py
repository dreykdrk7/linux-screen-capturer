from config import TOKEN, GROUP_ID, IMAGE_FOLDER
import telebot
import os
from time import sleep
from PIL import ImageGrab


bot = telebot.TeleBot(TOKEN)


def take_screenshot(initial_id, current_count):
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
    
    screenshot_filename = os.path.join(IMAGE_FOLDER, f"{initial_id + current_count}.png")
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_filename)
    return screenshot_filename


if __name__ == '__main__':

    new_session_msg = input('Introduce un texto para identificar la nueva sesión de capturas:\n')
    sleep_between_captures = float(input('Establece un tiempo de retardo entre las capturas (en minutos):\n')) * 60 
    max_iteration_cycles = int(input('Número de veces que quieres repetir el proceso (0 para repetir de forma indefinida):\n'))
    
    initial_msg = bot.send_message(GROUP_ID, new_session_msg, parse_mode='Markdown')
    initial_msg_id = initial_msg.message_id

    current_count = 1
    messages_to_delete = []

    os.system('clear')
    print(f"Resumen de la sesión:\n- Texto de identificación: {new_session_msg}\n- Retardo entre capturas: {sleep_between_captures / 60} minutos\n- Número máximo de ciclos: {'Infinito' if max_iteration_cycles == 0 else max_iteration_cycles}")

    while max_iteration_cycles == 0 or current_count <= max_iteration_cycles:
        screenshot_filename = take_screenshot(initial_msg_id, current_count)

        # Enviar la captura de pantalla al grupo
        with open(screenshot_filename, 'rb') as photo:
            sent_photo_msg = bot.send_photo(GROUP_ID, photo)
            messages_to_delete.append(sent_photo_msg.message_id)
            print(f"Captura realizada y enviada correctamente: {screenshot_filename}")
        
        # Eliminar mensajes antiguos si hemos alcanzado 20 imágenes
        if len(messages_to_delete) > 20:
            # Eliminar el mensaje de Telegram
            oldest_message_id = messages_to_delete.pop(0)
            bot.delete_message(GROUP_ID, oldest_message_id)
            
            # Calcular el nombre del archivo de la imagen más antigua basándonos en current_count
            oldest_image_number = current_count - len(messages_to_delete) - 20
            image_path_to_delete = f"{IMAGE_FOLDER}/{initial_msg_id + oldest_image_number}.png"
            
            # Eliminar el archivo de imagen local
            if os.path.exists(image_path_to_delete):
                os.remove(image_path_to_delete)
                print(f"Imagen borrada localmente: {image_path_to_delete}")

        current_count += 1
        sleep(sleep_between_captures)

    print("Sesión finalizada.")
