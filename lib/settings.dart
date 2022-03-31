import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter_layout_grid/flutter_layout_grid.dart';
import 'package:project_time_saver/basic_actions.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/layout_configurator.dart';
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
                    ((MediaQuery.of(context).size.width) / 2).px,
                    ((MediaQuery.of(context).size.width) / 2).px
                  ]
                //Vertical column sizes
                : [
                    (MediaQuery.of(context).size.width / 2).px,
                    (MediaQuery.of(context).size.width / 2).px
                  ],
            rowSizes: MediaQuery.of(context).size.width > _minWidth
                //Horizontal rows and sizes
                ? [50.px, 50.px, 50.px, 50.px]
                //Vertical rows and sizes
                : [50.px, 50.px, 50.px, 50.px],
            children: MediaQuery.of(context).size.width > _minWidth
                //Desktop (horizontal) layout
                ? [
                    Align(
                        child: _oneDriveFolderText(),
                        alignment: Alignment.centerRight),
                    Align(
                        child: _getFolder("OneDrive"),
                        alignment: Alignment.centerLeft),
                    Align(
                        child: _backupFolderText(),
                        alignment: Alignment.centerRight),
                    Align(
                        child: _getFolder("Backup"),
                        alignment: Alignment.centerLeft),
                    Center(
                            child: BasicWidgets.horizontal(
                                [_backupDatabase(), _restoreDatabase()]))
                        .withGridPlacement(
                            columnStart: 0, columnSpan: 2, rowStart: 2),
                    Center(
                            child: BasicWidgets.horizontal(
                                [_layoutButton(), _backButton()]))
                        .withGridPlacement(
                            columnStart: 0, columnSpan: 2, rowStart: 3)
                  ]
                //Desktop (vertical) mobile-like layout
                : [
                    Align(
                        child: _oneDriveFolderText(),
                        alignment: Alignment.centerRight),
                    Align(
                        child: _getFolder("OneDrive"),
                        alignment: Alignment.centerLeft),
                    Align(
                        child: _backupFolderText(),
                        alignment: Alignment.centerRight),
                    Align(
                        child: _getFolder("Backup"),
                        alignment: Alignment.centerLeft),
                    Center(
                            child: BasicWidgets.horizontal(
                                [_backupDatabase(), _restoreDatabase()]))
                        .withGridPlacement(
                            columnStart: 0, columnSpan: 2, rowStart: 2),
                    _backButton().withGridPlacement(
                        columnStart: 0, columnSpan: 2, rowStart: 3)
                  ],
          ),
        ),
      );

  // Variables

  String _oneDriveFolder = "";
  String _backupFolder = "";
  final int _minWidth = 814;

  // Widgets

  // This widget returns the text label for the folder input. Has a tooltip.
  Widget _oneDriveFolderText() => Tooltip(
      message: "Current value: " + _oneDriveFolder,
      child: const Text(
        "OneDrive Proofed Runs Folder:",
        style: TextStyle(fontSize: 18),
      ));

  // This widget returns the text label for the folder input. Has a tooltip.
  Widget _backupFolderText() => Tooltip(
      message: "Current value: " + _backupFolder,
      child: const Text(
        "OneDrive Database Backup Folder:",
        style: TextStyle(fontSize: 18),
      ));

  // This widget will take you back home.
  Widget _backButton() => BasicWidgets.pad(ElevatedButton(
      onPressed: () => Navigator.pop(context), child: const Text("Cancel")));

  // This widget will open the layout configurator screen
  Widget _layoutButton() => BasicWidgets.pad(BasicWidgets.mainNavigationButton(
      context,
      "Incident Sheet Layout Configurator",
      const layoutConfiguratorUI(),
      restricted: false));

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
              setState(() {});
              _submitToPython();
            }
          },
          icon: const Icon(Icons.folder_open),
          label: Text(_buttonText(folderToUpdate))));

  //Adds a button to trigger a database backup
  Widget _backupDatabase() => BasicWidgets.pad(ElevatedButton(
      onPressed: () async {
        await API.triggerDatabaseBackup();
        bool errors = await BasicActions.displayThenClearErrors(context);
        if (!errors) {
          BasicWidgets.snack(
              context, "Database successfully backed up!", Colors.green);
        }
      },
      child: const Text("Backup the database")));

  //Adds a button to trigger a restore on the database
  Widget _restoreDatabase() => BasicWidgets.pad(ElevatedButton(
        onPressed: () async {
          BasicActions.actionableAlertBox(
              context,
              [
                const Text(
                    "This action will overwrite the current copy of the database with the most recent backup, this could result in data loss."),
                const Text("\nAre you sure you wish to continue?")
              ],
              "Restore the backup database?",
              "Yes", () async {
            await API.triggerDatabaseURestore();
            Navigator.of(context).pop();
            bool errors = await BasicActions.displayThenClearErrors(context);
            if (!errors) {
              BasicWidgets.snack(
                  context, "Database successfully restored!", Colors.green);
            }
          });
        },
        child: const Text("Restore the database"),
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
      ));

  // Helper functions

  // This method gets and sets the strings containing the current config values.
  void _updateStrings() async {
    _oneDriveFolder = await API.getOneDriveFolder();
    _backupFolder = await API.getBackupFolder();
    setState(() {});
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
  String _buttonText(String folderToDisplay) {
    String variable = "";
    switch (folderToDisplay) {
      case "OneDrive":
        API.getOneDriveFolder().then((value) {
          _oneDriveFolder = value;
        });
        variable = _oneDriveFolder;
        return variable != ""
            ? "Selected: " + variable.split("\\").last
            : "Select Folder";
      case "Backup":
        API.getBackupFolder().then((value) {
          _backupFolder = value;
        });
        variable = _backupFolder;
        return variable != ""
            ? "Selected: " + variable.split("\\").last
            : "Select Folder";
      default:
        return "Select Folder";
    }
  }
}
