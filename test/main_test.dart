import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:project_time_saver/main.dart';
import 'package:project_time_saver/payroll.dart';

void main() {
  testWidgets("Test correct number of buttons", (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    var elevatedButton = find.byType(ElevatedButton);
    expect(elevatedButton, findsNWidgets(5));
  });

  testWidgets("Test correct number of buttons", (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    var elevatedButton = find.byType(ElevatedButton);
    expect(elevatedButton, findsNWidgets(5));
  });
}
