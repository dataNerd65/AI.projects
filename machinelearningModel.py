from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report

def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = [line.strip().split(', ') for line in file]
    return data

def read_responses_from_file(file_path):
    with open(file_path, 'r') as file:
        responses = dict(line.strip().split(', ') for line in file)
    return responses

def split_data(data):
    X, y = zip(*data)
    return X, y

def train_and_evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    #Printing the confusion matrix
    print(f"{type(model).__name__} Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    #Printing the classification report
    print(f"{type(model).__name__} Classification Report:")
    print(classification_report(y_test, y_pred))
    
    #Printing the accuracy score
    accuracy = metrics.accuracy_score(y_test, y_pred)
    print(f"{type(model).__name__} Accuracy: {accuracy}")
    
    return model

def predict_intent(model, responses, user_input):
    predicted_intent = model.predict([user_input])[0]
    response = responses.get(predicted_intent, "Sorry, I don't understand. Please try again.")
    print(f"{type(model).__name__} Predicted Intent: {predicted_intent}")
    print(f"Response: {response}")

# Loading data
file_path = r'C:\Users\ADMIN\SoftwareDeveloper\questions+categories.txt'
data = read_data_from_file(file_path)

# Loading responses
file_path_responses = r'C:\Users\ADMIN\SoftwareDeveloper\responses.txt'
responses = read_responses_from_file(file_path_responses)

# Splitting data
X, y = split_data(data)

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# The Param grid declaration for SVM
param_grid_svm = {
    'svc__kernel': ['linear', 'rbf'],
    'svc__C': [0.1, 1, 10, 100],
    'svc__gamma': [0.1, 0.01, 0.001, 'scale', 'auto']
}

# SVM Model
svm_model = make_pipeline(CountVectorizer(), SVC())
grid_search_svm = GridSearchCV(svm_model, param_grid_svm, cv=5, scoring='accuracy')
best_svm_model = train_and_evaluate_model(grid_search_svm, X_train, y_train, X_test, y_test)

# RandomForestClassifier Model
rf_model = make_pipeline(CountVectorizer(), RandomForestClassifier())
best_rf_model = train_and_evaluate_model(rf_model, X_train, y_train, X_test, y_test)

# MultinomialNB Model
nb_model = make_pipeline(CountVectorizer(), MultinomialNB())
best_nb_model = train_and_evaluate_model(nb_model, X_train, y_train, X_test, y_test)

# LogisticRegression Model
lr_model = make_pipeline(CountVectorizer(), LogisticRegression(max_iter=1000))
best_lr_model = train_and_evaluate_model(lr_model, X_train, y_train, X_test, y_test)

# Continuous user input loop
while True:
    user_input = input("Enter your question (type 'exit' to quit): ")
    
    if user_input.lower() == 'exit':
        print("Have an octostatic day. Goodbye!")
        break
    
    # Predict intent using each model
    predict_intent(best_svm_model, responses, user_input)
    predict_intent(best_rf_model, responses, user_input)
    predict_intent(best_nb_model, responses, user_input)
    predict_intent(best_lr_model, responses, user_input)
