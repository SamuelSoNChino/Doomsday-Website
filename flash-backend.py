from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


def first_day_of_year(year: int) -> int:
    delta = year - 1
    offset = delta + delta // 4 - delta // 100 + delta // 400
    return (offset + 6) % 7


def calculate_day_of_week(date: str) -> int:
    pass


def caluclate_day_and_month(day: int, is_leap: bool) -> tuple[int, int]:
    month = 1
    month_length = 31
    while day > month_length:
        day -= month_length
        month += 1
        if month == 2:
            month_length = 29 if is_leap else 28
        elif month < 8 and month % 2 == 1:
            month_length = 31
        elif month < 8:
            month_length = 30
        elif month % 2 == 0:
            month_length = 31
        else:
            month_length = 30
    return day, month


def to_date_string(year: int, day_of_the_year: int):
    is_leap = year % 4 == 0
    day, month = caluclate_day_and_month(day_of_the_year, is_leap)
    return f'{year}-{month}-{day}'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-dates', methods=['POST'])
def generate_dates():
    data = request.json
    start_year = int(data['startYear'])
    end_year = int(data['endYear'])
    num_dates = int(data['numDates'])

    dates = []
    for _ in range(num_dates):
        random_year = random.randint(start_year, end_year)
        day_count = 365 if random_year % 4 != 0 else 365
        random_day_of_year = random.randint(1, day_count)
        date = to_date_string(random_year, random_day_of_year)
        dates.append(date)

    return jsonify(dates)


@app.route('/check-answers', methods=['POST'])
def check_answers():
    data = request.json
    answers = data['answers']

    # Here you would verify against the generated dates and days
    # (In a real app, store the generated dates temporarily on the server)
    result = "Your answers are evaluated!"
    return jsonify({'message': result})


if __name__ == '__main__':
    app.run(debug=True)
