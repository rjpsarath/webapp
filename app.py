from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# Path to the Excel file
EXCEL_FILE = 'users.xlsx'

# Function to check if the file exists and create it if it doesn't
def create_excel_file():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=['email', 'password', 'manager_name', 'manager_email'])
        df.to_excel(EXCEL_FILE, index=False)

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    create_excel_file()  # Ensure the Excel file exists

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        manager_name = request.form['manager_name']
        manager_email = request.form['manager_email']
        
        # Load existing data
        df = pd.read_excel(EXCEL_FILE)

        # Check if email already exists
        if email in df['email'].values:
            flash("Email already exists. Please use a different email.")
        else:
            # Append new user data to the DataFrame
            new_user = pd.DataFrame({
                'email': [email],
                'password': [password],  # In production, hash the password
                'manager_name': [manager_name],
                'manager_email': [manager_email]
            })
            df = df.append(new_user, ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)  # Save to Excel
            flash("Signup successful! Please log in.")
            return redirect(url_for('login'))
    
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Load existing data
        df = pd.read_excel(EXCEL_FILE)

        # Check for valid credentials
        if email in df['email'].values and df.loc[df['email'] == email, 'password'].values[0] == password:
            flash("Login successful!")
            return redirect(url_for('login'))  # Redirect to login for now
        else:
            flash("Invalid email or password. Please try again.")
    
    return render_template('login.html')

# Run the app
if __name__ == '__main__':
    create_excel_file()  # Create Excel file on startup
    app.run(debug=True)
