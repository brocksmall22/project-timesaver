import 'package:flutter/material.dart';
import 'basic_widgets.dart';
import 'payroll.dart';

void main() {
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
