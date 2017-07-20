import os
from datetime import datetime
import csv
import re


class Utilities():
    def main_menu(self):
        '''Displays the main menu of the program and helps to choose
        correct option for further actions.
        '''
        print("\n\tWORK LOG")
        print("\tWhat would you like to do?")
        print("\n\ta. Add new entry")
        print("\tb. Search in existing entries")
        print("\tc. Quit program")
        while True:
            choice = ''
            choice = input('\t> ')
            if (choice.lower() == 'a' or choice.lower() == 'b' or
                    choice.lower() == 'c'):
                return choice
            else:
                print('\n\tInvalid action!!!')
                continue

    def clear_screen(self):
        '''Clearing the screen
        '''
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_file_empty(self):
        '''Checking if the file to write to is empty.
        '''
        try:
            with open("worklog.csv") as csvfile:
                csvfile.seek(0)
                first_char = csvfile.read(1)
                if not first_char:
                    return True
                else:
                    return False
        except FileNotFoundError:
            return True

    def search_menu(self):
        '''Displays the search menu of the program.
        '''
        print("\n\tDo you want to search by:")
        print("\ta. Exact date")
        print("\tb. Range of dates")
        print("\tc. Time spent")
        print("\td. Exact search")
        print("\te. Regex pattern")
        print("\tf. Return to main menu")
        while True:
            workentries = WorkEntries()
            search_choice = ''
            search_choice = input('\t> ')
            if search_choice.lower() == 'a':
                workentries.by_exact_date()
                break
            elif search_choice.lower() == 'b':
                workentries.by_rangeof_date()
                break
            elif search_choice.lower() == 'c':
                workentries.by_time_spent()
                break
            elif search_choice.lower() == 'd':
                workentries.by_exact_search()
                break
            elif search_choice.lower() == 'e':
                workentries.by_regex_pattern()
                break
            elif search_choice.lower() == 'f':
                main()
                break
            else:
                print('\n\tInvalid action!!!')
                continue

    def read_worklog(self):
        '''Reading entries from csv file.
        Then return the entries if any.
        '''
        rows = []
        try:
            with open('worklog.csv') as csvfile:
                worklog_reader = csv.DictReader(csvfile, delimiter=',')
                rows = list(worklog_reader)
            return rows
        except FileNotFoundError:
            input("\n\tThe file does not exist!" +
                  " Press Enter to return to menu.")
            return rows


