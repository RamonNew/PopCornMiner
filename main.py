#coding: utf-8

import time

from uclcoin import KeyPair, Transaction, Block
import requests
url = 'https://moeda.ucl.br'

from tkinter import Widget

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


from kivy.config import Config
Config.set("modules", "console", "")

#Armazena saldo para a primeira inicialização
res = requests.get(f'{url}/balance/02d9475b6a68b3b4bab991ae537479e08e3279bda23ac8e77edef8c1eba6b326e7')
res = res.json()
balance = res['balance']

#Declaração de variavel de QTD Minerado após a iniciação do programa
qtdMinerado = 0

#Variavel tempo ultimo minerado, inicia com indeterminado depois recebe tempo mineração
tempUltMinerado= "Indeterminado"

#Situação Mineração
situacao = "Em curso"

#contador em segundos de tempo de para minerar
ini = time.time()
def minerar():
    # Função que faz a requisição do bloco e armazena seu index para comparar com o index do bloco atual sendo minerado
    def getIndexBlockChain(carteira):
        global blockIndexBlockChain
        res2 = requests.get(f'{url}/block/minable/02d9475b6a68b3b4bab991ae537479e08e3279bda23ac8e77edef8c1eba6b326e7')
        res2 = res2.json()
        block2 = res2['block']
        block2 = Block.from_dict(block2)
        blockIndexBlockChain = block2.index

    cont = 0  # Contador para verificar se o bloco já foi minerado depois de um tempo
    loop = 1  # contador para gerar o loop infinito

    # loop infinito, pois sempre será verdadeiro
    while loop == 1:
        res = requests.get(
            f'{url}/block/minable/02d9475b6a68b3b4bab991ae537479e08e3279bda23ac8e77edef8c1eba6b326e7')  # Faz a requisição de um novo bloco
        res = res.json()
        dificuldade = res['difficulty']  # armazena em uma variável a dificuldade do bloco atual
        block = res['block']
        indexSendoMinerado = block['index']  # armazena o index do bloco requerido

        block = Block.from_dict(block)  # transforma o bloco em um objeto Block e o armazena em uma variável

        # mineração que acrescenta a quantidade de zeros a esquerdas de acordo com a dificuldade atual e tenta achar o nonce do bloco
        while block.current_hash[:dificuldade].count('0') < dificuldade:
            block.nonce += 1
            block.recalculate_hash()
            cont += 1

            # condição para verificiar se o bloco já foi minerado
            if cont == 2000000:
                getIndexBlockChain(KeyPair())  # invoca a função que armazenou o index do bloco

                if indexSendoMinerado != blockIndexBlockChain:  # Se o index for diferente, o bloco já foi minerado
                    print('quebrou')
                    cont = 0  # zera o contador
                    break  # quebra o while e volta para o loop par apegar outro bloco
                else:
                    cont = 0  # caso a comparação for falsa, zera o contador e volta para  mineração

        # submeta o block para a block_chain
        res = requests.post(f'{url}/block', json=dict(block))
        if res.ok:
            print('MINERADO :)!!! - INDEX: ' + str(
                indexSendoMinerado))  # Se o bloco foi minerado, exibe na tela a mensagem!
            #somaqtdMinerado
            global qtdMinerado
            qtdMinerado += str

            #Contador de tempo mineração
            global tempUltMinerado
            tempUltMinerado = time.time()

class MeuBotao(Widget):
    pass

#Tela Inicial
class Tela1(BoxLayout):
    # Faz a requisição do saldo atual e armazena o parâmetro de 'balance' que seria o saldo em uma variável, limpa a tela e
    # gera uma nova de saldo
    def on_press_bt_saldo(self):
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Tela2())
        res = requests.get(f'{url}/balance/02d9475b6a68b3b4bab991ae537479e08e3279bda23ac8e77edef8c1eba6b326e7')
        res = res.json()
        global balance
        balance = res['balance']

    #Limpa a tela e gera uma nova de qtd minerado
    def on_press_bt_qtdminerado(self):
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Tela3())

    #Limpa a tela e gera uma nova de tempo para minerar
    def on_press_bt_tempMiner(self):
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Tela4())

    # Limpa a tela e gera uma nova de opções de mineração
    def on_press_bt_opcoes(self):
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Tela5())

    #Definição de botões
    def __init__(self, **kwargs):
        super(Tela1, self).__init__(**kwargs)
        self.orientation = "vertical"
        bt1 = Button(text="Confira seu saldo")
        bt1.on_press = self.on_press_bt_saldo
        self.add_widget(bt1)

        bt2 = Button(text="Confira Total Minerado Nessa Seção")
        bt2.on_press = self.on_press_bt_qtdminerado
        self.add_widget(bt2)

        bt3 = Button(text="Tempo da ultima mineração")
        bt3.on_press = self.on_press_bt_tempMiner
        self.add_widget(bt3)

        bt4 = Button(text="Mineração | Opções")
        bt4.on_press = self.on_press_bt_opcoes
        self.add_widget(bt4)

#Tela de Saldo
class Tela2(BoxLayout):

    #Função de Retorno Tela inicial
    def on_press_bt(self):
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Tela1())

    def __init__(self, **kwargs):
        super(Tela2, self).__init__(**kwargs)
        self.orientation = "vertical"
        bt = Button(text="            Seu saldo é " + str(balance) +"\n" "\nClique e confira mais opções")
        bt.on_press = self.on_press_bt
        self.add_widget(bt)

class Tela3(BoxLayout):

    #Função de Retorno Tela inicial
    def on_press_bt(self):
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Tela1())

    def __init__(self, **kwargs):
        super(Tela3, self).__init__(**kwargs)
        self.orientation = "vertical"
        bt = Button(text="Minerado após ultima iniciação: " + str(qtdMinerado) +"\n" "\n    Clique e confira mais opções")
        bt.on_press = self.on_press_bt
        self.add_widget(bt)

#Tela Mineração
class Tela4(BoxLayout):
    #Função de Retorno Tela inicial
    def on_press_bt(self):
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Tela1())

    def __init__(self, **kwargs):
        super(Tela4, self).__init__(**kwargs)
        self.orientation = "vertical"
        bt = Button(text="Tempo da ultima mineração: " + str(tempUltMinerado) +"\n" "\n    Clique e confira mais opções")
        bt.on_press = self.on_press_bt
        self.add_widget(bt)

class Tela5(BoxLayout):

    # Função de Retorno Tela inicial
    def on_press_bt_voltar(self):
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Tela1())

    def __init__(self, **kwargs):
        super(Tela5, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.add_widget(Button(text="Status mineração: " + situacao))

        bt2 = Button(text="Iniciar Mineraração")
        bt2.on_press = minerar()
        self.add_widget(bt2)

        bt3 = bt2 = Button(text="Parar Mineração")
        bt3.on_press = minerar()
        self.add_widget(bt3)

        bt1 = Button(text="Voltar")
        bt1.on_press = self.on_press_bt_voltar
        self.add_widget(bt1)


class KVvsPY(App):
    def build(self):
        return Tela2()

janela = KVvsPY()
janela.run()










