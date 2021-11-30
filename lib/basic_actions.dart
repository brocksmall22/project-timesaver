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
}
