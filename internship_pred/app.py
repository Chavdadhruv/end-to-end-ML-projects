# from flask import Flask, request, render_template, redirect, url_for, flash
# import mysql.connector
# from mysql.connector import errorcode, DataError, DatabaseError

# app = Flask(__name__)
# app.secret_key = "your_secret_key"  # Replace with a strong secret key

# # MySQL database connection
# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd="DHRUV@4508chavda",
#         database="sq"
#     )

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/submit', methods=['POST'])
# def submit():
#     cgpa = request.form['cgpa']
#     iq = request.form['iq']
#     dsp_solves = request.form['dsp_solves']
#     experience_years = request.form['experience_years']
#     gender = request.form['gender']
#     max_spi = request.form['max_spi']
#     min_spi = request.form['min_spi']
#     get_job_percent = 1 if float(cgpa) > 8.0 and int(dsp_solves) > 200 else 0

#     data = (cgpa, iq, dsp_solves, experience_years, gender, max_spi, min_spi, get_job_percent)

#     try:
#         db = get_db_connection()
#         cursor = db.cursor()
#         cursor.execute("""
#             INSERT INTO Check_internship (cgpa, iq, Data_structure_problem_solves, experience_years, gender, max_spi, min_spi, get_job_percent)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """, data)
#         db.commit()
#         cursor.close()
#         db.close()
#         flash('Data submitted successfully!', 'success')
#     except (DataError, DatabaseError) as e:
#         flash(f'Data error occurred: {e}', 'danger')

#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="DHRUV@4508chavda",  # Replace with your MySQL password
        database="sq"
    )

# Create LJstudent_data table if it doesn't exist
def create_table():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS LJstudent_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                enrollment_number VARCHAR(50) NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                divi VARCHAR(10) NOT NULL,
                branch VARCHAR(100) NOT NULL,
                spi_sem1 FLOAT NOT NULL,
                spi_sem2 FLOAT NOT NULL,
                spi_sem3 FLOAT NOT NULL,
                over_all_ppi FLOAT NOT NULL,
                roll_number VARCHAR(50) NOT NULL,
                career_branch VARCHAR(100) NOT NULL
            )
        """)
        db.commit()
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if 'db' in locals():
            cursor.close()
            db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    enrollment_number = request.form['enrollment_number']
    phone_number = request.form['phone_number']
    divi = request.form['divi']
    branch = request.form['branch']
    spi_sem1 = float(request.form['spi_sem1'])
    spi_sem2 = float(request.form['spi_sem2'])
    spi_sem3 = float(request.form['spi_sem3'])
    over_all_ppi = float(request.form['over_all_ppi'])
    roll_number = request.form['roll_number']
    career_branch = request.form['career_branch']

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO ljstudent_data (
                first_name, last_name, enrollment_number, phone_number, divi, branch,
                spi_sem1, spi_sem2, spi_sem3, over_all_ppi, roll_number, career_branch
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, enrollment_number, phone_number, divi, branch,
              spi_sem1, spi_sem2, spi_sem3, over_all_ppi, roll_number, career_branch))
        db.commit()
        flash('Data submitted successfully!', 'success')
    except Error as e:
        flash(f'Data error occurred: {e}', 'danger')
    finally:
        if 'db' in locals():
            cursor.close()
            db.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()  # Ensure LJstudent_data table is created
    app.run(host='0.0.0.0', port=5000, debug=True)
