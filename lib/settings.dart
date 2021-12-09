import 'package:file_picker/file_picker.dart';
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
                ? [
                    ((MediaQuery.of(context).size.width - 160) / 2).px,
                    160.px,
                    ((MediaQuery.of(context).size.width - 160) / 2).px
                  ]
                : [auto, auto],
            rowSizes: MediaQuery.of(context).size.width > _minWidth
                ? [50.px, 50.px]
                : [200.px, 200.px, 200.px],
            children: MediaQuery.of(context).size.width > _minWidth
                ? [
                    Align(
                        child: _folderText(), alignment: Alignment.centerRight),
                    Center(child: _getFolder()),
                    Align(
                        child: _seletedFolder(),
                        alignment: Alignment.centerLeft),
                    _navigationOptions().withGridPlacement(
                        columnStart: 0, columnSpan: 3, rowStart: 1)
                  ]
                : [
                    Align(
                        child: _folderText(),
                        alignment: Alignment.bottomCenter),
                    Center(child: _getFolder()),
                    _navigationOptions().withGridPlacement(
                        columnStart: 0, columnSpan: 2, rowStart: 2)
                  ],
          ),
        ),
      );

  // Variables

  String _oneDriveFolder = "";
  String _currentOneDriveFolder = "";
  final int _minWidth = 700;

  // Widgets

  // This widget returns the text label for the folder input. Has a tooltip.
  Widget _folderText() => Tooltip(
      message: "Current value: " + _currentOneDriveFolder,
      child: const Text(
        "OneDrive Proofed Runs Folder Name:",
        style: TextStyle(fontSize: 18),
      ));

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

  Widget _getFolder() => BasicWidgets.pad(ElevatedButton.icon(
      onPressed: () async {
        String? result = await FilePicker.platform.getDirectoryPath();
        if (result != null) {
          _oneDriveFolder = result;
        }
        setState(() {});
      },
      icon: const Icon(Icons.folder_open),
      label: const Text("Select Folder")));

  Widget _seletedFolder() => Text(_selectedFolderText());

  // Helper functions

  // This method gets and sets the strings containing the current config values.
  void _updateStrings() {
    API.getOneDriveFolder().then((value) => setState(() {
          _currentOneDriveFolder = value;
        }));
  }

  // This method updates the config values.
  void _submitToPython() async {
    List<String> errors = [];
    String folderResponse = await API.updateOneDriveFolder(_oneDriveFolder);
    folderResponse != "" ? errors.add(folderResponse) : null;
    if (errors.isNotEmpty) {
      BasicActions.generalAlertBox(context, errors, "Errors occured!");
    } else {
      BasicWidgets.snack(context, "Settings have been applied!", Colors.green);
    }
    _updateStrings();
  }

  String _selectedFolderText() {
    return _oneDriveFolder != ""
        ? "Currently selected folder is: " + _oneDriveFolder
        : "";
  }
}
