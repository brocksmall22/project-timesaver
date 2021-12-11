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
  static Future<void> generatePayrollFiles(List<String> dates) async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/generate_report');
    String filesAsJsonArray =
        jsonEncode({"startDate": dates[0], "endDate": dates[1]});
    Map<String, String> header = {"Content-Type": "application/json"};
    await post(_url, headers: header, body: filesAsJsonArray);
  }

  /*
  Calls to the backend to get the current config folder value.

  returns..
    A string containing the current folder
  */
  static Future<String> getOneDriveFolder() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/get_one_drive_folder');
    Response response = await get(_url);
    Map retrunValue = jsonDecode(response.body);
    return retrunValue["oneDriveFolder"];
  }

  /*
  Requests that the backend update the config value for one drive folder.

  inputs..
    folderString: the new folder
  returns..
    case 1: An empty string indicating success
    case 2: A string with an error
  */
  static Future<void> updateOneDriveFolder(String folderString) async {
    if (folderString != "") {
      Uri _url = Uri.parse('http://127.0.0.1:8080/set_one_drive_folder');
      String postJson = jsonEncode({"oneDriveFolder": folderString});
      Map<String, String> header = {"Content-Type": "application/json"};
      await post(_url, headers: header, body: postJson);
    }
  }

  /*
  Gets the most recent update to the DB from the backend.

  returns..
    The last update from the log
  */
  static Future<String> getMostRecentDatabaseUpdate() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/get_most_recent_db_update');
    Response response = await get(_url);
    Map returnValue = jsonDecode(response.body);
    return returnValue["lastUpdate"];
  }

  /*
  Gets the most recent run in the DB from the backend.

  returns..
    The most recent run
  */
  static Future<int> getMostRecentRun() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/get_most_recent_run');
    Response response = await get(_url);
    Map returnValue = jsonDecode(response.body);
    return returnValue["update"];
  }

  /*
  Triggers the backend to update the DB.
  */
  static Future<void> triggerDatabaseUpdate() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/trigger_update');
    await get(_url);
    await Future.delayed(const Duration(seconds: 5));
  }

  /*
  Gets the errors logged from the backend.

  returns..
    A list of map objects describing the errors.
  */
  static Future<List> getErrors() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/get_errors');
    Response response = await get(_url);
    List returnValue = jsonDecode(response.body);
    return returnValue;
  }

  //Triggers the backend to clear all of the errors logged.
  static Future<void> clearErrors() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/clear_errors');
    await get(_url);
  }

  /*
  Gets the success messages for generating the reports from the log.

  returns..
    A list of strings
  */
  static Future<List> getGenerationMessages() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/get_generation_messages');
    Response response = await get(_url);
    List returnValue = jsonDecode(response.body);
    return returnValue;
  }

  //Triggers the backend to clear out the generation messages.
  static Future<void> clearGenerationMessages() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/clear_generation_messages');
    await get(_url);
  }
}
