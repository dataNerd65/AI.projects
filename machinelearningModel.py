from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
#RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
#MultinomialNB
from sklearn.naive_bayes import MultinomialNB
#LogisticRegression
from sklearn.linear_model import LogisticRegression

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

#Defining the parameter grid
param_grid = {
    'svc__kernel': ['linear', 'rbf'],
    'svc__C': [0.1, 1, 10, 100],
    'svc__gamma': [0.1, 0.01, 0.001, 'scale', 'auto']
}
#Creating the pipeline with CountVectorizer and SVC
model = make_pipeline(CountVectorizer(), SVC())

#Using GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

#Printing the best hyperparameters
print("Best hyperparameters:", grid_search.best_params_)

#Get the best model
best_model = grid_search.best_estimator_

#Exploring RandomForestClassifier
#Creating the pipeline with CountVectorizer and RandomForestClassifier
model_rf = make_pipeline(CountVectorizer(), RandomForestClassifier())

#Trainning the RandomForestClassifier model
model_rf.fit(X_train, y_train)

#Evaluating the model
y_pred_rf = model_rf.predict(X_test)
print("RandomForestClassifier Accuracy:", metrics.accuracy_score(y_test, y_pred_rf))

#Using the model for intent recognition in the chatbot
predicted_intent_rf = model_rf.predict([user_input])[0]
print("RandomForestClassifier Predicted intent: ", predicted_intent_rf)

#Exploring MultinomialNB
#Creating the pipeline with CountVectorizer and MultinomialNB
model_nb = make_pipeline(CountVectorizer(), MultinomialNB())

#Training the MultinomialNB model
model_nb.fit(X_train, y_train)

#Evaluating the MultinomialNB model
y_pred_nb = model_nb.predict(X_test)
print("MultinomialNB Accuracy:", metrics.accuracy_score(y_test, y_pred_nb))

#Using the MultinomialNB model for intent recognition in the chatbot
predicted_intent_nb = model_nb.predict([user_input])[0]
print("MultinomialNB Predicted intent: ", predicted_intent_nb)

#Exploring LogisticRegression
#Creating the pipeline with CountVectorizer and LogisticRegression
model_lr = make_pipeline(CountVectorizer(), LogisticRegression(max_iter=1000))

#Training the LogisticRegression model
model_lr.fit(X_train, y_train)

#Evaluating the LogisticRegression model
y_pred_lr = model_lr.predict(X_test)
print("LogisticRegression Accuracy:", metrics.accuracy_score(y_test, y_pred_lr))

#Using the LogisticRegression model for intent recognition in the chatbot
predicted_intent_lr = model_lr.predict([user_input])[0]
print("LogisticRegression Predicted intent: ", predicted_intent_lr)

