"""
File handles quiz attempt validations
-----------------------------------------------------
 - validating answer correct or not
 - promptly updating the score of players
 - return a flag for processing other complex works
"""


def getQnObj(qid):
    """
    Fetch the question object from the storage and return it.
    """
    return {"quiz_id": "", "qn_id": "", "question": "", "correct_answer": "", "score": 0}


def validateQuizAnswer(qid, selectedOption, player):
    qnObj = getQnObj(qid)
    flag = qnObj["correct_answer"] == selectedOption
    if not flag:
        # TODO: Find a better game logic for answering correct and wrong
        player.cash -= qnObj["score"]
    return flag
