import 'package:flutter/material.dart';
import 'package:project_time_saver/basic_actions.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/ui_api.dart';
import 'dart:math';

class LayoutConfiguratorUI extends StatefulWidget {
  const LayoutConfiguratorUI({Key? key}) : super(key: key);

  @override
  State<LayoutConfiguratorUI> createState() => _LayoutConfiguratorUIState();
}

class _LayoutConfiguratorUIState extends State<LayoutConfiguratorUI> {
  _LayoutConfiguratorUIState() {
    _setConfigurations();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
      appBar: AppBar(title: const Text("Incident Report Layout Configurator")),
      body: _selectedConfiguration == "Select a layout"
          ? BasicWidgets.vertical([
              _topBarLayout(),
              const Expanded(
                  child: Center(child: Text("Select a layout to begin")))
            ])
          : BasicWidgets.vertical([_topBarLayout(), _layoutForm()]));

  // Variables

  final RegExp _cellRegex = RegExp(r"^([a-zA-Z]{1,2})(\d{1,3})$");
  GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  List<String> _alreadySaved = [];
  Map<String, Map<int, TextEditingController>> _controllers = {};
  final Map<String, Map<String, dynamic>> _configurations = {};
  final _blankLayout = {
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
    "runType": {},
    "apparatus": {},
    "township": {
      "harrison": {"city": "", "county": ""},
      "lancaster": {"city": "", "county": ""}
    },
    "givenAid": {},
    "takenAid": {}
  };
  String _selectedConfiguration = "Select a layout";

  // Widgets

  /// This function draws a dropdown at the top of the screen.
  /// This dropdown allows the user to select which configuration they want to
  /// edit.
  Widget _configurationDropDown() {
    List<String> options = ["Select a layout"];
    options += _configurations.keys.toList();
    return DropdownButton(
        value: _selectedConfiguration,
        items: options.map<DropdownMenuItem<String>>((String value) {
          return DropdownMenuItem<String>(
            value: value,
            child: Text(value),
          );
        }).toList(),
        onChanged: (String? newValue) {
          _selectedConfiguration = newValue!;
          _controllers = {};
          _alreadySaved = [];
          _formKey = GlobalKey<FormState>();
          setState(() {});
        });
  }

  /// This button is for creating a new configuration layout the user can edit.
  Widget _addNewConfigurationButton() => SizedBox(
      width: 200,
      child: ElevatedButton(
        child: const Text("Create New Layout"),
        onPressed: () {
          _addBlankConfig();
          setState(() {});
        },
      ));

