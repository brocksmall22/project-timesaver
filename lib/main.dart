import 'package:flutter/material.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/file.dart';
import 'package:project_time_saver/payroll.dart';
import 'dart:io';

void main() {
  bool debug = true;

  !debug
      ? Process.run("waitress-serve", [
          "--host=127.0.0.1",
          "--port=8080",
          "lib.api:app"
        ]).then((ProcessResult pr) {
          print(pr.exitCode);
          print(pr.stdout);
          print(pr.stderr);
        })
      : null;

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Project Time Saver',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MainPage(),
    );
  }
}

class MainPage extends StatelessWidget {
  const MainPage({Key? key}) : super(key: key);

  //This is the main layout of the opening page. Each element in the Column
  //object are the buttons on the main page.
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Project Time Saver"),
      ),
      body: Center(
        child: BasicWidgets.vertical(
          [
            _payrollButton(context),
            _gotToFileUpload(context),
            _nifrsButton(context),
            _statsButton(context),
            _settingsButton(context)
          ],
        ),
      ),
    );
  }

  Widget _payrollButton(BuildContext context) {
    return BasicWidgets.mainNavigationButton(
        context, "Generate Payroll", const PayrollUI());
  }

  Widget _gotToFileUpload(BuildContext context) {
    return BasicWidgets.mainNavigationButton(
        context, "Upload reports", const FileUploader());
  }

  Widget _nifrsButton(BuildContext context) {
    return BasicWidgets.mainNavigationButton(context, "Generate NIFRS", null);
  }

  Widget _statsButton(BuildContext context) {
    return BasicWidgets.mainNavigationButton(context, "View Statistics", null);
  }

  Widget _settingsButton(BuildContext context) {
    return BasicWidgets.mainNavigationButton(context, "Settings", null);
  }
}
