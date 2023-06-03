import re
import mysql.connector
from mysql.connector import Error
import langchain.prompts as prompts
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import os

sql_prompt = prompts.PromptTemplate(
    input_variables=["question", "schema"],
    template="You are a sql expert."
    "I'll ask a question, and provide you a list of tables with their definition. These tables are stored in a MySQL server."
    "Based on the provided content, what sql query I need to use in order to answer the question? Make sure to includ the ';'"
    "at the end of the query."
    "Question: {question}"
    "Table definition: {schema}"
)

answer_prompt = prompts.PromptTemplate(
    input_variables=["question", "query", "result"],
    template="You are a HR administrator."
    "I'll ask a question, and provide you a dataset ."
    "Based on the provided content, give me a SQL query, togather with the query result."
    "Answer the question based on the query and query result. If the context is not sufficient, answer I don't know."
    "Question: {question}"
    "Query: {query}"
    "Result: {result}"
)

class Sql():
    @staticmethod
    def extract(context):
        context = context.replace('\n', ' ').replace('\r', '')
        x = re.findall("SELECT.*;", context)
        query = x[0].strip(";")
        return query

class Connection():
    def __init__(self, database, host='localhost', user='root', password=None):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.connection = None
        self.connect()

    def connect(self):
        if not self.is_connected():
            try:
                self.connection = mysql.connector.connect(host=self.host,
                                                          database=self.database,
                                                          user=self.user,
                                                          password=self.password)

                self.cursor = self.connection.cursor(dictionary=True)

            except Error as e:
                print("Error while connecting to MySQL", e)

    def close(self):
        if self.is_connected():
            try:
                self.cursor.close()
                self.connection.close()
            except Error as e:
                print("Error while connecting to MySQL", e)

    def is_connected(self):
        if self.connection and self.connection.is_connected():
            return True
        return False

class Db():

    def __init__(self, database, host='localhost', user='root', password=None, schema_file=None):

        self.connection = Connection(database=database,host=host,user=user, password=password)
        if self.is_connected():
            print("Connected to database {} at {}".format(database, host))

        with open(schema_file, 'r') as file:
            self.schema = file.read()

        #self.llm = OpenAI(temperature=0, model_name="text-davinci-003")
        #self.llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo")
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-4")
        self.sql_chain = LLMChain(prompt=sql_prompt, llm=self.llm)
        self.answer_chain = LLMChain(prompt=answer_prompt, llm=self.llm)

    def connect(self):
        if not self.is_connected():
            self.connection.connect()

    def close(self):
        if self.is_connected():
            self.connection.close()
    
    def is_connected(self):
        return self.connection.is_connected()

    def query(self, query):
        self.connection.cursor.execute(query)
        res = ""
        for i in self.connection.cursor:
            res = res + str(i)
        return res
    
    def ask(self, question):
        #print("Q:  " + question)

        answer = self.sql_chain.run({
            "question" : question,
            "schema" : self.schema
            })

        query = Sql.extract(answer)
        res = self.query(query)

        answer = self.answer_chain.run({
            "question" : question,
            "query" : query,
            "result" : res
            })
        
        return answer
    
    # For testing purpose only
    def ask_debug(self, question, dryrun=False):
        print("Q:     " + question)

        answer = self.sql_chain.run({
            "question" : question,
            "schema" : self.schema
            })

        query = Sql.extract(answer)
        print("Query: " + query)

        if dryrun:
            return query

        res = self.query(query)

        answer = self.answer_chain.run({
            "question" : question,
            "query" : query,
            "result" : res
            })
        print("Answer: " + answer)
        return answer
