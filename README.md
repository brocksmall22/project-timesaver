# project-timesaver

## Documentation from main.dart for the UI:

**void main()**
>
> This method runs the UI. If you set `debug` to false, it check to see if an
> instance of the server is running. If so, it will continue as normal, if not, it
> will start the server.
>
> **Bugs..**
>>   *medium:* A small bug prevents the server from being closed with the UI. There
>>     is no way to capture when the UI is closing and close the server with it.
>>     In the next iteration, with some tuning, that is to be expected behavior.

**class MyApp extends StatelessWidget**
This class contains all of the logic to construct the application

> **Widget build(BuildContext context)**
> 
> This is an ovveride of the default method and is responsible for actually rendering the UI.

**class MainPage extends StatelessWidget**

This class houses the actual layout of the home/main page of the UI. It contains
buttons to navigate to the several different features of the program. It serves
no other purpose.

> **Widget build(BuildContext context)**
> 
> This is the main layout of the opening page. Each element in the Column
> object are the buttons on the main page

> **Widget _payrollButton(BuildContext context)**
> 
> This widget is the button that will navigate to the payroll page.

> **Widget _gotToFileUpload(BuildContext context)**
> 
> This widget is the button that will navigate to the file submission page.

> **Widget _nifrsButton(BuildContext context)**
> 
> This widget is the button that will navigate to the NIFRS reporting page.

> **Widget _statsButton(BuildContext context)**
> 
> This widget is the button that will navigate to the statistics generating page.

> **Widget _settingsButton(BuildContext context)**
> 
> This widget is the button that will navigate to the settings page.

## Documentation for the payroll.dart file:

**class PayrollUI extends StatefulWidget**

This class is responsible for creating the payroll page.

**class _PayrollUIState extends State<PayrollUI>**
 
This class contains all of the UI elements and front-end logic for the payroll page.

> **Widget build(BuildContext context)**
>
> This is an ovveride method that is responsible for actually generating the page.

> **Widget _currentDatabaseContents()**
>
> This widget is a combination of the text describing the database and the
  button to update the DB.

> **Widget _databaseContentsText()**
>
>This widget is the text describing the database.

> **Widget _databaseUpdateButton()**
>
> This widget is the button that updates the database.



> **Widget _getDate(BuildContext context)**
>
> This button opens a DateRangePicker dialog to pick the start and end dates.

> **Widget _confirmationButtons(BuildContext context)**
>
> This widget contains the cancel and the generate buttons.

> **Widget _generatePayroll(BuildContext context)**
>
> This widget is the button that will request the API to generate the reports.

> **Widget _cancel(BuildContext context)**
>
> This button will take you to the home page.

> **Widget _boxedBuilder(Widget? child)**
>
> The showDateRangePicker built in function opens the DateRangePicker widget
> full screen which looks really sloppy on desktop. This widget overrides the
> default builder to open the DateRangePicker widget as a popup.
>
> **Bugs..**
>>   *minor:* You cannot close the dialouge by clicking out of it unless you click
>>     above or below it. Ideally it would close if you click anywhere outside.

> **String _getDateRange()**
>
> This returns the text in the _getDate button.

> **void _pickDates() async**
>
> This calls the DateRangePicker and then updates the state.

> **void _checkDates()**
>
> This determines if valid dates were chosen (more than one day).

> **Future<bool> _submitToPython() async**
>
> This method is responseible for interfacing with the API and handling the
> server response. It will draw a dialog for both failed and successful cases.
>
> **returns..**
>>  *case 1:* True if the server could generate the files
>>
>>   *case 2:* False if the files could not be generated

> **void _passedGenerationAlert(BuildContext context, List response)**
>
>  Draws an alert with information about the files as well as a way to open the
>  generated files.
>
>  **inputs..**
>>    *response:* A list containing true followed by strings with information about
>>      the reports.

>   **void _databaseUpdateTime() async**
>
>  This metod is responsible for getting the time of the last database update for
  the db text.

> **void _updateMostRecentRun() async**
>
>This method gets the most recent run for the DB text.

> **void _updateTheDatabase() async**
>
>This method is responsible for triggering the database update. While the
  process is running, it will display a loading screen. It displays an error
  message if any errors arise.



> **

## Documentation for file.dart

**class FileUploader extends StatefulWidget**
 
This class loads in all of the necessary elements.

**class _FileUploaderState extends State<FileUploader>**
 
