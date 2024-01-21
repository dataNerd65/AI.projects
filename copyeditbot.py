#Purpose: A chatbot that can answer questions about MMUST
#Importing the necessary libraries
import json
from config import DATABASE_CONFIG
import logging
import mysql.connector
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)

class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(**DATABASE_CONFIG)
        self.cursor = self.connection.cursor()
        self.create_users_table()

    def create_users_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            reg_number VARCHAR(100),
            google_email VARCHAR(100),
            student_email VARCHAR(100),
            username VARCHAR(100),
            password VARCHAR(100)
        )
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def signup_user(self, name, reg_number, google_email, student_email, username, password):
        insert_data_query = '''
        INSERT INTO users(name, reg_number, google_email, student_email, username, password) VALUES
        (%s, %s, %s, %s, %s, %s)
        '''
        user_data = (name, reg_number, google_email, student_email, username, password)
        self.cursor.execute(insert_data_query, user_data)
        self.connection.commit()

    def authenticate_user(self, username, password):
        self_user_query = '''
        SELECT * FROM users WHERE username = %s AND password = %s
        '''
        user_credentials = (username, password)
        self.cursor.execute(self_user_query, user_credentials)
        return bool(self.cursor.fetchone())

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

class Chatbot:
    def __init__(self):
        self.name = "MMUSTbot"
        self.lemmatizer = WordNetLemmatizer()
        self.lemmatizer_words = []
        self.database_manager = DatabaseManager()
        self.current_user = self.load_session()
        self.intents = {
            "greeting": ["hello", "hi", "hey", "how are you", "what's up", "sup"],
            "goodbye": ["bye", "goodbye", "see you later", "take care"],
            "questions": ["what", "where", "when", "why", "how", "who"],
            "services": ["hostel", "fees", "fee", "admission", "units", "unit", "classes", "class", "courses", "course",
                          "timetable", "exams", "results", "transcript",
                          "graduation", "alumni", "library", "sports", "clubs", "chapel", "health", "security",
                          "catering", "transport", "ICT", "portal", "email", "e-mail", "wifi", "e-learning", "odel"],
            "query": ["access", "get", "find", "know", "check", "confirm", "locate", "search", "view", "see", "show",
                      "tell", "give", "provide", "display", "send", "receive", "read", "write", "print", "download",
                      "upload", "submit", "register", "login", "log in", "log out", "sign in", "sign out", "sign up",
                      "sign", "create", "delete", "remove", "add", "insert", "update", "edit", "change", "modify",
                      "cancel", "book", "reserve", "pay", "buy", "purchase", "order", "apply", "enroll", "register",
                      "join", "leave", "exit", "graduate"]
        }

    def save_session(self):
        if self.current_user:
            with open("user_session.json", "w") as file:
                json.dump(self.current_user, file)

    def load_session(self):
        try:
            with open("user_session.json", "r") as file:
                user = json.load(file)
                return user
        except FileNotFoundError:
            return None

    def authenticate_user(self):
        if not self.current_user:
            user_auth_input = input("Enter '1' to log in or '2' to signup: ")
            if user_auth_input == '1':
                self.login_user()
            elif user_auth_input == '2':
                self.signup_user()
            else:
                print("Invalid input. Please enter '1' to log in or '2' to sign up.")

    def signup_user(self):
        name = input("Enter your name: ")
        reg_number = input("Enter your registration number: ")
        google_email = input("Enter your google email: ")
        student_email = input("Enter your student email: ")
        username = input("Choose a username: ")
        password = input("Choose a password: ")

        self.database_manager.signup_user(name, reg_number, google_email, student_email, username, password)
        print("Signup successful. Please log in to continue.")
        self.process_if_user("signup")

    def login_user(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if self.database_manager.authenticate_user(username, password):
            print("Login successful.")
            self.current_user = {'username': username, 'password': password}
        else:
            print("Authentication failed. Please try again.")


    def process_if_user(self, user_input):
        if not self.current_user:
            self.authenticate_user()
        else:
            return self.process_input(user_input)

    def run(self):
        print("Hello! I am MMUSTbot. I am here to help you.")
        try:
            while True:
                if not self.current_user:
                    user_auth_input = input("Enter '1' to log in or '2' to signup: ")
                    if user_auth_input == '1':
                        self.login_user()
                    elif user_auth_input == '2':
                        self.signup_user()
                    else:
                        print("Invalid input. Please enter '1' to log in or '2' to sign up.")
                else:
                    user_input = input("> ")
                    if user_input.lower() == "exit":
                       self.save_session()
                       print("Bye! Have a nice day.")
                       break
                    elif user_input.lower() == "logout":
                       self.current_user = None
                       self.save_session()
                       print("Logged out successfully. Type exit to quit or continue chatting.")
                    else:
                       response = self.process_input(user_input)
                       if response is not None:
                          print(response)
                       else:
                          print("I'm sorry, I don't understand. Can you please rephrase?")
        finally:
            self.database_manager.close_connection()

    def process_input(self, user_input):
        self.authenticate_user()
        words = set(nltk.word_tokenize(user_input.lower()))
        self.lemmatizer_words = [self.lemmatizer.lemmatize(word) for word in words]
        print("Lemmatized words: ", self.lemmatizer_words)
        print("Original words: ", words)

        for query in self.intents["query"]:
            for service in self.intents["services"]:
                lemmatized_words = set(nltk.word_tokenize(user_input.lower()))
                lemmatized_words = [self.lemmatizer.lemmatize(word) for word in lemmatized_words]
                if service in lemmatized_words and query in lemmatized_words:
                    return self.recognize_question_type([service], [query])

        for intent, keywords in self.intents.items():
            for word in self.lemmatizer_words:
                if word in keywords:
                    return self.respond(intent)

        return "I'm sorry, I don't understand. Can you please rephrase?"

    def recognize_question_type(self, services_intersection, query_intersection):
        # Implementing logic to recognize the type of question based on services and queries
        if "fees" in services_intersection or "fee" in services_intersection:
            if "pay" in query_intersection:
                return "You can pay your fees via the jiunge app on Google PlayStore. Sign up with your details and do confirm them. Then proceed to pay your fees. The link is https://play.google.com/store/apps/details?id=com.jiunge.app&hl=en&gl=US."
            elif "check" in query_intersection:
                return "You can check your fees balance by logging into the student portal and the link is https://portal.mmust.ac.ke/."
            elif "confirm" in query_intersection:
                return "You can confirm your fees payment by logging into the student portal and the link is https://portal.mmust.ac.ke/."
            elif "view" in query_intersection:
                return "You can view your fees structure and balance by logging into the student portal and the link is https://portal.mmust.ac.ke/."
            elif "download" in query_intersection:
                return "You can download your fees structure by logging into the student portal and the link is https://portal.mmust.ac.ke/."
            elif "print" in query_intersection:
                return "You can print your fees structure by logging into the student portal and the link is https://portal.mmust.ac.ke/."

        if "admission" in services_intersection:
            if "apply" in query_intersection:
                return "You can apply for admission by logging into the student portal and the link is https://portal.mmust.ac.ke/."
            elif "enroll" in query_intersection:
                return "You can enroll for admission by logging into the student portal and the link is https://portal.mmust.ac.ke/."
            elif "register" in query_intersection:
                return "You can register for admission by logging into the student portal and the link is https://portal.mmust.ac.ke/."
            elif "join" in query_intersection:
                return "You can join for admission by logging into the student portal and the link is https://portal.mmust.ac.ke/."

        if any(keyword in self.lemmatizer_words for keyword in ["units", "unit", "class", "classes", "courses", "course"]) and any(query in self.lemmatizer_words for query in ["access", "get", "find", "check", "know", "check", "confirm", "search", "view", "see", "tell", ]):
            return "You can know more about your classes and units by logging into the student portal and the link is https://portal.mmust.ac.ke/."

        if "hostel" in services_intersection:
            if "check" in query_intersection:
                return "You can check your hostel by logging into the student portal and the link is https://portal.mmust.ac.ke/."
            elif "confirm" in query_intersection:
                return "You can confirm your hostel by logging into the student portal and the link is https://portal.mmust.ac.ke/."
            elif "view" in query_intersection:
                return "You can view your hostel by logging into the student portal and the link is https://portal.mmust.ac.ke/."
            elif "check" in query_intersection:
                return "You can check in your hostel by logging into the student portal and the link is https://portal.mmust.ac.ke/."

        if "portal" in self.lemmatizer_words and any(query in self.lemmatizer_words for query in ["access", "get", "find", "know", "check", "confirm", "locate", "search", "view", "see", "tell", "give", "provide", "display", "receive", "register", "login", "log in", "log out", "sign in", "sign out", "sign up", "sign", "create", "add", "update", "edit", "change", "apply", "enroll", "register", "join"]):
            return "You can access the student portal by logging into the student portal and the link is https://portal.mmust.ac.ke/"

        if any(keyword in self.lemmatizer_words or keyword == "e-mail" for keyword in ["email", "e-mail"]) and any(query in self.lemmatizer_words for query in ["access", "get", "find", "check", "know", "check", "confirm", "locate", "search", "view", "see", "tell", "give", "provide", "display", "receive", "register", "login", "log in", "log out", "sign in", "sign out", "sign up", "sign", "create", "add", "update", "edit", "change", "apply", "enroll", "register", "join"]):
            return "You can access your email by first creating it as shown in admission details and then logging into it. If facing any challenges, please visit the ICT department."

        if any(keyword in self.lemmatizer_words for keyword in ["e-learning", "odel"]) and any(query in self.lemmatizer_words for query in ["access", "get", "find", "check", "know", "check", "confirm", "locate", "search", "view", "see", "tell", "give", "provide", "display", "receive", "register", "login", "log in", "log out", "sign in", "sign out", "sign up", "sign", "create", "add", "update", "edit", "change", "apply", "enroll", "register", "join"]):
            return "You can access the e-learning portal by logging into the e-learning portal, and the link is https://elearning.mmust.ac.ke/."
        else:
            return "I'm sorry, I don't understand. Can you please rephrase?"

    def respond(self, intent):
        if intent == "greeting":
            return "Hello! How can I help you today?"
        elif intent == "goodbye":
            return "Bye! Have a nice day."
        elif intent == "questions":
            return "I'm here to help you. What would you like to know?"

# Instantiate the Chatbot class
chatbot = Chatbot()

# Run the chatbot
chatbot.run()
