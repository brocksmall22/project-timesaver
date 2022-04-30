import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_layout_grid/flutter_layout_grid.dart';
import 'package:project_time_saver/basic_actions.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/ui_api.dart';

class layoutConfiguratorUI extends StatefulWidget {
  const layoutConfiguratorUI({Key? key}) : super(key: key);

  @override
  State<layoutConfiguratorUI> createState() => _layoutConfiguratorUIState();
}

class _layoutConfiguratorUIState extends State<layoutConfiguratorUI> {
  @override
  Widget build(BuildContext context) => Scaffold(
      appBar: AppBar(title: const Text("Incident Report Layout Configurator")),
      body: BasicWidgets.vertical([_configurationDropDown(), _layoutForm()]));

  // This is where the layout is generated.
  // @override
  // Widget build(BuildContext context) => Scaffold(
  //       appBar: AppBar(
  //         title: const Text("Settings"),
  //       ),
  //       body: Center(
  //         child: LayoutGrid(
  //           columnSizes: MediaQuery.of(context).size.width > _minWidth
  //               //Horizontal column sizes
  //               ? [
  //                   ((MediaQuery.of(context).size.width) / 2).px,
  //                   ((MediaQuery.of(context).size.width) / 2).px
  //                 ]
  //               //Vertical column sizes
  //               : [
  //                   (MediaQuery.of(context).size.width / 2).px,
  //                   (MediaQuery.of(context).size.width / 2).px
  //                 ],
  //           rowSizes: MediaQuery.of(context).size.width > _minWidth
  //               //Horizontal rows and sizes
  //               ? [50.px, 50.px, 50.px, 50.px]
  //               //Vertical rows and sizes
  //               : [50.px, 50.px, 50.px, 50.px],
  //           children: MediaQuery.of(context).size.width > _minWidth
  //               //Desktop (horizontal) layout
  //               ? [
  //                   Align(
  //                       child: _oneDriveFolderText(),
  //                       alignment: Alignment.centerRight),
  //                   Align(
  //                       child: _getFolder("OneDrive"),
  //                       alignment: Alignment.centerLeft),
  //                   Align(
  //                       child: _backupFolderText(),
  //                       alignment: Alignment.centerRight),
  //                   Align(
  //                       child: _getFolder("Backup"),
  //                       alignment: Alignment.centerLeft),
  //                   Center(
  //                           child: BasicWidgets.horizontal(
  //                               [_backupDatabase(), _restoreDatabase()]))
  //                       .withGridPlacement(
  //                           columnStart: 0, columnSpan: 2, rowStart: 2),
  //                   _bakcButton().withGridPlacement(
  //                       columnStart: 0, columnSpan: 2, rowStart: 3)
  //                 ]
  //               //Desktop (vertical) mobile-like layout
  //               : [
  //                   Align(
  //                       child: _oneDriveFolderText(),
  //                       alignment: Alignment.centerRight),
  //                   Align(
  //                       child: _getFolder("OneDrive"),
  //                       alignment: Alignment.centerLeft),
  //                   Align(
  //                       child: _backupFolderText(),
  //                       alignment: Alignment.centerRight),
  //                   Align(
  //                       child: _getFolder("Backup"),
  //                       alignment: Alignment.centerLeft),
  //                   Center(
  //                           child: BasicWidgets.horizontal(
  //                               [_backupDatabase(), _restoreDatabase()]))
  //                       .withGridPlacement(
  //                           columnStart: 0, columnSpan: 2, rowStart: 2),
  //                   _bakcButton().withGridPlacement(
  //                       columnStart: 0, columnSpan: 2, rowStart: 3)
  //                 ],
  //         ),
  //       ),
  //     );

  // Variables

  final RegExp _cellRegex = RegExp(r"^([a-zA-Z]{1,2})(\d{1,3})$");
  final _formKey = GlobalKey<FormState>();
  List<String> _alreadySaved = [];
  Map<String, Map<int, TextEditingController>> _controllers = {};
  Map<String, Map<String, Object>> _configurations = {
    "old": {
      "startDate": "",
      "endDate": "",
      "incidentNumber": "",
      "date": "",
      "shift": "",
      "OIC": "",
      "SO": "",
      "filer": "",
      "reported": "",
      "paged": "",
      "1076": "",
      "1023": "",
      "UC": "",
      "1008": "",
      "stationCovered": "",
      "weekend": "",
      "workingHours": "",
      "offHours": "",
      "shiftCovered": "",
      "runTime": "",
      "firstEmployeeRow": "",
      "runType": {"asdf": "", "oiuyouiy": ""},
      "apparatus": {"vwefvdsj": "wrbtyyjuj", "wfbrtb": "asdfe"},
      "township": {
        "harrison": {"city": "", "county": ""},
        "lancaster": {"city": "", "county": ""}
      },
      "givenAid": {},
      "takenAid": {}
    },
    "less-old": {"string": 5},
    "newest": {"string": 5}
  };
  String _selectedConfiguration = "old";

