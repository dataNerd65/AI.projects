# Purpose: A chatbot that helps students with their queries about MMUST
# Importing necessary libraries
import nltk
import json
import logging
from nltk.stem import WordNetLemmatizer

logging.basicConfig(level=logging.DEBUG)

class Chatbot:
    def __init__(self):
        self.name = "MMUSTbot"
        self.lemmatizer = WordNetLemmatizer()
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
        self.greeting_provided = False

    def run(self):
        print("Hello! I am MMUSTbot. I am here to help you.")
        try:
            while True:
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
                    recognized_intent, response_provided = self.process_input(user_input)

                    if response_provided:
                        continue  # Skip the remaining steps and continue to the next iteration

                    if recognized_intent:
                        self.respond(recognized_intent)
                    else:
                        print("I'm sorry, I don't understand. Can you please rephrase?")
        finally:
            print("Chatbot session ended.")

    def process_input(self, user_input):
        words = set(nltk.word_tokenize(user_input.lower()))
        self.lemmatizer_words = [self.lemmatizer.lemmatize(word) for word in words]

        recognized_intent = None
        response_provided = False  # Flag to track if a response has been provided

        for intent, keywords in self.intents.items():
            if any(word in self.lemmatizer_words for word in keywords):
               recognized_intent = intent
               break

        print("Recognized intent: ", recognized_intent)  # Debugging
        if recognized_intent:
            if recognized_intent == "questions":
                self.recognize_question_type(
                    set(self.intents["services"]), set(self.intents["query"])
                )
                response_provided = True

        return recognized_intent, response_provided

    def recognize_question_type(self, services_intersection, query_intersection):
        # Implementing logic to recognize the type of question based on services and queries
        recognized_services = set(services_intersection) & set(self.lemmatizer_words)
        recognized_queries = set(query_intersection) & set(self.lemmatizer_words)
        relevant_responses = []

        if {"fees", "fee"} & recognized_services:
           if "pay" in recognized_queries:
               relevant_responses.append("You can pay your fees via the jiunge app on Google PlayStore. Sign up with your details and do confirm them. Then proceed to pay your fees. The link is https://play.google.com/store/apps/details?id=com.jiunge.app&hl=en&gl=US.")
           elif "check" in recognized_queries:
               relevant_responses.append("You can check your fees balance by logging into the student portal and the link is https://portal.mmust.ac.ke/.")
           elif "confirm" in recognized_queries:
               relevant_responses.append("You can confirm your fees payment by logging into the student portal and the link is https://portal.mmust.ac.ke/.")
           elif "view" in recognized_queries:
               relevant_responses.append("You can view your fees structure and balance by logging into the student portal and the link is https://portal.mmust.ac.ke/.")
           elif "download" in recognized_queries:
               relevant_responses.append("You can download your fees structure by logging into the student portal and the link is https://portal.mmust.ac.ke/.")
           elif "print" in recognized_queries:
               relevant_responses.append("You can print your fees structure by logging into the student portal and the link is https://portal.mmust.ac.ke/.")

        if {"admission"} & recognized_services:
           if any(keyword in recognized_queries for keyword in ["apply", "enroll", "register", "join"]):
              relevant_responses.append("You can apply for admission by logging into the student portal and the link is https://portal.mmust.ac.ke/.")

        if {"units", "unit", "class", "classes", "courses", "course"} & set(self.lemmatizer_words) and any(query in recognized_queries for query in ["access", "get", "find", "check", "know", "confirm", "search", "view", "see", "tell"]):
            relevant_responses.append("You can know more about your classes and units by logging into the student portal and the link is https://portal.mmust.ac.ke/.")

        if {"hostel"} & recognized_services:
           if any(keyword in recognized_queries for keyword in ["check", "confirm", "view"]):
              relevant_responses.append("You can check your hostel details by logging into the student portal and the link is https://portal.mmust.ac.ke/.")

        if {"portal"} & set(self.lemmatizer_words):
           if any(query in recognized_queries for query in ["access", "get", "find", "know", "check", "confirm", "locate", "search", "view", "see", "tell", "give", "provide", "display", "receive", "register", "login", "log in", "log out", "sign in", "sign out", "sign up", "sign", "create", "add", "update", "edit", "change", "apply", "enroll", "register", "join"]):
              relevant_responses.append("You can access the student portal by logging into the student portal and the link is https://portal.mmust.ac.ke/.")

        if {"email", "e-mail"} & set(self.lemmatizer_words):
           if any(query in recognized_queries for query in ["access", "get", "find", "check", "know", "check", "confirm", "locate", "search", "view", "see", "tell", "give", "provide", "display", "receive", "register", "login", "log in", "log out", "sign in", "sign out", "sign up", "sign", "create", "add", "update", "edit", "change", "apply", "enroll", "register", "join"]):
              relevant_responses.append("You can access your email by first creating it as shown in admission details and then logging into it. If facing any challenges, please visit the ICT department.")

        if {"e-learning", "odel"} & set(self.lemmatizer_words):
           if any(query in recognized_queries for query in ["access", "get", "find", "check", "know", "check", "confirm", "locate", "search", "view", "see", "tell", "give", "provide", "display", "receive", "register", "login", "log in", "log out", "sign in", "sign out", "sign up", "sign", "create", "add", "update", "edit", "change", "apply", "enroll", "register", "join"]):
            relevant_responses.append("You can access the e-learning portal by logging into the e-learning portal, and the link is https://elearning.mmust.ac.ke/.")

       # Printing the relevant response
        if relevant_responses:
           print(relevant_responses[0])
        else:
           print("I'm sorry, I don't understand. Can you please rephrase?")


    def respond(self, intent):
        if intent == "greeting" and not self.greeting_provided:
            print("Hello! How can I help you today?")
            self.greeting_provided = True  # Set the flag to True to avoid repeating the greeting
        elif intent == "goodbye":
            print("Bye! Have a nice day.")
        elif intent == "questions":
            print("I'm here to help you. What would you like to know?")

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

# Instantiate the Chatbot class
chatbot = Chatbot()

# Run the chatbot
chatbot.run()
