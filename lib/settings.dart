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
                //Horizontal column sizes
                ? [
                    ((MediaQuery.of(context).size.width - 160) / 2).px,
                    160.px,
                    ((MediaQuery.of(context).size.width - 160) / 2).px
                  ]
                //Vertical column sizes
                : [
                    (MediaQuery.of(context).size.width / 2).px,
                    (MediaQuery.of(context).size.width / 2).px
                  ],
            rowSizes: MediaQuery.of(context).size.width > _minWidth
                //Horizontal rows and sizes
                ? [75.px, 75.px, 75.px]
                //Vertical rows and sizes
                : [50.px, 50.px, 50.px, 50.px, 50.px],
            children: MediaQuery.of(context).size.width > _minWidth
                //Desktop (horizontal) layout
                ? [
                    Align(
                        child: _processedReportFolderText(),
                        alignment: Alignment.centerRight),
                    Center(child: _getFolder("OneDrive")),
                    Align(
                        child: _seletedFolder("OneDrive"),
                        alignment: Alignment.centerLeft),
                    Align(
                        child: _backupFolderText(),
                        alignment: Alignment.centerRight),
                    Center(child: _getFolder("Backup")),
                    Align(
                        child: _seletedFolder("Backup"),
                        alignment: Alignment.centerLeft),
                    _navigationOptions().withGridPlacement(
                        columnStart: 0, columnSpan: 3, rowStart: 2)
                  ]
                //Desktop (vertical) mobile-like layout
                : [
                    Align(
                        child: _processedReportFolderText(),
                        alignment: Alignment.centerRight),
                    Align(
                        child: _getFolder("OneDrive"),
                        alignment: Alignment.centerLeft),
                    Align(
                            child: _seletedFolder("OneDrive"),
                            alignment: Alignment.topCenter)
                        .withGridPlacement(
                            columnStart: 0, columnSpan: 2, rowStart: 1),
                    Align(
                        child: _backupFolderText(),
                        alignment: Alignment.centerRight),
                    Align(
                        child: _getFolder("Backup"),
                        alignment: Alignment.centerLeft),
                    Align(
                            child: _seletedFolder("Backup"),
                            alignment: Alignment.topCenter)
                        .withGridPlacement(
                            columnStart: 0, columnSpan: 2, rowStart: 3),
                    _navigationOptions().withGridPlacement(
                        columnStart: 0, columnSpan: 2, rowStart: 4)
                  ],
          ),
        ),
      );

  // Variables

  String _oneDriveFolder = "";
  String _backupFolder = "";
  String _currentOneDriveFolder = "";
  String _currentBackupFolder = "";
  final int _minWidth = 814;

  // Widgets

  // This widget returns the text label for the folder input. Has a tooltip.
  Widget _processedReportFolderText() => Tooltip(
      message: "Current value: " + _currentOneDriveFolder,
      child: const Text(
        "OneDrive Proofed Runs Folder Name:",
        style: TextStyle(fontSize: 18),
      ));

  // This widget returns the text label for the folder input. Has a tooltip.
  Widget _backupFolderText() => Tooltip(
      message: "Current value: " + _currentBackupFolder,
      child: const Text(
        "OneDrive Database Backup Folder Name:",
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

  //This widget is a button that spawns a folder choosing window.
  Widget _getFolder(String folderToUpdate) =>
      BasicWidgets.pad(ElevatedButton.icon(
          onPressed: () async {
            String? result = await FilePicker.platform.getDirectoryPath();
            if (result != null) {
              switch (folderToUpdate) {
                case "OneDrive":
                  _oneDriveFolder = result;
                  break;
                case "Backup":
                  _backupFolder = result;
                  break;
              }
            }
            setState(() {});
          },
          icon: const Icon(Icons.folder_open),
          label: const Text("Select Folder")));

  Widget _seletedFolder(String folderToDisplay) =>
      Text(_selectedFolderText(folderToDisplay));

  // Helper functions

  // This method gets and sets the strings containing the current config values.
  void _updateStrings() {
    API.getOneDriveFolder().then((value) => setState(() {
          _currentOneDriveFolder = value;
        }));
    API.getBackupFolder().then((value) => setState(() {
          _currentBackupFolder = value;
        }));
  }

  // This method updates the config values.
  void _submitToPython() async {
    await API.updateOneDriveFolder(_oneDriveFolder);
    await API.updateBackupFolder(_backupFolder);
    if (!await BasicActions.displayThenClearErrors(context)) {
      BasicWidgets.snack(context, "Settings have been applied!", Colors.green);
    }
    _updateStrings();
  }

  /*
  This method makes the selected folder text.

  inputs..
    folderToDisplay: a string that says which folder tooltip to return
  returns..
    A string describing the selected folder
  */
  String _selectedFolderText(String folderToDisplay) {
    switch (folderToDisplay) {
      case "OneDrive":
        return _oneDriveFolder != ""
            ? "Currently selected folder is: " + _oneDriveFolder
            : "";
      case "Backup":
        return _backupFolder != ""
            ? "Currently selected folder is: " + _backupFolder
            : "";
      default:
        return "";
    }
  }
}
