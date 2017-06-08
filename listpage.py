import datetime
import data_manager
import common
import displays_a_question
from flask import request, render_template, redirect


def extend_url(idx):
    """
    Extends the query string in the Url with the latest sorting priority input
    """
    order = {key: request.args[key] for key in request.args}
    if idx not in order:
        order[idx] = 'desc'
    elif order[idx] == 'desc':
        order[idx] = 'asc'
    else:
        order.pop(idx)
    url = '&'.join([key + '=' + order[key] for key in order])
    url = '/list?' + url
    return redirect(url)


def print_table():
    """
    Based on sorting priorities stored in the query string,
    lists Questions with list.html
    """
    pairs = {
        'ID': 'id', 'Question': 'title', 'Date': 'submission_time',
        'Number of Views': 'view_number', 'Votes': 'vote_number'
    }
    sortingcols = request.args
    order = ','.join([pairs[col] + ' ' + sortingcols[col] for col in sortingcols][::-1])
    sql_query = """SELECT id, title, submission_time, view_number, vote_number, image FROM question"""
    if order:
        sql_query += '\nORDER BY ' + order + ';'
    questions = data_manager.run_query(sql_query)
    headers = ['question_id', 'title', 'submission_time', 'view_number', 'vote_number', 'image']
    questions = data_manager.build_dict(questions, headers)
    url = '&'.join([key + '=' + sortingcols[key] for key in sortingcols])
    return render_template('list.html', questions=questions, url=url)
