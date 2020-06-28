import pandas as pd
import datetime
import random

pd.set_option('display.max_colwidth', -1)
#Load CSV data
df = pd.read_csv('jeopardy.csv')
#Clean up column names - added underscores and lowercase to allow . notation
df.rename(columns={
        'Show Number': 'show_number',
        ' Air Date': 'air_date',
        ' Round': 'round',
        ' Category': 'category',
        ' Value': 'value',
        ' Question': 'question',
        ' Answer': 'answer'},
        inplace=True)

#Fixes value column to be straight floats with no $'s commas or "None"
df['value_float'] = df.value.apply(lambda x: float(x[1:].replace(',','')) if x != 'None' else 0)

#Add datetime column instead of string 'air_date'
df['date'] = df.air_date.apply(lambda x: pd.to_datetime(x))

#Filters dataset to only include rows with questions that contain all words in the user inputed list
def word_filter(dataset, words):
    filter = lambda x: all(word.lower() in x.lower() for word in words)
    return dataset.loc[dataset["question"].apply(filter)]

#Returns a sum of each answer to a question that has the keywords 
def unique_answer(dataset, words):
    filtered_data = word_filter(dataset, words)
    unique_column = filtered_data.groupby('answer').value.count().reset_index()
    return unique_column.sort_values(by=['value'], ascending=False)

#Tests the unique answer formula 
#df2 = unique_answer(df, ['King'])

#End of basic questions

#Computer use in 90s vs 2000s
filtered_by_computer = word_filter(df, ['computer'])
filtered_by_computer_90s = filtered_by_computer[(filtered_by_computer.date > datetime.datetime(1990, 1, 1)) & (filtered_by_computer.date < datetime.datetime(1999, 12, 31))]
filtered_by_computer_00s = filtered_by_computer[(filtered_by_computer.date > datetime.datetime(2000, 1, 1)) & (filtered_by_computer.date < datetime.datetime(2009, 12, 31))]
#267 questions including computer in 00s and 98 in 90s

#Jeopardy Game
def random_question(df):
    y_or_n = 'Yes'
    correct = 0
    incorrect = 0
    while (y_or_n == 'Yes'):
        random_index = random.randint(0, 216930)
        question = df.question.iloc[random_index]
        answer = df.answer.iloc[random_index]
        print(question)
        user_input = input('Please answer the question: ')
        if (user_input.lower() == answer.lower()):
            print('Good Job! You got it correct!')
            correct += 1
            score = "Correct: " + str(correct) + ' - Incorrect: ' + str(incorrect)
            print('Current Score: ' + str(score))
            y_or_n = input('Would you like another question? (Yes or No): ')
        else:
            print('Bummer. You got it incorrect! The correct answer was: ' + answer)
            incorrect += 1
            score = "Correct: " + str(correct) + ' - Incorrect: ' + str(incorrect)
            print('Current Score: ' + score)
            y_or_n = input('Would you like another question? (Yes or No)')
    return 'Final Score: ' + score

random_question(df)
    