This class contains the entire layout of the file submission page. It contains a
button that will open a file chooser dialogue, a button to submit, and a ListView
of Cards that display which files have been selected for uploading. Each card
has a delete button to remove it from the list of files to submit.

> **Widget build(BuildContext context)**
>
> This is the override widget that contains all of the UI for this page.

> **Widget _getLayout()**
>
>This widget determines which layout to use.
>
 >> returns..
    case 1: The main layout of the page
    case 2: A circular progress indicator when reports are being processed

> **Widget _getFile(BuildContext context)**
>
> This is the button to select new files

> **Widget _processButton(BuildContext context)**
> 
> This is the button to submit new files to the server for DB addition.

> **Widget _listOfFiles(BuildContext context)**
>
> This is the ListView of Cards that show which files are slated for
> submission.

> **List<Widget> _getFileCards(BuildContext context)**
> 
> This is a list of Card widgets that contains each file slated for submission

> **Widget _fileCard(String fileName)**
>
> This is the actual card that will contain the filename and delete button for
> files slated for submission
>
> **inputs..**
>>   *fileName:* the name of the file as a string

> **Widget _deleteButton(String fileName)**
>
> This widget is the delete button on each card.
>
> **inputs..**
>>   *fileName:* the name of the file to be removed as a String

> **void _removeFileByName(String fileName)**
>
> This function is called by the delete button on the Card and will remove the
> file from the list of files to submit.
>
> **inputs..**
>>   *fileName:* the name of the file as a String

> **Future<bool> _submitToPython() async**
>
> This is the function responsible for interfacing with the API and submitting
> the files.
>
> **returns..** 
>>   *case 1:* true if successful
>>
>>   *case 2:* false if not

> **void _failedSubmissionsAlert(BuildContext context, List response)**
>
> This function is responsible for drawing an error alert if not all files could
> be imported into the DB.
>
> **inputs..** 
>>   *response:* a list of Strings; each string is an error message

## Documentation for ui_api.dart file:

**class API**
 
This is the class that contains everything we need for connecting to the Flask side of python.

> **static Future<bool> checkIfServerIsAlive() async**
>
> This method sends a GET request to the server to determine if it is alive.
> This runs before the UI begins so that the program can spawn a new instance
> of the server as needed.
>
> **returns..**
>>   *case 1:* True if server is alive
>>
>>   *case 2:* False if server is dead

> **static Future<List> submitFilesToDatabase(List<File> files) async**
>
> This function will send a POST containing file paths to the server. The server
> is then expected to add those files to the database and return a pass/fail
> response.
>
> **inputs..** 
>>   *files:* A list of File (dart.io) objects.
> **returns..** 
>>   *case 1:* A list containing either one value of true
>>
>>   *case 2:* A list of files that could not be added to the database

> **static Future<List> generatePayrollFiles(List<String> dates) async**
>
> This function will send a POST to the server containing a Json object with
> startDate and endDate values denoting the start and end of the pay period.
> The server is expected to respond with a list of information regarding the
> generated files or a list of errors.
>
>> **inputs..**
>>   *dates:* A list of dates in string format
>> **returns..**
>>   *case 1:* A list containing true followed by information regarding the files
>>     and the path of the files generated
>>
>>   *case 2:* A list containing some errors

> **static Future<String> getOneDriveFolder() async**
>
>Calls to the backend to get the current config folder value.
>  returns..
>    A string containing the current folder

> **static Future<void> updateOneDriveFolder(String folderString) async**
>
>Requests that the backend update the config value for one drive
> folder.
>>  inputs..
    folder String:
     the new folder
  returns..
    case 1: An empty string indicating success
    case 2: A string with an error

> **static Future<String> getMostRecentDatabaseUpdate() async**
>
>Gets the most recent update to the DB from the backend.
  returns..
    The last update from the log

> **static Future<int> getMostRecentRun() async**
>
>Gets the most recent run in the DB from the backend.
  returns..
    The most recent run

> **static Future<void> triggerDatabaseUpdate() async**
>
>Triggers the backend to update the DB.

> **static Future<List> getErrors() async**
>
>Gets the errors logged from the backend.
  returns..
    A list of map objects describing the errors.

> **static Future<void> clearErrors() async**
>
>Triggers the backend to clear all of the errors logged.

> **static Future<List> getGenerationMessages() async**
>
>Gets the success messages for generating the reports from the log.
  returns..
    A list of strings

> **static Future<void> clearGenerationMessages() async**
>
>Triggers the backend to clear out the generation messages

