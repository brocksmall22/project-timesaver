import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_application_1/basic_widgets.dart';
import 'package:intl/intl.dart';
import 'package:filepicker_windows/filepicker_windows.dart';

class PayrollUI extends StatefulWidget {
  const PayrollUI({Key? key}) : super(key: key);

  @override
  State<PayrollUI> createState() => _PayrollUIState();
}

class _PayrollUIState extends State<PayrollUI> {
  //TODO: Add code for error messages. Cannot be properly implemented until the
  //REST API is complete
  //TODO: Remove the redamentary file picking dialogue when we have
  //OneDrive integration
  DateTimeRange _dates =
      DateTimeRange(start: DateTime.now(), end: DateTime.now());
  bool _hasDates = false;
  OpenFilePicker file = OpenFilePicker()
    ..filterSpecification = {
      'Excel Document (*.xlsx; *.xls)': '*.xlsx;*.xls',
      'All Files': '*.*'
    }
    ..defaultFilterIndex = 0
    ..defaultExtension = 'xlsx'
    ..title = 'Select a document';
  File result = File("");

  Future<bool> _submitToPython() async {
    //TODO: add the code to connect python and flutter.
    //Cannot be properly implemented until the REST API is complete
    await Future.delayed(const Duration(seconds: 1));
    print("It works!");
    return true;
  }

  void _checkDates() {
    //Remove everything after "0" in this if when OneDrive is integrated
    if (_dates.duration.inDays == 0 || result.path.isEmpty) {
      _hasDates = false;
    } else {
      _hasDates = true;
    }
  }

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

  String _getFileName() {
    if (result.path == "") {
      return "Press to select a file";
    } else {
      return "Selected: " + result.path.split("\\").last;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text("Payroll Generator"),
        ),
        body: BasicWidgets.vertical(
          [
            _getDate(context),
            _getFile(context),
            _confirmationButtons(context),
          ],
        ));
  }

  Widget _getDate(BuildContext context) {
    return BasicWidgets.pad(ElevatedButton.icon(
      icon: const Icon(Icons.calendar_today),
      label: Text(_getDateRange()),
      onPressed: () async {
        _dates = (await showDateRangePicker(
            context: context,
            builder: (context, child) {
              return Center(
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
            },
            initialDateRange: DateTimeRange(
                start: DateTime.now().subtract(const Duration(days: 14)),
                end: DateTime.now()),
            firstDate: DateTime(DateTime.now().year - 1),
            lastDate: DateTime(DateTime.now().year + 1)))!;
        _checkDates();
        setState(() {});
      },
    ));
  }

  Widget _getFile(BuildContext context) {
    return BasicWidgets.pad(ElevatedButton.icon(
        onPressed: () async {
          result = file.getFile()!;
          _checkDates();
          setState(() {});
        },
        icon: const Icon(Icons.folder_open),
        label: Text(_getFileName())));
  }

  Widget _generatePayroll(BuildContext context) {
    return ElevatedButton(
        onPressed: _hasDates
            ? () async => ({
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
                      content: Text("Generating, please wait..."))),
                  if (await _submitToPython() == true)
                    {
                      ScaffoldMessenger.of(context).clearSnackBars(),
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                            content: const Text("Payroll generated!"),
                            backgroundColor: Colors.green,
                            action: SnackBarAction(
                              label: "Open file",
                              onPressed: () => {
                                //TODO: Code for opening the generated file
                              },
                              textColor: Colors.white,
                            )),
                      )
                    }
                  else
                    {
                      ScaffoldMessenger.of(context).clearSnackBars(),
                      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
                        content: Text("Payroll was not generated!"),
                        backgroundColor: Colors.red,
                      ))
                    }
                })
            : null,
        child: const Text("Generate"));
  }

  Widget _cancel(BuildContext context) {
    return ElevatedButton(
        onPressed: () => Navigator.pop(context), child: const Text("Cancel"));
  }

  Widget _confirmationButtons(BuildContext context) {
    return BasicWidgets.horizontal(
      [
        BasicWidgets.pad(_generatePayroll(context)),
        BasicWidgets.pad(_cancel(context))
      ],
    );
  }
}
