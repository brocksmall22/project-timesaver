import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart';

class API {
  static final Uri _url = Uri.parse('http://127.0.0.1:8080/submit_reports');
  static Future<List> submitFilesToDatabase(List<File> files) async {
    List<String> filesAsStrings = files.map((e) => e.path).toList();
    String filesAsJsonArray = jsonEncode(filesAsStrings);
    Map<String, String> header = {"Content-Type": "application/json"};
    Response response =
        await post(_url, headers: header, body: filesAsJsonArray);
    //Response response = await get(_url);
    List returnValue = jsonDecode(response.body);
    return returnValue;
  }
}
