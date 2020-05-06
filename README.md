# FYP-Smart-Partol-Robot
INSTALLATION
############################################################
There are some step before using the this product. This assume python is installed. 


1. Create virtual environment
1.1 open a terminal and move to this directory. 
1.2 create a virtual environment using “python -m venv venv”
1.3 activate the environment using “{folder location}/venv/Scripts/activate”, you will see “(venv)” at the start of the terminal if this is successfully done.
1.4 use “pip install pipenv” to install pipenv
1.5 use “pipenv install” to install all the pre-request package prerequisite

Everytime before using this program, virtual environment must be activated first.

2. Start a MySQL server
2.1 download “MySQL Community Server 8.0” from https://dev.mysql.com/downloads/mysql/
2.2 install the server follow the instruction. MySQL workbench also needed.
2.3 create a root account for the server during installation.
2.4 after installation, MySQL server is installed as service. Go to “service” and start a service named”MYSQL80”
2.5 use My SQL workbench to connect to the service. First start a connection to the service using the account name and password set during installation.
2.6 start a new schema and import the database from /chatbot/airport_info.sql
2.7 change the dbargs in UI.py(line 9) in the form of (ip address, username, password, schema name) and save.

Same as before, before using the program, MySQL server must be activated first

3.Start coreNLP server
3.1 download coreNLP 4.0.0 from https://stanfordnlp.github.io/CoreNLP/download.html and unzip it
3.2 start a new terminal and move the to file
3.3 start the server using ‘java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000’

Same as before, before using the program, coreNLP server must be activated first

4.0 install nltk data
4.1 start a new new terminal and move to “{project folder}/chatbot”
4.2 run the nltk_download_setup.py
4.3 download word2vec model from https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
4.4 unzip the model and put into “{project folder}/chatbot/nltk_data/models/ GoogleNews-vectors-negative300/ GoogleNews-vectors-negative300.bin”


Start the program
######################################
1. first make sure all the set up have done and all required server is started.
2. run UI.py, it need to take few minute to load the word2vec model
