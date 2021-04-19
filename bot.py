import sys 
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np


token = "1788036923:AAHsklxGfq0s0ch4V-E9uqJ-kFyX8JfxajM"

def start(bot, update):
    try:
        username = update.message.from_user.username
        message = "Hola " + username
        update.message.reply_text(message)
    except Exception as error:
        print ("Error 001 {}".format(error.args[0]))

def echo(bot, update):
    try:
        text = update.message.text
        update.message.reply_text(text)
    except Exception as error:
        print("Error 002 {}".format(error.args[0]))

def help(bot, update):
    try:
        message = "Agrega la imagen del transporte que deseas verificar"
        update.message.reply_text(message)
    except Exception as error:
        print("Error 003 {}".format(error.args[0]))

def error(bot, update, error):
    try:
        print(error)
    except Exception as error:
        print("Error 004 {}".format(error.args[0]))

def getimage(bot, update):
    try:

        message = "Imagen en proceso"
        update.message.reply_text(message)

        file = bot.getFile(update.message.photo[-1].file_id)      
        id = file.file_id 

        filename = os.path.join("descargas/", "{}.jpg".format(id))
        file.download(filename)

        message = "Verificando imagen"
        update.message.reply_text(message)

        prediction = analisis ("descargas/{}.jpg".format(id))
        print(prediction)
        update.message.reply_text(prediction)

    except Exception as e:
        print("Error 007 {}".format(e.args[0]))

def analisis (image_path):
        np.set_printoptions(suppress=True)   

        model = tensorflow.keras.models.load_model('keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        image = Image.open(image_path)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array

        prediction = model.predict(data)
        for i in prediction:
            if i [0] > 0.7:
                resultado = "transportes terrestres"
                return resultado

            elif i [1]> 0.7:
                resultado = "transportes aereos"
                return resultado

            elif i [2]> 0.7:
                resultado = "transportes maritimos"
                return resultado

            elif i [3]> 0.7:
                resultado = "transportes ferrovarios"
                return resultado       

def main():
    try:
        updater = Updater(token)
        dp = updater.dispatcher 

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))

        dp.add_handler(MessageHandler(Filters.text, echo))
        dp.add_handler(MessageHandler(Filters.photo, getimage))

        dp.add_error_handler(error)

        updater.start_polling()
        updater.idle()
        print ("Bot listo")

    except Exception as e:
        print("Error 005 {}".format(e.args[0]))

if _name_ =="_main_":
    try:
        main()
    except Exception as e:
        print("Error 006 {}".format(e.args[0]))