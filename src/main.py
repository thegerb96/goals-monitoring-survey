import os
import sys
import argparse
import enquiries
import random

import numpy as np
import pandas as pd
from datetime import date
from datetime import timedelta

import survey_content


def start_survey(weekly_entry_dict, goals_questions):
    """Initialize the survey and start the method calls."""

    # Step 1: Print welcome message:
    print("\n"
          "===================================== Weekly Goal Progression Survey ====================================\n"
          "=========================================================================================================\n"
          "======================= Another week has ended, time to see how you feel you did ! ======================\n"
          "=========================================================================================================\n"
          "---------------------------------------------------------------------------------------------------------\n"
          "\n"
          "At any time, press ctrl+c to exit the program. Your data will not be stored and next time, you will start\n"
          " with a clean slate. If a question doesn't apply to what you have done this week, please enter a 0. For \n"
          "questions that accept a float entry, please denote it as such: #.#.\n\n"

          "Let's get started with the survey:\n\n"
          "---------------------------------------------------------------------------------------------------------\n"
          f"----------------------- End of Week Goal Progression Survey: Week {date.today().strftime('%V')}, {date.today().strftime('%Y')} ------------------------------\n"
          "---------------------------------------------------------------------------------------------------------\n")

    # Step 2: Start prompting all the questions (main method of the document).
    response_dict = prompt_questions(weekly_entry_dict, goals_questions)

    # Step 3: Print thank you message, concluding the survey and letting the responded know where there answers are
    # stored
    print("\n"
          "---------------------------------------------------------------------------------------------------------\n"
          "---------------------- This is the end of the survey, thank you for taking part ! -----------------------\n"
          "---------------------------------------------------------------------------------------------------------\n"
          f"\nYour answers have been stored, recorded and can be found under:\n {os.getcwd()}/goals_monitoring"
          f"{today.strftime('%Y')}.csv\n")

    return pd.DataFrame(response_dict, index=[0])


def prompt_questions(storage_dict, content):
    """Prompt questions to respondent, record valid answers.

    This method prompts questions from the .py file referenced in the content argument. It follows a structure of:
    Overarching goals
    --> Sub goals
        --> Specific questions per sub goal

    As a start, the overarching goals are presented to the respondent for reference. Then for each of the overarching
    goals, the sub goals are shown one by one. For every sub goal, a series of predefined questions are prompted, all
    of which can be found in the content object. Then each time the user answers a question, the response is validated
    based on the measurement level as defined in the content object. Once the respondent has entered a valid response,
    it will be recorded in the storage dictionary provided.

    :param storage_dict: A dictionary thich eventually will contain a response for each question id
    :param content: a .py file containing all goals and questions.

    :return: Nothing, the provided dictionary is being mutated.
    """
    # Step 1: Welcome respondent to the start of the survey by printing the first overarching goal.
    print("You have set 2 overarching goals this year. Let's reflect on each of "
          "them and their sub goals.\n")

    for i, goal in enumerate(content.overarching_goals):

        if i == 0:
            print(f"Let's first take a look at overarching goal number 1:\n")
            print("--  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --")
            print(f"\nGoal #{i + 1}:\n{goal}\n")
        else:
            print(f"\nNext up is overarching goal number {i + 1}\n")
            print("--  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --")
            print(f"\nGoal #{i + 1}:\n{goal}\n")

        # Step 2: Once the overarching goal is printed, a count is given for the number of sub goals.
        print(f"For this goal {len(content.sub_goals[f'og_{i + 1}'])} sub goals have been defined, "
              "you will reflect on each of them.\n")
        print("--  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --")

        for j, sg in enumerate(content.sub_goals[f'og_{i + 1}']):
            # Step 3: Each sub goal is printed
            print(f'\nSub goal {i + 1}.{j + 1}: {sg}')

            for k, question in enumerate(content.questions_by_subgoals[f'og_{i + 1}_{j + 1}']):
                # Step 4: For each sub goal, we print the relevant questions.
                print('\n' + question[0])
                # Step 4a: An exception is made for the nested measurement level, the slightly different structure
                # demands a difference in logic. in actually asking the question and recording the answer given by the
                # respondent.
                if question[1] == 'nested':
                    for element in question[2]:
                        print('\n - ' + element[0])
                        response = validate_response(element[1])
                        storage_dict[f'sg_{i + 1}_{j + 1}_{k + 1}_{element[0].lower()}'] = response
                else:
                    # Step 4b: For the other questions we question the response directly and store it in the storage
                    # dictionary under a key identifiable by the order of goals_sub goals_questions.
                    response = validate_response(question[1])
                    if response in ('n', 'no', 0):
                        break
                    storage_dict[f'sg_{i + 1}_{j + 1}_{k + 1}'] = response

    # Step 5: Lastly, general goals are printed and recorded individually, for each goal the fourth general question
    # is all that is desired to know.
    print("\nLastly, there are some general goals to reflect on:")
    question = content.general_questions[3]

    for i, goal in enumerate(content.sub_goals['gnrl']):
        print(f"\nGeneral goal #{i+1}/{len(content.sub_goals['gnrl'])}: {goal}\n")
        print(question[0] + '\n')
        response = validate_response(question[1])

        storage_dict[f'gnrl_{i + 1}'] = response

    return storage_dict


