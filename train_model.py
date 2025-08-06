from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle


def split_data(df):
    y = df['binary_label']
    X = df.drop(columns=['binary_label', 'Label'])
    
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, stratify=y,random_state=42)
    X_test, X_val, y_test, y_val = train_test_split(X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)
    return (X_train, y_train, X_val, y_val, X_test, y_test)

def train_model(X_train, y_train, X_val, y_val):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    #Validation
    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred)
    recall = recall_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred)

    validation_results = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

    return model, validation_results

def save_model(model):
    try:
        with open("cybersecurity_model.pkl", 'wb') as file:
            pickle.dump(model, file)
            print("Model saved to cybersecurity_model.pkl")
    except Exception as e:
        raise Exception(f"Error saving model: {e}")