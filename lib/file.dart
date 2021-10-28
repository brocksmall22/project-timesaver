import 'dart:convert';
import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/ui_api.dart';

class FileUploader extends StatefulWidget {
  const FileUploader({Key? key}) : super(key: key);

  @override
  State<FileUploader> createState() => _FileUploaderState();
}

class _FileUploaderState extends State<FileUploader> {
  List<File> files = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Process run reports"),
      ),
      body: Center(
          child: BasicWidgets.pad(
        BasicWidgets.horizontal([
          BasicWidgets.vertical([_getFile(context), _processButton(context)]),
          BasicWidgets.vertical(
              [const Text("Selected Files"), _listOfFiles(context)])
        ]),
      )),
    );
  }

  Widget _getFile(BuildContext context) {
    return BasicWidgets.pad(ElevatedButton.icon(
        onPressed: () async {
          FilePickerResult? result = await FilePicker.platform.pickFiles(
              type: FileType.custom,
              allowedExtensions: ['xls', 'xlsx'],
              allowMultiple: true);
          if (result != null) {
            files = result.paths.map((path) => File(path.toString())).toList();
          }
          setState(() {});
        },
        icon: const Icon(Icons.folder_open),
        label: const Text("Select files")));
  }

  Widget _processButton(BuildContext context) {
    return ElevatedButton(
        onPressed: files.isEmpty
            ? null
            : () async {
                await _submitToPython();
              },
        child: const Text("Process reports"));
  }

  Widget _listOfFiles(BuildContext context) {
    return Expanded(
        child: Container(
            width: 250,
            child: ListView(
              shrinkWrap: true,
              scrollDirection: Axis.vertical,
              children: _getFileCards(context),
            )));
  }

  List<Widget> _getFileCards(BuildContext context) {
    if (files.isNotEmpty) {
      return files.map((e) => Card(child: _fileCard(e.path))).toList();
    } else {
      return [
        const Card(
          child: SizedBox(
              height: 50,
              child: Center(child: Text("There are no files selected!"))),
        )
      ];
    }
  }

  Widget _fileCard(String fileName) {
    return BasicWidgets.pad(BasicWidgets.horizontal([
      Expanded(child: Text(fileName.split("\\").last)),
      IconButton(
          onPressed: () => _removeFileByName(fileName),
          icon: const Icon(Icons.delete))
    ]));
  }

  void _removeFileByName(String fileName) {
    for (var i = 0; i < files.length; i++) {
      if (files[i].path == fileName) {
        files.removeAt(i);
      }
      setState(() {});
    }
  }

  Future<bool> _submitToPython() async {
    //TODO: add the code to connect python and flutter.
    //Cannot be properly implemented until the REST API is complete.
    BasicWidgets.snack(context, "Processing, please wait...");
    //This Future.delayed represents the action of contacting the API. Currently
    //returns a bool signifiying if it worked. Does not need to do this.
    var _response = await API.submitFilesToDatabase(files);
    if (_response[0] == "True") {
      BasicWidgets.snack(context, "Reports have been processed!", Colors.green);
      return true;
    } else {
      BasicWidgets.snack(context, "Error processing reports!", Colors.red);
      _failedSubmissionsAlert(context, _response);
      return false;
    }
  }

  void _failedSubmissionsAlert(BuildContext context, List response) {
    showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text("Some reports could not be processed!"),
            content: SizedBox(
              width: 100,
              height: 75,
              child: ListView(
                children:
                    response.map((e) => Text(e.split("\\").last)).toList(),
              ),
            ),
            actions: [
              TextButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text("Okay"))
            ],
          );
        });
  }
}
