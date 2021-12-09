import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:project_time_saver/basic_actions.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/ui_api.dart';

class FileUploader extends StatefulWidget {
  const FileUploader({Key? key}) : super(key: key);

  @override
  State<FileUploader> createState() => _FileUploaderState();
}

/*
This class contains the entire layout of the file submission page. It contains a
button that will opena file chooser dialogue, a button to submit, and a ListView
of Cards that display which files have been selected for uploading. Each card
has a delete button to remove it from the list of files to submit.
*/
class _FileUploaderState extends State<FileUploader> {
  //This widget is the main layout of the page
  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: const Text("Process run reports"),
        ),
        body: _getLayout(),
      );

  //Variables:

  List<File> files = [];
  bool processing = false;

  //Widgets:

  /*
  This widget determines which layout to use.

  returns..
    case 1: The main layout of the page
    case 2: A circular progress indicator when reports are being processed
  */
  Widget _getLayout() {
    if (processing == false) {
      return Center(
          child: BasicWidgets.pad(
        BasicWidgets.horizontal([
          BasicWidgets.vertical([_getFile(context), _processButton(context)]),
          BasicWidgets.vertical(
              [const Text("Selected Files"), _listOfFiles(context)])
        ]),
      ));
    } else {
      return Center(
          child: BasicWidgets.vertical([
        BasicWidgets.pad(const Text("Processing... This may take a while.")),
        BasicWidgets.pad(const CircularProgressIndicator())
      ]));
    }
  }

  //This is the button to select new files
  Widget _getFile(BuildContext context) => BasicWidgets.pad(ElevatedButton.icon(
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

  //This is the button to submit new files to the server for DB addition
  Widget _processButton(BuildContext context) => ElevatedButton(
      onPressed: files.isEmpty
          ? null
          : () async {
              await _submitToPython();
              files = [];
              setState(() {});
            },
      child: const Text("Process reports"));

  /*
  This is the ListView of Cards that show which files are slated for
  submission
  */
  Widget _listOfFiles(BuildContext context) => Expanded(
      child: SizedBox(
          width: 250,
          child: ListView(
            shrinkWrap: true,
            scrollDirection: Axis.vertical,
            children: _getFileCards(context),
          )));

  //This is a list of Card widgets that contains each file slated for submission
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

  /*
  This is the actual card that will contain the filename and delete button for
  files slated for submission

  inputs..
    fileName: the name of the file as a string
  */
  Widget _fileCard(String fileName) =>
      BasicWidgets.pad(BasicWidgets.horizontal([
        Expanded(child: Text(fileName.split("\\").last)),
        _deleteButton(fileName)
      ]));

  /*
  This widget is the delete button on each card.

  inputs..
    fileName: the name of the file to be removed as a String
  */
  Widget _deleteButton(String fileName) => IconButton(
      onPressed: () => _removeFileByName(fileName),
      icon: const Icon(Icons.delete));

  //Helper functions:

  /*
  This function is called by the delete button on the Card and will remove the
  file from the list of files to submit.

  inputs..
    fileName: the name of the file as a String
  */
  void _removeFileByName(String fileName) {
    for (var i = 0; i < files.length; i++) {
      if (files[i].path == fileName) {
        files.removeAt(i);
      }
      setState(() {});
    }
  }

  /*
  This is the function responsible for interfacing with the API and submitting
  the files.

  returns.. 
    case 1: true if successful
    case 2: false if not
  */
  Future<bool> _submitToPython() async {
    setState(() {
      processing = true;
    });
    var response = await API.submitFilesToDatabase(files);
    setState(() {
      processing = false;
    });
    if (response[0] == true) {
      BasicWidgets.snack(context, "Reports have been processed!", Colors.green);
      return true;
    } else {
      BasicWidgets.snack(context, "Error processing reports!", Colors.red);
      BasicActions.generalAlertBox(
          context,
          response.map((e) => e.split("\\").last.toString()).toList(),
          "Some reports could not be processed!");
      return false;
    }
  }
}
