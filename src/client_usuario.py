import json
import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import traceback
from controller.controller_usuario import UsuarioController
from controller.controller_servidor import ServidorClienteController

from datetime import datetime, timedelta

import tkinter as tk
from tkinter import messagebox

def data_atual_datetime_br():
    # Obtém o datetime atual em UTC
    datetime_utc = datetime.utcnow()
    # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
    datetime_brasil = datetime_utc - timedelta(hours=3)
    return datetime_brasil

def string_data_atual_datetime_br():
    # Obtém o datetime atual em UTC
    datetime_utc = datetime.utcnow()
    # Subtrai 3 horas do horario (HORARIO BRASILEIRO)
    datetime_brasil = datetime_utc - timedelta(hours=3)
    formato_brasil = "%d/%m/%Y %H:%M:%S"
    datetime_brasil_formatado = datetime_brasil.strftime(formato_brasil)
    return datetime_brasil_formatado

def string_para_datetime_br(horario_formatado_brasil):
    formato_brasil = "%d/%m/%Y %H:%M:%S"
    datetime_brasil_formatado = horario_formatado_brasil.strftime(formato_brasil)
    return datetime.strptime(datetime_brasil_formatado, formato_brasil)

class PopupUI:
    def __init__(self):
        self.janela = tk.Tk()

        # Resto do código...

    @classmethod
    def mostrar_alerta(self, mensagemalerta):
        messagebox.showinfo("Alerta", mensagemalerta)

    @classmethod
    def mostrar_informacao(self, mensageminformacao):
        messagebox.showinfo("Informação", mensageminformacao)

    @classmethod
    def mostrar_aviso(self, mensagemaviso):
        messagebox.showwarning("Aviso", mensagemaviso)

    @classmethod
    def mostrar_erro(self, mensagemerro):
        messagebox.showerror("Erro", mensagemerro)

    @classmethod
    def mostrar_confirmacao(self):
        resposta = messagebox.askyesno("Confirmação", "Você deseja continuar?")
        if resposta:
            print("Usuário confirmou.")
            return True
        else:
            print("Usuário cancelou.")
            return False

    @classmethod
    def mostrar_pergunta(self, pergunta):
        resposta = messagebox.askquestion("Pergunta", pergunta)
        return resposta



