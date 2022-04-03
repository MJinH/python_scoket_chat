import socket
from threading import Thread 
import tkinter


IP = ""
PORT = 0
SIZE = 1024

def connect_to_sever(event=None):
    global IP, PORT
    address = str_input.get().split(":")
    IP = address[0]
    PORT = int(address[1])
    connect.destroy()
    
    
def get_message(sock):
    while True:
        message = sock.recv(SIZE).decode()
        list_chats.insert(tkinter.END,message)
        list_chats.see(tkinter.END)
        
def send_message(event=None):
    message = insert_message.get()
    sock.send(message.encode())
    insert_message.set("")
    if message == "/leave":
        chat.quit()
        sock.close()


connect = tkinter.Tk()
connect.title("Connect")
tkinter.Label(connect,text="Address").grid(row=0,column=0)
str_input = tkinter.StringVar(value="127.0.0.1:8800")
input_addr = tkinter.Entry(connect,textvariable=str_input,width=20)
input_addr.grid(row=0,column=1)
c_button = tkinter.Button(connect,text="Connect",command=connect_to_sever)
c_button.grid(row=0,column=2, padx=5,pady=5)
connect.mainloop()


chat = tkinter.Tk()
chat.title("Client")

frame = tkinter.Frame(chat)
scroll = tkinter.Scrollbar(frame)
scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)


list_chats = tkinter.Listbox(frame,height=15,width=50,yscrollcommand=scroll.set)
list_chats.pack(side=tkinter.LEFT,fill=tkinter.BOTH,padx=5,pady=5)
frame.pack()


insert_message = tkinter.StringVar()
inputbox = tkinter.Entry(chat, textvariable=insert_message)
inputbox.bind("<Return>",send_message)
inputbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH,expand=tkinter.YES,padx=5,pady=5)
send_button = tkinter.Button(chat,text="Send",command=send_message)
send_button.pack(side=tkinter.RIGHT,fill=tkinter.X, padx=5,pady=5)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP,PORT))

th = Thread(target=get_message,args=(sock,))
th.daemon = True
th.start()

chat.mainloop()