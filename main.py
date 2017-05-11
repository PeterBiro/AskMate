from flask import Flask, request, render_template, redirect
import datetime
import data_manager
import common
import displays_a_question
from displays_a_question import sort
from displays_a_question import vote

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/list")


@app.route('/extend/<idx>')
def extend_url(idx):
    order = {key: request.args[key] for key in request.args}
    if idx not in order:
        order[idx] = 'desc'
    elif order[idx] == 'desc':
        order[idx] = 'asc'
    else:
        order.pop(idx)
    url = '&'.join([key + '=' + order[key] for key in order])
    url = '/list?' + url
    print(url)
    return redirect(url)


@app.route("/list")
def print_table():
    pairs = {'ID': 'question_id', 'Question': 'title', 'Date': 'submisson_time', 'Number of Views': 'view_number','Votes': 'vote_number'}
    questions = data_manager.get_dict('question', 'question.csv')
    order = request.args
    for key in order.keys():
        questions = sorted(questions, key=lambda x: x[pairs[key]], reverse=True if order[key] == 'desc' else False)
    url = '&'.join([key + '=' + order[key] for key in order])
    return render_template('list.html', questions=questions, url=url)


@app.route('/new-question')
def new_question():
    """Show new question page"""
    return render_template("new-question.html")


@app.route('/newpost', methods=["POST"])
def add_new_question():
    """Add new story to list, then redirect to /list page"""
    questions = data_manager.get_dict("question", "question.csv")
    row = {}
    row["question_id"] = str(len(questions))
    row["submisson_time"] = str(datetime.datetime.timestamp(datetime.datetime.now()))
    row["view_number"] = "0"
    row["vote_number"] = "0"
    row["title"] = request.form["title"]
    row["message"] = request.form["message"]
    row["image"] = ""
    questions.append(row)
    data_manager.save_dict(questions, "question", "question.csv")
    return redirect("/list")


@app.route("/question/<int:question_id>/vote-up")
def vote_question_up(question_id):
    vote("question", "question.csv", "up", question_id, "question_id")
    return redirect("/question/{0}".format(question_id))


@app.route("/question/<int:question_id>/vote-down")
def vote_question_down(question_id):
    vote("question", "question.csv", "down", question_id, "question_id")
    return redirect("/question/{0}".format(question_id))


@app.route("/question/<int:question_id>/<int:answer_id>/vote-up")
def vote_answer_up(question_id, answer_id):
    vote("answer", "answer.csv", "up", answer_id, "answer_id")
    return redirect("/question/{0}".format(question_id))


@app.route("/question/<int:question_id>/<int:answer_id>/vote-down")
def vote_answer_down(question_id, answer_id):
    vote("answer", "answer.csv", "down", answer_id, "answer_id")
    return redirect("/question/{0}".format(question_id))


@app.route("/question/<int:question_id>")
def displays_a_single_question_A(question_id):
    question_with_answers = displays_a_question.displays_a_single_question(question_id)
    sort_by = request.args.get("sort_by", "answer_id")
    direction = request.args.get("direction", "up")
    question_with_answers["answers"] = sort(question_with_answers["answers"], sort_by, direction)
    return render_template("display_a_question.html", question_with_answers=question_with_answers)


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    answer = common.get_answer(answer_id)
    question = common.get_question(answer["question_id"])
    date_time = datetime.datetime.fromtimestamp(int(float(answer["submisson_time"]))).strftime('%Y-%m-%d %H:%M:%S')
    return render_template("del_answer.html", answer=answer, question=question, date_time=date_time)


@app.route("/answer/<answer_id>/delete", methods=["POST"])
def delete_answer_post(answer_id):
        answers_list = data_manager.get_dict("answer", "answer.csv")
        answer = answers_list.pop(common.get_index_from_id(answers_list, answer_id))
        data_manager.save_dict(answers_list, "answer", "answer.csv")
        return redirect("/question/{}".format(answer["question_id"]), code=302)


@app.route("/question/<question_id>/new-answer")
def new_answer(question_id):
    question = common.get_question(question_id)
    return render_template("answer.html", question=question, error="")


@app.route("/question/<question_id>/new-answer", methods=["POST"])
def new_answer_post(question_id):
    if len(request.form["answer"]) < 10:
        question = common.get_question(question_id)
        return render_template("answer.html", question=question, error="10 char")
    answers_list = data_manager.get_dict("answer", "answer.csv")
    answer = {}
    answer["answer_id"] = str(common.get_max_id(answers_list) + 1)
    answer["submisson_time"] = str(datetime.datetime.timestamp(datetime.datetime.now()))
    answer["vote_number"] = "0"
    answer["question_id"] = question_id
    answer["message"] = request.form["answer"]
    answer["image"] = ""
    answers_list.append(answer)
    data_manager.save_dict(answers_list, "answer", "answer.csv")
    return redirect("/", code=302)


@app.route("/question/<int:question_id>/answer/<int:answer_id>/edit")
def edit_answer(question_id, answer_id):
    answers = data_manager.get_dict("answers", "answer.csv")

    data_manager.save_dict(answers, "answers", "answer.csv")
    return redirect("/question/question_id")


@app.route("/question/<int:question_id>/answer/<int:answer_id>/delete")
def delete_an_answer(question_id, answer_id):
    answers = data_manager.get_dict("answers", "answer.csv")
    for index, row in enumerate(answers):
        if row['question_id'] == question_id and row['answer_id'] == answer_id:
            answers.remove(answers[index])
            break
    data_manager.save_dict(answers, "answers", "answer.csv")
    return redirect("/question/{0}".format(question_id))


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()