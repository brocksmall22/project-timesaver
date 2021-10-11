import 'package:flutter/material.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:intl/intl.dart';
import 'package:project_time_saver/file.dart';

class PayrollUI extends StatefulWidget {
  const PayrollUI({Key? key}) : super(key: key);

  @override
  State<PayrollUI> createState() => _PayrollUIState();
}

class _PayrollUIState extends State<PayrollUI> {
  //TODO: Add code for error messages. Cannot be properly implemented until the
  //REST API is complete
  //TODO: Remove the redamentary file picking info and button when we have
  //OneDrive integration
  //TODO: Resolve remaining function specific tasks

  // Layout of the page //
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text("Payroll Generator"),
        ),
        body: BasicWidgets.vertical(
          [
            //TODO: Remove the next two widgets when OneDrive functionality is
            //added
            const Text(
                "Don't forget to ensure all run reports have been processed!"),
            _gotToFileUpload(context),
            _getDate(context),
            _confirmationButtons(context),
          ],
        ));
  }

  // Variables //
  DateTimeRange _dates =
      DateTimeRange(start: DateTime.now(), end: DateTime.now());
  bool _hasDates = false;

  // Widgets //
  //TODO: Remove this widget when OneDrive is integrated
  Widget _gotToFileUpload(BuildContext context) {
    return BasicWidgets.mainNavigationButton(
        context, "Upload reports", const FileUploader());
  }

  Widget _getDate(BuildContext context) {
    return BasicWidgets.pad(ElevatedButton.icon(
      icon: const Icon(Icons.calendar_today),
      label: Text(_getDateRange()),
      onPressed: () async {
        _pickDates();
        _checkDates();
        setState(() {});
      },
    ));
  }

  Widget _confirmationButtons(BuildContext context) {
    return BasicWidgets.horizontal(
      [
        BasicWidgets.pad(_generatePayroll(context)),
        BasicWidgets.pad(_cancel(context))
      ],
    );
  }

  Widget _generatePayroll(BuildContext context) {
    return ElevatedButton(
        onPressed: _hasDates ? () async => _submitToPython() : null,
        child: const Text("Generate"));
  }

  Widget _cancel(BuildContext context) {
    return ElevatedButton(
        onPressed: () => Navigator.pop(context), child: const Text("Cancel"));
  }

  Widget _boxedBuilder(Widget? child) {
    return Center(
      child: ListView(
        shrinkWrap: true,
        children: [
          Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 400, maxHeight: 630),
              child: child,
            ),
          )
        ],
      ),
    );
  }

  // Helper Functions //
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
  }

  void _checkDates() {
    if (_dates.duration.inDays == 0) {
      _hasDates = false;
    } else {
      _hasDates = true;
    }
  }

  Future<bool> _submitToPython() async {
    //TODO: add the code to connect python and flutter.
    //Cannot be properly implemented until the REST API is complete.
    BasicWidgets.snack(context, "Generating, please wait...");
    //This Future.delayed represents the action of contacting the API. Currently
    //returns a bool signifiying if it worked. Does not need to do this.
    await Future.delayed(const Duration(seconds: 1));
    bool _worked = true;
    if (_worked) {
      BasicWidgets.snack(
          context, "Payroll generated!", Colors.green, _openPayroll());
    } else {
      BasicWidgets.snack(context, "Error generating payroll!", Colors.red);
    }
    return _worked;
  }

  SnackBarAction _openPayroll() {
    return SnackBarAction(
      label: "Open file",
      onPressed: () => {
        //TODO: Code for opening the generated file
      },
      textColor: Colors.white,
    );
  }
}
