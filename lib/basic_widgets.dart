import 'package:flutter/material.dart';
import 'package:project_time_saver/basic_actions.dart';

class BasicWidgets {
  /*
  This widget is a wrapper for a Padding with 5 on all sides

  inputs..
    toPad: the widget you wish to pad
  */
  static Widget pad(Widget toPad) => Padding(
        padding: const EdgeInsets.all(5),
        child: toPad,
      );

  /*
  This widget is a wrapper for a SizeBox with a width of 150

  inputs..
    toBox: the widget you wish to box
  */
  static Widget mainBox(Widget toBox) => SizedBox(
        width: 150,
        child: toBox,
      );

  /*
  This is a wrapper for a the Column widget with center aligned elements

  inputs..
    widgets: a list of widgets you wish to put in a Column
  */
  static Widget vertical(List<Widget> widgets) => Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: widgets,
      );

  /*
  This is a wrapper for a the Row widget with center aligned elements

  inputs..
    widgets: a list of widgets you wish to put in a Row
  */
  static Widget horizontal(List<Widget> widgets) => Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: widgets,
      );

  /*
  This is a wrapper for all of the nav buttons on the main page.

  inputs..
    page: a class that contains a new page
    text: The text you wish to display on the button

  returns..
    case 1: If page is null, it will return a button that is disabled
    case 2: If page is not null, it will return a button that will navigate to
      the new page
  */
  static Widget mainNavigationButton(BuildContext context, String text, page,
      {restricted = true}) {
    //This if, and everything in it, can be removed when all main UI buttons
    //have a page they link to
    if (page == null) {
      return pad(mainBox(ElevatedButton(onPressed: null, child: Text(text))));
    }
    return restricted
        ? pad(mainBox(ElevatedButton(
            onPressed: () => BasicActions.nextPage(context, page),
            child: Text(text))))
        : pad(ElevatedButton(
            onPressed: () => BasicActions.nextPage(context, page),
            child: Text(text)));
  }

  /*
  This function will draw a snakbar on the bottom of the page.

  inputs..
    text: the text you wish to display on the snackbar
    color (optional): the color of the snackabar
        default: a dark grey color
    action (optional): a SnackAction object to provide a button the user can
      press on the snackbar.
        default: null
  */
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
