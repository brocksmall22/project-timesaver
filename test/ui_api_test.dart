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
  test("Test that the api will fail when no server is running.", () async {
    // NOTE: This test is expected to fail if the server is running.
    try {
      await API.generatePayrollFiles(arbitratyRange);
      print("Is the server running? If so, this fail is expected.");
      expect(true, false);
    } on SocketException {
      print("Test part 1/2 pass");
      try {
        await API.submitFilesToDatabase(arbitraryFiles);
        print("Is the server running? If so, this fail is expected.");
        expect(true, false);
      } on SocketException {
        print("Test part 2/2 pass");
        expect(true, true);
      } catch (e) {
        expect(true, false);
      }
    } catch (e) {
      expect(true, false);
    }
  });

  test("Ensure that the server can be reached if running.", () async {
    //NOTE: This test is expected to fail if the server is stopped.
    try {
      await API.generatePayrollFiles(arbitratyRange);
      print("Test part 1/2 pass");
      await API.submitFilesToDatabase(arbitraryFiles);
      print("Test part 2/2 pass");
      expect(true, true);
    } on SocketException {
      print("Is the server running? If not, this fail is expected.");
      expect(true, false);
    } catch (e) {
      print("Test failed with unexpected error");
      print(e);
      expect(true, false);
    }
  });
}
