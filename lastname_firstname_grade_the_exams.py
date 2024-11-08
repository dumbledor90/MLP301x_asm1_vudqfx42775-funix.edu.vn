import sys, re, os
import numpy as np
import pandas as pd


class TestGradeCalculator:

    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
    default_dir = 'Data Files'
    output_dir = 'Output'
    id_pattern = r'^N[0-9]{8}$'
    answer_count = 25

    def __init__(self):

        self.key = np.array(self.answer_key.split(','))
        self.students = []
        self.file = ''

        self.avai_files = [
            f.replace('.txt', '') 
            for f in os.listdir(self.default_dir) if f.endswith('.txt')
        ]
        
        # Setup an empty data table to insert records later
        self.student_df = pd.DataFrame(columns=['id', 'answer'])

    def grade(self):
        '''
        Method to start grading.
        Act as a wrapper for main execution method "execute_grading"
        '''
        file = self.user_input()

        # Grade every class
        if file in ['all', 'please']:
            self.execute_grading(self.avai_files)

        # Only grade that specific class
        else:
            self.execute_grading([file])

    def execute_grading(self, files):
        '''Main method for the execution of grading'''
        
        for file in files:
            self.select_class(file)
            self.check_valid()
            self.score()
            self.output_to_file()
            self.reset_data()

    def user_input(self):
        '''Handle input from user'''
        file = input('Enter a class to grade (i.e. "class1" for class1.txt, or "all" to grade everything): ').strip().lower()

        # If user enters empty string, then find and print all available classes' name for user to select
        if not file:

            if not self.avai_files:
                print("\nThere's no class to grade")
                sys.exit(1)
            
            print("\nName's empty. Here are available classes to grade:", *self.avai_files, sep='\n')
            sys.exit(1)

        # User can inputs class1 or class1.txt
        # In case user inputs class1, add ".txt" to file name
        file = file.replace('.txt', '')

        return file
    
    def select_class(self, file):
        '''
        Check for availability of a file, return a list of strings, 
        each contains student ID and their answer string
        '''
        # Try to open file. If file's not available, exit program
        try:
            with open(f'{self.default_dir}/{file}.txt') as f:
                print(f'\nSuccessfully opened {file}.txt')
                self.file = file
                self.students = f.read().splitlines()
        
        except FileNotFoundError:
            print('\nFile cannot be found.')
            sys.exit(1)

    def check_valid(self):
        '''
        Evaluate the student ID and their answer string.
        Update the valid answer and student ID to the data table.
        '''
        print('\n**** ANALYZING ****')

        # In case the list of students' empty (i.e. file content's empty)
        if not self.students:
            print('Empty data')
            sys.exit(1)

        for student in self.students:

            # We can use regular expression to evaluate the whole student string,
            # but since we need to evaluate student ID and answer string separately,
            # we have to split here
            id, *answers = student.split(',')

            valid = True

            # Check for valid student ID
            if not re.search(self.id_pattern, id):
                print('\nInvalid line of data: N# is invalid:', student, sep='\n')
                valid = False

            # Too many or too few answers
            elif len(answers) != self.answer_count:
                print('\nInvalid line of data: does not contain exactly 26 values:', student, sep='\n')
                valid = False

            # If all's good, insert student record to a data table
            if valid:
                self.student_df = pd.concat([
                    self.student_df, 
                    pd.Series([id, answers], index=['id', 'answer']).to_frame().T
                ], ignore_index=True)

        # All students are in data table
        if len(self.student_df['id']) == len(self.students):
            print('\nNo errors found!')

        print('\n**** REPORT ****')
        print(f'\nTotal valid lines of data: {len(self.student_df['id'])}')
        print(f'Total invalid lines of data: {len(self.students) - len(self.student_df['id'])}')

    def score(self):
        '''Calculate the score of each student'''

        # Add a "score" column to data table
        self.student_df['score'] = self.student_df['answer'].map(self.calculate_score)

        print(f'Mean (average) score: {self.student_df['score'].mean():.1f}')
        print(f'Highest score: {self.student_df['score'].max()}')
        print(f'Lowest score: {self.student_df['score'].min()}')
        print(f'Range of scores: {self.student_df['score'].max() - self.student_df['score'].min()}')
        print(f'Median score: {self.student_df['score'].median()}')
        print(f'\n============== End of {self.file} ==============\n')

    def output_to_file(self):
        '''
        Write grade result to a txt file inside output folder.
        Also check if that folder exists.
        '''
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        output_file = self.file + '_grades.txt'

        # The string to write is student ID and his/her score
        self.student_df['out_string'] = self.student_df['id'] + ',' + (self.student_df['score']).map(str)

        with open(f'{self.output_dir}/{output_file}', 'w') as f:
            f.write('\n'.join(self.student_df['out_string']))

    def reset_data(self):
        '''Empty data table, in case of multiple grading'''
        self.student_df = pd.DataFrame(columns=['id', 'answer'])

    def calculate_score(self, answer):
        '''
        Helper method: Compare the answer string of each student with answer key.
        Return the score as following:
        - +4 points for each correct one
        - -1 point for each incorrect one
        '''
        answer = np.array(answer)
        correct = (answer == self.key).sum()

        # Not empty and different from answer key
        incorrect = ((answer != '') & (answer != self.key)).sum()
        
        return (4 * correct - incorrect)
    

def main():

    grader = TestGradeCalculator()
    grader.grade()


if __name__ == '__main__':
    main()