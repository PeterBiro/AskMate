from flask import Flask, render_template, request, redirect
import data_manager
import datetime
import common
app = Flask(__name__)


def get_answers_for_question(question_id, sort_by, direction):
    query = """
        SELECT answer.*, users.name
        FROM answer
        LEFT JOIN users ON answer.users_id = users.id
        WHERE question_id={0}
        ORDER BY {1} {2};
        """.format(question_id, sort_by, direction)
    rows = data_manager.run_query(query)
    list_of_names = [
        "answer_id",
        "submission_time",
        "vote_number",
        "question_id",
        "message",
        "image",
        "accepted",
        "user_id",
        "user_name"
    ]
    answers = data_manager.build_dict(rows, list_of_names)
    return answers


def question_up(direction, question_id):
    vote("question", direction, question_id)


def question_down(direction, question_id):
    vote("question", direction, question_id)


def answer_up(direction, question_id, answer_id):
    vote("answer", direction, question_id, answer_id)


def answer_down(direction, question_id, answer_id):
    vote("answer", direction, question_id, answer_id)


def vote(type_, direction, id, answer_id=0):
    if type_ == "question":
        query = "SELECT vote_number FROM {0} WHERE id={1}".format(type_, id)
    elif type_ == "answer":
        query = "SELECT vote_number FROM {0} WHERE id={2} AND question_id = {1}".format(type_, id, answer_id)
    else:
        pass
    updated_number = 0
    vote_num = data_manager.run_query(query)
    if direction == "vote-up" and vote_num:
        updated_number = vote_num[0][0] + 1
    elif direction == "vote-down" and vote_num:
        updated_number = vote_num[0][0] - 1
    else:
        pass
    if type_ == "question":
        update_query = """UPDATE {0} SET vote_number = {1} WHERE id = {2}""".format(type_, updated_number, id)
    elif type_ == "answer":
        update_query = """UPDATE {0} SET vote_number = {1} WHERE id = {3}
                       AND question_id = {2}""".format(type_, updated_number, id, answer_id)
    else:
        pass
    data_manager.run_query(update_query)


def displays_a_single_question(question_id):

    list_of_key_of_question = ["id", "submission_time", "view_number", "vote_number", "title", "message"]
    title_of_question = ["ID", "Submisson time", "View number", "Vote number", "Title", "Message"]
    list_of_key_and_title_of_question = list(zip(list_of_key_of_question, title_of_question))

    list_of_key_of_answer = ["answer_id", "submission_time", "vote_number", "question_id", "message", "user_name"]
    title_of_answer = ["ID", "Submisson time", "Vote number", "Question id", "Message", "Author"]
    list_of_key_and_title_of_answers = list(zip(list_of_key_of_answer, title_of_answer))

    query = "SELECT * FROM question"
    rows = data_manager.run_query(query)
    list_of_names = ["id", "submission_time", "view_number", "vote_number", "title", "message"]
    all_question = data_manager.build_dict(rows, list_of_names)
    for question_ in all_question:
        if question_id == question_["id"]:
            question = question_
            break

    query = "SELECT * FROM answer"
    rows = data_manager.run_query(query)
    list_of_names = ["id", "submission_time", "vote_number", "question_id", "message"]
    all_answers = data_manager.build_dict(rows, list_of_names)
    answers = []
    for answer in all_answers:
        if question_id == answer["question_id"]:
            answers.append(answer)
    tags = common.read_tags(question_id)
    question_with_answers = {"tags": tags,
                             "question_id": question_id,
                             "question": question,
                             "answers": answers,
                             "list_of_key_of_question": list_of_key_of_question,
                             "list_of_key_of_answer": list_of_key_of_answer,
                             "title_of_question": title_of_question,
                             "title_of_answer": title_of_answer,
                             "list_of_key_and_title_of_question": list_of_key_and_title_of_question,
                             "list_of_key_and_title_of_answers": list_of_key_and_title_of_answers}

    return question_with_answers


if __name__ == "__main__":
    app.run(debug=True)
