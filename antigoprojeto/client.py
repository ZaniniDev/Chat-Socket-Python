import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def receive(client_socket, msg_list, my_name):
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            msg_split = msg.split("@")
            print(msg_split)
            if len(msg_split) > 1:
                destino = msg_split[1]
                print(destino)
                if destino == my_name.get():
                    print(msg_split)
                    msg_list.insert(tk.END, "By: " + msg_split[0])
                    msg_list.insert(tk.END, "Assunto: " + msg_split[2])
                    msg_list.insert(tk.END, "Mensagem: " + msg_split[3])
                    msg_list.insert(tk.END, " ")

            if len(msg_split) == 1:
                msg_list.insert(tk.END, msg)
                print(msg)

        except OSError:  # Possibly client has left the chat.
            break


def send_name(client_socket, my_name):
    """Handles sending of name."""
    msg = my_name.get()
    print(msg)
    client_socket.send(bytes(msg, "utf8"))


def send(client_socket, my_destinatario, my_assunto, my_msg):
    """Handles sending of messages."""
    if my_destinatario.get() != "" and my_msg.get() != "":
        msg = (
            "@"
            + my_destinatario.get()
            + "@"
            + my_assunto.get()
            + "@"
            + my_msg.get()
        )
        my_destinatario.set("")
        my_assunto.set("")
        my_msg.set("")
        client_socket.send(bytes(msg, "utf8"))


def sair(client_socket, janela):
    """Encerrar a conexão"""
    msg = "{quit}"
    client_socket.send(bytes(msg, "utf8"))
    client_socket.close()
    janela.quit()


def on_closing(client_socket, my_msg):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send(client_socket, my_destinatario, my_assunto, my_msg)


def start_chat_client():
    janela = tk.Tk()
    janela.title("Client3")
    janela.configure(bg="#DCDCDC")
    janela.geometry("+905+10")

    messages_frame = tk.Frame(janela)
    my_name = tk.StringVar()
    my_destinatario = tk.StringVar()
    my_assunto = tk.StringVar()
    my_msg = tk.StringVar()

    scrollbar = tk.Scrollbar(messages_frame)

    l_seu_nome = tk.Label(
        janela,
        text="   Seu nome:",
        font="Verdana 16 bold",
        width=11,
        height=2,
        bg="#DCDCDC",
    )
    l_destinatario = tk.Label(
        janela,
        text=" Destinatário:",
        font="Verdana 16 bold",
        width=11,
        height=2,
        bg="#DCDCDC",
    )
    l_assunto = tk.Label(
        janela,
        text="       Assunto:",
        font="Verdana 16 bold",
        width=11,
        height=1,
        bg="#DCDCDC",
    )
    l_mensagem = tk.Label(
        janela,
        text="   Mensagem:",
        font="Verdana 16 bold",
        width=11,
        height=2,
        bg="#DCDCDC",
    )

    l_caixa_de_entrada = tk.Label(
        janela, text="Caixa de Entrada", font="Verdana 16 bold", height=1, bg="#DCDCDC"
    )

    l_divisoriac = tk.Label(janela, width=1, height=1, bg="#DCDCDC")
    l_divisorian = tk.Label(janela, width=1, height=1, bg="#2F4F4F")
    l_divisorias = tk.Label(janela, width=1, height=1, bg="#2F4F4F")
    l_divisoriae = tk.Label(janela, width=1, height=1, bg="#2F4F4F")
    l_divisoriaw = tk.Label(janela, width=1, height=1, bg="#2F4F4F")

    msg_list = tk.Listbox(
        janela,
        height=11,
        width=38,
        font="Verdana 12 bold",
        fg="#2F4F4F",
        border=2,
        yscrollcommand=scrollbar.set,
    )

    e_seu_nome = tk.Entry(
        janela, font="Verdana 12 bold", fg="#2F4F4F", textvariable=my_name
    )
    e_seu_nome.bind("<Return>", lambda event: send_name(client_socket, my_name))
    e_destinatario = tk.Entry(
        janela, font="Verdana 12 bold", fg="#2F4F4F", textvariable=my_destinatario
    )
    e_destinatario.bind("<Return>", lambda event: send(client_socket, my_destinatario, my_assunto, my_msg))
    e_assunto = tk.Entry(
        janela, font="verdana 12 bold", fg="#2F4F4F", textvariable=my_assunto
    )
    e_assunto.bind("<Return>", lambda event: send(client_socket, my_destinatario, my_assunto, my_msg))
    e_mensagem = tk.Entry(
        janela, font="Verdana 12 bold", fg="#2F4F4F", textvariable=my_msg
    )
    e_mensagem.bind("<Return>", lambda event: send(client_socket, my_destinatario, my_assunto, my_msg))

    janela.protocol("WM_DELETE_WINDOW", lambda: on_closing(client_socket, my_msg))

    b_enviar_nome = tk.Button(
        janela,
        text="    Enviar Nome    ",
        font="Verdana 14 bold",
        height=1,
        border=3,
        relief="groove",
        fg="#2F4F4F",
        command=lambda: send_name(client_socket, my_name),
    )
    b_enviar = tk.Button(
        janela,
        text="Enviar Mensagem",
        font="Verdana 14 bold",
        height=1,
        border=3,
        relief="groove",
        fg="#2F4F4F",
        command=lambda: send(client_socket, my_destinatario, my_assunto, my_msg),
    )
    b_sair = tk.Button(
        janela,
        text="Sair",
        font="Verdana 14 bold",
        fg="#B22222",
        border=3,
        relief="groove",
        command=lambda: sair(client_socket, janela),
    )

    scrollbar.grid()
    msg_list.grid(row=10, column=1, columnspan=2)
    messages_frame.grid()

    l_divisorian.grid(row=0, column=0, columnspan=3, sticky="e" + "w")
    l_divisorias.grid(row=13, column=0, columnspan=3, sticky="e" + "w")
    l_divisoriae.grid(row=0, column=0, rowspan=13, sticky="n" + "s")
    l_divisoriaw.grid(row=0, column=3, rowspan=14, sticky="n" + "s")

    l_seu_nome.grid(row=1, column=1, sticky="w")
    l_destinatario.grid(row=3, column=1, sticky="w")
    l_assunto.grid(row=4, column=1, sticky="w")
    l_mensagem.grid(row=5, column=1, sticky="w")
    l_divisoriac.grid(row=8, column=1)
    l_caixa_de_entrada.grid(row=9, column=1, columnspan=3)

    e_seu_nome.grid(row=1, column=2)
    e_destinatario.grid(row=3, column=2)
    e_assunto.grid(row=4, column=2)
    e_mensagem.grid(row=5, column=2)

    HOST = "localhost"
    PORT = 33000
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)

    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive, args=(client_socket, msg_list, my_name))
    receive_thread.start()

    # Starts GUI execution.
    janela.mainloop()


if __name__ == "__main__":
    start_chat_client()
