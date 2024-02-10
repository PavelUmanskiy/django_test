from typing import Any

import pandas as pd


AnswerStats = dict[str, str | int | float]
QuestionStats = dict[str, int | float | list[AnswerStats]]
SurveyStats = dict[str, int | list[QuestionStats]]


def reorganize_question_stats(db_rows: list[tuple[Any, ...]]) -> SurveyStats:
    db_columns = [
        'question_id',
        'chosen_answer', 
        'respondents_amount',
        'answer_chosen_amount',
        'this_answer_ratio',
        'total_respondents'
    ]
    df = pd.DataFrame(db_rows, columns=db_columns)
    stats = {
        'total_respondents': df['total_respondents'][0],
        'questions': [],
    }
    for id_ in df['question_id'].unique():
        question_df = df.copy()[df['question_id'] == id_].sort_values(
            by='respondents_amount',
            ascending=False
        )
        q_df_copy = question_df.copy()
        q_df_copy = q_df_copy.groupby('question_id', as_index=False)
        respondents_amount = q_df_copy.agg({'respondents_amount': 'sum'})\
            .values[0][1]
        resp_to_part_ratio = respondents_amount / df['total_respondents'][0]
        question_stats_dict = {
            'question_id': id_,
            'respondents_amount': respondents_amount,
            'resp_to_part_ratio': resp_to_part_ratio,
            'answers': [],
        }
        for answer in question_df['chosen_answer']:
            answer_df = question_df[question_df['chosen_answer'] == answer]
            answer_stats_dict = {
                'chosen_answer': answer_df.values[0][1],
                'answer_chosen_amount': answer_df.values[0][3],
                'this_answer_ratio': answer_df.values[0][4],
            }
            question_stats_dict['answers'].append(answer_stats_dict)
        stats['questions'].append(question_stats_dict)
    return stats