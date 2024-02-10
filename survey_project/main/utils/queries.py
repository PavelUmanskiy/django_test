# Реализовать с помощью минимального кол-ва SQL-запросов *без использования ORM*:
# - Общее кол-во участников опроса (например, 100)
# - На каждый вопрос:
#     - Кол-во ответивших и их доля от общего кол-ва участников опроса (например, 95 / 95%)
#     - Порядковый номер вопроса по кол-ву ответивших. Если кол-во совпадает, то и номер должен совпадать (например, для трех вопросов с 95, 95, 75 ответивших получаются соответствующие им номера 1, 1, 2)
#     - Кол-во ответивших на каждый из вариантов ответа и их доля от общего кол-ва ответивших на этот вопрос после завершения опроса.
QUESTION_STATS_QUERY = """
WITH respondents_general AS (
    SELECT 
        COUNT(DISTINCT au.id) AS total_respondents
    FROM public.main_survey AS ms
    JOIN public.main_question AS mq
        ON mq.survey_id = ms.id
    JOIN public.main_answer AS ma
        ON ma.question_id = mq.id
    JOIN public.auth_user AS au
        ON au.id = ma.respondent_id
    WHERE ms.id = %(survey_id)s
), survey_query AS (
    SELECT
        ms.id AS s_id
    FROM public.main_survey AS ms
    WHERE ms.id = %(survey_id)s
)
SELECT
    mq.id AS question,
    ma.answer_text AS chosen_answer,
    COUNT(DISTINCT au.id) AS respondents_amount,
    COUNT(ma.answer_text) AS answer_chosen_amount,
    (COUNT(ma.answer_text) / COUNT(DISTINCT au.id)) AS this_answer_ratio,
    (SELECT total_respondents FROM respondents_general) AS total_respondents
FROM public.main_survey AS ms
JOIN public.main_question AS mq
    ON mq.survey_id = ms.id
JOIN public.main_answer AS ma
    ON ma.question_id = mq.id
JOIN public.auth_user AS au
    ON au.id = ma.respondent_id
WHERE ms.id = (SELECT s_id FROM survey_query) 
GROUP BY question, chosen_answer
ORDER BY respondents_amount DESC
"""