## Documentation for the basic_widgets.dart file:

**class BasicWidgets**
 
This class contains abstractions for a handful of widgets that are frequently used.

> **static Widget pad(Widget toPad)**
>
> This widget is a wrapper for a Padding with 5 on all sides
>
> **inputs..**
>>   *toPad:* the widget you wish to pad

> **static Widget mainBox(Widget toBox)**
>
> This widget is a wrapper for a SizeBox with a width of 150
>
> **inputs..**
>>   *toBox:* the widget you wish to box

> **static Widget vertical(List<Widget> widgets)**
>
> This is a wrapper for a the Column widget with center aligned elements
>
> **inputs..**
>>   *widgets:* a list of widgets you wish to put in a Column

> **static Widget horizontal(List<Widget> widgets)**
>
> This is a wrapper for a the Row widget with center aligned elements
>
> **inputs..**
>>   *widgets:* a list of widgets you wish to put in a Row

> **static Widget mainNavigationButton(BuildContext context, String text, page)**
>
> This is a wrapper for all of the nav buttons on the main page.
>
> **inputs..**
>>   *page:* a class that contains a new page
>>
>>   *text:* The text you wish to display on the button
> **returns..**
>>   *case 1:* If page is null, it will return a button that is disabled
>>
>>   *case 2:* If page is not null, it will return a button that will navigate to
>>     the new page

> **static void snack(BuildContext context, String text, [Color? color = Colors.black54, action])**
>
> This function will draw a snakbar on the bottom of the page.
>
> **inputs..**
>>   *text:* the text you wish to display on the snackbar
>>
>>   *color (optional):* the color of the snackabar
>>       default: a dark grey color
>>
>>   *action (optional):* a SnackAction object to provide a button the user can
>>     press on the snackbar.
>>       default: null

## Documentation for the basic_actions.dart file:

**class BasicActions**
 
This class contains some methods that were frequently reused.

> **static nextPage(BuildContext context, page)**
>
> This action will add a page to the layout stack.
>
> **inputs..** 
>>   *page:* a class that contains a new page

> **static void generalAlertBox**
>
>Draws an alert that informs the user of various conditions.
  inputs..
    response: A list containing message strings. Each string goes on a new line.
    title: A string of the title for the alert box.

> **static Future<bool> displayThenClearErrors(BuildContext context) async**
>
>This method gets all the errors from the log, displays them if there are any,
  and returns if there are any.
  returns..
    case 1: true if there are errors
    case 2: false if there are not errors

## Documentation from the  payroll.py file for the backend

### This is for looping through the Excel workbooks.

> **loadWorkBooks(fileList)**
>
>Loops through the fileList array and runs the readWorkBook on each file. This is the main driver for the program.
>This requires the whole file list.
>It returns the return array of the failed files, or true if no files have failed.

> **readWorkBook(wb, filename)**
>
>Reads an individual work book then prints the resulting values in the range of cells A21->F55.
>It requires the Workbook and the Filename.

> **getRange(wb)**
>
>This function loops through the work book file.
>It requires the work book file.

> **checkForErrors(wb)**
>
>This method stops execution and raises an error if there is a detectable issue
>    with a run sheet.
>    *inputs..*
>>
>>       wb: the workbook of the current run sheet



> **getEmpinfo(conn, wb, date, rNum)**
>
>This gets the Employee information from the wb file then it runs the employee and Responded SQL insertions.
>It requires the SQL connection workbookFile and the Date and RunNumber from the getRunInfo.

> **getRunInfo(conn, wb)**
>
>This gets the Run info from the sheet and runs the SQL import statements.
>it requires the SQL connection and the workbook file.
>It returns the Run Date and Number.

 > **getFullCover(sheet, shift)**
 >This function is responsible for determining if a run was fully
 >   covered by its respective shift.
 >   *inputs..*
 >
 >>       sheet: the current run sheet
 >>       shift: the shift of the run
 >   *returns..*
 >
 >>       case 1: interger 1 if the run is fully covered
 >>       case 2: interger 0 if the run is not fully covered

### SQL insertions and updates for the backend:

#### This contains the SQL functions related to the Runs table.



> **createRun(conn, runNumber, date, stopTime, endTime, runTime, Covered, Medrun, shift)**
>
>This is the general insertion of runs into the database.
>It requires the runNumber, Date, StartTime, EndTime, Runtime,Bool for station covered, bool for Medrun, and the connection to the sql database.

