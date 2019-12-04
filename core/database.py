import sqlite3
import os


class Database:
    def __init__(self, database):
        self.connection = sqlite3.connect("data/{}".format(database))

    def _execute_script(self, sql):
        cursor = self.connection.cursor()
        cursor.executescript(sql)
        self.connection.commit()

    def _execute_script_with_return(self, sql):
        cursor = self.connection.cursor()
        cursor.executescript(sql)
        return cursor.fetchall()

    def _execute_script_params(self, sql, *argv):
        args = tuple(argv)
        cursor = self.connection.cursor()
        cursor.execute(sql, args)
        self.connection.commit()

    def _execute_script_params_with_return(self, sql, *argv):
        args = tuple(argv)
        cursor = self.connection.cursor()
        cursor.execute(sql, args)
        return cursor.fetchall()

    def create_base(self):
        with open("core/scripts/extruture.sql") as file_script:
            sql = file_script.read()
        self._execute_script(sql)

    def create_site(self, name, subtitle, url, max_posts):
        with open("core/scripts/insert_settings.sql") as file_script:
            sql = file_script.read()
        self._execute_script_params(sql, name, subtitle, url, max_posts)

    def update_site(self, id, name, subtitle, url, max_posts):
        with open("core/scripts/update_settings.sql") as file_script:
            sql = file_script.read()
        self._execute_script_params(sql, name, subtitle, url, max_posts, id)

    def create_post(self, title, text, tags, id_site):
        with open("core/scripts/insert_posts.sql") as file_script:
            sql = file_script.read()
        self._execute_script_params(sql, title, text, tags, id_site)

    def update_post(self, id, title, text, tags):
        with open("core/scripts/update_posts.sql") as file_script:
            sql = file_script.read()
        self._execute_script_params(sql, title, text, tags, id)

    def list_sites(self):
        with open("core/scripts/list_sites.sql") as file_script:
            sql = file_script.read()
        query = self._execute_script_with_return(sql)
        return query
