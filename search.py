"""Search in questions & answers module
"""

from flask import Flask, request, render_template, redirect
import data_manager


def make_fancy(term, table, key):
    """insert html tag into string for jinja formatting"""
    searchterm = term.lower()
    for row in table:
        row[key] = row[key].replace(term, "<mark>" + term + "</mark>")
        row[key] = row[key].replace(searchterm, "<mark>" + searchterm + "</mark>")
    return table


def search_questions(term):
    """search for answers and questions with the given search term and display it
    # search for answers with search term in their message"""

    searchterm = term.lower()

    # select questions

    question_query = """SELECT DISTINCT id, title, message, submission_time
                        FROM question
                            WHERE id = ANY (SELECT question_id
                                                FROM answer
                                                    WHERE LOWER(title) LIKE '%{0}%' OR LOWER(message) LIKE '%{0}%')
                                    OR LOWER(message) LIKE '%{0}%' OR LOWER(title) LIKE '%{0}%';""".format(searchterm)

    table = data_manager.run_query(question_query)

    if table:
        keys = ("question_id", "title", "message", "submission_time")
        questions = data_manager.build_dict(table, keys)
        fancy_questions = make_fancy(term, questions, "title")
        fancy_questions = make_fancy(term, questions, "message")
    else:
        return render_template('search_results.html', questions=[], answers=[])

    # select related answers

    answer_query = """SELECT DISTINCT id, message, question_id
                        FROM answer
                            WHERE question_id = ANY (SELECT id
                                                        FROM question
                                                            WHERE LOWER(title) LIKE '%{0}%' OR LOWER(message) LIKE '%{0}%')
                                    OR LOWER(message) LIKE '%{0}%';""".format(searchterm)

    table = data_manager.run_query(answer_query)
    keys = ("answer_id", "message", "question_id")
    answers = data_manager.build_dict(table, keys)
    fancy_answers = make_fancy(term, answers, "message")

    return render_template('search_results.html', questions=fancy_questions, answers=fancy_answers)


def main():
    pass


if __name__ == '__main__':
    main()