> **updateRun(conn, num, date, startTime, endTime, runTime)**
>
>This updates the run given that it has already been inserted into the database and has differing information then the run already has.
>It requires the runNumber, Date, StartTime, EndTime, Runtime,Bool for station covered, bool for Medrun, and the connection to the sql database.

> **runNeedsUpdated(conn, num, date)**
>
>This checks the runs already in the database against the given information to see if the run needs to be updated.
>It requires the Run number, date, and connection to the sql database.


#### This contains all of the SQL functions related to the Responded table.


> **createResponded(conn, empNumber, payRate, date, num)**
>
>This is the general insertion for the Responded Table.
>It requires the connection to the SQL database as well as the Employee number, payrate, date of the run, and the run number.

> **respondedNeedsUpdated(conn, empNumber, date, rNum)**
>
>This is to check the responded table against the given information to see if the responded table needs to be updated 
>It requires the SQL Connection as well as Employee number, date of the run, and the run number.

> **updateResponded(conn, empNumber, payRate, date, rNum)**
>This is to update the responded table.
>It requires the connection to the SQL database as well as the Employee number, payrate, date of the run, and the run number.


#### This contains the SQL functions related to the Employee table.



> **createEmployee(conn, name, empNumber)**
>
>This is the insertion for the Employee table.
>It requires the SQL connection as well as the name, and employee number.

> **empNeedsUpdated(conn, empNumber)**
>
>This checks the Employee table against the given information to see if it needs to be updated.
>It requires the SQL connection as well as the Employee number.

> **updateEmp(conn, name ,empNumber)**
>
>This updates the employee table given the new information.
>It requires the SQL connection as well as the Employee Name and Number.


## Documentation for the api.py file:

> **def verify_awake():**
>
>This function is for the UI to determine if the server is running. If the server
>sees any call to this address, it will return a signal signifying the server is alive.
>If the UI receives a socket error, that means the server is not running and needs
>to be started.
>
> *inputs..*
>>    (request) Any request on this address
> *returns..* 
>>    case 1: A Json object signifying the server is alive


> **def submit_reports():**
>
>This is the function responsible for accepting a request from the UI that
>contains a list of file paths and forwarding that to the backend to insert
>the information into the database.
>
> *inputs..*
>>    (request): A post request containing a Json array of strings.
> *returns..*
>>    case 1: A Json array containing true (in the case of successful inserts)
>>    case 2: A list of files that failed to be inserted


> **def generate_reports():**
>
>This is the function responsible for accepting a request from the UI
>to tell the backend the user wishes to generate the pay reports.
>
> *inputs..*
>>    (request): A Json object containing two key value pairs
>>        startDate and endDate that express the start and end of the
>>        pay period as strings
> *returns..* 
>>    case 1: A Json array that either contains a True value
>>        and several strings
>>    case 2: A Json array that contains one or more strings in
>>        the event that the files could not be generated

## Documentation for generate_report.py file:

> **def generate_report(start_date, end_date):**
>
>This function is responsible for being called from the API, running all the
>    generation steps, and returning a confirmation or fail message.
>    *inputs..*
>>        start_date: the first date as a string
>>        end_date: the last date as a string
>    *returns..*
>>        case 1: a list containing True in the first position followed be some
>>            strings with basic details about the report
>>        case 2: an error message to be displayed to the user


> **def get_number_of_runs(conn, start_date, end_date):**
>
>This method gets the number of runs for a given period.
>    *inputs..*
>>        conn: the connection to the SQL
>>        start_date: the first date as a string
>>        end_date: the last date as a string
>    *returns..*
>>        case 1: the number of runs


> **def get_first_run_number(conn, start_date, end_date):**
>This method gets the lowest run number for a given period.
>    inputs..
>>        conn: the connection to the SQL
>>        start_date: the first date as a string
>>        end_date: the last date as a string
>    *returns..*
>>        case 1: the first run


> **def get_last_run_number(conn, start_date, end_date):**
>
>This method gets the highest run number for a given period.
>    *inputs..*
>>        conn: the connection to the SQL
>>        start_date: the first date as a string
>>        end_date: the last date as a string
>    *returns..*
>>        case 1: the last run


> **def fill_sheet(conn, wb, start_date, end_date):**
>
> This method fills and saves a copy of the master copy of the tally sheet.
>    *inputs..*
>>        conn: the connection to the SQL
>>        wb: the xlsx workbook we are working with
>>        start_date: the first date as a string
 >>       end_date: the last date as a string


