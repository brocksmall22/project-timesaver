# project-timesaver

## Documentation from main.dart for the UI:

**void main()**
This method runs the UI. If you set `debug` to false, it check to see if an
instance of the server is running. If so, it will continue as normal, if not, it
will start the server.

**Bugs..**
  *medium:* A small bug prevents the server from being closed with the UI. There
    is no way to capture when the UI is closing and close the server with it.
    In the next iteration, with some tuning, that is to be expected behavior.

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
createRun 
this is the general insertion of runs into the data base.
it requires the runNumber, Date, StartTime, EndTime, Runtime, and the connextion to the sql database
-------------------------------------------------------------------------------------------------------
updateRun(conn, num, date, startTime, endTime, runTime)
this updates the run given that it has alredy been insterted into the database and has differing information then therun alredy has
it requires the runNumber, Date, StartTime, EndTime, Runtime, and the connextion to the sql database
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
