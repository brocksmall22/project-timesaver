import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart';

class API {
  /*
  This method sends a GET request to the server to determine if it is alive.
  This runs before the UI begins so that the program can spawn a new instance
  of the server as needed.

  returns..
    case 1: True if server is alive
    case 2: False if server is dead
  */
  static Future<bool> checkIfServerIsAlive() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/verify');
    try {
      Response response = await get(_url);
      return jsonDecode(response.body)["result"];
    } on SocketException {
      return false;
    } catch (e) {
      return false;
    }
  }

  /*
  This function will send a POST containing file paths to the server. The server
  is then expected to add those files to the database and return a pass/fail
  response.

  inputs.. 
    files: A list of File (dart.io) objects.
  returns.. 
    case 1: A list containing either one value of true
    case 2: A list of files that could not be added to the database
  */
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

  /*
  This function will send a POST to the server containing a Json object with
  startDate and endDate values denoting the start and end of the pay period.
  The server is expected to respond with a list of information regarding the
  generated files or a list of errors.

  inputs..
    dates: A list of dates in string format
  returns..
    case 1: A list containing true followed by information regarding the files
      and the path of the files generated
    case 2: A list containing some errors
  */
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