> **def get_count(conn, city_number, start_date, end_date):**
>
>This method gets the number of runs a specific person
>    responded to in a given period.
>    *inputs..*
>>        conn: the connection to the SQL
>>        city_number: the city assigned employee ID
>>        start_date: the first date as a string
>>        end_date: the last date as a string
>    *returns..*
>>        case 1: the number of runs in a given period


> **def get_hours(conn, city_number, start_date, end_date):**
>
>This method gets the number of hours a specific person
>    worked on runs in a given period.
>    *inputs..*
>>        conn: the connection to the SQL
>>        city_number: the city assigned employee ID
>>        start_date: the first date as a string
>>        end_date: the last date as a string
>    *returns..*
>>        case 1: the number of hours a given employee worked


> **def update_employee_nulls(conn, sheet):**
>
>This method updates the Employee table to ensure no employees have a NULL
>    value in the city_number column. If they do they will not be paid.
>    *inputs..*
>>        conn: the connection to the SQL
>>        sheet: the sheet for the tally xlsx


> **def insert_city_ids(conn, nullEmps, sheet):**
>
>This method actually inserts the city IDs for update_employee_nulls
>    *inputs..*
>>        conn: the connection to the SQL
>>        nullEmps: a list of employee rows that have null city_number values 
>>        sheet: the sheet for the tally xlsx

> **def getRange(sheet):**
>
>This method gets the final row that we are concerned with editing.
>    *inputs..*
>>        sheet: the sheet for the tally xlsx


> **def match_names(name, fname, lname):**
>
>This method will take a name from the run reports and compare it to
>    a name in the tally xlsx in order to determine if they are the same
>    person.
>    *inputs..*
>>        name: the name from the run report/responded table
>>        fname: the first name from the tally
>>        lname: the last name from the tally
>    *returns..*
>>        case 1: True if they are the same person
>>        case 2: False if they aren't the same person


## Documentation for logger.py file:
> **createLogIfNotExists(file = "")**
>
>Detects if log file is present.

> **def getLastUpdate(file = "")**
>
>Checks if the config file has been created, then returns the last update.

> **def setLastUpdate(newUpdate, file = "")**
>
>Updates the last update value.

> **getErrors(file = "")**
>
>Gets the logged errors.

> **addNewError(type: str, datetime: datetime, message: str, file = "")**
>
>Adds a new error to the log.

> **clearErrors(file = "")**
>
>Removes all logged errors.

> **getGenerateMessages(file = "")**
>
>Gets the generation messages.

> **addNewGenerateMessage(newMessage, file = "")**
>
>Adds a new generation message.

> **clearGenerateMessages(file = "")**
>
>Resets the generation messages.

## Documentation for Backup_manager.py

    
>    **getLocalDB(database_path)**
>    This method gets the local database file.
>    
>    *inputs..*
>>        (database_path): takes a filepath as a string to the database used for testing.
>    *returns..*
>>        The database file
   
    
>    **uploadLocalDB(database, onedrive_path)**
>    This method uploads the database to the onedrive folder.
>
>    *inputs..*
>>        (database, onedrive_path):takes the database folder itself. takes a filepath to the one drive folder as a string used for testing.
>    *returns..*
>>        The full filepath of the uploaded folder
    

>    *getCloudDB(database_path)*
>    This method gets the cloud database file.
>
>    *inputs..*
>>        (database_path): takes a filepath as a string to the database used for testing.
>    *returns..*
>>        The database file


>    **downloadCloudDB(database, local_path)**
>    This method checks to see if the two databases are different. If different, it downloads the database.
>
>    *inputs..*
>>        (database, local_path):takes the database folder itself. takes a filepath to the local database as a string used for testing.
>    *returns..*
>>        The full filepath of the downloaded file
>>        Database is already on current version. if the database does not need updated


>    **generateHash(filepath)**
>    This method generates the Hash of files contents.
>
>    *inputs..*
>>        (filepath): takes a filepath as a string.
>    *returns..*
>        The hash hexdigest upon completion


>    **checksum(local_filePath, cloud_filePath)**
>    This method runs the generate function on two files and checks the hashes.
>
>    *inputs..*
>>        (local_filePath, cloud_filePath): these are the paths to the local file path and cloud filepath.
>    *returns..*
>>        True upon Matching Hashes 
>>
>>        False upon non matching hashes
>>
