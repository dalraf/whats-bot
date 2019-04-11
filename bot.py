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
        self.bot = ChatBot(nome_bot)
        self.botname = nome_bot

        self.bot.set_trainer(ListTrainer)

        self.chrome = self.dir_path+'/chromedriver'
        
        self.options = webdriver.ChromeOptions()
        #self.options.headless = True
        self.options.add_argument(r"user-data-dir="+self.dir_path+"/profile/wpp")
        #self.options.add_argument("--headless") 
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)
        self.ultima_resposta = ''

    def inicia(self,nome_contato):

        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)
        
        try:
            self.contato = self.driver.find_element_by_class_name('_2wP_Y')
            self.contato.click()
            time.sleep(2)
        except:
            pass



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
        time.sleep(1)
        unread = self.driver.find_elements_by_class_name("OUeyt")
        if len(unread) > 0:
            ele = unread[-1]
            self.action = webdriver.common.action_chains.ActionChains(self.driver)
            self.action.move_to_element_with_offset(ele, 0, -20)
            try:
                self.action.click()
                self.action.perform()
                self.action.click()
                self.action.perform()
            except:
                pass
        
        try:
            nome = self.driver.find_elements_by_class_name('_1wjpf')[-1].text
            print("usuário é:" + nome)
        except:
            pass
        post = self.driver.find_elements_by_class_name('_3_7SH')
        ultimo = len(post) - 1

        try:
            self.ultima_resposta = post[ultimo - 1].find_element_by_css_selector('span.selectable-text').text.replace(self.botname ,'')
        except Exception as error:
            print(error)
            self.ultima_resposta = ""

        try:
            texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text
        except Exception as error:
            print(error)
            texto = "erro"
        return texto


    def responde(self,texto):
        print("Pergunta:" + " " + texto)
        print("Ultimo texto:" + " " + self.ultima_resposta)
        if self.ultima_resposta != "":
            novo = []
            novo.append(self.ultima_resposta)
            novo.append(texto)
            print("Treinamento:" + " " + str(novo))
            self.bot.train(novo)
        response = self.bot.get_response(texto)
        print("Resposta:" + " " + str(response) + " " + str(response.confidence))            
        if response.confidence > 0:
            response = str(response)
            response = self.botname + response
#            response = "oi"
            self.caixa_de_mensagem = self.driver.find_element_by_class_name('_2S1VP')
            self.caixa_de_mensagem.send_keys(response)
            time.sleep(1)
            self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
            self.botao_enviar.click()
        else:
            self.ultima_resposta = texto

    def treina(self,nome_pasta):
        self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.train('chatterbot.corpus.portuguese')
        self.bot.set_trainer(ListTrainer)