class WorkEntries():
    date_task = None
    time_spent = None
    title_task = ""
    notes = ""

    def new_entry(self):
        '''Capturing attributes' values of a new task.
        Then write the task to work log file.
        '''
        utilities = Utilities()
        self.capture_data()
        try:
            self.write_header()
            self.save_entry(self.date_task, self.title_task,
                            self.time_spent, self.notes)
            utilities.clear_screen()
            input("\n\tThe entry is added. Press enter to return to menu ")
        except:
            utilities.clear_screen()
            input("\n\tENTRY NOT ADDED! Press enter to return to the menu ")
        self.clear_values()
        main()

    def clear_values(self):
        '''Initializing work log's instance state after
        recording or updating current values.
        '''
        self.date_task = None
        self.time_spent = None
        self.title_task = ""
        self.notes = ""

    def capture_date(self):
        '''Capturing and validating date of particular task.
        '''
        print("\tEnter date of task")
        while True:
            date_input = input("\tPlease use DD/MM/YYYY: ")
            try:
                datetask = datetime.strptime(date_input, "%d/%m/%Y")
                self.date_task = date_input
                break
            except ValueError:
                print("\tIncorrect date!")
                continue

    def capture_title(self):
        '''Capturing and validating name of particular task.
        '''
        while True:
            self.title_task = input("\n\tEnter the name of the task: ")
            if len(self.title_task) < 1:
                continue
            else:
                break

    def capture_time_spent(self):
        '''Capturing and validating time spent on a particular task.
        '''
        while True:
            time_input = input("\n\tEnter time spent (rounded in minutes): ")
            try:
                self.time_spent = int(time_input)
                break
            except ValueError:
                print("\tIncorrect time spent!")
                continue

    def populate_data(self, current_entry):
        '''Work log instance refreshes its state
        to reflect the currently selected entry.
        '''
        self.date_task = current_entry["DATE_TASK"]
        self.title_task = current_entry["TITLE"]
        self.time_spent = current_entry["TIME_SPENT"]
        self.notes = current_entry["NOTES"]

    def capture_data(self):
        '''Accepting data from user.
        Received information are used to either add new entry
        or updating an existing one.
        If updating, users have option to keep value of specific
        attribute or to changed it.
        '''
        keep_it = ''
        if self.date_task:
            keep_it = input("\n\tCurrent date: " +
                            "'{}'. Keep it? (Y/N): ".format(self.date_task))
            keep_it = keep_it.upper()
            if keep_it == "N":
                self.capture_date()
                keep_it = ''
        else:
            self.capture_date()

        if self.title_task:
            keep_it = input("\n\tCurrent name: " +
                            "'{}'. Keep it? (Y/N): ".format(self.title_task))
            keep_it = keep_it.upper()
            if keep_it == "N":
                self.capture_title()
                keep_it = ''
        else:
            self.capture_title()

        if self.time_spent:
            keep_it = input("\n\tCurrent time spent: " +
                            "'{}'. Keep it? (Y/N): ".format(self.time_spent))
            keep_it = keep_it.upper()
            if keep_it == "N":
                self.capture_time_spent()
                keep_it = ''
        else:
            self.capture_time_spent()

        if self.notes:
            keep_it = input("\n\tCurrent notes: " +
                            "'{}'. Keep it? (Y/N): ".format(self.notes))
            keep_it = keep_it.upper()
            if keep_it == "N":
                self.notes = input("\n\tEnter notes (Optional, " +
                                   "you can leave this empty): ")
                keep_it = ''
        else:
            self.notes = input("\n\tEnter notes (Optional, " +
                               "you can leave this empty): ")

    def write_header(self):
        '''Writting the work log file header or field names.
        '''
        utilities = Utilities()
        with open("worklog.csv", "a", newline='') as csvfile:
            fieldnames = ['DATE_TASK', 'TITLE', 'TIME_SPENT', 'NOTES']
            workwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if utilities.check_file_empty():
                workwriter.writeheader()

    def save_entry(self, date_task, title_task, time_spent, notes):
        '''Writing a nes work log to the file.
        All attributes of an entry are provided as parameters.
        '''
        with open("worklog.csv", "a", newline='') as csvfile:
            fieldnames = ['DATE_TASK', 'TITLE', 'TIME_SPENT', 'NOTES']
            workWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            workWriter.writerow({
                'DATE_TASK': date_task,
                'TITLE': title_task,
                'TIME_SPENT': time_spent,
                'NOTES': notes
                })

    def display_entry(self, search_result):
        '''Accepting a list of work log which is a result of a search.
        Then if the list is not empty, its elements are displayed one at time.
        '''
        utilities = Utilities()
        index = 0
        while True:
            utilities.clear_screen()
            if len(search_result) == 0:
                print('\n\tNo entries were found!')
                action = input("\n\t(R)eturn to menu: ")
                utilities.search_menu()
                break
            current_record = search_result[index]
            print("\n\tDate: {},".format(current_record['DATE_TASK']))
            print("\tTitle: {},".format(current_record['TITLE']))
            print("\tTime spent: {},".format(current_record['TIME_SPENT']))
            print("\tNotes: {}\n".format(current_record['NOTES']))
            print("\tResult {} of {}\n".format(index + 1, len(search_result)))
            if index == 0 and len(search_result) > 1:
                action = input("\t(N)ext, (L)ast, (E)dit," +
                               " (D)elete, (R)eturn: ")
            elif index == (len(search_result) - 1) and len(search_result) > 1:
                action = input("\t(F)irst, (P)revious, (E)dit," +
                               " (D)elete, (R)eturn: ")
            elif index == 0 and len(search_result) == 1:
                action = input("\t(E)dit, (D)elete, (R)eturn: ")
            else:
                action = input("\t(F)irst, (N)ext, (P)revious," +
                               " (L)ast, (E)dit, (D)elete, (R)eturn: ")
            if action.upper() == "N":
                if index < len(search_result) - 1:
                    index = index + 1
                    continue
            elif action.upper() == "P":
                if index > 0:
                    index = index - 1
                    continue
            elif action.upper() == "F":
                index = 0
                continue
            elif action.upper() == "L":
                index = (len(search_result) - 1)
                continue
            elif action.upper() == "D":
                self.delete_entry(current_record)
                break
            elif action.upper() == "E":
                self.edit_entry(current_record)
                break
            elif action.upper() == "R":
                utilities.clear_screen()
                utilities.search_menu()
                break

    def by_exact_date(self):
        '''Searching records using an EXACT DATE:
        Users are required to provide a date to be mached with
        work log entry's date.
        Then maching entries, if any, are displayed one at time.
        '''
        utilities = Utilities()
        result = []
        dates = []
        date_input = ""
        rows = utilities.read_worklog()
        if len(rows) == 0:
            main()
        else:
            for row in rows:
                if row['DATE_TASK'] not in dates:
                    dates.append(row['DATE_TASK'])
            print("\n\tDates having tasks: {}".format(", ".join(dates)))
            print("\n\tEnter the date")
            while True:
                date_input = input("\tPlease use DD/MM/YYYY: ")
                try:
                    date_task = datetime.strptime(date_input, "%d/%m/%Y")
                    break
                except ValueError:
                    print("\tIncorrect date!")
                    continue
            for row in rows:
                if row['DATE_TASK'] == date_input:
                    result.append(row)
            self.display_entry(result)

    def by_rangeof_date(self):
        '''Searching records using a RANGE OF DATES:
        Users are required to provide starting date and ending date.
        If starting date is before ending date, nothing is returned as result.
        Otherwise entries of which date of task are between
        the two provided dates are displayed one at time.
        '''
        utilities = Utilities()
        utilities.clear_screen()
        rows = utilities.read_worklog()
        result = []
        end_date = None
        start_date = None
        if len(rows) == 0:
            main()
        else:
            while True:
                print("\n\tStarting date")
                date_input = input("\tPlease use DD/MM/YYYY: ")
                try:
                    start_date = datetime.strptime(date_input, "%d/%m/%Y")
                    break
                except ValueError:
                    print("\tIncorrect date!")
                    continue
            while True:
                print("\n\tEnding date")
                date_input = input("\tPlease use DD/MM/YYYY: ")
                try:
                    end_date = datetime.strptime(date_input, "%d/%m/%Y")
                    break
                except ValueError:
                    print("\tIncorrect date!")
                    continue
            if end_date < start_date:
                input("\n\tEnding date must be greater than " +
                      "or equal to Starting date! " +
                      "Press enter to return to menu")
                utilities.clear_screen()
                utilities.search_menu()
            else:
                for row in rows:
                    row_date = datetime.strptime(row['DATE_TASK'], "%d/%m/%Y")
                    if start_date <= row_date and end_date >= row_date:
                        result.append(row)
                self.display_entry(result)

    def by_time_spent(self):
        '''Searching records using a TIME SPENT:
        Users are required to provide time spent to be mached with
        work log entry's time spent.
        Then maching entries, if any, are displayed one at time.
        '''
        utilities = Utilities()
        result = []
        time_spent = None
        rows = utilities.read_worklog()
        if len(rows) == 0:
            main()
        else:
            while True:
                t_spent = input("\n\tEnter time spent (rounded in minutes): ")
                try:
                    time_spent = int(t_spent)
                    break
                except ValueError:
                    print("\tIncorrect time spent!")
                    continue
            for row in rows:
                if int(row['TIME_SPENT']) == time_spent:
                    result.append(row)
            self.display_entry(result)

    def by_exact_search(self):
        '''Searching records using a EXACT STRING:
        Users are required to provide string to be mached with
        work log title/name or/and notes.
        Then maching entries, if any, are displayed one at time.
        '''
        utilities = Utilities()
        result = []
        str_search = None
        rows = utilities.read_worklog()
        if len(rows) == 0:
            input("No entries in worklog.csv file!" +
                  " Press Enter to return to menu.")
            main()
        else:
            while True:
                str_search = input("\n\tEnter your string: ")
                if len(str_search) < 1:
                    print("\tThe string must have at least one character!")
                    continue
                else:
                    break
            for row in rows:
                if (re.search(r'{}'.format(str_search), row['TITLE']) or
                        re.search(r'{}'.format(str_search), row['NOTES'])):
                    result.append(row)
            self.display_entry(result)

    def by_regex_pattern(self):
        '''Searching records using a correct REGULAR EXPRESSION:
        Users are required to provide regular expression to be mached with
        work log title/name or/and notes.
        Then maching entries, if any, are displayed one at time.
        '''
        utilities = Utilities()
        result = []
        str_search = None
        rows = utilities.read_worklog()
        if len(rows) == 0:
            main()
        else:
            while True:
                str_search = input("\n\tExample this regex will find " +
                                   "entries with number(s) in 'Name' or " +
                                   "in 'Notes': \d{1,}" +
                                   "\n\n\tEnter your regular expression: "
                                   )
                if len(str_search) < 1:
                    print("\tThat's not a regular expression!")
                    continue
                else:
                    break
            for row in rows:
                if (re.search(r'{}'.format(str_search), row['TITLE']) or
                        re.search(r'{}'.format(str_search), row['NOTES'])):
                    result.append(row)
            self.display_entry(result)

    def edit_entry(self, work_log_entry):
        '''Editing the selected entry (work log record)
        and writes changes to the file.
        '''
        utilities = Utilities()
        utilities.clear_screen()
        rows = utilities.read_worklog()
        self.populate_data(work_log_entry)
        self.capture_data()
        try:
            os.remove("tempfile.csv")
        except FileNotFoundError:
            pass
        with open("tempfile.csv", "a", newline='') as tmpfile:
            fieldnames = ['DATE_TASK', 'TITLE', 'TIME_SPENT', 'NOTES']
            workwriter = csv.DictWriter(tmpfile, fieldnames=fieldnames)
            workwriter.writeheader()
            for row in rows:
                if (row['DATE_TASK'] == work_log_entry['DATE_TASK'] and
                    row['TITLE'] == work_log_entry['TITLE'] and
                    row['TIME_SPENT'] == work_log_entry['TIME_SPENT'] and
                        row['NOTES'] == work_log_entry['NOTES']):
                    workwriter.writerow({
                        'DATE_TASK': self.date_task,
                        'TITLE': self.title_task,
                        'TIME_SPENT': self.time_spent,
                        'NOTES': self.notes
                        })
                else:
                    workwriter.writerow({
                        'DATE_TASK': row['DATE_TASK'],
                        'TITLE': row['TITLE'],
                        'TIME_SPENT': row['TIME_SPENT'],
                        'NOTES': row['NOTES']
                        })
        os.remove("worklog.csv")
        os.rename('tempfile.csv', 'worklog.csv')
        utilities.clear_screen()
        input("\n\tEntry Edited. Press enter to return to menu")
        utilities.clear_screen()
        utilities.search_menu()

    def delete_entry(self, work_log_entry):
        '''Deletes the selected entry (work log record)
        and writes changes to the file.
        '''
        utilities = Utilities()
        utilities.clear_screen()
        rows = utilities.read_worklog()
        try:
            os.remove("tempfile.csv")
        except FileNotFoundError:
            pass
        with open("tempfile.csv", "a", newline='') as tmpfile:
            fieldnames = ['DATE_TASK', 'TITLE', 'TIME_SPENT', 'NOTES']
            workwriter = csv.DictWriter(tmpfile, fieldnames=fieldnames)
            workwriter.writeheader()
            for row in rows:
                if (row['DATE_TASK'] == work_log_entry['DATE_TASK'] and
                    row['TITLE'] == work_log_entry['TITLE'] and
                    row['TIME_SPENT'] == work_log_entry['TIME_SPENT'] and
                        row['NOTES'] == work_log_entry['NOTES']):
                    continue
                workwriter.writerow({
                    'DATE_TASK': row['DATE_TASK'],
                    'TITLE': row['TITLE'],
                    'TIME_SPENT': row['TIME_SPENT'],
                    'NOTES': row['NOTES']
                    })
        os.remove("worklog.csv")
        os.rename('tempfile.csv', 'worklog.csv')
        utilities.clear_screen()
        input("\n\tEntry deleted. Press enter to return to menu")
        utilities.clear_screen()
        utilities.search_menu()


def main():
    '''Start utilities to run the program by displaying main menu otions.
    Depending on the choosen option, allow user to perform specific action.
    Or quit / end the program
    '''
    utilities = Utilities()
    utilities.clear_screen()
    menu = utilities.main_menu()
    if menu.lower() == 'a':
        utilities.clear_screen()
        work_log = WorkEntries()
        work_log.new_entry()
    elif menu.lower() == 'b':
        utilities.clear_screen()
        utilities.search_menu()
    elif menu.lower() == 'c':
        utilities.clear_screen()
        print("\n\t\t\t======= See you next time. Good bye! =======")


if __name__ == '__main__':
    main()
