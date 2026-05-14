import socket
import cv2
import os
import numpy as np

class Servidor():
    """
    Classe Servidor - API Socket
    """

    def __init__(self, host, port):
        """
        Construtor da classe servidor
        """
        self._host = host
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self):
        """
        Método que inicializa a execução do servidor
        """
        endpoint = (self._host, self._port)
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(1)
            print("Servidor iniciado em ", self._host, ": ", self._port)
            while True:
                con, client = self.__tcp.accept()
                self._service(con, client)
        except Exception as e:
            print("Erro ao inicializar o servidor", e.args)

    def _service(self, con, client):
        """
        Método que implementa o serviço de identificação e marcação de faces
        :param con: objeto socket utilizado para enviar e receber dados
        :param client: é o endereço do cliente
        """
        print("Atendendo cliente ", client)
        while True:
            try:
                tamanho_da_imagem_codificado = con.recv(1024)
                tam = int.from_bytes(tamanho_da_imagem_codificado, 'big')
                
                img_bytes = con.recv(tam)
                
                buffer = np.frombuffer(img_bytes, np.uint8) 
                  
                
                img = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

                xml_classificador = os.path.join(os.path.relpath(
                cv2.__file__).replace('__init__.py', ''), 'data/haarcascade_frontalface_default.xml')
                face_cascade = cv2.CascadeClassifier(
                xml_classificador)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                # Desenha retângulos nas áreas onde as faces foram detectadas
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
                
                # codificação para bytes
                _, img_bytes = cv2.imencode('.jpg', img) 
                img_bytes_m = bytes(img_bytes)
                tamanho_da_imagem_codificado_m = len(img_bytes).to_bytes(4, 'big')
            
                con.send(tamanho_da_imagem_codificado_m)
            
                con.send(img_bytes_m)

                print(client, " -> requisição atendida")
            except OSError as e:
                print("Erro de conexão ", client, ": ", e.args)
                return
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente ",
                      client, ": ", e.args)
                con.send(bytes("Erro", 'ascii'))
                return