class ClienteUsuario:
    def __init__(self, usuario, keyusuario, host, port, celular):
        self.host = host
        self.usuario = usuario
        self.keyusuario = keyusuario
        self.port = port
        self.celularusuario = celular
        
        self.janela = tk.Tk()
        self.janela.title("Cliente")
        self.janela.configure(bg="#DCDCDC")
        self.janela.geometry("+1024+10")
        # largura = 800  # Defina a largura desejada da janela
        # altura = 600   # Defina a altura desejada da janela
        
        # # Calcula a posição para centralizar a janela na tela
        # x_pos = (self.janela.winfo_screenwidth() - largura) // 2
        # y_pos = (self.janela.winfo_screenheight() - altura) // 2
        
        # # Define a geometria da janela com largura, altura e posição
        # self.janela.geometry(f"{largura}x{altura}+{x_pos}+{y_pos}")

        self.messages_frame = tk.Frame(self.janela)
        self.meu_nome = tk.StringVar()
        self.meu_destinatario = tk.StringVar()
        self.meu_assunto = tk.StringVar()
        self.minha_msg = tk.StringVar()
        self.meu_destinatario.set("13991550539")

        self.scrollbar = tk.Scrollbar(self.messages_frame)

        self.l_seu_nome = tk.Label(
            self.janela,
            text="   Seu nome:",
            font="Verdana 16 bold",
            width=11,
            height=2,
            bg="#DCDCDC",
        )
        self.l_destinatario = tk.Label(
            self.janela,
            text=" Destinatário:",
            font="Verdana 16 bold",
            width=11,
            height=2,
            bg="#DCDCDC",
        )
        
        self.l_mensagem = tk.Label(
            self.janela,
            text="   Mensagem:",
            font="Verdana 16 bold",
            width=11,
            height=2,
            bg="#DCDCDC",
        )

        self.l_caixa_de_entrada = tk.Label(
            self.janela,
            text="Caixa de Entrada",
            font="Verdana 16 bold",
            height=1,
            bg="#DCDCDC",
        )

        self.l_divisoriac = tk.Label(self.janela, width=1, height=1, bg="#DCDCDC")
        self.l_divisorian = tk.Label(self.janela, width=1, height=1, bg="#2F4F4F")
        self.l_divisorias = tk.Label(self.janela, width=1, height=1, bg="#2F4F4F")
        self.l_divisoriae = tk.Label(self.janela, width=1, height=1, bg="#2F4F4F")
        self.l_divisoriaw = tk.Label(self.janela, width=1, height=1, bg="#2F4F4F")

        # self.msg_list = tk.Listbox(
        #     self.janela,
        #     height=11,
        #     width=38,
        #     font="Verdana 12 bold",
        #     fg="#2F4F4F",
        #     border=2,
        #     yscrollcommand=self.scrollbar.set,
        # )
        
        self.msg_list = tk.Text(
            self.janela,
            height=11,
            width=90,
            font="Verdana 12 bold",
            fg="#2F4F4F",
            wrap='word',  # Configura o wrap para quebrar as palavras
        )
        self.msg_list.grid(row=10, column=1, columnspan=2)

        self.scrollbar2 = tk.Scrollbar(self.janela, command=self.msg_list.yview)
        self.scrollbar2.grid(row=10, column=3, sticky='ns')
        self.msg_list['yscrollcommand'] = self.scrollbar2.set

        self.e_seu_nome = tk.Entry(
            self.janela, font="Verdana 12 bold", fg="#2F4F4F", textvariable=self.meu_nome
        )
        self.e_seu_nome.bind("<Return>", lambda event: self.estabelecer_conexao_servidor_chatbot())
        self.e_destinatario = tk.Entry(
            self.janela,
            font="Verdana 12 bold",
            fg="#2F4F4F",
            textvariable=self.meu_destinatario,
        )
        self.e_destinatario.bind("<Return>", lambda event: self.enviar())
        # self.e_assunto = tk.Entry(
        #     self.janela,
        #     font="verdana 12 bold",
        #     fg="#2F4F4F",
        #     textvariable=self.meu_assunto,
        # )
        # self.e_assunto.bind("<Return>", lambda event: self.enviar())
        self.e_mensagem = tk.Entry(
            self.janela,
            font="Verdana 9 bold",
            fg="#2F4F4F",
            textvariable=self.minha_msg,
        )
        self.e_mensagem.bind("<Return>", lambda event: self.enviar())

        self.janela.protocol("WM_DELETE_WINDOW", self.ao_fechar)

        self.b_estabelecer_conexao_servidor_chatbot = tk.Button(
            self.janela,
            text="    Estabelecer Conexão    ",
            font="Verdana 14 bold",
            height=1,
            border=3,
            relief="groove",
            fg="#2F4F4F",
            command=self.estabelecer_conexao_servidor_chatbot,
        )
        self.b_enviar = tk.Button(
            self.janela,
            text="Enviar Mensagem",
            font="Verdana 14 bold",
            height=1,
            border=3,
            relief="groove",
            fg="#2F4F4F",
            command=self.enviar,
        )
        self.b_sair = tk.Button(
            self.janela,
            text="Sair",
            font="Verdana 14 bold",
            fg="#B22222",
            border=3,
            relief="groove",
            command=self.sair,
        )

        # self.scrollbar.grid()
        # self.msg_list.grid(row=10, column=1, columnspan=2)
        
        self.messages_frame.grid()

        self.l_divisorian.grid(row=0, column=0, columnspan=3, sticky="e" + "w")
        self.l_divisorias.grid(row=13, column=0, columnspan=3, sticky="e" + "w")
        self.l_divisoriae.grid(row=0, column=0, rowspan=13, sticky="n" + "s")
        self.l_divisoriaw.grid(row=0, column=3, rowspan=14, sticky="n" + "s")

        self.l_seu_nome.grid(row=1, column=1, sticky="w")
        self.l_destinatario.grid(row=3, column=1, sticky="w")
        # self.l_assunto.grid(row=4, column=1, sticky="w")
        self.l_mensagem.grid(row=5, column=1, sticky="w")
        self.l_divisoriac.grid(row=8, column=1)
        self.l_caixa_de_entrada.grid(row=9, column=1, columnspan=3)

        self.e_seu_nome.grid(row=1, column=2)
        self.e_destinatario.grid(row=3, column=2)
        # self.e_assunto.grid(row=4, column=2)
        self.e_mensagem.grid(row=5, column=2)
        
        self.b_enviar.grid(row=6, column=2, sticky="n")
        self.b_estabelecer_conexao_servidor_chatbot.grid(row=2, column=2, sticky="n")
        self.b_sair.grid(row=12, column=1, columnspan=3)
        
        # setando variaveis iniciais
        self.meu_nome.set(self.celularusuario)
        self.msg_list.bind("<KeyPress>", lambda e: "break")
        self.BUFSIZ = 25000  
        
        self.inicar_conexao_servidor()
        
        self.receive_thread = Thread(target=self.receber)
        self.receive_thread.start()
        
        # Inicia a execução da GUI.
        self.janela.mainloop()
        
    def inicar_conexao_servidor(self):
        try:      
            self.estabelecerConexaoServidor()
        except:
            traceback.print_exc()
            print("Falha ao estabelecer conexao")
            exit()
       
    def inserir_mensagem_usuario(self, mensagem):
        self.msg_list.insert(tk.END, mensagem + '\n', "green")
    
    def inserir_mensagem_robo(self, mensagem):
        self.msg_list.insert(tk.END, mensagem + '\n', "blue")
    
    def estabelecerConexaoServidor(self):
        host = self.host
        port = self.port
        self.client_socket = ServidorClienteController.conectar_servidor_chatbot(host, port)
        ServidorClienteController.enviar_mensagem_cliente_servidor_boasvindas(self.client_socket, self.usuario, self.keyusuario)
        
    def receber(self):
        """Lida com o recebimento de mensagens."""
        while True:
            try:
                print("Esperando para receber novas mensagens...")
                msg = self.client_socket.recv(self.BUFSIZ)
                msg = msg.decode("utf8")
                print("Recebeu...")
                print(msg)                
                if(msg == "autorizado para enviar novas mensagens"):
                    pass
                else:
                    try:
                        mensagemJson = json.loads(msg)
                        self.receber_mensagens_bot(mensagemJson)                        
                    except:
                        # traceback.print_exc()
                        pass
            except OSError:  # Possivelmente o cliente saiu do chat.
                break

    
    def receber_mensagens_bot(self, mensagemJson):        
        destinatario = mensagemJson["destinatario"]
        if(destinatario != self.celularusuario):
            return
        remetente = mensagemJson["remetente"]
        mensagens_bot = mensagemJson["mensagens"]
        if(len(mensagens_bot) < 1):
            return
        for msg_bot in mensagens_bot:
            mensagem = msg_bot["mensagem"]
            mensagem_display = remetente+":"+str(mensagem)
            mensagem_display = "Robo:"+str(mensagem)
            self.inserir_mensagem_robo(mensagem_display)
            # self.msg_list.insert(tk.END, mensagem_display)
    
    def estabelecer_conexao_servidor_chatbot(self):
        """Lida com o envio do nome."""
        self.inicar_conexao_servidor()

    def enviar(self):
        """Lida com o envio de mensagens."""
        if self.meu_destinatario.get() != "" and self.minha_msg.get() != "":
            mensagem = self.minha_msg.get()
            remetente = self.meu_nome.get()
            destinatario = self.meu_destinatario.get()
            horariomensagem = string_data_atual_datetime_br()
            # Formata a data e hora no formato brasileiro (dd/mm/yyyy HH:mm:ss)            
            self.minha_msg.set("")  
            ServidorClienteController.enviar_mensagem_cliente_servidor(self.client_socket, remetente, destinatario, mensagem, horariomensagem)         
            self.inserir_mensagem_usuario(self.usuario+":"+mensagem)
            # self.client_socket.send(bytes(msg, "utf8"))

    def sair(self):
        """Encerra a conexão"""
        try:
            msg = "{quit}"
            self.client_socket.send(bytes(msg, "utf8"))
            self.client_socket.close()
        except:
            traceback.print_exc()
        finally:            
            self.janela.quit()

    def ao_fechar(self):
        """Esta função é chamada quando a janela é fechada."""
        self.minha_msg.set("{quit}")
        # self.enviar()


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 33000
    caminhoBD = "C:\\Users\\MarcusViniciusSoares\\OneDrive - GRANT THORNTON BRASIL\\Área de Trabalho\\Projetos\\ChatBotUniversal\\ChatBotUniversal\\chatbotui\\db\\repository\\chatbot.db"
    idusuario = input("Digite o id do usuario: ")
    controllerUsuario = UsuarioController(caminhoBD)
    usuario = controllerUsuario.buscar_usuario_por_id(idusuario) 
    idusuario = usuario.id
    nomeusuario = usuario.nome
    keyusuario = usuario.keyacesso
    celular = usuario.celular
    print(nomeusuario+" logado com sucesso!")
    # nomeusuario = "Marcus"
    # keyusuario = "2c6b9dd458761558ed5b0317fea87d0c76d58137323e9bd5ee2b5af2d12e6c98" #sha256    
    ClienteUsuario(nomeusuario, keyusuario, HOST, PORT, celular)
