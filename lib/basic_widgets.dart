import 'package:flutter/material.dart';
import 'package:project_time_saver/basic_actions.dart';

class BasicWidgets {
  //This widget is a wrapper for a Padding with 5 on all sides
  static Widget pad(Widget toPad) {
    return Padding(
      padding: const EdgeInsets.all(5),
      child: toPad,
    );
  }

  //This widget is a wrapper for a SizeBox with a width of 150
  static Widget mainBox(Widget toBox) {
    return SizedBox(
      width: 150,
      child: toBox,
    );
  }

  //This is a wrapper for a the Column widget with center aligned elements
  static Widget vertical(List<Widget> widgets) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: widgets,
    );
  }

  //This is a wrapper for a the Row widget with center aligned elements
  static Widget horizontal(List<Widget> widgets) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: widgets,
    );
  }

  //This is a wrapper for all of the nav buttons on the main page. The "page"
  //variable is a class variable, such as "payrollUI()"
  static Widget mainNavigationButton(BuildContext context, String text, page) {
    //This if, and everything in it, can be removed when all main UI buttons
    //have a page they link to
    if (page == null) {
      return pad(mainBox(ElevatedButton(onPressed: null, child: Text(text))));
    }

    return pad(mainBox(ElevatedButton(
        onPressed: () => BasicActions.nextPage(context, page),
        child: Text(text))));
  }

  static void snack(BuildContext context, String text,
      [Color? color = Colors.black54, action]) {
    ScaffoldMessenger.of(context).clearSnackBars();
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text(text),
      backgroundColor: color,
      action: action,
    ));
  }
}
