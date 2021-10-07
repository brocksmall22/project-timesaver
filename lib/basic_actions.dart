import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

//This action will add a page to the layout stack. The "page" variable is a new
//class object (i.e. payrollUI()).
class BasicActions {
  static nextPage(BuildContext context, page) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => page));
  }
}