  /// This button allows the user to delete the selected configuration.
  Widget _removeCurrentConfigurationButton() => SizedBox(
      width: 200,
      child: ElevatedButton(
        child: const Text("Delete Current Layout"),
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.resolveWith<Color?>(
            (Set<MaterialState> states) {
              if (states.contains(MaterialState.pressed)) return Colors.red;
              if (states.contains(MaterialState.hovered)) {
                return Colors.red[300];
              }
              return null; // Use the component's default.
            },
          ),
        ),
        onPressed: () async {
          _configurations.remove(_selectedConfiguration);
          _selectedConfiguration = "Select a layout";
          await API.updateLayoutConfigs(_configurations.values.toList());
          setState(() {});
        },
      ));

  /// Populates the controls that appear at the top of this UI page
  Widget _topBarLayout() {
    if (_selectedConfiguration == "Select a layout") {
      return BasicWidgets.horizontal([
        BasicWidgets.pad(_configurationDropDown()),
        BasicWidgets.pad(_addNewConfigurationButton())
      ]);
    } else {
      return BasicWidgets.horizontal([
        BasicWidgets.pad(_configurationDropDown()),
        BasicWidgets.pad(_addNewConfigurationButton()),
        BasicWidgets.pad(_removeCurrentConfigurationButton())
      ]);
    }
  }

  /// This widget is the actual form that is displayed to the user for editing a
  /// configuration. It contains every text entry box.
  Widget _layoutForm() => Form(
        key: _formKey,
        child: Expanded(
            child: SingleChildScrollView(
                child: Column(
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
                "Cell of Station Covered Indicator:", "stationCovered",
                canBeEmpty: true),
            _inputNameValue("Cell of Weekend Incident Indicator:", "weekend",
                canBeEmpty: true),
            _inputNameValue(
                "Cell of Commitment Hours Indicator:", "workingHours",
                canBeEmpty: true),
            _inputNameValue(
                "Cell of Non-Commitment Hours Indicator:", "offHours",
                canBeEmpty: true),
            _inputNameValue(
                "Cell of Full Shift Cover Indicator:", "shiftCovered",
                canBeEmpty: true),
            _inputNameValue("Cell of run Duration:", "runTime"),
            _inputNameValue(
                "Row Number of First Employee Row:", "firstEmployeeRow",
                number: true),
            _inputKeyValueTable("Name and Cell of Run Types", "runType"),
            _inputKeyValueTable("Name and Cell of Apparatus", "apparatus"),
            _inputKeyTownship(),
            _aidKeyValueTable("Given mutual aid", "givenAid"),
            _aidKeyValueTable("Taken mutual aid", "takenAid"),
            BasicWidgets.horizontal(
                [_checkFormButton(), _clearEmptyValuesButton()])
          ],
        ))),
      );

  /// This widget draws one of the actual text entry boxes for the form. It
  /// requires the key of the input for the config layout. It also has several
  /// optional parameters. Name, number, startDate, endDate, and canBeEmpty are
  /// all optional bools that will change how the input text is validated.
  /// FillValue will change the text that is automatically filled in the text
  /// box. AltOnSave is a string indictor of which saving method should be
  /// utilized when saving the values into the map. AltController will override
  /// the text editing controller, it is used for any text box taht requires a
  /// special method of saving the values.
  Widget _formField(String configKey,
          {name = false,
          number = false,
          startDate = false,
          endDate = false,
          canBeEmpty = false,
          autosave = false,
          fillValue,
          String? altOnSave,
          TextEditingController? altController}) =>
      Center(
          child: BasicWidgets.pad(BasicWidgets.mainBox(TextFormField(
        controller: altController,
        initialValue: fillValue ?? altController == null
            ? _getFillValue(configKey)
            : null,
        validator: (value) {
          return _validateInput(
              value, configKey, name, number, startDate, endDate, canBeEmpty);
        },
        onSaved: (value) {
          _alreadySaved = [];
          if (altOnSave == null) {
            _onSaveAction(value, configKey);
          } else if (altOnSave == "list") {
            _saveSublist(configKey);
          } else if (altOnSave == "township") {
            _saveTownship();
          } else if (altOnSave == "mututalAid") {
            _saveAid(configKey);
          }
        },
        onChanged: (value) {
          _alreadySaved = [];
          if (autosave) {
            if (altOnSave == null) {
              _onSaveAction(value, configKey);
            } else if (altOnSave == "list") {
              _saveSublist(configKey);
            } else if (altOnSave == "township") {
              _saveTownship();
            } else if (altOnSave == "mututalAid") {
              _saveAid(configKey);
            }
          }
        },
      ))));

  /// This button is used to check the form, save its values, and submit it to
  /// the backend to be saved.
  Widget _checkFormButton() =>
      BasicWidgets.pad(BasicWidgets.mainBox(ElevatedButton(
          onPressed: () => _submitButtonLogic(), child: const Text("Submit"))));

  Widget _clearEmptyValuesButton() =>
      BasicWidgets.pad(BasicWidgets.mainBox(ElevatedButton(
          onPressed: () => _deleteEmptyValues(),
          child: const Text("Clear Empty Values"))));

  /// This item combines a description of a text entry box and the box itself
  /// into a fixed width row to make the layout look nicer. It has the same
  /// optional inputs ad `_formField` and it requires a text description of the
  /// input box (*inputName*) and the key for that input box (*key*).
  Widget _inputNameValue(String inputName, String key,
          {startDate = false,
          endDate = false,
          number = false,
          name = false,
          canBeEmpty = false}) =>
      Center(
        child: BasicWidgets.pad(SizedBox(
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
            ]))),
      );

  /// This function makes the input table for any variable-length parameter. It
  /// adds a "add new" button that puts a couple empty boxes as well as fills
  /// any boxes that are already there. It requires a description of the inputs
  /// and the key for the map.
  Widget _inputKeyValueTable(String inputName, String key) {
    List<Widget> displayList = [
      BasicWidgets.pad(BasicWidgets.horizontal([
        SizedBox(width: 200, child: Text(inputName)),
        const Spacer(),
        SizedBox(
            width: 190,
            child: ElevatedButton(
              child: const Text("Add New"),
              onPressed: () => _addNewValueToList(key),
            ))
      ])),
      BasicWidgets.pad(BasicWidgets.horizontal([
        const SizedBox(width: 195, child: Text("Value Name:")),
        const Spacer(),
        const SizedBox(width: 195, child: Text("Cell Location:"))
      ]))
    ];
    displayList.addAll(_getKeyValues(key));
    return Center(
        child: SizedBox(width: 400, child: BasicWidgets.vertical(displayList)));
  }

  /// This function handles the input boxes for the townships. It draws them
  /// in a row with descriptions on the left and fill boxes on the right.
  Widget _inputKeyTownship() {
    List<Widget> displayList = [];
    displayList.addAll(_getTownshipKeyValues());
    return Center(
        child: SizedBox(width: 400, child: BasicWidgets.vertical(displayList)));
  }

  /// This function is responsible for populating all of the key-value pairs for
  /// the variable length inputs. Requres the key of the value types.
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
        returnlist.add(BasicWidgets.pad(BasicWidgets.horizontal([
          _formField(key,
              name: true,
              altController: _controllers[key]![count],
              altOnSave: "list",
              autosave: true),
          const Spacer(),
          _formField(key,
              altController: _controllers[key]![count + 1],
              altOnSave: "list",
              autosave: true)
        ])));
        count = count + 2;
      }
    }
    return returnlist;
  }

  /// This function is responsible for drawing te actual input boxs for the
  /// townships.
  List<Widget> _getTownshipKeyValues() {
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
        returnlist.add(BasicWidgets.pad(BasicWidgets.horizontal([
          SizedBox(width: 200, child: Text(cellDescriptions[i])),
          const Spacer(),
          _formField("township",
              name: true,
              altController: _controllers["township"]![i],
              altOnSave: "township",
              autosave: true)
        ])));
      }
    }
    return returnlist;
  }

  /// This function creates the table for adding the departments for mutual aid.
  /// It draws one input for the department name and then two more below it for
  /// the manual labor and apparatus types of aid. Requires a description and
  /// the key for the type of aid (given or taken).
  Widget _aidKeyValueTable(String inputName, String key) {
    List<Widget> displayList = [
      BasicWidgets.pad(BasicWidgets.horizontal([
        SizedBox(width: 200, child: Text(inputName)),
        const Spacer(),
        SizedBox(
            width: 190,
            child: ElevatedButton(
              child: const Text("Add New"),
              onPressed: () => _addNewValueToAid(key),
            ))
      ]))
    ];
    displayList.addAll(_getAidKeyValues(key));
    return Center(
        child: SizedBox(width: 400, child: BasicWidgets.vertical(displayList)));
  }

  /// This function is responsible for actually populating the already filled
  /// aid values. Requires the type of aid to be input.
  List<Widget> _getAidKeyValues(String aidType) {
    List<Widget> returnlist = [];
    var current = _configurations[_selectedConfiguration]![aidType];
    _controllers[aidType] = {};
    int count = 0;
    if (current is Map) {
      for (String department in current.keys) {
        var departmentCell = current[department];
        _controllers[aidType]!
            .putIfAbsent(count, () => TextEditingController(text: department));
        _controllers[aidType]!.putIfAbsent(
            count + 1,
            () => TextEditingController(
                text: departmentCell is Map ? departmentCell["man"] : ""));
        _controllers[aidType]!.putIfAbsent(
            count + 2,
            () => TextEditingController(
                text: departmentCell is Map ? departmentCell["app"] : ""));
        returnlist.add(BasicWidgets.pad(BasicWidgets.horizontal([
          const SizedBox(width: 200, child: Text("Department: ")),
          const Spacer(),
          _formField(aidType,
              name: true,
              altController: _controllers[aidType]![count],
              altOnSave: "mututalAid",
              autosave: true)
        ])));
        returnlist.add(BasicWidgets.horizontal([
          const SizedBox(
              width: 200, child: Text("Cell indicating manual labor: ")),
          const Spacer(),
          const SizedBox(width: 200, child: Text("Cell indicating apparauts: "))
        ]));
        returnlist.add(BasicWidgets.horizontal([
          _formField(aidType,
              name: true,
              altController: _controllers[aidType]![count + 1],
              altOnSave: "mututalAid",
              autosave: true),
          const Spacer(),
          _formField(aidType,
              name: true,
              altController: _controllers[aidType]![count + 2],
              altOnSave: "mututalAid",
              autosave: true)
        ]));
        count = count + 3;
      }
    }
    return returnlist;
  }

  // Helper functions

  /// This method validates the input for each text entry box. Requires a lot of
  /// parameters. The first is the value of the text entry box. The next
  /// variables are all booleans that denote the type of checks that should be
  /// applied.
  String? _validateInput(String? value, String configKey, bool name,
      bool number, bool startDate, bool endDate, bool canBeEmpty) {
    if (name) {
      if (value == null || value == "") return "Value cannot be empty!";
    } else if (number) {
      if (value == null || value == "" || !RegExp(r"^\d*$").hasMatch(value)) {
        return "Value must be a number!";
      }
    } else if (startDate) {
      if (value == null) {
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
    } else if (canBeEmpty && (value == "" || value == null)) {
      return null;
    } else if (!_cellRegex.hasMatch(value!)) {
      return "Invalid Input!";
    }
    return null;
  }

  /// This method is the default saving method.
  void _onSaveAction(String? value, String configKey) {
    _configurations[_selectedConfiguration]![configKey] = value!;
  }

  /// This method adds an empt key value pair to any of the list-wise variable
  /// length configuration options. Requires the key of the variable.
  void _addNewValueToList(key) {
    var _current = _configurations[_selectedConfiguration]![key];
    if (_current is Map) {
      _current.putIfAbsent("", () => "");
      _configurations[_selectedConfiguration]![key] = _current;
      setState(() {});
    }
  }

  /// Adds a new empty set of values to the mutual aid map keys. Requires a
  /// key specifying which type of aid.
  void _addNewValueToAid(key) {
    var _current = _configurations[_selectedConfiguration]![key];
    if (_current is Map) {
      _current.putIfAbsent("", () => {"man": "", "app": ""});
      _configurations[_selectedConfiguration]![key] = _current;
      setState(() {});
    }
  }

  /// The method that saves any of the variable length list-wise types.
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

  /// This method is the logic for the submit button.
  void _submitButtonLogic() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      if (_selectedConfiguration !=
          _getTitle(_configurations[_selectedConfiguration]!)) {
        Map<String, dynamic> updated = _configurations[_selectedConfiguration]!;
        _configurations.remove(_selectedConfiguration);
        _configurations.putIfAbsent(_getTitle(updated), () => updated);
        _selectedConfiguration = _getTitle(updated);
      }
      _alreadySaved = [];
      await API.updateLayoutConfigs(_configurations.values.toList());
      BasicWidgets.snack(
          context, "Configuration successfully saved!", Colors.green);
      setState(() {});
    } else {
      BasicWidgets.snack(
          context, "Configuration could not be saved!", Colors.red);
    }
  }

  /// This method will delete all empty list values in the layout.
  void _deleteEmptyValues() {
    for (String key in ["givenAid", "takenAid"]) {
      Map<int, TextEditingController> values = _controllers[key]!;
      for (int i = 0; i <= values.keys.reduce(max); i += 3) {
        if (values[i]!.text == "" &&
            values[i + 1]!.text == "" &&
            values[i + 2]!.text == "") {
          _controllers[key]!.remove(i);
          _controllers[key]!.remove(i + 1);
          _controllers[key]!.remove(i + 2);
          _configurations[_selectedConfiguration]![key]!.remove("");
          setState(() {});
        }
      }
    }
    for (String key in ["apparatus", "runType"]) {
      var _current = _configurations[_selectedConfiguration]![key];
      if (_current is Map) {
        _current.remove("");
        _configurations[_selectedConfiguration]![key] = _current;
        setState(() {});
      }
    }
  }

  /// This method is responsible for saving the township values to the map.
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

  /// This method is responsible for saving the aid values to the map. Requires
  /// a key denoting the type of aid.
  void _saveAid(String key) {
    if (!_alreadySaved.contains(key)) {
      Map<int, TextEditingController> values = _controllers[key]!;
      Map<String, Map<String, String>> toSave = {};
      for (int i = 0; i <= values.keys.reduce(max); i += 3) {
        toSave.putIfAbsent(values[i]!.text,
            () => {"man": values[i + 1]!.text, "app": values[i + 2]!.text});
      }
      _configurations[_selectedConfiguration]![key] = toSave;
      _alreadySaved.add(key);
    }
  }

  /// This method adds all of the possible configurations to the dropdown.
  void _setConfigurations() async {
    List<Map<String, dynamic>> layouts = await API.getCellLocations();
    if (layouts.isEmpty) {
      _addBlankConfig();
    } else {
      for (Map<String, dynamic> layout in layouts) {
        String title = _getTitle(layout);
        _configurations.putIfAbsent(title, () => layout);
      }
    }
    setState(() {});
  }

  /// This method adds a new blank configuration.
  void _addBlankConfig() {
    _configurations.putIfAbsent("New Layout", () => _blankLayout);
  }

  /// This method generates the title that is displayed in the dropdown.
  String _getTitle(Map<String, dynamic> layout) {
    var storedStart = layout["startDate"];
    var storedEnd = layout["endDate"];
    String start = "";
    String end = "";
    storedStart is String ? start = storedStart : "";
    storedEnd is String ? end = storedEnd : "";
    String title = "";
    end == "" ? title = start + " - Current" : title = start + " - " + end;
    return title;
  }

  /// This method gets the value to fill any of the standard key-value pairs.
  String _getFillValue(String key) {
    dynamic value = _configurations[_selectedConfiguration]![key];
    return value is String ? value : "";
  }
}
