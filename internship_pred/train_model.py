import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import mysql.connector

def get_data_from_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="DHRUV@4508chavda",
        database="sq"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT cgpa, iq, Data_structure_problem_solves, experience_years, gender, max_spi, min_spi, get_job_percent FROM Check_internship")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    
    columns = ['cgpa', 'iq', 'Data_structure_problem_solves', 'experience_years', 'gender', 'max_spi', 'min_spi', 'get_job_percent']
    data = pd.DataFrame(rows, columns=columns)
    
    # Convert gender to numeric
    data['gender'] = data['gender'].map({'Male': 0, 'Female': 1})
    
    return data

data = get_data_from_db()

# Prepare the data
X = data.drop('get_job_percent', axis=1)
y = data['get_job_percent']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
