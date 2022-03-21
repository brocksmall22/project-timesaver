import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
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
        body: Center(
            child: ElevatedButton(
          child: const Text("Generate Graphics"),
          onPressed: () => {API.generateCharts()},
        )),
      );

  // Variables

  // Widgets

  // Helper functions

}
