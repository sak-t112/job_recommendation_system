from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your Adzuna API credentials (replace with yours)
ADZUNA_APP_ID = "8fcb0b07"
ADZUNA_APP_KEY = "9eb67cd496b5569b576fc5bda269c367"

def fetch_jobs_from_adzuna(skills, filters):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    what = skills

    filter_map = {
        'remote': 'remote',
        'fulltime': 'full-time',
        'parttime': 'part-time',
        'internship': 'internship'
    }

    for f in filters:
        if f in filter_map:
            what += f" {filter_map[f]}"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": what,
        "results_per_page": 10,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        jobs = [{
            "title": job.get("title", "No title"),
            "company": job.get("company", {}).get("display_name", "Unknown"),
            "location": job.get("location", {}).get("display_name", "N/A"),
            "description": job.get("description", "")[:200],
            "url": job.get("redirect_url", "#")
        } for job in results]
        return jobs
    else:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['skills']
    selected_filters = request.form.getlist('filters')
    jobs = fetch_jobs_from_adzuna(user_input, selected_filters)
    return render_template('result.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
