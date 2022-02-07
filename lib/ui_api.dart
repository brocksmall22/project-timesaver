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
  static Future<void> generatePayrollFiles(
      List<String> dates, String blankPayroll, String blankBreakdown) async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/generate_report');
    String filesAsJsonArray = jsonEncode({
      "start_date": dates[0],
      "end_date": dates[1],
      "payroll": blankPayroll,
      "breakdown": blankBreakdown
    });
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
    return retrunValue["one_drive_folder"];
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
      String postJson = jsonEncode({"one_drive_folder": folderString});
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
    return returnValue["update"].toString();
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
    return returnValue["update"] == Null ? 0 : returnValue["update"];
  }

  /*
  Triggers the backend to update the DB.
  */
  static Future<void> triggerDatabaseUpdate() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/trigger_update');
    await get(_url);
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

  /*
  Requests that the backend update the config value for db backup folder.

  inputs..
    backupFolder: the new folder
  returns..
    case 1: An empty string indicating success
    case 2: A string with an error
  */
  static updateBackupFolder(String backupFolder) async {
    if (backupFolder != "") {
      Uri _url = Uri.parse('http://127.0.0.1:8080/set_backup_folder');
      String postJson = jsonEncode({"backup_folder": backupFolder});
      Map<String, String> header = {"Content-Type": "application/json"};
      await post(_url, headers: header, body: postJson);
    }
  }

  /*
  Calls to the backend to get the current db backup folder value.

  returns..
    A string containing the current folder
  */
  static Future<String> getBackupFolder() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/get_backup_folder');
    Response response = await get(_url);
    Map retrunValue = jsonDecode(response.body);
    return retrunValue["backup_folder"];
  }

  /*
  Requests that the backend update the config value for blank payroll path.

  inputs..
    blankPayroll: the new path
  */
  static updateBlankPayrollPath(String blankPayroll) async {
    if (blankPayroll != "") {
      Uri _url = Uri.parse('http://127.0.0.1:8080/set_blank_payroll_path');
      String postJson = jsonEncode({"blank_payroll_path": blankPayroll});
      Map<String, String> header = {"Content-Type": "application/json"};
      await post(_url, headers: header, body: postJson);
    }
  }

  /*
  Calls to the backend to get the current blank payroll path value.

  returns..
    A string containing the current blank payroll path
  */
  static Future<String> getBlankPayrollPath() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/get_blank_payroll_path');
    Response response = await get(_url);
    Map retrunValue = jsonDecode(response.body);
    return retrunValue["blank_payroll_path"];
  }

  /*
  Requests that the backend update the config value for blank breakdown path.

  inputs..
    blankBreakdown: the new path
  */
  static updateBlankBreakdownPath(String blankBreakdown) async {
    if (blankBreakdown != "") {
      Uri _url = Uri.parse('http://127.0.0.1:8080/set_blank_breakdown_path');
      String postJson = jsonEncode({"blank_breakdown_path": blankBreakdown});
      Map<String, String> header = {"Content-Type": "application/json"};
      await post(_url, headers: header, body: postJson);
    }
  }

  /*
  Calls to the backend to get the current blank breakdown path value.

  returns..
    A string containing the current path
  */
  static Future<String> getBlankBreakdownPath() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/get_blank_breakdown_path');
    Response response = await get(_url);
    Map retrunValue = jsonDecode(response.body);
    return retrunValue["blank_breakdown_path"];
  }

  /*
  Triggers the backend to backup the DB.
  */
  static Future<void> triggerDatabaseBackup() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/trigger_backup');
    await get(_url);
  }

  /*
  Triggers the backend to restore the DB.
  */
  static Future<void> triggerDatabaseURestore() async {
    Uri _url = Uri.parse('http://127.0.0.1:8080/trigger_restore');
    await get(_url);
  }
}
