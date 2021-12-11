import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:project_time_saver/ui_api.dart';

class BasicActions {
  /*
  This action will add a page to the layout stack.

  inputs.. 
    page: a class that contains a new page
  */
  static nextPage(BuildContext context, page) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => page));
  }

  /*
  Draws an alert that informs the user of various conditions.

  inputs..
    response: A list containing message strings. Each string goes on a new line.
    title: A string of the title for the alert box.
  */
  static void generalAlertBox(
          BuildContext context, List<Widget> response, String title) =>
      showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text(title),
              content: SizedBox(
                width: 100,
                height: 75,
                child: ListView(
                  children: response,
                ),
              ),
              actions: [
                TextButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text("Okay"))
              ],
            );
          });

  /*
  This method gets all the errors from the log, displays them if there are any,
  and returns if there are any.

  returns..
    case 1: true if there are errors
    case 2: false if there are not errors
  */
  static Future<bool> displayThenClearErrors(BuildContext context) async {
    List errors = await API.getErrors();
    if (errors.isNotEmpty) {
      BasicActions.generalAlertBox(
          context,
          errors
              .map((e) => Tooltip(
                  message: "error type: " + e["type"] + "\ntime: " + e["time"],
                  child: Text(e["message"])))
              .toList(),
          "Errors occured!");
      await API.clearErrors();
      return true;
    }
    return false;
  }
}
