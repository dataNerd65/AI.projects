#Purpose: A chatbot that can answer questions about MMUST
#Importing the necessary libraries
import logging
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
#setting up the logging configuration
logging.basicConfig(level=logging.DEBUG)

class Chatbot:
    def __init__(self):
        self.name = "MMUSTbot101"
        self.lemmatizer = WordNetLemmatizer()
        self.lemmatizer_words = [] #Defining lemmatized_words as a class attribute
        self.intents = {
            "greeting": ["hello", "hi", "hey", "how are you", "what's up", "sup"],
            "goodbye": ["bye", "goodbye", "see you later", "take care"],
            "questions": ["what", "where", "when", "why", "how", "who"],
            "services": ["hostel", "fees", "fee", "admission", "units","unit", "classes", "class","courses", "course", "timetable", "exams", "results", "transcript",
                          "graduation", "alumni", "library", "sports", "clubs", "chapel", "health", "security",
                          "catering", "transport", "ICT","portal", "email", "e-mail", "wifi", "e-learning", "odel"],
            "query": ["access", "get", "find", "know", "check", "confirm", "locate", "search", "view", "see", "show",
                      "tell", "give", "provide", "display", "send", "receive", "read", "write", "print", "download",
                      "upload", "submit", "register", "login", "log in", "log out", "sign in", "sign out", "sign up",
                      "sign", "create", "delete", "remove", "add", "insert", "update", "edit", "change", "modify",
                      "cancel", "book", "reserve", "pay", "buy", "purchase", "order", "apply", "enroll", "register",
                      "join", "leave", "exit", "graduate"]
        }

    def greet(self):
        return f"Hello! I am {self.name}. How can I assist you today?"

    def process_input(self, user_input):
        words = set(nltk.word_tokenize(user_input.lower()))
        self.lemmatizer_words = [self.lemmatizer.lemmatize(word) for word in words]
        print("Lemmatized words: ", self.lemmatizer_words)
        print("Original words: ", words)

        # Check for both services and query intent in a single step
        for query in self.intents["query"]:
            for service in self.intents["services"]:
                lemmatized_words = set(nltk.word_tokenize(user_input.lower()))
                lemmatized_words = [self.lemmatizer.lemmatize(word) for word in lemmatized_words]
                if service in lemmatized_words and query in lemmatized_words:
                   return self.recognize_question_type([service], [query])

         # Check each intent for a match
        for intent, keywords in self.intents.items():
            for word in self.lemmatizer_words:
                 if word in keywords:
                    return self.respond(intent)

        # If no intent was matched, ask the user to rephrase
        return "I'm sorry, I don't understand. Can you please rephrase?"


    def recognize_question_type(self, services_intersection, query_intersection):
        print("Services intersection: %s", services_intersection)
        print("Query intersection: %s", query_intersection)
        
       #Implementing logic to recognize the type of question based on services and queries
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
        if any(keyword in self.lemmatizer_words for keyword in ["units", "unit", "class", "classes", "courses", "course"]) and any(query in self.lemmatizer_words for query in ["access", "get", "find", "check", "know", "check", "confirm", "search", "view", "see", "tell",]):
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
        if "portal" in self.lemmatizer_words and any(query in self.lemmatizer_words for query in ["access", "get", "find", "know", "check", "confirm", "locate", "search", "view", "see", "tell", "give", "provide", "display", "receive", "register", "login", "log in", "log out", "sign in", "sign out", "sign up", "sign", "create",  "add",  "update", "edit", "change", "apply", "enroll", "register", "join"]):
            return "You can access the student portal by logging into the student portal and the link is https://portal.mmust.ac.ke/"

        #if "email" in self.lemmatizer_words and any(query in self.lemmatizer_words for query in ["access", "get", "find", "check", "know", "check", "confirm", "locate", "search", "view", "see", "tell", "give", "provide", "display", "receive", "register", "login", "log in", "log out", "sign in", "sign out", "sign up", "sign", "create", "add", "update", "edit", "change", "apply", "enroll", "register", "join"]):
            #return "You can access your email by first creating it as shown in admission details and then logging into it. If facing any challenges, please visit the ICT department."
        
        if any(keyword in self.lemmatizer_words or keyword == "e-mail" for keyword in ["email", "e-mail"]) and any(query in self.lemmatizer_words for query in ["access", "get", "find", "check", "know", "check", "confirm", "locate", "search", "view", "see", "tell", "give", "provide", "display", "receive", "register", "login", "log in", "log out", "sign in", "sign out", "sign up", "sign", "create", "add", "update", "edit", "change", "apply", "enroll", "register", "join"]):
            return "You can access your email by first creating it as shown in admission details and then logging into it. If facing any challenges, please visit the ICT department."

                        
        if any(keyword in self.lemmatizer_words for keyword in ["e-learning", "odel"]) and any(query in self.lemmatizer_words for query in ["access", "get", "find", "check", "know", "check", "confirm", "locate", "search", "view", "see", "tell", "give", "provide", "display", "receive", "register", "login", "log in", "log out", "sign in", "sign out", "sign up", "sign", "create",  "add",  "update", "edit", "change", "apply", "enroll", "register", "join"]):
                return "You can access the e-learning portal by logging into the e-learning portal, and the link is https://elearning.mmust.ac.ke/."

        else:
            return "I'm sorry, I don't understand. Can you please rephrase?"
    def respond(self, intent):
        #logic to generate a response based on the intent
        if intent == "greeting":
            return "Hello! How can I help you today?"
        elif intent == "goodbye":
            return "Bye! Have a nice day."
        elif intent == "questions":
            return "I'm here to help you. What would you like to know?"
        

    def run(self):
        print(self.greet())
        while True:
            user_input = input("> ")
            if user_input.lower() == "exit":
                break
            response = self.process_input(user_input)
            if response is not None:
                print(response)
            else:
                print("I'm sorry, I don't understand. Can you please rephrase?")
            

#Creating an instance of the chatbot and running it
chatbot = Chatbot()
chatbot.run()