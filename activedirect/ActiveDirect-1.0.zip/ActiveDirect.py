#!/usr/local/bim/python
# _*_ iso:8859-1 _*_

import socketserver, time, mysql.connector,  zeep
from datetime import datetime





# Configuração do servidor
HostSocket = ''
Porta = 2034
KeepAlive = '05'
Status = 'A'  # A para ativo e I para inativo
NumeroSdc = 0
CodigoImei = None
TipoEvento = None
Canal = '224'

# Configuração da coneçao Mysql
BDHost = '5.135.68.92'
BDUser = 'root'
BDPass = 'root'
BDBanco = 'confimonit'
SQLresult = None

# acerta url webservice
cliente = zeep.Client(wsdl = 'http://confmonit.com/webservice/webservice.asmx?WSDL')

#Retorna a hora do sistema
def agora(): return time.ctime(time.time())


def SQL(query):

    '''
    Cria uma conexão com o banco de dados que vai receber
    os eventos vindo dos alarmes, tratando os erros de
    usuario, senha e banco
    '''
    try:
        # Cria uma conexão na variavel cnx
        cnx = mysql.connector.connect(user     = BDUser,
                                      password = BDPass,
                                      host     = BDHost,
                                      database = BDBanco)
    except mysql.connector.Error as erro:
        if erro.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de USUARIO ou SENHA")
        elif erro.errno == errorcode.ER_BAD_BD_ERROR:
            print("Banco de Dados Inexistente")
        else: print(erro)

    cursor = cnx.cursor()

    cursor.execute(query)

    resultado = cursor.fetchone()

    if (query[:6] != 'SELECT'):
        cnx.commit()
    cursor.close()
    cnx.close()

    return resultado



class Clientes(socketserver.BaseRequestHandler):
   try:
        def handle(self):
            # Para cada conexão de um novo cliente
            # implimimos a identificação e o horario da conexão
            global CodigoImei, CodigoImei
            print(self.client_address, agora())

            while True:

                # Recebe dados do Cliente
                evento = self.request.recv(40)
                if not evento: break
                
                # Pega o codigo para verificação se e conexao '!'(33)
                # ou se é keep Alive '@'(64) ou evento '$'(36)
                cmd = evento[0]

                if cmd == 33: # pedido de conexão
                    EventoCod = evento[1:16]
                    CodigoImei = EventoCod.decode("utf-8")
                    SQLresult = SQL("SELECT dispositivos_cliente, dispositivos_ativo, dispositivos_KeepAlive" +
                                    " FROM dispositivos" +
                                    " WHERE dispositivos_imei = " + CodigoImei)
                    NumeroSdc = SQLresult[0]
                    Status = SQLresult[1]
                    KeepAlive = SQLresult[2]
                    print(NumeroSdc, CodigoImei)
                    # Evia + para aceitar conexão
                    if Status == 'A': self.request.send(b'+')

                    # Evia - para recusar conexão
                    else: self.request.send(b'-')

                if cmd == 64: # pedido Keep Alive
                    EventoCod = evento[1:14]
                    ContactID = EventoCod.decode("utf-8")
                    print(CodigoImei, '->', agora())                    
                    SQLresult = SQL("SELECT dispositivos_KeepAlive" +
                                    " FROM dispositivos" +
                                    " WHERE dispositivos_imei = " + CodigoImei)
                    KeepAlive = SQLresult[0]
                    if (Contactid[0:4] == ''):
                        conta = '9999'
                    else:
                        conta = Contactid[0:4]
                    
                    TipoEvento = "M017"
                    cliente.service.Proc_Evt(str(NumeroSdc), conta, 
                        Canal, datetime.now(), datetime.now(), TipoEvento, ContactID[10:14], '0', 0, 
                        TipoEvento, TipoEvento, False, 0, False, '0', 0, datetime.now(), 
                        'confmonitvirtual')
                    self.request.send(b'@' + bytes.fromhex(KeepAlive))  # Envia tempo de Keep Alive

                if cmd == 36: # Informa evento
                    EventoCod = evento[1:14]
                    ContactID = EventoCod.decode("utf-8")
                    print(ContactID)

                    # cria a query para inserção no banco
                    SQLresult = SQL("INSERT INTO recebeeventos (" +
                                    "recebeeventos_sdc, recebeeventos_imei, recebeeventos_contactid)" +
                                    " VALUES (" + str(NumeroSdc) + ", " + CodigoImei + ", " + ContactID + ")")

                    if (ContactID[4] == '1'): TipoEvento = 'E' + ContactID[5:8]
                    if (ContactID[4] == '3'): TipoEvento = 'R' + ContactID[5:8]          
                    
                    cliente.service.Proc_Evt(str(NumeroSdc), ContactID[0:4], 
                        Canal, datetime.now(), datetime.now(), TipoEvento, 
                        TipoEvento, TipoEvento, ContactID[10:14], '0', 0, 
                        False, 0, False, '0', 0, datetime.now(), 
                        'confmonitvirtual')

                    self.request.send(b'@' + bytes.fromhex(KeepAlive))  # Envia tempo de Keep Alive
   except:
       raise Exception("Perda de conecão")


local = (HostSocket, Porta)
Servidor = socketserver.ThreadingTCPServer(local, Clientes)
Servidor.serve_forever()




