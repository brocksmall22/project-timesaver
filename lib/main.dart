import 'package:flutter/material.dart';
import 'package:project_time_saver/basic_actions.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/payroll.dart';
import 'package:project_time_saver/settings.dart';
import 'package:project_time_saver/data.dart';
import 'package:project_time_saver/ui_api.dart';
import 'package:window_size/window_size.dart';
import 'dart:io';

/*
This method runs the UI. If you set `debug` to false, it check to see if an
instance of the server is running. If so, it will continue as normal, if not, it
will start the server.

Bugs..
  medium: A small bug prevents the server from being closed with the UI. There
    is no way to capture when the UI is closing and close the server with it.
    In the next iteration, with some tuning, that is to be expected behavior.
*/
void main() async {
  bool debug = false;
  bool awake = await API.checkIfServerIsAlive();

  //exe of python code here: must be in the same directory
  !debug & !awake ? Process.run("dist\\project-timesaver.exe", []) : null;

  WidgetsFlutterBinding.ensureInitialized();
  if (Platform.isWindows) {
    setWindowMinSize(const Size(620, 750));
  }

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'Project Time Saver',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        home: const MainPage(),
      );
}

/*
This class houses the actual layout of the home/main page of the UI. It contains
buttons to navigate to the several different features of the program. It serves
no other purpose.
*/
class MainPage extends StatelessWidget {
  const MainPage({Key? key}) : super(key: key);

  //This is the main layout of the opening page. Each element in the Column
  //object are the buttons on the main page.
  @override
  Widget build(BuildContext context) {
    BasicActions.displayThenClearErrors(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text("Project Time Saver"),
      ),
      body: Center(
        child: BasicWidgets.vertical(
          [
            _payrollButton(context),
            //_nifrsButton(context),
            _statsButton(context),
            _settingsButton(context)
          ],
        ),
      ),
    );
  }

  //This button will open the "Generate Payroll" page
  Widget _payrollButton(BuildContext context) =>
      BasicWidgets.mainNavigationButton(
          context, "Generate Payroll", const PayrollUI());

  //This button will open the NIFRS reporting page once implemented
  // Widget _nifrsButton(BuildContext context) =>
  //     BasicWidgets.mainNavigationButton(context, "Generate NIFRS", null);

  //This button will open the stats generation page once implemented
  Widget _statsButton(BuildContext context) =>
      BasicWidgets.mainNavigationButton(
          context, "View Statistics", const DataUI());

  //This button will open the settings page once implemented
  Widget _settingsButton(BuildContext context) =>
      BasicWidgets.mainNavigationButton(
          context, "Settings", const SettingsUI());
}
