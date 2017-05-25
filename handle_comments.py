import datetime
import data_manager
from flask import Flask, render_template, redirect


def add_new_question_comment(question_id):
    sql_query = """SELECT message FROM question WHERE id={}""".format(question_id)
    question_content = data_manager.run_query(sql_query)[0][0]
    return render_template(
        'comment.html', basis='question', mode='Add_new', button='Create',
        content=question_content, question_id=str(question_id), answer_id='', title='Add a'
        )


def add_new_answer_comment(answer_id):
    question_id = data_manager.run_query("""SELECT question_id FROM answer WHERE id={}""".format(answer_id))[0][0]
    sql_query = """SELECT message FROM answer WHERE id={}""".format(answer_id)
    answer_content = data_manager.run_query(sql_query)[0][0]
    return render_template(
        'comment.html', basis='answer', mode='Add_new', button='Create',
        content=answer_content, question_id=str(question_id), answer_id=str(answer_id), title='Add a'
        )


def add_comment_to_db(q_or_a, id, comment):
    curr_time = str(datetime.datetime.now())[:16]
    if q_or_a == 'question':
        print(id, comment, curr_time)
        sql_query = (
            """INSERT INTO comment (question_id, message, submission_time)
            VALUES ({}, '{}', '{}');""".format(int(id), comment, curr_time)
        )
        question_id = id
    else:
        sql_query = (
            """INSERT INTO comment (answer_id, message, submission_time)
            VALUES ({}, '{}', '{}' )""".format(int(id), comment, curr_time)
        )
        question_id = str(data_manager.run_query("""SELECT question_id FROM answer WHERE id={}""".format(id))[0][0])
    data_manager.run_query(sql_query)
    return redirect('/question/' + question_id)


def edit_comment(comment_id):
    sql_query = """SELECT message FROM comment WHERE id={}""".format(comment_id)
    content = data_manager.run_query(sql_query)[0][0]
    return render_template(
        'comment.html', basis='comment', mode='Edit', button='Update',
        content=content, question_id='', answer_id='', comment_id=comment_id, title='Edit'
        )


def update_comment_in_db(comment_id, comment):
    counter = data_manager.run_query("SELECT edited_count FROM comment WHERE id={}".format(int(comment_id)))[0][0]
    curr_time = str(datetime.datetime.now())[:16]
    counter = 1 if not counter else counter + 1
    sql_query = (
            """UPDATE comment
            SET submission_time='{}', message='{}', edited_count={}
            WHERE id={}""".format(curr_time, comment, counter, int(comment_id))
        )
    data_manager.run_query(sql_query)
    question_id = get_question_for_comment(comment_id)
    return redirect('/question/' + question_id)


def delete_comment(comment_id):
    return handle_comments.delete_comment(comment_id)


def get_question_for_comment(comment_id):
    sql_query = "SELECT question_id, answer_id FROM comment WHERE id={}".format(int(comment_id))
    ids = data_manager.run_query(sql_query)[0]
    question_id = ids[0]
    answer_id = ids[1]
    if question_id is None:
        question_id = data_manager.run_query("SELECT question_id FROM answer WHERE id={}".format(int(answer_id)))[0][0]
    return str(question_id)
