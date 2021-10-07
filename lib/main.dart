import 'package:flutter/material.dart';
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

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: const Text("Project Time Saver"),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          // Column is also a layout widget. It takes a list of children and
          // arranges them vertically. By default, it sizes itself to fit its
          // children horizontally, and tries to be as tall as its parent.
          //
          // Invoke "debug painting" (press "p" in the console, choose the
          // "Toggle Debug Paint" action from the Flutter Inspector in Android
          // Studio, or the "Toggle Debug Paint" command in Visual Studio Code)
          // to see the wireframe for each widget.
          //
          // Column has various properties to control how it sizes itself and
          // how it positions its children. Here we use mainAxisAlignment to
          // center the children vertically; the main axis here is the vertical
          // axis because Columns are vertical (the cross axis would be
          // horizontal).
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            _payrollButton(context),
            _NIFRSButton(context),
            _statsButton(context),
            _settingsButton(context)
          ],
        ),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }

  Widget _payrollButton(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.all(5),
        child: SizedBox(
            width: 150,
            child: ElevatedButton(
                onPressed: () => Navigator.push(context,
                    MaterialPageRoute(builder: (context) => PayrollUI())),
                child: const Text("Generate Payroll"))));
  }

  Widget _NIFRSButton(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.all(5),
        child: SizedBox(
            width: 150,
            child: ElevatedButton(
                onPressed: null, child: const Text("Generate NIFRS"))));
  }

  Widget _statsButton(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.all(5),
        child: SizedBox(
            width: 150,
            child: ElevatedButton(
                onPressed: null, child: const Text("View Statistics"))));
  }

  Widget _settingsButton(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.all(5),
        child: SizedBox(
            width: 150,
            child: ElevatedButton(
                onPressed: null, child: const Text("Settings"))));
  }
}
