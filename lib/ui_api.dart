import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart';

class API {
  static Future<List> submitFilesToDatabase(List<File> files) async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/submit_reports');
    List<String> filesAsStrings = files.map((e) => e.path).toList();
    String filesAsJsonArray = jsonEncode(filesAsStrings);
    Map<String, String> header = {"Content-Type": "application/json"};
    Response response =
        await post(_url, headers: header, body: filesAsJsonArray);
    List returnValue = jsonDecode(response.body);
    return returnValue;
  }

  static Future<List> generatePayrollFiles(List<String> dates) async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/generate_report');
    String filesAsJsonArray =
        jsonEncode({"startDate": dates[0], "endDate": dates[1]});
    Map<String, String> header = {"Content-Type": "application/json"};
    Response response =
        await post(_url, headers: header, body: filesAsJsonArray);
    List returnValue = jsonDecode(response.body);
    return returnValue;
  }
}
