from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)

# Dummy employee credentials
employee_credentials = {
    'ED1234': '1234',
    'ED5678': '5678'
}

# Function to get response from Gemini
def get_gemini_response(input_text):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') 
    response = model.generate_content(input_text)
    return response.text

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    employee_id = request.form['employee_id']
    mpin = request.form['mpin']

    if employee_id in employee_credentials and mpin == employee_credentials[employee_id]:
        # If credentials are correct, redirect to job requirement page
        return redirect(url_for('job_requirements'))
    else:
        error_message = 'Invalid employee ID or MPIN. Please try again.'
        return render_template('login.html', error_message=error_message)

@app.route('/job-requirements')
def job_requirements():
    return render_template('job_requirements.html')

@app.route('/generate', methods=['POST'])
def generate():
    job_title = request.form['job_title']
    job_location = request.form['job_location']
    years_of_experience = request.form.get('years_of_experience', type=int)
    vacancy_count = request.form.get('vacancy_count', type=int)
    company_name = request.form['company_name']
    domain_selection = request.form['domain_selection']

    input_prompt = f"Act as a job requirement page creator with SEO(Search Engine Opimatization) knowledge that push the reach  and create a  job requirement form with the following inputs: {job_title}, {job_location}, {years_of_experience} years of experience, {vacancy_count} vacancies, {company_name}, {domain_selection} with each response points with bulletin only and response points should be bold and slightly big in size."
    response = get_gemini_response(input_prompt)
    response = response.replace('**', '')
    # Split the response into separate points
    response_points = response.split('\n')

    # Pass the job attributes and generated job description points to result.html template
    return render_template('result.html',
                           job_title=job_title,
                           job_location=job_location,
                           years_of_experience=years_of_experience,
                           vacancy_count=vacancy_count,
                           company_name=company_name,
                           domain_selection=domain_selection,
                           response_points=response_points)

if __name__ == '__main__':
    app.run(debug=True)