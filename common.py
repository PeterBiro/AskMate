import data_manager


def get_max_id(answers_list):
    id_list = [int(answer["answer_id"]) for answer in answers_list]
    if len(id_list) == 0:
        return -1
    else:
        return max(id_list)



def get_question(id):
    questions_list = data_manager.get_dict("question", "question.csv")
    for question in questions_list:
        if question["question_id"] == id:
            return question


def get_answer(id):
    answers_list = data_manager.get_dict("answer", "answer.csv")
    for answer in answers_list:
        if answer["answer_id"] == id:
            return answer


def get_index_from_id(list, id):
    """
    Return the index of an answer record by its id
    """
    for i in range(len(list)):
        if list[i]["answer_id"] == id:
            return i


def type_converter(dicts_in_list, keys, func):
    """
    This mapping function expects a list of dictionaries
    returns same data structure but func() is called on all key values with keys matching key param
    """
    for row in dicts_in_list:
        for key in row:
            if key in keys:
                row[key] = func(row[key])
    return dicts_in_list


def main():
    pass

if __name__ == '__main__':
    main()