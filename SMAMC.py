# Sun and Moon Apparent Motion Calculator
# Author: Thomas Jin
# Course: Programming with Python
# Date: Dec 2023

# IMPORT

import math
import datetime
from zhdate import ZhDate
import matplotlib.pyplot as plt
import csv

# FUNCTION

def sexagesimalLatitudeConverter(decimalDegree):
    degree = int(decimalDegree)
    minute = int((decimalDegree - degree) * 60)
    second = round(((decimalDegree - degree) * 60 - minute) * 60, 4)
    if decimalDegree >= 0:
        DMS = str(degree) + '° ' + str(minute) + '\' ' + str(second) + '" N'
    else:
        DMS = str(abs(degree)) + '° ' + str(abs(minute)) + '\' ' + str(abs(second)) + '" S'
    return DMS

def sexagesimalTimeConverter(decimalHour):
    hour = int(decimalHour)
    minute = int((decimalHour - hour) * 60)
    second = round(((decimalHour - hour) * 60 - minute) * 60)
    if second == 60:
        minute += 1
        second = 0
    else:
        pass
    HMS = str('%02d' % hour) + ':' + str('%02d' % minute) + ':' + str('%02d' % second)
    return HMS

def directionalAzimuthConverter(angularAzimuth):
    if 0 < angularAzimuth < 90:
        directionalAzimuth = str(round(angularAzimuth, 4)) + '° east of north'
    elif angularAzimuth == 90:
        directionalAzimuth = 'East'
    elif 90 < angularAzimuth < 180:
        directionalAzimuth = str(round((180 - angularAzimuth), 4)) + '° east of south'
    elif angularAzimuth == 180:
        directionalAzimuth = 'South'
    elif 90 < angularAzimuth < 270:
        directionalAzimuth = str(round((angularAzimuth - 180), 4)) + '° west of south'
    elif angularAzimuth == 270:
        directionalAzimuth = 'West'
    elif 270 < angularAzimuth < 360:
        directionalAzimuth = str(round((360 - angularAzimuth), 4)) + '° west of north'
    else:
        directionalAzimuth = 'North'
    return directionalAzimuth

# Based on the geometric method, I have to set the following preconditions which may lead to some inevitable numerical errors (differences):
# 1. We assume that the earth is perfectly spherical.
# 2. We ignore the atmospheric refraction of sunlight.
# 3. The time results calculated by this function are all local time.
# For example, there may be an error of several minutes when computing the sunrise time using geometric method, compared with physical optics method.
def sunApparentMotionCalculator(m, d, y, lat):
    normalizedDate = str('%02d' % m) + '/' + str('%02d' % d) + '/' + str(y)
    latitude = sexagesimalLatitudeConverter(lat)
    solarDeclination = 23.44 * math.sin(math.radians(30 * m + 1 * d - 112))
    halfdayDuration = 1/math.radians(15) * math.acos(-math.tan(math.radians(lat)) * math.tan(math.radians(solarDeclination)))
    sunriseTime = 12 - halfdayDuration
    sunsetTime = 12 + halfdayDuration
    daylength = sunsetTime - sunriseTime
    nightlength = 24 - daylength
    sinθr = math.cos((sunriseTime - 12) * 15) * math.cos(solarDeclination) * math.cos(lat) + math.sin(solarDeclination) * math.sin(lat)
    solarAzimuthSunrise = math.degrees(math.acos((math.sin(solarDeclination) - sinθr * math.sin(lat))/math.cos(math.asin(sinθr)) * math.cos(lat)))
    solarAzimuthSunset = 180 + (180 - solarAzimuthSunrise)
    solarElevationNoon = 90 - abs(lat - solarDeclination)
    sexagesimalSolarDeclination = sexagesimalLatitudeConverter(solarDeclination)
    sexagesimalSunriseTime = sexagesimalTimeConverter(sunriseTime)
    sexagesimalSunsetTime = sexagesimalTimeConverter(sunsetTime)
    sexagesimalDaylength = sexagesimalTimeConverter(daylength)
    sexagesimalNightlength = sexagesimalTimeConverter(nightlength)
    directionalAzimuthSunrise = directionalAzimuthConverter(solarAzimuthSunrise)
    directionalAzimuthSunset = directionalAzimuthConverter(solarAzimuthSunset)
    roundElevationNoon = str(round(solarElevationNoon, 4)) + '°'
    sunApparentMotionData = 'Date:				' + normalizedDate + '\nLatitude:			' + latitude + '\nSolar declination:		' + sexagesimalSolarDeclination + '\nSunrise time:			' + sexagesimalSunriseTime + '\nSunset time:			' + sexagesimalSunsetTime + '\nDaylength:			' + sexagesimalDaylength + '\nNightlength:			' + sexagesimalNightlength + '\nSolar azimuth of sunrise:	' + directionalAzimuthSunrise + '\nSolar azimuth of sunset:	' + directionalAzimuthSunset + '\nSolar elevation at noon:	' + roundElevationNoon
    return sunApparentMotionData

