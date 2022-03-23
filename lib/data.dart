import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:project_time_saver/basic_actions.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/ui_api.dart';

class DataUI extends StatefulWidget {
  const DataUI({Key? key}) : super(key: key);

  @override
  State<DataUI> createState() => _DataUIState();
}

class _DataUIState extends State<DataUI> {
  //This is where the layout is generated.
  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: const Text("Settings"),
        ),
        body: !images ? Center(child: _noImageLayout()) : _imageLayout(),
      );

  // Variables
  DateTimeRange _dates =
      DateTimeRange(start: DateTime.now(), end: DateTime.now());
  bool images = false;
  Map<String, ImageProvider<Object>> imageMap = {};
  bool _readyToGenerate = false;

  // Widgets

  //This widget is the layout without any generated images.
  Widget _noImageLayout() =>
      BasicWidgets.vertical([_getDate(context), _generateButton()]);

  //This is the widget layout for when there are images.
  Widget _imageLayout() {
    List<Widget> imageWidgets = [];
    for (var key in imageMap.keys) {
      imageWidgets.add(BasicWidgets.vertical([
        const SizedBox(
          height: 25,
        ),
        _title(key),
        Image(
            image: imageMap[key]!,
            width: MediaQuery.of(context).size.width * .9),
      ]));
    }
    imageWidgets.add(BasicWidgets.vertical([
      const SizedBox(
        height: 25,
      ),
      _noImageLayout(),
      const SizedBox(
        height: 25,
      )
    ]));
    return ListView(
      children: imageWidgets,
    );
  }

  //This widget is to make the title displaying a little nicer
  Widget _title(String text) => Text(
        text,
        style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
      );

  //This button opens a DateRangePicker dialog to pick the start and end dates.
  Widget _getDate(BuildContext context) => BasicWidgets.pad(ElevatedButton.icon(
        icon: const Icon(Icons.calendar_today),
        label: Text(_getDateRange()),
        onPressed: () async {
          _pickDates();
        },
      ));

  //This button is to tigger the generation of the images.
  Widget _generateButton() => ElevatedButton(
      child: const Text("Generate Graphics"),
      onPressed: _readyToGenerate
          ? () async {
              imageMap = await API.generateCharts(
                  _dates.start.toString(), _dates.end.toString());
              if (imageMap.isEmpty) {
                BasicActions.generalAlertBox(
                    context,
                    [
                      const Text(
                          "No plots were returned, this is almost certainly caused by having selected a set of dates during which no runs have occured.")
                    ],
                    "Errors occured!");
                images = false;
                setState(() {});
              } else {
                images = true;
                setState(() {});
              }
            }
          : null);

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

  // Helper functions

  //This returns the text in the _getDate button.
  String _getDateRange() {
    if (_dates.duration.inDays == 0) {
      return "Press to select the date range";
    } else {
      DateFormat format = DateFormat("MM-dd-yyyy");
      DateTime start = _dates.start;
      DateTime end = _dates.end;
      return "Selected: " + format.format(start) + " - " + format.format(end);
    }
  }

//This determines if the program is in a valid state to generate the files.
  void _checkIfReadyToGenerate() {
    _dates.duration.inDays == 0
        ? _readyToGenerate = false
        : _readyToGenerate = true;
    setState(() {});
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
    _checkIfReadyToGenerate();
  }
}
