import 'package:flutter/material.dart';
import 'package:flutter_layout_grid/flutter_layout_grid.dart';
import 'package:project_time_saver/basic_actions.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/ui_api.dart';

class SettingsUI extends StatefulWidget {
  const SettingsUI({Key? key}) : super(key: key);

  @override
  State<SettingsUI> createState() => _SettingsUIState();
}

class _SettingsUIState extends State<SettingsUI> {
  _SettingsUIState() {
    _updateStrings();
  }

  //This is where the layout is generated.
  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: const Text("Settings"),
        ),
        body: Center(
          child: LayoutGrid(
            columnSizes: MediaQuery.of(context).size.width > _minWidth
                ? [auto, auto]
                : [auto],
            rowSizes: MediaQuery.of(context).size.width > _minWidth
                ? [50.px, 50.px, 50.px]
                : [50.px, 50.px, 50.px, 50.px, 50.px],
            children: MediaQuery.of(context).size.width > _minWidth
                ? [
                    Align(
                      child: _clientText(),
                      alignment: Alignment.centerRight,
                    ),
                    _clientIDTextEntryBox(),
                    Align(
                        child: _folderText(), alignment: Alignment.centerRight),
                    _oneDriveFolderTextEntryBox(),
                    _navigationOptions().withGridPlacement(
                        columnStart: 0, columnSpan: 2, rowStart: 2)
                  ]
                : [
                    Align(
                        child: _clientText(),
                        alignment: Alignment.bottomCenter),
                    Center(child: _clientIDTextEntryBox()),
                    Align(
                        child: _folderText(),
                        alignment: Alignment.bottomCenter),
                    Center(child: _oneDriveFolderTextEntryBox()),
                    _navigationOptions()
                  ],
          ),
        ),
      );

  // Variables

  String _clientIDString = "";
  String _oneDriveFolder = "";
  String _currentClientID = "";
  String _currentOneDriveFolder = "";
  final int _minWidth = 700;

  // Widgets

  // This widget returns the text label for the client ID input. Has a tooltip.
  Widget _clientText() => Tooltip(
      message: "Current value: " + _currentClientID,
      child: const Text(
        "OneDrive Client ID:",
        style: TextStyle(fontSize: 18),
      ));

  // This widget returns the text label for the folder input. Has a tooltip.
  Widget _folderText() => Tooltip(
      message: "Current value: " + _currentOneDriveFolder,
      child: const Text(
        "OneDrive Proofed Runs Folder Name:",
        style: TextStyle(fontSize: 18),
      ));

  // This widget is the text entry for the client ID.
  Widget _clientIDTextEntryBox() => BasicWidgets.pad(SizedBox(
      width: 300,
      height: 60,
      child: TextField(
        decoration: InputDecoration(
            hintText: _getCurrentClientIDHint(),
            border: const OutlineInputBorder()),
        onChanged: (value) => _clientIDString = value,
      )));

  // This widget is the text entry for the cfolder.
  Widget _oneDriveFolderTextEntryBox() => BasicWidgets.pad(SizedBox(
      width: 300,
      height: 60,
      child: TextField(
        decoration: InputDecoration(
            hintText: _getCurrentOneDriveFolderHint(),
            border: const OutlineInputBorder()),
        onChanged: (value) => _oneDriveFolder = value,
      )));

  // This widget contains the save and close buttons in a horizontal layout.
  Widget _navigationOptions() =>
      BasicWidgets.horizontal([_cancelButton(), _saveButton()]);

  // This widget calls the save methods and saves current strings to the config.
  Widget _saveButton() => BasicWidgets.pad(ElevatedButton(
      onPressed: () {
        _submitToPython();
      },
      child: const Text("Save Changes")));

  // This widget will take you back home.
  Widget _cancelButton() => BasicWidgets.pad(ElevatedButton(
      onPressed: () => Navigator.pop(context), child: const Text("Cancel")));

  // Helper functions

  // This method gets the hint text for the client ID input box.
  String _getCurrentClientIDHint() => _currentClientID == ""
      ? "Type client ID here."
      : "The current ID is: " + _currentClientID;

  // This method gets the hint text for the folder input box.
  String _getCurrentOneDriveFolderHint() => _currentOneDriveFolder == ""
      ? "Enter the name of the folder containing proofed runreports."
      : "Current folder is: " + _currentOneDriveFolder;

  // This method gets and sets the strings containing the current config values.
  void _updateStrings() {
    API.getClientID().then((value) => setState(() {
          _currentClientID = value;
        }));
    API.getOneDriveFolder().then((value) => setState(() {
          _currentOneDriveFolder = value;
        }));
  }

  // This method updates the config values.
  void _submitToPython() async {
    List<String> errors = [];
    String clientResponse = await API.updateClientID(_clientIDString);
    String folderResponse = await API.updateOneDriveFolder(_oneDriveFolder);
    clientResponse != "" ? errors.add(clientResponse) : null;
    folderResponse != "" ? errors.add(folderResponse) : null;
    if (errors.isNotEmpty) {
      BasicActions.generalAlertBox(context, errors, "Errors occured!");
    } else {
      BasicWidgets.snack(context, "Settings have been applied!", Colors.green);
    }
    _updateStrings();
  }
}
