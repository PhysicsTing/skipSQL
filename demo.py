#!/usr/bin/python3

import os
import json
import subprocess

from lib.skipsql import Db, Connection

# skipsql connector are used to interact with database with
# natural language. Therefore to run this demo you must have
# a relational database set up already, and fill in below database
# connection information. The user you provided must at least have
# "SELECT" privilege on the database.

# Replace below info!!!

DATABASE = "hr"
HOST = "localhost"
USER = "admin"
PASSWORD = "password"
SCHEMA_FILE = "demo_schema.txt"

def query_demo1():
    db = Db(database=DATABASE,
            host=HOST,
            user=USER,
            password=PASSWORD,
            schema_file=SCHEMA_FILE)
    if not db.is_connected():
        print("Unable to connect to database")
        print("Please make sure the connection info are properly filled in")
    else:
        # output = db.ask_debug("What is the average salary of Daniel Faviet's department?", False)
        question = "What is the average salary of Daniel Faviet's department?"
        output = db.ask(question)
        print("Q:  {}".format(question))
        print("A:  {}".format(output))

if __name__ == "__main__":
    query_demo1()

