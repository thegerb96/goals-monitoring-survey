"""
This document acts as storage for all goals and questions.

There are 4 total variables: overarching_goals, sub_goals, general_questions, questions_by_subgoals. The structure of
these objects is essentially arbitrary and entirely based on the current situation and how I have decided to define my
goals this year. Each goal is presented in block quotes and every question is ended with a space and questionmark.
Questions are recorded here as lists with 2 items. The first element is the question itself and the second element is
the measurement level.

There are 4 measurement levels:
    quantity: any integer greater than 0 imaginable
    likert_5: a likert scale consisting of 5 items
    yes_no: a nominal dichotomy between yes and no
    scale_10: a grade between 1 and 10
    nested: an x number of elements are given for likert_5 estimation

The measurement level is used later in requesting a response from the respondent

"""
overarching_goals = [
    """“Generate intuitive understanding of our data where I am able to clearly and comprehensively explain the data and
    its origin to my stakeholders and allowing myself to function as a point of contact.”""",
    """“Outline and continuously apply a plan of approach to every task in order to structure my approach to novel as
    well as recurring problems and a distinct feeling of having truly wrapped-up a task more often than before.”"""
]

sub_goals = {'og_1': [
        """“Become a point of contact to which questions surrounding our data can be directed.”""",
        """“Jump at every opportunity to present and hone your skills in presenting findings.”""",
        """“Reduce the time spent on issues of coverage of our features.”""",
        """“Reduce the time spent on bugs or changes in the data pipeline.”""",
        """“Generate more standardized workflows; try to explore details and tools less.”"""
    ],
    'og_2': [
        """“Always consider multiple paths before diving deep into one.”""",
        """“Employ a more structured approach, write up or think of a plan prior to starting a task.”""",
        """“Work towards feeling more finished with your tasks by having considered all elements.”""",
        """“Improve my abilities with the tools: Python, SQL, Tableau and Powerpoint.”"""
    ],
    'gnrl': [
        """“Take up more responsibility.”""",
        """“Become a better team member by improving on scrum abilities.”""",
        """“Create a clearer image of the future of my career.”"""
    ]
}

general_questions = [
    ["Were there opportunities to work towards this sub goal ?", 'yes_no'],
    ["How many times were you able to act in accordance with this sub goal ?", 'quantity'],
    ["How many hours did you spent on this ?", 'quantity'],
    ["To what extent do you feel you have come closer to achieving this this week ?", 'likert_5'],
    ["Do you think you have acted accordingly ?", 'likert_5'],
    ["How happy are you currently at work ?", 'scale_10']
]

questions_by_subgoals = {'og_1_1': [
    general_questions[0],
    general_questions[1],
    ["How many times did you answer the questions without help ?", 'quantity'],
], 'og_1_2': [
    general_questions[0],
    general_questions[1],
    ["How well do you think you have satisfied the questions ?", 'likert_5'],
], 'og_1_3': [
    ["How many coverage issues did you fix ?", 'quantity'],
    general_questions[2]
], 'og_1_4': [
    ["How many bugs have you worked on ?", 'quantity'],
    general_questions[2],
], 'og_1_5': [
    ["On a scale from 1 to 10, how standardized was your workflow this week ?", 'scale_10'],
    ["On a scale from 1 to 10, how new were the tasks you worked on this week?", 'scale_10'],
],
    'og_2_1': [
        general_questions[4],
    ], 'og_2_2': [
        general_questions[1],
        ['Do you think you did this enough ?', 'yes_no'],
    ], 'og_2_3': [
        ["When putting tasks in done, how sure were you that they were actually entirely finalized ?", 'likert_5'],
    ], 'og_2_4': [
        ["For the following tools, how much have you improved over the past week ?", 'nested',
         [
             ['Python', 'likert_5'],
             ['SQL', 'likert_5'],
             ['Tableau', 'likert_5'],
             ['Powerpoint', 'likert_5']
         ]
         ],
    ]
}
