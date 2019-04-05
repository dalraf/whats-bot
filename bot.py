import os
import time
import re
import requests
import json
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot import ChatBot
from selenium import webdriver




class wppbot:
    dir_path = os.getcwd()

    def __init__(self, nome_bot):
        print(self.dir_path)
        self.bot = ChatBot(nome_bot,logic_adapters=[
            {
              'import_path': 'chatterbot.logic.BestMatch',
              'default_response': 'Xii, Cara, não entendi',
              'maximum_similarity_threshold': 0.50
            }
          ]
        )


        self.bot.set_trainer(ListTrainer)

        self.chrome = self.dir_path+'/chromedriver'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir="+self.dir_path+"\profile\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)
        self.ultima_resposta = ''

    def inicia(self,nome_contato):

        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)

        self.caixa_de_pesquisa = self.driver.find_element_by_class_name('jN-F5')


        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)
        print(nome_contato)
        self.contato = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(nome_contato))
        self.contato.click()
        time.sleep(2)



    def saudacao(self,frase_inicial):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_2S1VP')

        if type(frase_inicial) == list:
            for frase in frase_inicial:
                self.caixa_de_mensagem.send_keys(frase)
                time.sleep(1)
                self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
                self.botao_enviar.click()
                time.sleep(1)
        else:
            return False

    def escuta(self):
        post = self.driver.find_elements_by_class_name('_3_7SH')
        ultimo = len(post) - 1
        texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text
        return texto


    def responde(self,texto):
        response = self.bot.get_response(texto)
        if self.ultima_resposta != "":
            novo = []
            novo.append(texto)
            novo.append(self.ultima_resposta)
            self.bot.train(novo)       
        self.ultima_resposta = response
        response = str(response)
        response = 'bot: ' + response
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_2S1VP')
        self.caixa_de_mensagem.send_keys(response)
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
        self.botao_enviar.click()

    def treina(self,nome_pasta):
        self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.train('chatterbot.corpus.portuguese')
        self.bot.set_trainer(ListTrainer)
