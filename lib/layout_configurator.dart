import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
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
      body: Center(child: _configurationDropDown()));

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

  Map<String, Map<String, Object>> _configurations = {
    "old": {"string": 5},
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
        });
      });

  // Helper functions

}