# The function uses a simplified method when computing the apparent motion data of the moon, without considering geographical coordinates, so there are some errors.
def moonApparentMotionCalculator(m, d, y, lat):
    date = datetime.datetime(y, m, d)
    lunarDate = str(ZhDate.from_datetime(date))
    # I am turning lunarDate into a list instead of using index directly because the number of digits of the month and date in lunarDate is uncertain.
    formattedLunarDate = lunarDate.replace('农历', '').replace('年', ' ').replace('月', ' ').replace('日', '')
    splitLunarDate = formattedLunarDate.split()
    normalizedLunarDate = str('%02d' % int(splitLunarDate[1])) + '/' + str('%02d' % int(splitLunarDate[2])) + '/' + str(splitLunarDate[0])
    extractedLunarDate = int(splitLunarDate[2])
    moonriseTime = extractedLunarDate * 0.8 + 6
    if moonriseTime >= 24:
        moonriseTime = moonriseTime - 24
    else:
        pass
    moonsetTime = extractedLunarDate * 0.8 - 6
    if moonsetTime < 0:
        moonsetTime = moonsetTime + 24
    else:
        pass
    if extractedLunarDate <= 15:
        floodTideTime = extractedLunarDate * 0.8
    else:
        floodTideTime = (extractedLunarDate - 15) * 0.8
    ebbTideTime = floodTideTime - 6
    if ebbTideTime < 0:
        ebbTideTime = ebbTideTime + 24
    else:
        pass
    sexagesimalMoonriseTime = sexagesimalTimeConverter(moonriseTime)
    sexagesimalMoonsetTime = sexagesimalTimeConverter(moonsetTime)
    sexagesimalFloodTideTime = sexagesimalTimeConverter(floodTideTime)
    sexagesimalEbbTideTime = sexagesimalTimeConverter(ebbTideTime)
    if lat < 0:
        moonPhase = 'The actual moon phase and the figure displayed are centrosymmetry (Southern Hemisphere).'
    else:
        moonPhase = 'The moon phase is as the figure displayed (Northern Hemisphere).'
    moonApparentMotionData = 'Lunar date:			' + normalizedLunarDate + '\nMoonrise time:			' + sexagesimalMoonriseTime + '\nMoonset time:			' + sexagesimalMoonsetTime + '\nFlood tide time:		' + sexagesimalFloodTideTime + '\nEbb tide time:			' + sexagesimalEbbTideTime + '\nMoon phase:			' + moonPhase
    return moonApparentMotionData

def moonPhase(m, d, y):
    date = datetime.datetime(y, m, d)
    lunarDate = str(ZhDate.from_datetime(date))
    formattedLunarDate = lunarDate.replace('农历', '').replace('年', ' ').replace('月', ' ').replace('日', '')
    splitLunarDate = formattedLunarDate.split()
    extractedLunarDate = int(splitLunarDate[2])
    figure = plt.gcf()
    axes = plt.gca()
    figure.set_facecolor('black')
    axes.patch.set_facecolor('black')
    fullMoon = plt.Circle((0.5, 0.5), 0.49, color = 'white')
    if 2 <= extractedLunarDate <= 5:
        shade = plt.Circle((0, 0.5), 0.7, color = 'black')
        plt.title('Waxing Crescent', color = 'white')
    elif 6 <= extractedLunarDate <= 9:
        shade = plt.Rectangle((0, 0), 0.5, 1, color = 'black')
        plt.title('First Quarter', color = 'white')
    elif 10 <= extractedLunarDate <= 13:
        shade = plt.Circle((1, 0.5), 0.7, color = 'black', alpha = 0.1)
        plt.title('Waxing Gibbous', color = 'white')
    elif 14 <= extractedLunarDate <= 16:
        shade = fullMoon
        plt.title('Full Moon', color = 'white')
    elif 17 <= extractedLunarDate <= 20:
        shade = plt.Circle((0, 0.5), 0.7, color = 'black', alpha = 0.1)
        plt.title('Waning Gibbous', color = 'white')
    elif 21 <= extractedLunarDate <= 24:
        shade = plt.Rectangle((0.5, 0), 0.5, 1, color = 'black')
        plt.title('Last Quarter', color = 'white')
    elif 25 <= extractedLunarDate <= 28:
        shade = plt.Circle((1, 0.5), 0.7, color = 'black')
        plt.title('Waning Crescent', color = 'white')
    else:
        shade = plt.Circle((0.5, 0.5), 0.49, color = 'black')
        plt.title('New Moon', color = 'white')
    axes.add_patch(fullMoon)
    axes.add_patch(shade)
    moonPhase = plt.show()
    return moonPhase

# START

print('Welcome to SMAMC (the Sun and Moon Apparent Motion Calculator)!')
print('*You may need to close the figure window to view the text results. Please note if there is a message of invalidation.')
choice = input('Would you like to get the current date (1) or enter a specified date (2)? Please enter 1 or 2:\n>>')
while choice != '1' and choice != '2':
    choice = input('Please enter 1 or 2 only:\n>>')

