import os
from bottle import Bottle, request, static_file, redirect
from jinja2 import Environment, FileSystemLoader
from core.database import Database
from os import listdir
from os.path import isfile, join


class Server:
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self._load_environment()
        self._load_server()

    def _load_environment(self):
        file_loader = FileSystemLoader("core/admin")
        self.env = Environment(loader=file_loader)

    def _load_databases(self):
        databases = [db for db in listdir("data/") \
                     if isfile("data/" + db) and (db.endswith(".db") or db.endswith(".DB"))]
        self.database_list = databases

    def _load_server(self):
        self.app = Bottle()
        self.route()

    def route(self):
        self.app.route("/", method="GET", callback=self.index)
        self.app.route("/public/<filename>", method="GET", callback=self.public)
        self.app.route("/database/<action>", method=["GET", "POST"], callback=self.database)
        self.app.route("/manage/<dbname>", method=["GET"], callback=self.manage_index)

    def start(self):
        self.app.run(host=self.host, port=self.port)

    def public(self, filename):
        return static_file(filename, root="core/admin/public")

    def index(self):
        template = self.env.get_template("index.html")
        self._load_databases()
        return template.render(dbs=self.database_list)

    def database(self, action):
        if action == "create":
            name = request.forms.get("dbname").replace(" ", "_")
            if name.endswith(".db"):
                name = name.replace(".db", "")
            name = "".join([letter for letter in name if letter.isalnum() or letter == "_"])
            name = name + ".db"
            name = name.upper()
            db = Database(database=name)
            db.create_base()
        elif action == "delete":
            file = request.forms.get("dbtodel")
            if self._db_exist(file):
                os.remove(str(os.getcwd()) + "/data/" + file)
        redirect("/")

    def manage_index(self, dbname):
        if not self._db_exist(dbname):
            redirect("/")
        db = Database(dbname)
        data = db.list_sites()
        template = self.env.get_template('manage.html')
        return template.render(data=data)

    def _db_exist(self, dbname):
        dir_fd = os.getcwd()
        path = str(dir_fd) + "/data/" + dbname
        if os.path.exists(path):
            return True
        return False
