import datetime
import common
import displays_a_question
import listpage
import random
import handle_question
import handle_comments
import search
from flask import Flask, request, render_template, redirect
from displays_a_question import question_up
from displays_a_question import question_down
from displays_a_question import answer_up
from displays_a_question import answer_down
import data_manager

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/list")


@app.route('/extendurl/<col_idx>')
def extend_url(col_idx):
    return listpage.extend_url(col_idx)


@app.route("/list")
def print_table():
    return listpage.print_table()


@app.route('/new-question')
def new_question():
    """Show new question page"""
    return handle_question.new_question_route()


@app.route('/newpost', methods=["POST"])
def add_new_question():
    """Add new story to list, then redirect to /list page"""
    return handle_question.add_new_question()


@app.route('/question/<question_id>/edit')
def edit_question_route(question_id):
    return handle_question.edit_question_route(question_id)


@app.route('/modify/<question_id>', methods=["POST"])
def edit_question(question_id):
    return handle_question.edit_question(question_id)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    return handle_question.delete_question(question_id)


@app.route("/question/<int:question_id>/vote-up")
def vote_question_up(question_id):
    direction = "vote-up"
    question_up(direction, question_id)
    return redirect("/question/{0}".format(question_id))


@app.route("/question/<int:question_id>/vote-down")
def vote_question_down(question_id):
    direction = "vote-down"
    question_down(direction, question_id)
    return redirect("/question/{0}".format(question_id))


@app.route("/question/<int:question_id>/<int:answer_id>/vote-up")
def vote_answer_up(question_id, answer_id):
    direction = "vote-up"
    answer_up(direction, question_id, answer_id)
    return redirect("/question/{0}".format(question_id))


@app.route("/question/<int:question_id>/<int:answer_id>/vote-down")
def vote_answer_down(question_id, answer_id):
    direction = "vote-down"
    answer_down(direction, question_id, answer_id)
    return redirect("/question/{0}".format(question_id))


@app.route("/question/<int:question_id>")
def displays_a_single_question_A(question_id):
    sort_by = request.args.get("sort_by", "id")
    direction = request.args.get("direction", "ASC")
    answers = displays_a_question.get_answers_for_question(question_id, sort_by, direction)
    question_with_answers = displays_a_question.displays_a_single_question(question_id)
    question_with_answers["answers"] = answers
    question_with_answers["sort_by"] = sort_by
    question_with_answers["direction"] = direction
    q_comments = common.get_comments("question", question_id)  # comments for the question
    a_comments = common.get_comments("answer", question_id)  # comments for the question's answers
    return render_template(
        "display_a_question.html",
        question_with_answers=question_with_answers,
        q_comments=q_comments,
        a_comments=a_comments
    )


@app.route("/answer/<answer_id>/edit")
def edit_answer(answer_id):
    answer = common.get_answer(answer_id)
    question = common.get_question(answer["question_id"])
    return render_template("answer.html", question=question, answer=answer, mode="Edit", error="")


@app.route("/answer/<answer_id>/edit", methods=["POST"])
def edit_answer_post(answer_id):
    if len(request.form["answer"]) < 10:
        answer = common.get_answer(answer_id)
        question = common.get_question(answer["question_id"])
        return render_template("answer.html", question=question, answer=answer, mode="Edit", error="10 char")
    answer = common.get_answer(answer_id)
    answer["message"] = request.form["answer"]
    common.update("answer", answer_id, "message", answer["message"])
    return redirect("/question/{}".format(answer["question_id"]), code=302)


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    answer = common.get_answer(answer_id)
    question = common.get_question(answer["question_id"])
    date_time = answer["submission_time"]
    return render_template("del_answer.html", answer=answer, question=question, date_time=date_time)


@app.route("/answer/<answer_id>/delete", methods=["POST"])
def delete_answer_post(answer_id):
    answer = common.get_answer(answer_id)
    common.delete("answer", answer_id)
    return redirect("/question/{}".format(answer["question_id"]), code=302)


@app.route("/question/<question_id>/new-answer")
def new_answer(question_id):
    question = common.get_question(question_id)
    return render_template("answer.html", question=question, mode="Send new", error="")


@app.route("/question/<question_id>/new-answer", methods=["POST"])
def new_answer_post(question_id):
    answer = {}
    answer["submission_time"] = str(datetime.datetime.now())[:16]
    answer["vote_number"] = 0
    answer["question_id"] = question_id
    answer["message"] = request.form["answer"]
    common.insert_answer(answer)
    return redirect("/", code=302)


@app.route('/question/<question_id>/new-comment')
def add_new_question_comment(question_id):
    return handle_comments.add_new_question_comment(question_id)


@app.route('/answer/<answer_id>/new-comment')
def add_new_answer_comment(answer_id):
    return handle_comments.add_new_answer_comment(answer_id)


@app.route('/add_comment_to_db/<q_or_a>/<id>')
def add_comment_to_db(q_or_a, id):
    commit = request.args['comment']
    return handle_comments.add_comment_to_db(q_or_a, id, commit)


@app.route('/comments/<comment_id>/edit')
def edit_comment(comment_id):
    return handle_comments.edit_comment(comment_id)


@app.route('/update_comment/<comment_id>')
def update_comment_in_db(comment_id):
    comment = request.args['comment']
    return handle_comments.update_comment_in_db(comment_id, comment)


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    return handle_comments.delete_comment(comment_id)


@app.route('/handlesearch')
def search_route():
    return redirect('/search?q=' + request.args['search'])


@app.route('/search')
def search_questions_route():
    search_phrase = request.args['q']
    return search.search_questions(search_phrase)


@app.route("/question/create_new_tag")
def create_new_tag():
    rgb_color = random_color()
    return render_template("create_new_tag.html", rgb_color=rgb_color)


@app.route("/question/<int:question_id>/<int:tag_id>/delete")
def delete_tag(question_id, tag_id):
    common.delete_tag(tag_id, question_id)
    return displays_a_single_question_A(question_id)


@app.route("/question/save_new_tag/<random_color>", methods=['POST'])
def save_new_tag_and_color(random_color):
    new_tag_name = request.form["new_tag_name"]
    red_color = request.form["red_color"]
    green_color = request.form["green_color"]
    blue_color = request.form["blue_color"]
    rgb_color = "rgb({0},{1},{2})".format(red_color, green_color, blue_color)
    random_color = random_color.replace("<", "")
    random_color = random_color.replace(">", "")
    color = ""
    if rgb_color == "rgb(,,)":
        color = random_color
    else:
        color = rgb_color
    if new_tag_name != "":
        common.insert_tag(new_tag_name, color)
    else:
        pass
    return redirect("/")


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
