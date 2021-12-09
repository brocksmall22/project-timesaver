import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

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
          BuildContext context, List<String> response, String title) =>
      showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text(title),
              content: SizedBox(
                width: 100,
                height: 75,
                child: ListView(
                  children: response.map((e) => Text(e)).toList(),
                ),
              ),
              actions: [
                TextButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text("Okay"))
              ],
            );
          });
}
