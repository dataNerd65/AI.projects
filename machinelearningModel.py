#Importing the libraries and their dependencies
import numpy as np
import spacy
import scipy.sparse
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

#Loading the spacy model
nlp = spacy.load('en_core_web_sm')

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

def process_text_with_spacy(text_or_array):
    if isinstance(text_or_array, np.ndarray):
        # Convert the NumPy array to a string
        text = ' '.join(map(str, text_or_array))
    else:
        # Use the input text directly
        text = text_or_array

    # Process the text with spaCy
    doc = nlp(text)

    # Extract lemmatized tokens
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]

    return lemmatized_tokens


def train_and_evaluate_model(model, X_train, y_train, X_test, y_test):
    if isinstance(model, GridSearchCV):
        # Fit GridSearchCV to find the best hyperparameters
        model.fit(X_train, y_train)

        # Extract the best estimator from GridSearchCV
        best_estimator = model.best_estimator_
    elif hasattr(model, 'named_steps'):
        # If model is a simple pipeline, use it directly
        best_estimator = model
    else:
        print("Invalid model. Please provide a valid model.")
        return model

    # Process text with spaCy for training and testing sets
    X_train_spacy = [' '.join(process_text_with_spacy(text)) for text in X_train]
    X_test_spacy = [' '.join(process_text_with_spacy(text)) for text in X_test]

    # Use CountVectorizer for feature extraction
    if not X_train_spacy or not X_test_spacy:
        print("No valid text data to process.")
        return model

    # Use the same CountVectorizer instance for both training and prediction
    count_vectorizer = CountVectorizer()
    X_train_transformed = count_vectorizer.fit_transform(X_train_spacy)
    X_test_transformed = count_vectorizer.transform(X_test_spacy)

    # Update the model with the trained CountVectorizer
    best_estimator.named_steps['countvectorizer'] = count_vectorizer

    # Print available steps
    print(f"Available steps: {best_estimator.named_steps.keys()}")

    # Get the last step dynamically
    last_step_name = list(best_estimator.named_steps.keys())[-1]
    final_estimator = best_estimator.named_steps[last_step_name]

    if isinstance(final_estimator, RandomForestClassifier):
        # Fit the RandomForestClassifier
        final_estimator.fit(X_train_transformed, y_train)
        # Predict and evaluate the model
        y_pred = final_estimator.predict(X_test_transformed)
    else:
        print("Invalid model step. Please provide a valid step for fitting.")
        return model

    # Printing the confusion matrix
    print(f"{type(best_estimator).__name__} Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Printing the classification report
    print(f"{type(best_estimator).__name__} Classification Report:")
    print(classification_report(y_test, y_pred))

    # Printing the accuracy score
    accuracy = metrics.accuracy_score(y_test, y_pred)
    print(f"{type(best_estimator).__name__} Accuracy: {accuracy}")

    return model

def predict_intent(model, responses, user_input):
    # Process user input with spaCy
    processed_input = [' '.join(process_text_with_spacy(text)) for text in user_input]

    # Extract the CountVectorizer from the best estimator
    count_vectorizer = model.best_estimator_['countvectorizer']

    # Transform the input using the CountVectorizer
    input_transformed = count_vectorizer.transform(processed_input)

    # Convert the sparse matrix to a dense array
    input_transformed_array = input_transformed.toarray()

    # Predict intent
    predicted_intent = model.predict(input_transformed_array)

    # Get the response
    response = [responses.get(intent, "Sorry, I don't understand. Please try again.") for intent in predicted_intent]

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
