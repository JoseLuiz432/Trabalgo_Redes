import math


class ControleEnvio(object):
    def __init__(self):
        self.buffersize = 104857600  # 100MB
        self.windowsize = 8388608  # 8MB

    def sendmsg(self, msg, cliente, udp):
        """
        formata a msg para envio
        :param msg: msg a ser enviada
        :return:
        """
        if type(msg) == str:
            msg = msg.encode('utf-8')

        lista_msg = self.fragmenta(msg)

        cont = 0
        numero_grande = (2 ** 32) - 1
        for mensagem in lista_msg:
            udp.sendto(self.adiciona_cabecalho(mensagem, cont % numero_grande), cliente)
            cont += 1
        udp.sendto(
            self.adiciona_cabecalho(
                'encerramento_lista'.encode('utf-8'), cont % numero_grande)
            , cliente
        )

    def fragmenta(self, msg):
        # em bytes
        tamanho = len(msg)

        # 1024 tamanho do pacote
        numero_pacotes = math.ceil(tamanho / 1016)

        lista_envio = []
        for i in range(int(numero_pacotes)):
            if 1016*i+1016 <= len(msg):
                lista_envio.append(msg[1016*i:1016*i+1016])
            else:
                lista_envio.append(msg[1016 * i:len(msg)])

        return lista_envio

    def adiciona_cabecalho(self, msg, numero_sequencia):
        """

        :param numero_sequencia:
        :return:
        """
        head = numero_sequencia.to_bytes(4, 'big')
        cabecalho = head+self.windowsize.to_bytes(4, 'big')
        return cabecalho + msg