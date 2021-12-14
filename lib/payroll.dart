import 'dart:io';

import 'package:flutter/material.dart';
import 'package:project_time_saver/basic_actions.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:intl/intl.dart';
import 'package:project_time_saver/ui_api.dart';

class PayrollUI extends StatefulWidget {
  const PayrollUI({Key? key}) : super(key: key);

  @override
  State<PayrollUI> createState() => _PayrollUIState();
}

class _PayrollUIState extends State<PayrollUI> {
  _PayrollUIState() {
    _updateMostRecentRun();
    _databaseUpdateTime();
  }
  //TODO: Allow the user to just select the blank sheets when generating as
  // opposed to requiring a copies in a specific place

  //Layout of the page
  @override
  Widget build(BuildContext context) => Scaffold(
      appBar: AppBar(
        title: const Text("Payroll Generator"),
      ),
      body: _updating == false
          ? BasicWidgets.vertical(
              [
                _currentDatabaseContents(),
                const SizedBox(
                  height: 50,
                ),
                _getDate(context),
                _confirmationButtons(context),
              ],
            )
          : Center(
              child: BasicWidgets.vertical([
              BasicWidgets.pad(
                  const Text("Updating... This may take a while.")),
              BasicWidgets.pad(const CircularProgressIndicator())
            ])));

  //Variables:

  DateTimeRange _dates =
      DateTimeRange(start: DateTime.now(), end: DateTime.now());
  bool _hasDates = false;
  String _lastUpdateDate = "";
  int _mostRecentRun = 0;
  bool _updating = false;

  //Widgets:

  /*
  This widget is a combination of the text describing the database and the
  button to update the DB.
  */
  Widget _currentDatabaseContents() => BasicWidgets.horizontal(
      [_databaseContentsText(), _databaseUpdateButton()]);

  //This widget is the text describing the database.
  Widget _databaseContentsText() =>
      BasicWidgets.pad(Text("The most recent update to the database was on: " +
          _lastUpdateDate +
          "\nThe most recent run is: " +
          _mostRecentRun.toString()));

  //This widget is the button that updates the database.
  Widget _databaseUpdateButton() => BasicWidgets.pad(ElevatedButton(
      onPressed: () async {
        _updateTheDatabase();
      },
      child: const Text("Update Now")));

  //This button opens a DateRangePicker dialog to pick the start and end dates.
  Widget _getDate(BuildContext context) => BasicWidgets.pad(ElevatedButton.icon(
        icon: const Icon(Icons.calendar_today),
        label: Text(_getDateRange()),
        onPressed: () async {
          _pickDates();
        },
      ));

  //This widget contains the cancel and the generate buttons.
  Widget _confirmationButtons(BuildContext context) => BasicWidgets.horizontal(
        [
          BasicWidgets.pad(_generatePayroll(context)),
          BasicWidgets.pad(_cancel(context))
        ],
      );

  //This widget is the button that will request the API to generate the reports.
  Widget _generatePayroll(BuildContext context) => ElevatedButton(
      onPressed: _hasDates ? () async => _submitToPython() : null,
      child: const Text("Generate"));

  //This button will take you to the home page.
  Widget _cancel(BuildContext context) => ElevatedButton(
      onPressed: () => Navigator.pop(context), child: const Text("Cancel"));

  /*
  The showDateRangePicker built in function opens the DateRangePicker widget
  full screen which looks really sloppy on desktop. This widget overrides the
  default builder to open the DateRangePicker widget as a popup.

  Bugs..
    minor: You cannot close the dialouge by clicking out of it unless you click
      above or below it. Ideally it would close if you click anywhere outside.
  */
  Widget _boxedBuilder(Widget? child) => Center(
        child: ListView(
          shrinkWrap: true,
          children: [
            Center(
              child: ConstrainedBox(
                constraints:
                    const BoxConstraints(maxWidth: 400, maxHeight: 630),
                child: child,
              ),
            )
          ],
        ),
      );

  // Helper Functions //

  //This returns the text in the _getDate button.
  String _getDateRange() {
    if (_dates.duration.inDays == 0) {
      return "Press to set pay period";
    } else {
      DateFormat format = DateFormat("MM-dd-yyyy");
      DateTime start = _dates.start;
      DateTime end = _dates.end;
      return "Selected: " + format.format(start) + " - " + format.format(end);
    }
  }

  //This calls the DateRangePicker and then updates the state.
  void _pickDates() async {
    _dates = (await showDateRangePicker(
        context: context,
        builder: (context, child) {
          return _boxedBuilder(child);
        },
        initialDateRange: DateTimeRange(
            start: DateTime.now().subtract(const Duration(days: 14)),
            end: DateTime.now()),
        firstDate: DateTime(DateTime.now().year - 1),
        lastDate: DateTime(DateTime.now().year + 1)))!;
    _checkDates();
    setState(() {});
  }

  //This determines if valid dates were chosen (more than one day).
  void _checkDates() {
    if (_dates.duration.inDays == 0) {
      _hasDates = false;
    } else {
      _hasDates = true;
    }
  }

  /*
  This method is responseible for interfacing with the API and handling the
  server response. It will draw a dialog for both failed and successful cases.

  returns..
    case 1: True if the server could generate the files
    case 2: False if the files could not be generated
  */
  Future<void> _submitToPython() async {
    BasicWidgets.snack(context, "Generating, please wait...");
    await API
        .generatePayrollFiles([_dates.start.toString(), _dates.end.toString()]);
    if (!await BasicActions.displayThenClearErrors(context)) {
      BasicWidgets.snack(context, "Payroll generated!", Colors.green);
      _passedGenerationAlert(context, await API.getGenerationMessages());
      await API.clearGenerationMessages();
    } else {
      BasicWidgets.snack(context, "Error generating payroll!", Colors.red);
    }
  }

  /*
  TODO: Change output path.

  Draws an alert with information about the files as well as a way to open the
  generated files.

  inputs..
    response: A list containing true followed by strings with information about
      the reports.
  */
  void _passedGenerationAlert(BuildContext context, List response) =>
      showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text("Reports were sucessfully generated!"),
              content: SizedBox(
                width: 250,
                height: 150,
                child: ListView(
                  children: response.map((e) => Text(e)).toList(),
                ),
              ),
              actions: [
                TextButton(
                    onPressed: () {
                      Process.run("explorer.exe", [
                        "/e," +
                            Platform.environment["APPDATA"]! +
                            "\\project-time-saver"
                      ]);
                    },
                    child: const Text("Open files")),
                TextButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text("Close"))
              ],
            );
          });

  /*
  This metod is responsible for getting the time of the last database update for
  the db text.
  */
  void _databaseUpdateTime() async {
    String stored = await API.getMostRecentDatabaseUpdate();
    _lastUpdateDate = stored.isNotEmpty ? stored : "Unknown";
    setState(() {});
  }

  //This method gets the most recent run for the DB text.
  void _updateMostRecentRun() async {
    _mostRecentRun = await API.getMostRecentRun();
    setState(() {});
  }

  /*
  This method is responsible for triggering the database update. While the
  process in running, it will display a loading screen. It displays an error
  message if any errors arise.
  */
  void _updateTheDatabase() async {
    setState(() {
      _updating = true;
    });
    await API.triggerDatabaseUpdate();
    _updateMostRecentRun();
    _databaseUpdateTime();
    BasicActions.displayThenClearErrors(context);
    setState(() {
      _updating = false;
    });
  }
}