  // Widgets

  Widget _configurationDropDown() => DropdownButton(
      value: _selectedConfiguration,
      items: _configurations.keys.map<DropdownMenuItem<String>>((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value),
        );
      }).toList(),
      onChanged: (String? newValue) {
        setState(() {
          _selectedConfiguration = newValue!;
          _controllers = {};
        });
      });

  Widget _layoutForm() => Form(
        key: _formKey,
        child: Expanded(
            child: ListView(
          children: [
            _inputNameValue("First date to use this layout:", "startDate",
                startDate: true),
            _inputNameValue("Last date to use this layout:", "endDate",
                endDate: true),
            _inputNameValue("Cell of Incident Number:", "incidentNumber"),
            _inputNameValue("Cell of Incident Date:", "date"),
            _inputNameValue("Cell of Covering Shift:", "shift"),
            _inputNameValue("Cell of OIC:", "OIC"),
            _inputNameValue("Cell of SO:", "SO"),
            _inputNameValue("Cell of Filer:", "filer"),
            _inputNameValue("Cell of Reported Time:", "reported"),
            _inputNameValue("Cell of Paged Time:", "paged"),
            _inputNameValue("Cell of 1076 Time:", "1076"),
            _inputNameValue("Cell of 1023 Time:", "1023"),
            _inputNameValue("Cell of UC:", "UC"),
            _inputNameValue("Cell of 1008 Time:", "1008"),
            _inputNameValue(
                "Cell of Station Covered Indicator:", "stationCovered"),
            _inputNameValue("Cell of Weekend Incident Indicator:", "weekend"),
            _inputNameValue(
                "Cell of Commitment Hours Indicator:", "workingHours"),
            _inputNameValue(
                "Cell of Non-Commitment Hours Indicator:", "offHours"),
            _inputNameValue(
                "Cell of Full Shift Cover Indicator:", "shiftCovered"),
            _inputNameValue("Cell of run Duration:", "runTime"),
            _inputNameValue(
                "Row Number of First Employee Row:", "firstEmployeeRow",
                number: true),
            _inputKeyValueTable("Name and Cell of Run Types", "runType"),
            _inputKeyValueTable("Name and Cell of Apparatus", "apparatus"),
            _inputKeyTownshipTable(),
            _checkFormButton()
          ],
        )),
      );

  Widget _formField(String configKey,
          {name = false,
          number = false,
          startDate = false,
          endDate = false,
          canBeEmpty = false,
          fillValue,
          String? altOnSave,
          TextEditingController? altController}) =>
      Center(
          child: BasicWidgets.pad(BasicWidgets.mainBox(TextFormField(
              controller: altController,
              initialValue: fillValue,
              validator: (value) {
                return _validateInput(value, configKey, name, number, startDate,
                    endDate, canBeEmpty);
              },
              onSaved: (value) {
                if (altOnSave == null) {
                  _onSaveAction(value, configKey);
                } else if (altOnSave == "list") {
                  _saveSublist(configKey);
                } else if (altOnSave == "township") {
                  _saveTownship();
                }
              }))));

  Widget _checkFormButton() => Center(
      child: BasicWidgets.pad(BasicWidgets.mainBox(ElevatedButton(
          onPressed: () => _submitButtonLogic(),
          child: const Text("Submit")))));

  Widget _inputNameValue(String inputName, String key,
          {startDate = false,
          endDate = false,
          number = false,
          name = false,
          canBeEmpty = false}) =>
      Center(
        child: SizedBox(
            width: 400,
            child: BasicWidgets.horizontal([
              SizedBox(width: 200, child: Text(inputName)),
              const Spacer(),
              _formField(key,
                  name: name,
                  number: number,
                  startDate: startDate,
                  endDate: endDate,
                  canBeEmpty: canBeEmpty)
            ])),
      );

  Widget _inputKeyValueTable(String inputName, String key) {
    List<Widget> displayList = [
      BasicWidgets.horizontal([
        SizedBox(width: 200, child: Text(inputName)),
        const Spacer(),
        SizedBox(
            width: 200,
            child: ElevatedButton(
              child: const Text("Add New"),
              onPressed: () => _addNewValueToList(key),
            ))
      ]),
      BasicWidgets.horizontal([
        const SizedBox(width: 200, child: Text("Value Name")),
        const Spacer(),
        const SizedBox(width: 200, child: Text("Cell Location"))
      ])
    ];
    displayList.addAll(_getKeyValues(key));
    return Center(
        child: SizedBox(width: 400, child: BasicWidgets.vertical(displayList)));
  }

  Widget _inputKeyTownshipTable() {
    List<Widget> displayList = [];
    displayList.addAll(_geTwonshiptKeyValues());
    return Center(
        child: SizedBox(width: 400, child: BasicWidgets.vertical(displayList)));
  }

  List<Widget> _getKeyValues(String key) {
    List<Widget> returnlist = [];
    var _current = _configurations[_selectedConfiguration]![key];
    _controllers[key] = {};
    int count = 0;
    if (_current is Map) {
      for (String keyVal in _current.keys) {
        _controllers[key]!
            .putIfAbsent(count, () => TextEditingController(text: keyVal));
        _controllers[key]!.putIfAbsent(count + 1,
            () => TextEditingController(text: _current[keyVal] ?? ""));
        returnlist.add(BasicWidgets.horizontal([
          _formField(key,
              name: true,
              altController: _controllers[key]![count],
              altOnSave: "list"),
          const Spacer(),
          _formField(key,
              name: true,
              altController: _controllers[key]![count + 1],
              altOnSave: "list")
        ]));
        count = count + 2;
      }
    }
    return returnlist;
  }

  List<Widget> _geTwonshiptKeyValues() {
    List<String> townships = ["harrison", "harrison", "lancaster", "lancaster"];
    List<String> limits = ["city", "county", "city", "county"];
    List<String> cellDescriptions = [
      "Cell indicating if a run was in Harrison township inside city limits",
      "Cell indicating if a run was in Harrison township outside city limits",
      "Cell indicating if a run was in Lancaster township inside city limits",
      "Cell indicating if a run was in Lancaster township outside city limits"
    ];
    List<Widget> returnlist = [];
    var current = _configurations[_selectedConfiguration]!["township"];
    _controllers["township"] = {};
    if (current is Map) {
      for (int i = 0; i != 4; i++) {
        var townshipCell = current[townships[i]][limits[i]];
        _controllers["township"]!.putIfAbsent(
            i,
            () => TextEditingController(
                text: townshipCell is String ? townshipCell : ""));
        returnlist.add(BasicWidgets.horizontal([
          SizedBox(width: 200, child: Text(cellDescriptions[i])),
          const Spacer(),
          _formField("township",
              name: true,
              altController: _controllers["township"]![i],
              altOnSave: "township")
        ]));
      }
    }
    return returnlist;
  }

  // Helper functions

  String? _validateInput(String? value, String configKey, bool name,
      bool number, bool startDate, bool endDate, bool canBeEmpty) {
    if (name) {
      if (value == null) return "Value cannot be empty!";
    } else if (number) {
      if (value == null || !RegExp(r"^\d*$").hasMatch(value)) {
        return "Value must be a number!";
      }
    } else if (startDate) {
      if (value == null || value == null) {
        return "The starting date of a config cannot be empty!";
      }
      try {
        DateTime.parse(value);
      } on FormatException {
        return "Date is incorrectly formatted!";
      }
    } else if (endDate) {
      if (value == null || value == "") return null;
      try {
        DateTime.parse(value);
      } on FormatException {
        return "Date is incorrectly formatted!";
      }
    } else if (!canBeEmpty && value == null || !_cellRegex.hasMatch(value!)) {
      return "Invalid Input!";
    }
    return null;
  }

  void _onSaveAction(String? value, String configKey) {
    _configurations[_selectedConfiguration]![configKey] = value!;
  }

  void _addNewValueToList(key) {
    var _current = _configurations[_selectedConfiguration]![key];
    if (_current is Map) {
      _current.putIfAbsent("", () => "");
      _configurations[_selectedConfiguration]![key] = _current;
      setState(() {});
    }
  }

  void _saveSublist(String key) {
    if (!_alreadySaved.contains(key)) {
      Map<int, TextEditingController> values = _controllers[key]!;
      Map<String, String> toSave = {};
      String keyVal = "";
      String val = "";
      for (var index in values.keys) {
        if (index % 2 == 0) {
          keyVal = values[index]!.text;
        } else {
          val = values[index]!.text;
          toSave[keyVal] = val;
        }
      }
      _configurations[_selectedConfiguration]![key] = toSave;
      _alreadySaved.add(key);
    }
  }

  void _submitButtonLogic() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      _alreadySaved = [];
      print(_configurations[_selectedConfiguration]);
      BasicActions.generalAlertBox(
          context, [const Text("Okay")], "It is a good input!");
    }
  }

  void _saveTownship() {
    if (!_alreadySaved.contains("township")) {
      Map<int, TextEditingController> values = _controllers["township"]!;
      Map<String, Map<String, String>> toSave = {};
      toSave.putIfAbsent("harrison",
          () => {"city": values[0]!.text, "county": values[1]!.text});
      toSave.putIfAbsent("lancaster",
          () => {"city": values[2]!.text, "county": values[3]!.text});
      _configurations[_selectedConfiguration]!["township"] = toSave;
      _alreadySaved.add("township");
    }
  }
}
