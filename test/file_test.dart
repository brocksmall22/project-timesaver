import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/file.dart';

Widget _buildPayrollUI() => MaterialApp(
      title: 'Project Time Saver',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const FileUploader(),
    );

void main() {
  testWidgets("Test that selected files text appears.",
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildPayrollUI());
    var text = find.text("Selected Files");
    expect(text, findsOneWidget);
  });

  testWidgets("Test select files button exists.", (WidgetTester tester) async {
    await tester.pumpWidget(_buildPayrollUI());
    var button = find.ancestor(
        of: find.byIcon(Icons.folder_open),
        matching: find.byWidgetPredicate((widget) => widget is ElevatedButton));
    expect(button, findsOneWidget);
  });

  testWidgets("Test process reports button exists.",
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildPayrollUI());
    var button = find.widgetWithText(ElevatedButton, "Process reports");
    expect(button, findsOneWidget);
  });

  testWidgets("Test no selected files card exists.",
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildPayrollUI());
    var button = find.widgetWithText(Card, "There are no files selected!");
    expect(button, findsOneWidget);
  });

/*
  testWidgets("Test remove button when files are selected exists.",
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildPayrollUI());
    var button = find.widgetWithIcon(Card, Icons.delete);
    expect(button, findsOneWidget);
  });
  */
}
