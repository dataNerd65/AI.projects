from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics

#Reading the data from a file for code readability
def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = [line.strip().split(', ') for line in file]
    return data
#Usage
file_path = r'C:\Users\ADMIN\SoftwareDeveloper\questions+categories.txt'
data  = read_data_from_file(file_path)

#The data will contain the questions and the category they belong to
for question, category in data:
    print(f"Question: {question} , Category: {category}")

#now reading the responses from a file
def read_responses_from_file(file_path):
    with open(file_path, 'r') as file:
        responses = dict(line.strip().split(', ') for line in file)
    return responses
    
#The usage
file_path_responses = r'C:\Users\ADMIN\SoftwareDeveloper\responses.txt'
responses = read_responses_from_file(file_path_responses)

#the response response pairs
for intent,response in responses.items():
    print(f"Intent: {intent}, Response: {response}")
    

#The data with the questions and queries
data = [("How can i pay my fees?", "fees"),
        ("How much is the fee?", "fees"),
        ("How much is the fee for computer science?", "fees"),
        ("What are the admission requirements?", "admission"),
        ("How can i apply for admission?", "admission"),
        ("How can i enroll for admission?", "admission"),
        ("How can i register for admission?", "admission"),
        ("How can i join the university?", "admission"),
        ("How can i get my admission letter?", "admission"),
        ("How can i get my admission number?", "admission"),
]

#Splitting the data into features(X) and labels(y)
X, y = zip(*data)

#Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Creating a pipeline with CountVectorizer and SVM
model = make_pipeline(CountVectorizer(), SVC())

#training the model
model.fit(X_train, y_train)

#Evaluating the model
y_pred = model.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

#Using the model for intent recognition in the chatbot
user_input = input("Enter your question: ")
predicted_intent = model.predict([user_input])[0]
print("Predicted intent: ", predicted_intent)

