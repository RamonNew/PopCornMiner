import time
from uclcoin import KeyPair, Transaction, Block, BlockChain
import requests
from hashlib import sha256 as _sha256
import threading
import datetime

#var globais
url = 'https://moeda.ucl.br'
blockIndexBlockChain = 0

#Função para codificar o hash
def sha256(bytestr):
    return _sha256(bytestr).digest()

#Função para pegar primeiramente o index do bloco
def getIndexBlockChain(carteira):
    global blockIndexBlockChain
    res = requests.get(f'{url}/block/minable/{carteira.public_key}')
    res = res.json()
    block = res['block']
    block = Block.from_dict(block)
    blockIndexBlockChain = block.index

#Função para checar o index do block, para verificar se ele mudou
def checkIndexBlockChain(carteira):
    while(True):
        time.sleep(1);
        #Minha variavel global
        global blockIndexBlockChain
        #Request no bloco 'mineravel' atual
        res = requests.get(f'{url}/block/minable/{carteira.public_key}')
        res = res.json()
        block = res['block']
        block = Block.from_dict(block)
        #Passo o index do bloco 'mineravel' atual para o blockIndexBlockChain
        blockIndexBlockChain = block.index
        #print('bloco na block chain: ' + str(block.index))
        time.sleep(10)

#Função para enviar o bloco para o servidor da blockchain
def sendToBLockChain(block):
    #Transformo meu objeto bloco em json
    jsonBlock = dict(block)
    #Envio um post para o servidor com o corpo do meu bloco/json
    res = requests.post(f'{url}/block', json=jsonBlock)

    #Se me retorna ok==200, eu minerei o bloco, caso não, já mineraram
    if res.ok:
        print('\n/-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\\')
        print('Index: ' + str(block.index))
        print('Bloco Minerado!'); 
        print('\-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-/')
    else:
        print('\n/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\\')
        print('Provavelmente já mineraram esse!');
        print(res);
        print('\-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-/')

#Função para gravar logs
def logInfo(block, inicio, fim, carteira, saldoNovo, saldoAntigo, minerado):
    #Gravando logs
    arq = open('RelatorioMiner1.txt', 'a')
    arq.write("\n-------------Informações do bloco-------------")
    arq.write("\nBloco: " + str(blockIndexBlockChain))
    arq.write("\nHora: " + str(datetime.datetime.fromtimestamp(int(fim)).strftime('%Y-%m-%d %H:%M:%S')))
    arq.write("\nTempo gasto: " + str(fim-inicio))
    arq.write("\nOperações: " + str(block.nonce))
    arq.write("\nMoedas adiquiridas: " + str(saldoNovo - saldoAntigo))
    arq.write("\nSaldo total: " + str(saldoNovo))
    arq.write("\nPublicKey: " + carteira.public_key)
    arq.write("\nMinerado?: " + minerado)
    #arq.write("\nPrivateKey: " + carteira.private_key)
    arq.write("\n-------------------------------------------------")
    arq.close()
    time.sleep(1);

#Função miner Principal
def miner(block, dificuldade, carteira):
    #Verifico meu saldo inicial
    res = requests.get(f'{url}/balance/{carteira.public_key}');
    res = res.json();
    saldoAntigo = res['balance'];

    print('\n(>*-*)> M I N E R A N D O    O    B L O C O <(*-*<)\n')
    print(f'(>*-*)>               {block.index}                  <(*-*<)\n')

    #Checando o index
    getIndexBlockChain(carteira)

    #Inicio minha 'quebra' de hash
    inicio = time.time()
    while block.current_hash[:dificuldade].count('0') < dificuldade:
        if block.index == blockIndexBlockChain:
            block.nonce += 1
            block.current_hash = sha256(''.join(('%08d' % block.version,block.previous_hash,block.merkle_root,'%x' % block.timestamp,'%08d' % block.nonce)).encode()).hex()
        else:
            fim = time.time()
            return
    fim = time.time()

    #Verifico meu saldo final
    res = requests.get(f'{url}/balance/{carteira.public_key}');
    res = res.json();
    saldoNovo = res['balance'];

    #Envio o bloco para validação na blockchain
    sendToBLockChain(block)
    #Gravo logs
    logInfo(block, inicio, fim, carteira, saldoNovo, saldoAntigo, "sim")

#Função Main
def main():
    #Inicio da função Main
    text = '''         _  __     _       _    _           __  __ _                 
        | |/ /    | |     | |  | |         |  \/  (_)                
        | ' / __ _| |_ ___| | _| | _____   | \  / |_ _ __   ___ _ __ 
        |  < / _` | __/ _ \ |/ / |/ / _ \  | |\/| | | '_ \ / _ \ '__|
        | . \ (_| | ||  __/   <|   < (_) | | |  | | | | | |  __/ |   
        |_|\_\__,_|\__\___|_|\_\_|\_\___/  |_|  |_|_|_| |_|\___|_|                                                                                                                         
        '''                          
    print(text)

    var privatKey = input('Coloque sua chave privada aqui: ');
    
    print("\nAo minerar um bloco veja no log suas informações!")

    global blockIndexBlockChain

    #Instanciar a carteira baseada na chave sua privada
    carteira  = KeyPair(privateKey)

    #Inicializo minha thread de verificação de index da blockchain
    tVerification = threading.Thread(target=checkIndexBlockChain, args=(carteira,))

    #Inicio minha thread de verificação
    tVerification.start()

    #Manter minerando forever
    while(True):
        #Requisito um bloco 'mineravel' na API
        res = requests.get(f'{url}/block/minable/{carteira.public_key}')
        #Transformo em json a resposta do servidor
        res = res.json()
        #Verifico a dificuldade
        dificuldade = res['difficulty']
        #Pego o bloco em json
        block = res['block']
        #Transformo meu bloco em json em um objeto
        block = Block.from_dict(block)

        #Inicializo minha thread de mineração
        tMineration = threading.Thread(target=miner, args=(block, dificuldade, carteira,))
        
        #Inicio minha thread de mineração
        tMineration.start()

        #Espero o termino dela
        tMineration.join()

if __name__ == "__main__":
    main()