def validate_response(measurement_level):
    """Validate responses entered by the respondent.

    This method takes the question as it comes from the content object and after it is posed to the respondent by the
    prompt_questions method. After the question is posed, this method will check for the accompanying measurement level
    and answer the correct question accordingly. It will do until an acceptable response is given. -1000 and an empty
    string are used as defaults in order for the while loops to be able to run. yes_no responses are transformed to
    1 | 0.

    :param measurement_level: A question represented as a list with 2 elements, the question and the measurement level
                              as defined in the content object.

    :return: A validated response
    :rtype: integer or float
    """
    # Step 1: Initialize variables to be able to make the comparison within the while loops.
    user_input_num = -1000
    user_input_str = ''

    # Step 2a: If the measurement level is yes_no we only accept the words Yes No and their lowercase counter parts as
    # well as 0, the while loop will keep asking for input for as long as the criteria is not met.
    if measurement_level == 'yes_no':
        while user_input_str.lower().strip() not in ('y', 'n', 'yes', 'no', 0):
            user_input_str = input('Please answer the question with (Y)es or (N)o: ')

    # Step 2b: if the measurement level is likert 5, then the respondent will be requested to provide an input between
    # 1 and 5, here 0 is also accepted as that acts as a way to skip a question.
    elif measurement_level == 'likert_5':
        while 0 <= abs(user_input_num) > 5:
            try:
                user_input_num = int(input('Please give an integer between 1 (Not really) '
                                           'and 5 (Very much so!): '))
            except ValueError:
                continue

    # Step 2c: If the measurement level is scale_10, the respondent is asked to provide an input ranging from 1 to 10.
    # Here, too, 0 is accepted as a way to skip the question.
    elif measurement_level == 'scale_10':
        while 0 <= abs(user_input_num) > 11:
            try:
                user_input_num = float(input('Please enter a grade between 1 and 10: '))
            except ValueError:
                continue

    # Step 2d: If the measurement level is quantity this means that any integer above 0 is accepted. 0 is also accepted
    # in this case as a way to skip the question.
    elif measurement_level == 'quantity':
        while user_input_num < 0 or not isinstance(user_input_num, int):
            try:
                user_input_num = int(input('Please enter an integer above 0: '))
            except ValueError:
                continue

    # Step 3a: In case a string input is found, 1 will be returned for yes and 0 will be returned for no. Currently no
    # other string inputs are accepted.
    if user_input_str:
        if user_input_str.lower() in ('y', 'yes'):
            return 1
        else:
            return 0

    # Step 3b: In case a numeric (float | integer) input is found (by seeing whether or not it maches the default
    # value), this will be returned.
    elif user_input_num != -1000:
        return user_input_num
    

