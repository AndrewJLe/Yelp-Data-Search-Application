import json


def cleanStr4SQL(s):
    return s.replace("'", "`").replace("\n", " ")


def handleRecursiveData(returnList, dataDict):
    for key, value in dataDict.items():
        if isinstance(value, dict) == True:
            returnList = handleRecursiveData(returnList, value)
        else:
            returnList.append((key, value))
    return returnList


def parseBusinessData():
    # read the JSON file
    # We assume that the Yelp data files are available in the current directory. If not, you should specify the path when you "open" the function.
    with open('.//yelp_business.JSON', 'r') as f:
        outfile = open('.//business.txt', 'w', encoding="utf-8")
        line = f.readline()
        count_line = 0
        outfile.write(
            "HEADER: (business_id; name; address; state; state; city; postal_code; latitude; longitude; stars; is_open)\n")
        # read each JSON object and extract data
        while line:
            data = json.loads(line)
            outfile.write(str(count_line+1)+'- '+'business info: ')
            outfile.write(cleanStr4SQL(
                data['business_id'])+' ; ')  # business id
            outfile.write(cleanStr4SQL(data['name'])+' ; ')  # name
            outfile.write(cleanStr4SQL(data['address'])+' ; ')  # full_address
            outfile.write(cleanStr4SQL(data['state'])+' ; ')  # state
            outfile.write(cleanStr4SQL(data['city'])+' ; ')  # city
            outfile.write(cleanStr4SQL(data['postal_code']) + ' ; ')  # zipcode
            outfile.write(str(data['latitude'])+' ; ')  # latitude
            outfile.write(str(data['longitude'])+' ; ')  # longitude
            outfile.write(str(data['stars'])+' ; ')  # stars
            outfile.write(str(data['review_count'])+' ; ')  # reviewcount
            outfile.write(str(data['is_open'])+'\n')  # openstatus
            outfile.write('   categories: ')
            categories = data["categories"].split(', ')
            outfile.write(str(categories)+'\n')  # category list

            # TO-DO : write your own code to process attributes
            outfile.write('   attributes: ')
            attributes = []
            attributes = handleRecursiveData(attributes, data['attributes'])
            outfile.write(str(attributes)+'\n')

            # TO-DO : write your own code to process hours data
            hours = []
            outfile.write('   hours: ')
            for key, value in data['hours'].items():
                hours.append((key, value.split('-')))
            outfile.write(str(hours)+'\n')
            line = f.readline()
            count_line += 1
    print(count_line)
    outfile.close()
    f.close()


def parseUserData():
    with open('.//yelp_user.JSON', 'r') as f:
        outfile = open('.//user.txt', 'w', encoding="utf-8")
        line = f.readline()
        count_line = 0
        # read each JSON object and extract data
        outfile.write(
            "HEADER: (user_id; name; yelping_since; tipcount; fans; average_stars; (funny,useful,ccol))\n")
        while line:
            data = json.loads(line)
            outfile.write(str(count_line+1)+'- '+'user info: ')
            outfile.write(cleanStr4SQL(data['user_id'])+' ; ')  # user id
            outfile.write(cleanStr4SQL(data['name'])+' ; ')  # name
            # yelping since
            outfile.write(cleanStr4SQL(data['yelping_since'])+' ; ')
            outfile.write(str(data['tipcount'])+' ; ')  # tipcount
            outfile.write(str(data['fans'])+' ; ')  # fans
            outfile.write(str(data['average_stars']) + ' ; ')  # average stars
            outfile.write(
                '('+str(data['funny'])+','+str(data['useful'])+','+str(data['cool'])+')' + '\n')
            outfile.write('   friends: ')
            outfile.write(str(data['friends']) + '\n')
            line = f.readline()
            count_line += 1
    print(count_line)
    outfile.close()
    f.close()


def parseCheckinData():
    with open('.//yelp_checkin.JSON', 'r') as f:
        outfile = open('.//checkin.txt', 'w', encoding="utf-8")
        line = f.readline()
        count_line = 0
        outfile.write("HEADER: (business_id : (year month,day,time))\n")
        # read each JSON object and extract data
        while line:
            data = json.loads(line)
            outfile.write(str(count_line+1)+'- ' +
                          cleanStr4SQL(data['business_id'])+':\n')  # business id
            date = data['date'].split(',')
            for d in date:
                temp = d.split(' ')
                temp2 = temp[0].split('-')
                year = temp2[0]
                month = temp2[1]
                day = temp2[2]
                outfile.write(str((year, month, day, temp[1])))
            outfile.write('\n')

            line = f.readline()
            count_line += 1
    print(count_line)
    outfile.close()
    f.close()


def parseTipData():
    with open('.//yelp_tip.JSON', 'r') as f:
        outfile = open('.//tip.txt', 'w', encoding="utf-8")
        line = f.readline()
        count_line = 0
        outfile.write("HEADER: (business_id; date; likes; text; user_id)\n")
        # read each JSON object and extract data
        while line:
            data = json.loads(line)
            outfile.write(str(count_line+1)+'- ' +
                          cleanStr4SQL(data['business_id'])+' ; ')  # business id
            outfile.write(cleanStr4SQL(data['date'])+' ; ')
            outfile.write(str(data['likes'])+' ; ')
            outfile.write(cleanStr4SQL(data['text'])+' ; ')
            outfile.write(cleanStr4SQL(data['user_id'])+'\n')
            line = f.readline()
            count_line += 1
    print(count_line)
    outfile.close()
    f.close()


if __name__ == "__main__":
    parseBusinessData()
    parseUserData()
    parseCheckinData()
    parseTipData()
