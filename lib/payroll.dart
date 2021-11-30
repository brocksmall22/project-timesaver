import 'dart:io';

import 'package:flutter/material.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:intl/intl.dart';
import 'package:project_time_saver/file.dart';
import 'package:project_time_saver/ui_api.dart';

class PayrollUI extends StatefulWidget {
  const PayrollUI({Key? key}) : super(key: key);

  @override
  State<PayrollUI> createState() => _PayrollUIState();
}

class _PayrollUIState extends State<PayrollUI> {
  //TODO: Remove the redamentary file picking info and button when we have
  // OneDrive integration
  //TODO: Allow the user to just select the blank sheets when generating as
  // opposed to requiring a copies in a specific place

  //Layout of the page
  @override
  Widget build(BuildContext context) => Scaffold(
      appBar: AppBar(
        title: const Text("Payroll Generator"),
      ),
      body: BasicWidgets.vertical(
        [
          //TODO: Remove the next three widgets when OneDrive functionality is
          // added
          const Text(
              "Don't forget to ensure all run reports have been processed!"),
          _gotToFileUpload(context),
          const SizedBox(
            height: 50,
          ),
          _getDate(context),
          _confirmationButtons(context),
        ],
      ));

  //Variables:

  DateTimeRange _dates =
      DateTimeRange(start: DateTime.now(), end: DateTime.now());
  bool _hasDates = false;

  //Widgets:

  /*
  TODO: Remove this widget when OneDrive is integrated

  This widget is a button that will take you to the file submission page.
  */
  Widget _gotToFileUpload(BuildContext context) =>
      BasicWidgets.mainNavigationButton(
          context, "Upload reports", const FileUploader());

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
  Future<bool> _submitToPython() async {
    BasicWidgets.snack(context, "Generating, please wait...");
    var response = await API
        .generatePayrollFiles([_dates.start.toString(), _dates.end.toString()]);
    if (response[0] == true) {
      BasicWidgets.snack(context, "Payroll generated!", Colors.green);
      _passedGenerationAlert(
          context, response.getRange(1, response.length).toList());
      return true;
    } else {
      BasicWidgets.snack(context, "Error generating payroll!", Colors.red);
      _failedGenerationAlert(context, response);
      return false;
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
                width: 100,
                height: 75,
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
  Draws an alert that informs the user about a failed attempt to make the
  reports.

  inputs..
    response: A list containing error messages strings
  */
  void _failedGenerationAlert(BuildContext context, List response) =>
      showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text("Reports could not be generated!"),
              content: SizedBox(
                width: 100,
                height: 75,
                child: ListView(
                  children: response.map((e) => Text(e.toString())).toList(),
                ),
              ),
              actions: [
                TextButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text("Close"))
              ],
            );
          });
}