while choice == '1':
    try:
        today = str(datetime.date.today())
        month = int(today[5:7])
        date = int(today[8:])
        year = int(today[0:4])
        latitude = float(input('Please enter the latitude (e.g. -40.73):\n>>'))
        filename = input('Please enter the pathname where you can save your text results (CSV file only):\n>>')
        # +-66.56° is the arctic (antarctic) circle latitude, so the area is around polar day (night) when entering +-66.56° to +-90° and Jun (Dec) 19 to 25.
        if 66.56 <= latitude <= 90 and month == 6 and 19 <= date <= 25:
            result1 = 'The latitude and date show that the area is around the polar day.'
        elif 66.56 <= latitude <= 90 and month == 12 and 19 <= date <= 25:
            result1 = 'The latitude and date show that the area is around the polar night.'
        elif -90 <= latitude <= -66.56 and month == 6 and 19 <= date <= 25:
            result1 = 'The latitude and date show that the area is around the polar night.'
        elif -90 <= latitude <= -66.56 and month == 12 and 19 <= date <= 25:
            result1 = 'The latitude and date show that the area is around the polar day.'
        else:
            result1 = sunApparentMotionCalculator(month, date, year, latitude)
        result2 = moonApparentMotionCalculator(month, date, year, latitude)
        result3 = moonPhase(month, date, year)
        print(result1)
        print(result2)
        print(result3)
        try:
            with open(filename, 'a', newline = '') as file:
                writer = csv.writer(file)
                sunFields = result1.split('\n')
                sunValues = [line.split(':\t')[-1].strip() for line in sunFields]
                moonFields = result2.split('\n')
                moonValues = [line.split(':\t')[-1].strip() for line in moonFields]
                if file.tell() == 0:
                    header = [line.split(':')[0].strip() for line in sunFields + moonFields]
                    writer.writerow(header)
                writer.writerow(sunValues + moonValues)
            print('*The results above have been written to the CSV file successfully!')
        except IsADirectoryError:
            print('***The path entered is a directory, not a file. Please enter a valid file path ending with ".csv".***')
        except PermissionError:
            print('***You do not have permission to write to this location. Please try a different directory.***')
    except ValueError:
        print('***Invalid results. Please enter a correct coordinate***')
    except FileNotFoundError:
        print('***Invalid pathname***')
    choice = input('Would you like to get the current date (1) or enter a specified date (2)? Please enter 1 or 2:\n>>')
    while choice != '1' and choice != '2':
        choice = input('Please enter 1 or 2 only:\n>>')

while choice == '2':
    try:
        month = int(input('Please enter your specified month (e.g. 6):\n>>'))
        date = int(input('Please enter your specified date (e.g. 01):\n>>'))
        year = int(input('Please enter your specified year (e.g. 2023):\n>>'))
        latitude = float(input('Please enter the latitude (e.g. -40.73):\n>>'))
        filename = input('Please enter the pathname where you can save your text results (CSV file only):\n>>')
        if 66.56 <= latitude <= 90 and month == 6 and 19 <= date <= 25:
            result1 = 'The latitude and date show that the area is around the polar day.'
        elif 66.56 <= latitude <= 90 and month == 12 and 19 <= date <= 25:
            result1 = 'The latitude and date show that the area is around the polar night.'
        elif -90 <= latitude <= -66.56 and month == 6 and 19 <= date <= 25:
            result1 = 'The latitude and date show that the area is around the polar night.'
        elif -90 <= latitude <= -66.56 and month == 12 and 19 <= date <= 25:
            result1 = 'The latitude and date show that the area is around the polar day.'
        else:
            result1 = sunApparentMotionCalculator(month, date, year, latitude)
        result2 = moonApparentMotionCalculator(month, date, year, latitude)
        result3 = moonPhase(month, date, year)
        print(result1)
        print(result2)
        print(result3)
        try:
            with open(filename, 'a', newline = '') as file:
                writer = csv.writer(file)
                sunFields = result1.split('\n')
                sunValues = [line.split(':\t')[-1].strip() for line in sunFields]
                moonFields = result2.split('\n')
                moonValues = [line.split(':\t')[-1].strip() for line in moonFields]
                if file.tell() == 0:
                    header = [line.split(':')[0].strip() for line in sunFields + moonFields]
                    writer.writerow(header)
                writer.writerow(sunValues + moonValues)
            print('*The results above have been written to the CSV file successfully!')
        except IsADirectoryError:
            print('***The path entered is a directory, not a file. Please enter a valid file path ending with ".csv".***')
        except PermissionError:
            print('***You do not have permission to write to this location. Please try a different directory.***')
    except ValueError:
        print('***Invalid results. Please enter a correct time or coordinate***')
    except IndexError:
        print('***Invalid results. Please enter a correct year***')
    except FileNotFoundError:
        print('***Invalid pathname***')
    choice = input('Would you like to get the current date (1) or enter a specified date (2)? Please enter 1 or 2:\n>>')
    while choice != '1' and choice != '2':
        choice = input('Please enter 1 or 2 only:\n>>')