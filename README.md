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

> **Widget _gotToFileUpload(BuildContext context)**
>
> This widget will take you to the file submission page. It is slated to be removed in
> the next iteration.

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

> **void _failedGenerationAlert(BuildContext context, List response)**
>  Draws an alert that informs the user about a failed attempt to make the
>  reports.
>
>  **inputs..**
>>    *response:* A list containing error messages strings

## Documentation for file.dart

**class FileUploader extends StatefulWidget**
 
This class loads in all of the necessary elements.

**class _FileUploaderState extends State<FileUploader>**
 
This class contains the entire layout of the file submission page. It contains a
button that will opena file chooser dialogue, a button to submit, and a ListView
of Cards that display which files have been selected for uploading. Each card
has a delete button to remove it from the list of files to submit.

> **Widget build(BuildContext context)**
>
> This is the override widget that contains all of the UI for this page.

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

## Documentation from the  payroll.py file for the backend

### This is all for the looping through of the excel workbooks

loadWorkBooks(fileList)
loops Through the fileList array and runs the readWorkBook on each file this is the main driver for the program
This requires the whole file list
It returns the retun array of the failed files or true if no files have failed

readWorkBook(wb, filename)
reads an indiual work book then prints the resulting values from in the range of cells A21->F55
It requires the Workbook and the Filename

getRange(wb)
this function loops through the work book file
it requires the work book file

getEmpinfo(conn, wb, date, rNum)
This gets the Employee information from the wb file then it runs the employee and Responded SQL insertions
It requires the SQL connection workbookFile and the Date and RunNumber from the getRunInfo

getRunInfo(conn, wb)
This gets the Run info from the sheet and runs the SQL import statements
it requires the SQL connection and the workbook file
It retuns the Run Date and Number

### This is for the SQL insertions and updates for the backend

#### This contains all of the SQL functions related to Runs

```
-------------------------------------------------------------------------------------------------------
createRun(conn, runNumber, date, stopTime, endTime, runTime, Covered, Medrun, shift)
this is the general insertion of runs into the data base.
it requires the runNumber, Date, StartTime, EndTime, Runtime,Bool for station covered, bool for Medrun, and the connextion to the sql database
-------------------------------------------------------------------------------------------------------
updateRun(conn, num, date, startTime, endTime, runTime)
this updates the run given that it has alredy been insterted into the database and has differing information then therun alredy has
it requires the runNumber, Date, StartTime, EndTime, Runtime,Bool for station covered, bool for Medrun, and the connextion to the sql database
-------------------------------------------------------------------------------------------------------
runNeedsUpdated(conn, num, date)
this checks the runs alredy in the database against the given information to see if the run needs to be updatded
it requires the Run number, date, and connection to the sql database
```

#### This Contains all of the SQL functions related to the Responded tabel

```
-------------------------------------------------------------------------------------------------------
createResponded(conn, empNumber, payRate, date, num)
this is the general insertion for the Responded Table
it requires the connection to the SQL database as well as the Employee number, payrate, date of the run, and the run number
-------------------------------------------------------------------------------------------------------
respondedNeedsUpdated(conn, empNumber, date, rNum)
this is to check the responded table against the given information to see if the responded table needs to be updated 
it requires the SQL Connection as well as Employee number, date of the run, and the run number
-------------------------------------------------------------------------------------------------------
updateResponded(conn, empNumber, payRate, date, rNum)
this is to update the responded table
it requires the connection to the SQL database as well as the Employee number, payrate, date of the run, and the run number
```

#### This Contains all of the SQL functions related to the Employee tabel

```
-------------------------------------------------------------------------------------------------------
createEmployee(conn, name, empNumber)
This is the insertion for the Employee table
It requires the SQL connection as well as the name, and employee number
-------------------------------------------------------------------------------------------------------
empNeedsUpdated(conn, empNumber)
this checks the Employee table against the given information to see if it needs to be updated
it rquires the SQL connection as well as the Employee number
-------------------------------------------------------------------------------------------------------
updateEmp(conn, name ,empNumber)
this updates the employee table given the new information
it requires the SQL connection as well as the Employee Name and Number
```
