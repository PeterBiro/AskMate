import datetime
import common
import data_manager
from flask import Flask, render_template, redirect


def add_new_question_comment(question_id):
    """
    Routed to url: /question/question_id/new-comment
    Renders comment.html with arguments for adding new comment for a question
    """
    sql_query = """SELECT message FROM question WHERE id={}""".format(question_id)
    question_content = data_manager.run_query(sql_query)[0][0]
    users = common.get_users()
    return render_template(
        'comment.html', basis='question', mode='Add_new', button='Create', comment = '',
        content=question_content, question_id=str(question_id), answer_id='', title='Add a',
        users=users)


def add_new_answer_comment(answer_id):
    """
    Routed to url: /answer/answer_id/new-comment
    Renders comment.html with arguments for adding new comment for an answer
    """
    question_id = data_manager.run_query("""SELECT question_id FROM answer WHERE id={}""".format(answer_id))[0][0]
    sql_query = """SELECT message FROM answer WHERE id={}""".format(answer_id)
    answer_content = data_manager.run_query(sql_query)[0][0]
    users = common.get_users()
    return render_template(
        'comment.html', basis='answer', mode='Add_new', button='Create', comment='',
        content=answer_content, question_id=str(question_id), answer_id=str(answer_id), title='Add a',
        users=users)


def add_comment_to_db(q_or_a, id, comment, user):
    """
    Routed to url: /add_comment_to_db/<q_or_a>/<id>
    Saves to new entry in the database
    """
    sql_query = ("""SELECT id FROM users WHERE name='{}';""".format(user))
    user_id = data_manager.run_query(sql_query)[0][0]
    if q_or_a == 'question':
        sql_query = (
            """INSERT INTO comment (question_id, message, users_id)
            VALUES ({}, '{}', '{}');""".format(int(id), comment, user_id)
        )
        question_id = id
    else:
        sql_query = (
            """INSERT INTO comment (answer_id, message, users_id)
            VALUES ({}, '{}', '{}' )""".format(int(id), comment, user_id)
        )
        question_id = str(data_manager.run_query("""SELECT question_id FROM answer WHERE id={}""".format(id))[0][0])
    data_manager.run_query(sql_query)
    return redirect('/question/' + question_id)


def edit_comment(comment_id):
    """
    Routed to url: /comments/<comment_id>/edit
    Renders comment.html with arguments for editing a comment
    """
    sql_query = """SELECT name FROM users WHERE id=(SELECT users_id FROM comment WHERE id={})""".format(comment_id)
    name = data_manager.run_query(sql_query)[0][0]
    sql_query = """SELECT message FROM comment WHERE id={}""".format(comment_id)
    comment = data_manager.run_query(sql_query)[0][0]
    question_id = get_question_for_comment(comment_id)
    return render_template(
        'comment.html', basis='comment', mode='Edit', button='Update', comment=comment,
        content='', question_id=question_id, answer_id='', comment_id=comment_id, title='Edit',
        name=name)


def update_comment_in_db(comment_id, comment):
    """
    routed to url: /update_comment/<comment_id>
    Saves modifications of selected comment into the database
    """
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
    """
    routed to url: /comments/<comment_id>/delete
    Deletes seleted comment from database
    """
    question_id = get_question_for_comment(comment_id)
    sql_query = "DELETE FROM comment WHERE id={}".format(int(comment_id))
    data_manager.run_query(sql_query)
    return redirect('/question/' + question_id)


def get_question_for_comment(comment_id):
    """
    Utility function, gets the appropriate question_id for a comment_id
    """
    sql_query = "SELECT question_id, answer_id FROM comment WHERE id={}".format(int(comment_id))
    ids = data_manager.run_query(sql_query)[0]
    question_id = ids[0]
    answer_id = ids[1]
    if question_id is None:
        question_id = data_manager.run_query("SELECT question_id FROM answer WHERE id={}".format(int(answer_id)))[0][0]
    return str(question_id)
