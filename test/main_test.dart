import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:project_time_saver/main.dart';

void main() {
  testWidgets("Test for generate button", (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    var elevatedButton =
        find.widgetWithText(ElevatedButton, "Generate Payroll");
    expect(elevatedButton, findsOneWidget);
  });

  testWidgets("Test for submit button", (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    var elevatedButton = find.widgetWithText(ElevatedButton, "Upload reports");
    expect(elevatedButton, findsOneWidget);
  });

  testWidgets("Test NIFRS button", (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    var elevatedButton = find.widgetWithText(ElevatedButton, "Generate NIFRS");
    expect(elevatedButton, findsOneWidget);
  });

  testWidgets("Test for stats button", (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    var elevatedButton = find.widgetWithText(ElevatedButton, "View Statistics");
    expect(elevatedButton, findsOneWidget);
  });

  testWidgets("Test for settings button", (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    var elevatedButton = find.widgetWithText(ElevatedButton, "Settings");
    expect(elevatedButton, findsOneWidget);
  });
}
