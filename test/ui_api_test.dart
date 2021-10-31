import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:project_time_saver/ui_api.dart';

void main() {
  List<String> arbitratyRange = [
    "2000-03-24 00:00:00.0000",
    "2001-03-24 00:00:00.0000"
  ];
  List<File> arbitraryFiles = [File("C:\\Users\\dalto\\Desktop\\509.xlsx")];
  test("Test that the API can tell when the server is clsoed", () async {
    // NOTE: This test is expected to fail if the server is running.
    expect(await API.checkIfServerIsAlive(), false);
  });

  test("Ensure that the server can be reached if running.", () async {
    //NOTE: This test is expected to fail if the server is stopped.
    expect(await API.checkIfServerIsAlive(), true);
  });
}
