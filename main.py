from flask import Flask, render_template, request,redirect, url_for
from pyaiml21 import Kernel
from glob import glob
from nltk import word_tokenize, pos_tag
import numpy as np
from neo4j import GraphDatabase
import nltk
from database.webscrap import  get_latest_reddit_post,process_query
from database.ml import predict_gender
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from database.nlp_start import sementics
from py2neo import Graph,Node,Relationship

from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.wsd import lesk
import requests
from bs4 import BeautifulSoup


graph=Graph("bolt://localhost:7687" ,auth=("neo4j","password"))
app = Flask(__name__)
Bot = Kernel()

intent_sentences = ["What's the weather like today?", "Tell me a joke", "Who won the latest football match?"]
intent_labels = ["weather", "joke", "sports"]



# Train intent recognition model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(intent_sentences)
intent_model = LogisticRegression()
intent_model.fit(X, intent_labels)


nltk.download('punkt')  # Download the tokenization models
nltk.download('averaged_perceptron_tagger')  # Download the POS tagging models
nltk.download('wordnet')  # Download WordNet corpus for semantic analysis



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register1', methods=['POST'])
def register1():
    username=request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    graph.run(f"CREATE(n:person{{name:\"{username}\",email:\"{email}\",password:\"{password}\"}})")
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email,password)
    email_value1=graph.run(f"MATCH(n:person{{email:\"{email}\",password:\"{password}\"}}) return n")
    print(email_value1)
    # Retrieve user from Neo4j
    email_value=list(email_value1)
    print(email_value)
    if email_value:
        # Successful login, redirect to the home page
        return render_template('home.html')
    else:
        # Invalid login, show error message or redirect back to login page
        return render_template('login.html', error_message='Invalid credentials')


# Custom JSON encoder to handle DateTime objects

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)
@app.route('/graph')
def show_graph():
    # Perform the required operations to retrieve the graph from Neo4j
    # For example:
     nodes = graph.run("MATCH (n) RETURN n").data()
     relationships = graph.run("MATCH ()-[r]->() RETURN r").data()


     nodes= json.dumps(nodes, cls=DateTimeEncoder)
     relationships = json.dumps(relationships, cls=DateTimeEncoder)


     return render_template('graph.html', nodes=nodes, relationships=relationships)
    # Process the nodes and relationships data as needed to generate a graph representation

    # Pass the graph data to the template for rendering


aiml_files = glob("chatfiles/*")
for file in aiml_files:
    Bot.learn(file)

def process(query):
    tokens = nltk.word_tokenize(query)
    tagged_tokens = pos_tag(tokens)

    noun_data = []
    for word, tag in tagged_tokens:
        if  tag.startswith('NNP') and word.lower() not in ['hi', 'hello','bye']:
            return ("true")

    return ("false")


@app.route("/get")
def get_bot_response():

        query=request.args.get('msg')
        graph.run("MERGE (u:person {name: 'saim'}) "
                  "WITH u "
                  "MERGE (u)-[:INTERACTED_WITH]->(m:Memory {query: $query}) "
                  "SET m.timestamp = datetime()",
                  query=query)
        #neo4j relations

        query_to=process_query(query)
        que=process(query)
        if que=="true":
            response=get_latest_reddit_post(query_to)
            return response
        elif query.startswith("guess gender"):
            name1 = query.split("Guess gender", 1)[-1].strip()
            gender = predict_gender(name1)
            response = f"The predicted gender for the name '{name1}' is {gender}."
            return (str(response))
        else:
            response = Bot.respond(query, 'user')
            '''noun1,verb,noun2=sementics(query)
            node1=Node("Animal",name=noun1)
            graph.create(node1)
            node2= Node("object", name=noun2)
            graph.create(node2)
            relationship=Relationship(node1,verb,node2)
            graph.create(relationship)'''

            # Return the ML-generated or AIML-generated response
            print(str(response))
            return (str(response))
        ''''elif query.lower()=="show neo4j graph":
            nodes = graph.run("MATCH (n) RETURN n").data()
            print(nodes)
            relationships = graph.run("MATCH ()-[r]->() RETURN r").data()
            print(relationships)
            # Pass the graph data to the template for rendering
            return render_template('graph.html', nodes=nodes, relationships=relationships)
        '''


if __name__ == "__main__":
    app.run(debug=True)
 #elif query.lower() == "show graph":
  #             # Redirect to the graph route
   #                return redirect(url_for('show_graph'))'''