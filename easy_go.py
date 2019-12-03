import webbrowser
from core.server import Server

HOST = "localhost"
PORT = 8081
server = Server(HOST, PORT)
webbrowser.open("http://{}:{}".format(HOST, PORT))
server.start()
