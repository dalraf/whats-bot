import re
from bot import wppbot
from time import sleep

bot = wppbot('robozin')
#bot.treina('treino')
#bot.inicia('GRUPO SÉRIO 106')
bot.inicia('Fábio Assunção THE BOSS')
#bot.saudacao(['bot: Oi, sou um bot','bot: Bora conversar ?'])
ultimo_texto = ''
botname = 'Fábio Assunção:'



while True:

    texto = bot.escuta()

    if texto != ultimo_texto and not re.match(r'^' + botname, texto):

        ultimo_texto = texto
        texto = texto.replace('', '')
        texto = texto.lower()

        if texto != "erro":
            bot.responde(texto,botname)
    sleep(2)