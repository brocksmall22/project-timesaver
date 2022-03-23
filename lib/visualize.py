from matplotlib.figure import Figure
from .sqlFunctions import sqlFunctions
import numpy as np
import io

class visualize:
    #TODO: wrap each of these in a try catch and be sure that the errors are captured
    #   and logged
    def plotTypesOfRuns(startDate: str, endDate: str) -> str:
        """
        Takes two dates (formatted "YYYY-mm-dd") and uses
        them to fetch all of the types of runs for each
        incident between those dates to generate a
        frequency distribution bar chart for those variables.

        inputs..
            startDate: the (inclusive) date for the start of the period
            endDate: the (inclusive) date for the end of the period
        returns..
            A byte string of the generated image
        """
        with sqlFunctions() as sqlRunner:
            if sqlRunner.getTotalNumberOfRunsDuringPeriod(startDate, endDate) == 0:
                return None
            runTypes = sqlRunner.getRunTypes(startDate, endDate)
            values = {}
            for item in runTypes:
                if item[0] != "":
                    for run in item[0].split(","):
                        if run not in values.keys():
                            values[run] = 1
                        else:
                            values[run] += 1
            returnBuff = io.BytesIO()
            fig = Figure(figsize=(10, 5), dpi=300)
            plt = fig.subplots()
            plt.bar(values.keys(), values.values())
            plt.tick_params(axis = "x", labelrotation = 45)
            plt.set_ylabel("Number of Incidents")
            plt.set_xlabel("Type of Incident")
            fig.tight_layout()
            fig.savefig(returnBuff, format = "png")
            return returnBuff


    def plotRunStartTimeDistribution(startDate, endDate):
        with sqlFunctions() as sqlRunner: 
            if sqlRunner.getTotalNumberOfRunsDuringPeriod(startDate, endDate) == 0:
                return None
            startTimes = sqlRunner.getStartTimeOfRuns(startDate, endDate)
            hours = ["0000", "0100", "0200", "0300", "0400", "0500", "0600", "0700",
                    "0800", "0900", "1000", "1100", "1200", "1300", "1400", "1500",
                    "1600", "1700", "1800", "1900", "2000", "2100", "2200", "2300"]
            frequency = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0]
            for time in startTimes:
                if 0 <= time[0] < 100:
                    frequency[0] += 1
                elif 100 <= time[0] < 200:
                    frequency[1] += 1
                elif 200 <= time[0] < 300:
                    frequency[2] += 1
                elif 300 <= time[0] < 400:
                    frequency[3] += 1
                elif 400 <= time[0] < 500:
                    frequency[4] += 1
                elif 500 <= time[0] < 600:
                    frequency[5] += 1
                elif 600 <= time[0] < 700:
                    frequency[6] += 1
                elif 700 <= time[0] < 800:
                    frequency[7] += 1
                elif 800 <= time[0] < 900:
                    frequency[8] += 1
                elif 900 <= time[0] < 1000:
                    frequency[9] += 1
                elif 1000 <= time[0] < 1100:
                    frequency[10] += 1
                elif 1100 <= time[0] < 1200:
                    frequency[11] += 1
                elif 1200 <= time[0] < 1300:
                    frequency[12] += 1
                elif 1300 <= time[0] < 1400:
                    frequency[13] += 1
                elif 1400 <= time[0] < 1500:
                    frequency[14] += 1
                elif 1500 <= time[0] < 1600:
                    frequency[15] += 1
                elif 1600 <= time[0] < 1700:
                    frequency[16] += 1
                elif 1700 <= time[0] < 1800:
                    frequency[17] += 1
                elif 1800 <= time[0] < 1900:
                    frequency[18] += 1
                elif 1900 <= time[0] < 2000:
                    frequency[19] += 1
                elif 2000 <= time[0] < 2100:
                    frequency[20] += 1
                elif 2100 <= time[0] < 2200:
                    frequency[21] += 1
                elif 2200 <= time[0] < 2300:
                    frequency[22] += 1
                elif 2300 <= time[0]:
                    frequency[23] += 1
            returnBuff = io.BytesIO()
            fig = Figure(figsize=(10, 5), dpi=300)
            plt = fig.subplots()
            plt.bar(hours, frequency)
            plt.tick_params(axis = "x", labelrotation = 45)
            plt.set_ylabel("Number of Incidents")
            plt.set_xlabel("Incident Report Time (MST)")
            fig.tight_layout()
            fig.savefig(returnBuff, format = "png")
            return returnBuff


    def plotRunTownships(startDate, endDate):
        with sqlFunctions() as sqlRunner:
            if sqlRunner.getTotalNumberOfRunsDuringPeriod(startDate, endDate) == 0:
                return None
            townships = sqlRunner.getTownshipOfRuns(startDate, endDate)
            options = ["Harrison - City", "Harrison - County", "Lancaster - City",
                    "Lancaster - County"]
            frequency = [0, 0, 0, 0]
            for township in townships:
                match township[0]:
                    case "harrison,city":
                        frequency[0] += 1
                    case "harrison,county":
                        frequency[1] += 1
                    case "lancaster,city":
                        frequency[2] += 1
                    case "lancaster,county":
                        frequency[3] += 1
            returnBuff = io.BytesIO()
            fig = Figure(figsize=(5, 3), dpi=300)
            plt = fig.subplots()
            plt.pie(frequency, labels = options)
            fig.tight_layout()
            fig.savefig(returnBuff, format = "png")
            return returnBuff

    def plotRunDurationsByTypes():
        pass


    def plotApparatusUsageFrequency(startDate, endDate):
        with sqlFunctions() as sqlRunner:
            if sqlRunner.getTotalNumberOfRunsDuringPeriod(startDate, endDate) == 0:
                return None
            apparatus = sqlRunner.getApparatusOfRuns(startDate, endDate)
            values = {}
            for string in apparatus:
                for app in string[0].split(","):
                    if app in values.keys():
                        values[app] += 1
                    else:
                        values[app] = 1
            returnBuff = io.BytesIO()
            fig = Figure(figsize=(10, 5), dpi=300)
            plt = fig.subplots()
            plt.bar(values.keys(), values.values())
            plt.tick_params(axis = "x", labelrotation = 45)
            plt.set_ylabel("Number of Incidents")
            plt.set_xlabel("Apparatus")
            fig.tight_layout()
            fig.savefig(returnBuff, format = "png")
            return returnBuff


    def plotGivenAid(startDate, endDate):
        with sqlFunctions() as sqlRunner:
            if sqlRunner.getTotalNumberOfRunsDuringPeriod(startDate, endDate) == 0:
                return None
            givenAid = sqlRunner.getGivenAid(startDate, endDate)
            stations = []
            man = []
            app = []
            for item in givenAid:
                if item[0] != "":
                    for aid in item[0].split(";"):
                        department, aidType = aid.split(",")
                        if department not in stations:
                            stations.append(department)
                            man.append(0)
                            app.append(0)
                        if aidType == "man":
                            man[stations.index(department)] += 1
                        elif aidType == "app":
                            app[stations.index(department)] += 1
            returnBuff = io.BytesIO()
            fig = Figure(figsize=(10, 5), dpi=300)
            plt = fig.subplots()
            if man == app == []:
                yMax = 1
            else:
                yMax = max(man) if max(man) > max(app) else max(app)
            x = np.arange(len(stations))
            plt.bar(x + 0.2, man, width = 0.4)
            plt.bar(x - 0.2, app, width = 0.4)
            plt.set_yticks(range(0, yMax + 1))
            plt.set_xticks(x, stations)
            plt.tick_params(axis = "x", labelrotation = 45)
            plt.set_ylabel("Number of Incidents")
            plt.set_xlabel("Department Recieving Aid")
            plt.legend(["Manual Labor", "Apparatus"])
            fig.tight_layout()
            fig.savefig(returnBuff, format = "png")
            return returnBuff


    def plotTakenAid(startDate, endDate):
        with sqlFunctions() as sqlRunner:
            if sqlRunner.getTotalNumberOfRunsDuringPeriod(startDate, endDate) == 0:
                return None
            takenAid = sqlRunner.getTakenAid(startDate, endDate)
            stations = []
            man = []
            app = []
            for item in takenAid:
                if item[0] != "":
                    for aid in item[0].split(";"):
                        department, aidType = aid.split(",")
                        if department not in stations:
                            stations.append(department)
                            man.append(0)
                            app.append(0)
                        if aidType == "man":
                            man[stations.index(department)] += 1
                        elif aidType == "app":
                            app[stations.index(department)] += 1
            returnBuff = io.BytesIO()
            fig = Figure(figsize=(10, 5), dpi=300)
            plt = fig.subplots()
            if man == app == []:
                yMax = 1
            else:
                yMax = max(man) if max(man) > max(app) else max(app)
            x = np.arange(len(stations))
            plt.bar(x + 0.2, man, width = 0.4)
            plt.bar(x - 0.2, app, width = 0.4)
            plt.set_yticks(range(0, yMax + 1))
            plt.set_xticks(x, stations)
            plt.tick_params(axis = "x", labelrotation = 45)
            plt.set_ylabel("Number of Incidents")
            plt.set_xlabel("Department Providing Aid")
            plt.legend(["Manual Labor", "Apparatus"])
            fig.tight_layout()
            fig.savefig(returnBuff, format = "png")
            return returnBuff


    def plotAverageRunTimes():
        pass


    def plotShiftCoverage(startDate, endDate):
        with sqlFunctions() as sqlRunner:
            if sqlRunner.getTotalNumberOfRunsDuringPeriod(startDate, endDate) == 0:
                return None
            shiftCoverages = sqlRunner.getShiftCoverages(startDate, endDate)
            values = {}
            for run in shiftCoverages:
                if run[0].upper() not in values.keys():
                    values[run[0].upper()] = 0
                if run[1] == 1:
                    values[run[0].upper()] += 1
            returnBuff = io.BytesIO()
            fig = Figure(figsize=(10, 5), dpi=300)
            plt = fig.subplots()
            yMax = max(values.values())
            yMax = yMax + 1 if yMax == 0 else yMax
            plt.bar(values.keys(), values.values())
            plt.set_yticks(range(0, yMax + 1))
            plt.set_ylabel("Number of Incidents Fully Covered")
            plt.set_xlabel("Shift Responding")
            fig.tight_layout()
            fig.savefig(returnBuff, format = "png")
            return returnBuff