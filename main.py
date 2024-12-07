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


def is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def first_day_of_year(year: int) -> int:
    years = year - 1601
    offset = years + years // 4 - years // 100 + years // 400
    return offset % 7


def calculate_day_of_week(year: int, day_of_the_year: int) -> int:
    first_day = first_day_of_year(year)
    return (first_day + day_of_the_year) % 7


def calculate_day_and_month(day: int, is_leap: bool) -> tuple[int, int]:
    month = 1
    month_lengths = [31, 29 if is_leap else 28,
                     31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    while day > month_lengths[month - 1]:
        day -= month_lengths[month - 1]
        month += 1

    return day, month


def calculate_day_of_the_year(month: int, day: int, is_leap: bool) -> int:
    month_lengths = [31, 29 if is_leap else 28,
                     31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    return sum(month_lengths[:month - 1]) + day


def to_date_string(year: int, day_of_the_year: int):
    day, month = calculate_day_and_month(day_of_the_year, is_leap(year))
    return f'{year}-{month}-{day}'


def from_date_string(date: str) -> tuple[int, int]:
    parts = date.split("-")
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    day_of_the_year = calculate_day_of_the_year(month, day, is_leap(year))
    return year, day_of_the_year


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-dates', methods=['POST'])
def generate_dates():
    data = request.json
    start_year = max(int(data['startYear']), 1600)
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
    result = "Results: <br>"

    for i in range(len(answers)):
        answer: str = answers[i]
        date = dates[i]
        year, day_of_the_year = from_date_string(date)
        actual_answer = calculate_day_of_week(year, day_of_the_year)

        print(isinstance(answer, int))
        print(isinstance(answer, str))

        was_correct = False
        if (answer.isdigit() and int(answer) % 7 == actual_answer) or \
                answer.strip().lower() == DAYS_OF_THE_WEEK[actual_answer].lower():
            was_correct = True

        if was_correct:
            result += f"{date}: CORRECT <br>"
        else:
            result += f"{date}: WRONG | Answer: \
            {answer} | Was actually: {DAYS_OF_THE_WEEK[actual_answer]} <br>"

    return jsonify({'message': result})


if __name__ == '__main__':
    app.run(debug=True)
