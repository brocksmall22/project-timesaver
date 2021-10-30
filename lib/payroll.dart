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
            //TODO: Remove the next three widgets when OneDrive functionality is
            //added
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
    _checkDates();
    setState(() {});
  }

  void _checkDates() {
    if (_dates.duration.inDays == 0) {
      _hasDates = false;
    } else {
      _hasDates = true;
    }
  }

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

  void _passedGenerationAlert(BuildContext context, List response) {
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
                    //TODO: Add the ability to open the files
                    Navigator.of(context).pop();
                  },
                  child: const Text("Open files")),
              TextButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text("Close"))
            ],
          );
        });
  }

  void _failedGenerationAlert(BuildContext context, List response) {
    showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text("Reports could not be generated!"),
            content: SizedBox(
              width: 100,
              height: 75,
              child: ListView(
                children: response.map((e) => Text(e)).toList(),
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
}