def generate_targets(results, target_goals):
    """Generate targets for each goal we indicate that needs it

    Purely by chance, all of the goals are of measurement level liker_5, this means the targets are set at 3. The
    targets are only produced if we actually indicated that this goal was relevant for this week (indicated by
    any thing other than a 0.

    :rtype: Pandas DataFrame
    """
    targets = {}

    for goal in target_goals:
        targets[f't_{goal}'] = np.where((results[goal][0] == 0 or results[goal][0] == np.nan), 0, 3)

    return pd.DataFrame(targets, index=[0])


def generate_test_data(storage_dict, measurement_levels):
    """Generate random input for 52 weeks worth of data for testing purposes

    Looping 52 times represents the extent of a year. For each loop we assess every key for its measurement level, this
    way we can insert the correct random input. For the date field we increment today's date with 7 days at each
    iteration.
    """

    for week in range(0, 52):
        for key, value in storage_dict.items():

            if key == 'date':
                storage_dict[key].append(date.today() + timedelta(days=7 * week))

            elif key in measurement_levels['likert_5']:
                storage_dict[key].append(random.randint(1, 5))

            elif key in measurement_levels['scale_10']:
                storage_dict[key].append(random.randint(1, 10))

            elif key in measurement_levels['quantity']:
                storage_dict[key].append(random.randint(1, 15))

            elif key in measurement_levels['yes_no']:
                storage_dict[key].append(random.randint(0, 1))

    return pd.DataFrame(storage_dict)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['s', 'd', 't'], required=True,
                        help='With mode, you can specify how you want to initialize the program. There are 3 options:'
                             's = survey mode, this is to record new data. d = deletion mode, this is to delete old'
                             'records. t = test mode, this creates a test output that can be used to create analyses')
    args, unknown = parser.parse_known_args()

    # Step 1: Establish the date of today, this is to simplify syntax later on.
    today = date.today()

    # Depending on the mode the user desires to use the program in, different behaviour is triggered:
    # If the program is initialized in survey mode:
    if args.mode == 's':

        # Step 1: Initialize storage object
        weekly_result = {
            'date': today,
            'sg_1_1_1': np.nan, 'sg_1_1_2': np.nan, 'sg_1_1_3': np.nan,
            'sg_1_2_1': np.nan, 'sg_1_2_2': np.nan, 'sg_1_2_3': np.nan,
            'sg_1_3_1': np.nan, 'sg_1_3_2': np.nan,
            'sg_1_4_1': np.nan, 'sg_1_4_2': np.nan,
            'sg_1_5_1': np.nan, 'sg_1_5_2': np.nan,
            'sg_2_1_1': np.nan,
            'sg_2_2_1': np.nan, 'sg_2_2_2': np.nan,
            'sg_2_3_1': np.nan,
            'sg_2_4_1_python': np.nan, 'sg_2_4_1_sql': np.nan, 'sg_2_4_1_tableau': np.nan, 'sg_2_4_1_powerpoint': np.nan,
            'gnrl_1': np.nan,
            'gnrl_2': np.nan,
            'gnrl_3': np.nan
        }

        # Step 2: Start survey
        survey_results = start_survey(weekly_result, survey_content)

        # Step 3: Generate targets for relevant questions (mainly likert_5 questions).
        goals_needing_targets = ['sg_2_1_1', 'sg_2_2_2', 'sg_2_3_1', 'sg_2_4_1_python', 'sg_2_4_1_sql',
                                 'sg_2_4_1_tableau', 'sg_2_4_1_powerpoint', 'gnrl_1', 'gnrl_2', 'gnrl_3']

        results = pd.concat([survey_results, generate_targets(survey_results, goals_needing_targets)], axis=1)

        # Step 4: Store results
        try:
            existing_results = pd.read_csv(f"goals_monitoring_{today.strftime('%Y')}.csv",
                                           sep=';', index_col=0)
            full_df = pd.concat([existing_results, results], axis=0)
            full_df.to_csv(f"goals_monitoring_{today.strftime('%Y')}.csv", sep=';')
        except FileNotFoundError:
            results.to_csv(f"goals_monitoring_{today.strftime('%Y')}.csv", sep=';')

    # If the survey is initialized in deletion mode:
    elif args.mode == 'd':

        # Step 1: Load in the current data.
        current_data = pd.read_csv(f"goals_monitoring_{today.strftime('%Y')}.csv", sep=';')

        # Step 2: Generate the decision menu and present this to the user.
        options = list(current_data.sort_values('date', ascending=False)['date'])
        options.append('None')
        choice = enquiries.choose('Choose a date of which record you want to delete: ', options)

        # Step 2b: Allow early break. If None is selected, exit script.
        if choice == 'None':
            sys.exit(0)

        # Step 3: Ask the user for confirmation.
        confirmation = input(f'Are you sure you want to delete the record for {choice}?\n Write Yes to confirm: ')

        # Step 4: Check if confirmation is received. If so, delete record, else print notification and end script
        if confirmation.lower() == 'yes':
            current_data.drop(current_data[current_data['date'] == choice].index, inplace=True)
            current_data.to_csv(f"goals_monitoring_{today.strftime('%Y')}.csv", sep=';')
            print(f'The record for date {choice} has been deleted.')
        else:
            print("You did not answer 'Yes', nothing has been deleted")

    # If the program is initialized in test mode:
    elif args.mode == 't':

        print('Generating Test Data . . . ')

        # Step 1: Initialize Storage
        test_output = {
            'date': [],
            'sg_1_1_1': [], 'sg_1_1_2': [], 'sg_1_1_3': [],
            'sg_1_2_1': [], 'sg_1_2_2': [], 'sg_1_2_3': [],
            'sg_1_3_1': [], 'sg_1_3_2': [],
            'sg_1_4_1': [], 'sg_1_4_2': [],
            'sg_1_5_1': [], 'sg_1_5_2': [],
            'sg_2_1_1': [],
            'sg_2_2_1': [], 'sg_2_2_2': [],
            'sg_2_3_1': [],
            'sg_2_4_1_python': [], 'sg_2_4_1_sql': [], 'sg_2_4_1_tableau': [], 'sg_2_4_1_powerpoint': [],
            'gnrl_1': [],
            'gnrl_2': [],
            'gnrl_3': []
        }

        # Step 2: Initialize measurement levels, in order to ensure representative random output.
        measurement_levels_dict = {
            'likert_5': ['sg_1_2_3', 'sg_2_1_1', 'sg_2_3_1', 'sg_2_4_1_python', 'sg_2_4_1_sql', 'sg_2_4_1_tableau',
                         'sg_2_4_1_powerpoint', 'gnrl_1', 'gnrl_2', 'gnrl_3'],
            'scale_10': ['sg_1_5_1', 'sg_1_5_2'],
            'quantity': ['sg_1_1_2', 'sg_1_1_3', 'sg_1_2_2', 'sg_1_3_1', 'sg_1_3_2', 'sg_1_4_1', 'sg_1_4_2',
                         'sg_2_2_1'],
            'yes_no': ['sg_1_1_1', 'sg_1_2_1', 'sg_2_2_2']
        }

        generate_test_data(test_output, measurement_levels_dict).to_csv(
            f"TEST_DATA_goals_monitoring_{today.strftime('%Y')}.csv", sep=';')

        print(f"Done, data is stored under {os.getcwd()}/TEST_DATA_goals_monitoring_{today.strftime('%Y')}.csv")
