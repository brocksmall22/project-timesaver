import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:project_time_saver/basic_widgets.dart';
import 'package:project_time_saver/main.dart';
import 'package:project_time_saver/payroll.dart';

Widget _buildPayrollUI() => MaterialApp(
      title: 'Project Time Saver',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const PayrollUI(),
    );

void main() {
  testWidgets("Test that reminder text appears.", (WidgetTester tester) async {
    await tester.pumpWidget(_buildPayrollUI());
    var text = find
        .text("Don't forget to ensure all run reports have been processed!");
    expect(text, findsOneWidget);
  });

  testWidgets("Test cancel button exists.", (WidgetTester tester) async {
    await tester.pumpWidget(_buildPayrollUI());
    var button = find.widgetWithText(ElevatedButton, "Cancel");
    expect(button, findsOneWidget);
  });

  testWidgets("Test generate button exists.", (WidgetTester tester) async {
    await tester.pumpWidget(_buildPayrollUI());
    var button = find.widgetWithText(ElevatedButton, "Generate");
    expect(button, findsOneWidget);
  });

  testWidgets("Test submit reports button exists.",
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildPayrollUI());
    var button = find.widgetWithText(ElevatedButton, "Upload reports");
    expect(button, findsOneWidget);
  });

  testWidgets("Test select dates button exists.", (WidgetTester tester) async {
    await tester.pumpWidget(_buildPayrollUI());
    var button = find.ancestor(
        of: find.byIcon(Icons.calendar_today),
        matching: find.byWidgetPredicate((widget) => widget is ElevatedButton));
    expect(button, findsOneWidget);
  });
}
