import socketserver

SIZE = 1024

class Handler(socketserver.BaseRequestHandler):
    users_data = {}
    
    def send_message(self,message):
        for sock, _ in self.users_data.values():
            sock.send(message.encode())    
    
    
    def handle(self):
        while True:
            self.request.send("Enter a user name".encode())
            user_name = self.request.recv(SIZE).decode()
            if user_name in self.users_data:
                self.request.send("[{}] already exists.\n".format(user_name).encode())
            else:
                self.users_data[user_name] = (self.request,self.client_address)
                self.send_message("[{}] has joined the chat.".format(user_name))
                break
        
        
        while True:
            message = self.request.recv(SIZE)
            if message == "/leave":
                self.request.close()
                break
            self.send_message("[{}] {}".format(user_name,message.decode()))
        
        if user_name in self.users_data:
            del self.users_data[user_name]
            self.send_message("[{}] has left the chat".format(user_name))
        
    

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


server = Server(("",8800),Handler)
server.serve_forever()
server.shutdown()
server.server_close()
