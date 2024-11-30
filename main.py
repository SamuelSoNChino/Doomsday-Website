from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

DAYS_OF_THE_WEEK = ["Sunday",
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday"]


def first_day_of_year(year: int) -> int:
    delta = year - 1
    offset = delta + delta // 4 - delta // 100 + delta // 400
    return (offset + 6) % 7


def calculate_day_of_week(year: int, day_of_the_year: int) -> int:
    first_day = first_day_of_year(year)
    return (first_day + day_of_the_year) % 7


def calculate_day_and_month(day: int, is_leap: bool) -> tuple[int, int]:
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


def calculate_day_of_the_year(month: int, day: int, is_leap: bool) -> int:
    number_of_days = day
    month_index = 0
    while month > month_index:
        number_of_days += month_length
        month_index += 1
        if month_index == 2:
            month_length = 29 if is_leap else 28
        elif month_index < 8 and month_index % 2 == 1:
            month_length = 31
        elif month_index < 8:
            month_length = 30
        elif month_index % 2 == 0:
            month_length = 31
        else:
            month_length = 30

    return number_of_days


def to_date_string(year: int, day_of_the_year: int):
    is_leap = year % 4 == 0
    day, month = calculate_day_and_month(day_of_the_year, is_leap)
    return f'{year}-{month}-{day}'


def from_date_string(date: str) -> tuple[int, int]:
    parts = date.split("-")
    year = int(parts[0])
    is_leap = year % 4 == 0
    month = int(parts[1])
    day = int(parts[2])
    day_of_the_year = calculate_day_of_the_year(month, day, is_leap)
    return year, day_of_the_year


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
    dates = data['dates']
    result = "Results:\n"

    for i in range(len(answers)):
        answer = answers[i]
        date = dates[i]
        year, day_of_the_year = from_date_string(date)
        correct = calculate_day_of_week(year, day_of_the_year)
        if correct == answer or correct == DAYS_OF_THE_WEEK.index(answer):
            result += f"{date} CORRECT\n"
        else:
            result += f"{date} WRONG Answer: {
                answer} Was acually: {DAYS_OF_THE_WEEK[correct]}\n"

    return jsonify({'message': result})


if __name__ == '__main__':
    app.run(debug=True)
