import socket
import cv2
import os
import numpy as np

class Cliente():
    """
    Classe Cliente - API Socket
    """
    def __init__(self, server_ip, port):
        """
        Construtor da classe Cliente
        """
        self.__server_ip = server_ip
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def start(self):
        """
        Método que inicializa a execução do Cliente
        """
        endpoint = (self.__server_ip,self.__port)
        try:
            self.__tcp.connect(endpoint)
            print("Conexão realizada com sucesso!")
            self.__method()
        except:
            print("Servidor não disponível")

    
    def __method(self):
        """
        Método que implementa as requisições do cliente
        """
        try:
            # leitura da imagem
            caminho_imagem = 'faces/image_0001.jpg'
            if not os.path.exists('faces/image_0001.jpg'):
                raise FileNotFoundError("O arquivo de imagem não foi encontrado!")
            
            img = cv2.imread(caminho_imagem)

            # codificação para bytes
            _, img_bytes = cv2.imencode('.jpg', img) 
            img_bytes = bytes(img_bytes)
            tamanho_da_imagem_codificado = len(img_bytes).to_bytes(4, 'big')
            
            self.__tcp.sendall(tamanho_da_imagem_codificado)
            
            self.__tcp.sendall(img_bytes)
            

            print("Imagem Enviada")
            
            tamanho_da_imagem_codificado_m = self.__tcp.recv(1024)
            tam = int.from_bytes(tamanho_da_imagem_codificado_m, 'big')
            
            img_bytes_m = self.__tcp.recv(tam)

            
            img = cv2.imdecode(np.frombuffer(img_bytes_m, np.uint8), cv2.IMREAD_COLOR)

            print("Imagem Recebida")

            cv2.imshow('Imagem Processada', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            self.__tcp.close()
        except Exception as e:
            print("Erro ao realizar comunicação com o servidor", e.args)
