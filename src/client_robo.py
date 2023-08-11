import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import traceback
from controller.controller_servidor import ServidorClienteController
from controller.controller_usuario import UsuarioController

import datetime

import tkinter as tk
from tkinter import messagebox

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



class ClientRobo:
    def __init__(self, usuario, keyusuario, host, port):
        self.host = host
        self.usuario = usuario
        self.keyusuario = keyusuario
        self.port = port
        
        self.janela = tk.Tk()
        self.janela.title("Robo")
        self.janela.configure(bg="#DCDCDC")
        self.janela.geometry("+905+10")

        self.messages_frame = tk.Frame(self.janela)
        self.meu_nome = tk.StringVar()
        self.meu_destinatario = tk.StringVar()
        self.minha_msg = tk.StringVar()

        self.scrollbar = tk.Scrollbar(self.messages_frame)

        self.l_seu_nome = tk.Label(
            self.janela,
            text="   Nome robo:",
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

        self.msg_list = tk.Listbox(
            self.janela,
            height=11,
            width=38,
            font="Verdana 12 bold",
            fg="#2F4F4F",
            border=2,
            yscrollcommand=self.scrollbar.set,
        )

        self.e_seu_nome = tk.Entry(
            self.janela, font="Verdana 12 bold", fg="#2F4F4F", textvariable=self.meu_nome
        )
        self.e_seu_nome.bind("<Return>", lambda event: self.enviar_nome())
        self.e_destinatario = tk.Entry(
            self.janela,
            font="Verdana 12 bold",
            fg="#2F4F4F",
            textvariable=self.meu_destinatario,
        )
        self.e_destinatario.bind("<Return>", lambda event: self.enviar())
        self.e_mensagem = tk.Entry(
            self.janela,
            font="Verdana 12 bold",
            fg="#2F4F4F",
            textvariable=self.minha_msg,
        )
        self.e_mensagem.bind("<Return>", lambda event: self.enviar())

        self.janela.protocol("WM_DELETE_WINDOW", self.ao_fechar)

        self.b_enviar_nome = tk.Button(
            self.janela,
            text="    Enviar Nome    ",
            font="Verdana 14 bold",
            height=1,
            border=3,
            relief="groove",
            fg="#2F4F4F",
            command=self.enviar_nome,
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

        self.scrollbar.grid()
        self.msg_list.grid(row=10, column=1, columnspan=2)
        self.messages_frame.grid()

        self.l_divisorian.grid(row=0, column=0, columnspan=3, sticky="e" + "w")
        self.l_divisorias.grid(row=13, column=0, columnspan=3, sticky="e" + "w")
        self.l_divisoriae.grid(row=0, column=0, rowspan=13, sticky="n" + "s")
        self.l_divisoriaw.grid(row=0, column=3, rowspan=14, sticky="n" + "s")

        self.l_seu_nome.grid(row=1, column=1, sticky="w")
        self.l_destinatario.grid(row=3, column=1, sticky="w")
        self.l_mensagem.grid(row=5, column=1, sticky="w")
        self.l_divisoriac.grid(row=8, column=1)
        self.l_caixa_de_entrada.grid(row=9, column=1, columnspan=3)

        self.e_seu_nome.grid(row=1, column=2)
        self.e_destinatario.grid(row=3, column=2)
        self.e_mensagem.grid(row=5, column=2)
        
        self.b_enviar.grid(row=6, column=2, sticky="n")
        self.b_enviar_nome.grid(row=2, column=2, sticky="n")
        self.b_sair.grid(row=12, column=1, columnspan=3)
        
        # setando variaveis iniciais
        self.meu_nome.set(nomeusuario)
        
        self.BUFSIZ = 1024  
        try:      
            self.estabelecerConexaoServidor()
        except:
            traceback.print_exc()
            print("Falha ao estabelecer conexao")
            exit()
        
        self.receive_thread = Thread(target=self.receber)
        self.receive_thread.start()
        
        # Inicia a execução da GUI.
        self.janela.mainloop()
       
  
    def estabelecerConexaoServidor(self):
        host = self.host
        port = self.port
        self.client_socket = ServidorClienteController.conectar_servidor(host, port)
        ServidorClienteController.enviar_mensagem_cliente_servidor_boasvindas(self.client_socket, self.usuario, self.keyusuario)
        
    def receber(self):
        """Lida com o recebimento de mensagens."""
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                msg_split = msg.split("@")
                print(msg_split)
                if len(msg_split) > 1:
                    destino = msg_split[1]
                    print(destino)
                    if destino == self.meu_nome.get():
                        print(msg_split)
                        self.msg_list.insert(tk.END, "De: " + msg_split[0])
                        self.msg_list.insert(tk.END, "Assunto: " + msg_split[2])
                        self.msg_list.insert(tk.END, "Mensagem: " + msg_split[3])
                        self.msg_list.insert(tk.END, " ")

                if len(msg_split) == 1:
                    self.msg_list.insert(tk.END, msg)
                    print(msg)

            except OSError:  # Possivelmente o cliente saiu do chat.
                break

    def enviar_nome(self):
        """Lida com o envio do nome."""
        msg = self.meu_nome.get()
        print(msg)
        self.client_socket.send(bytes(msg, "utf8"))

    def enviar(self):
        """Lida com o envio de mensagens."""
        if self.meu_destinatario.get() != "" and self.minha_msg.get() != "":
            mensagem = self.minha_msg.get()
            remetente = self.meu_nome.get()
            destinatario = self.meu_destinatario.get()
            horariomensagem = datetime.time()
            self.meu_destinatario.set("")
            self.minha_msg.set("")  
            ServidorClienteController.enviar_mensagem_cliente_servidor(self.client_socket, remetente, destinatario, mensagem, horariomensagem)         
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
    HOST = "10.255.255.10"
    PORT = 33000
    caminhoBD = "C:\\Users\\MarcusViniciusSoares\\OneDrive - GRANT THORNTON BRASIL\\Área de Trabalho\\Projetos\\ChatBotUniversal\\ChatBotUniversal\\chatbotui\\db\\repository\\chatbot.db"
    controllerUsuario = UsuarioController(caminhoBD)
    idusuario = input("Digite o id do usuario: ")
    usuario = controllerUsuario.buscar_usuario_por_id(idusuario) 
    print(usuario)
    idusuario = usuario.id
    nomeusuario = usuario.nome
    keyusuario = usuario.keyacesso
    print(nomeusuario+" logado com sucesso!")
    # nomeusuario = "Marcus"
    # keyusuario = "2c6b9dd458761558ed5b0317fea87d0c76d58137323e9bd5ee2b5af2d12e6c98" #sha256    
    ClientRobo(nomeusuario, keyusuario, HOST, PORT)
