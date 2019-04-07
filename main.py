import re
from bot import wppbot

bot = wppbot('robozin')
bot.treina('treino')
#bot.inicia('Capitalismo Opressor News')
bot.inicia('Fábio Assunção THE BOSS')
bot.saudacao(['bot: Oi, sou um bot','bot: Bora conversar ?'])
ultimo_texto = ''




while True:

    texto = bot.escuta()

    if texto != ultimo_texto and not re.match(r'^bot:', texto):

        ultimo_texto = texto
        texto = texto.replace('', '')
        texto = texto.lower()

        if (texto == 'noticias' or texto == ' noticias' or texto == 'noticia' or texto == ' noticia' or texto == 'notícias' or texto == ' notícias' or texto == 'notícia' or texto == ' notícia'):
            bot.noticias()
        if texto == "erro":
            break
        else:
            bot.responde(texto)