# Andrew Le, Hien Duong, Eric Furukawa
# CptS 451 - Spring 2021
# Team DFL

# https://www.psycopg.org/docs/usage.html#query-parameters

#  if psycopg2 is not installed, install it using pip installer :  pip install psycopg2  (or pip3 install psycopg2)
import json
import psycopg2


def cleanStr4SQL(s):
    return s.replace("'", "`").replace("\n", " ")


def int2BoolStr(value):
    if value == 0:
        return 'False'
    else:
        return 'True'


def handleRecursiveData(returnList, dataDict):
    for key, value in dataDict.items():
        if isinstance(value, dict) == True:
            returnList = handleRecursiveData(returnList, value)
        else:
            returnList.append((key, value))
    return returnList


def insert2BusinessTable():
    # reading the JSON file
    with open('./yelp_business.JSON', 'r') as f:  # TODO: update path for the input file
        # outfile =  open('./yelp_business_out.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        # connect to yelpdb database on postgres server using psycopg2
        try:
            # TODO: update the database name, username, and password
            conn = psycopg2.connect(
                "dbname='yelpdbfinal' user='postgres' host='localhost' password='NA'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            try:
                cur.execute("INSERT INTO Business(business_id, businessname, address, state, city, zipcode, latitude, longitude, rating, checkincount, tipcount, is_open)"  # attributename, categoryname?
                            + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (data['business_id'], cleanStr4SQL(data["name"]), cleanStr4SQL(data["address"]), data["state"], data["city"], data["postal_code"], data["latitude"], data["longitude"], data["stars"], 0, 0, [False, True][data["is_open"]]))
            except Exception as e:
                print("Insert to business TABLE failed!", e)
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # sql_str = ("INSERT INTO businessTable (business_id, name, address, state, city, zipcode, latitude, longitude, stars, numCheckins, numTips, is_open)"
            #           + " VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, {10}, {11})").format(data['business_id'],cleanStr4SQL(data["name"]), cleanStr4SQL(data["address"]), data["state"], data["city"], data["postal_code"], data["latitude"], data["longitude"], data["stars"], 0 , 0 , [False,True][data["is_open"]] )
            # outfile.write(sql_str+'\n')

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    # outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


def insert2YelpUserTable():
    # reading the JSON file
    with open('./yelp_user.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # connect to yelpdb database on postgres server using psycopg2
        try:
            # TODO: update the database name, username, and password
            conn = psycopg2.connect(
                "dbname='yelpdbfinal' user='postgres' host='localhost' password='NA'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            try:
                cur.execute("INSERT INTO YelpUser(user_id, username, joindate, tipcount, tipLikeCount, votecount, fancount, averagestars, latitude, longitude, latesttip, funny, cool, useful)"
                            + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (data['user_id'], data['name'], data['yelping_since'], data["tipcount"], 0, 0, data["fans"], data["average_stars"], 0, 0, '', data["funny"], data["cool"], data["useful"]))
            except Exception as e:
                print("Insert to YelpUser TABLE failed!", e)
            conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2FriendshipTable():
    # reading the JSON file
    with open('./yelp_user.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # connect to yelpdb database on postgres server using psycopg2
        try:
            # TODO: update the database name, username, and password
            conn = psycopg2.connect(
                "dbname='yelpdbfinal' user='postgres' host='localhost' password='NA'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            for friend in data['friends']:
                try:
                    cur.execute("INSERT INTO Friendship(friender_id, friend_id)"
                                + " VALUES (%s, %s)",
                                (data['user_id'], friend))
                except Exception as e:
                    print("Insert to Friendship Table failed!", e)
                conn.commit()
                count_line += 1

            line = f.readline()

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2AttributeTable():
    # reading the JSON file
    with open('./yelp_business.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # connect to yelpdb database on postgres server using psycopg2
        try:
            # TODO: update the database name, username, and password
            conn = psycopg2.connect(
                "dbname='yelpdbfinal' user='postgres' host='localhost' password='NA'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            attributelist = []
            attributelist = handleRecursiveData(
                attributelist, data['attributes'])
            businessid = data['business_id']
            for attributename, attributevalue in attributelist:
                try:
                    cur.execute("INSERT INTO Attribute(attributename, attributevalue, business_id)"
                                + " VALUES (%s, %s, %s)",
                                (attributename, attributevalue, businessid))
                except Exception as e:
                    print("Insert to Attribute Table failed!", e)
                conn.commit()
                count_line += 1

            line = f.readline()

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2BusinessHoursTable():
    # reading the JSON file
    with open('./yelp_business.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # connect to yelpdb database on postgres server using psycopg2
        try:
            # TODO: update the database name, username, and password
            conn = psycopg2.connect(
                "dbname='yelpdbfinal' user='postgres' host='localhost' password='NA'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            hoursdict = data['hours']
            businessid = data['business_id']
            for day, time in hoursdict.items():
                try:
                    weekday = day
                    openclose = time.split('-')
                    opentime = openclose[0]
                    closetime = openclose[1]
                    cur.execute("INSERT INTO BusinessHours(business_id, weekday, openingtime, closingtime)"
                                + " VALUES (%s, %s, %s, %s)",
                                (businessid, weekday, opentime, closetime))
                except Exception as e:
                    print("Insert to BusinessHours Table failed!", e)
                conn.commit()
                count_line += 1

            line = f.readline()

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2CategoryTable():
    # reading the JSON file
    with open('./yelp_business.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # connect to yelpdb database on postgres server using psycopg2
        try:
            # TODO: update the database name, username, and password
            conn = psycopg2.connect(
                "dbname='yelpdbfinal' user='postgres' host='localhost' password='NA'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            categories = data['categories']
            categorylist = categories.split(', ')
            for category in categorylist:
                try:
                    cur.execute("INSERT INTO Category(categoryname)"
                                + " VALUES (%s)",
                                ([category]))
                except Exception as e:
                    print("Insert to Category Table failed!", e)
                conn.commit()
                count_line += 1

            line = f.readline()

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2HasCategoryTable():
    # reading the JSON file
    with open('./yelp_business.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # connect to yelpdb database on postgres server using psycopg2
        try:
            # TODO: update the database name, username, and password
            conn = psycopg2.connect(
                "dbname='yelpdbfinal' user='postgres' host='localhost' password='NA'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            categories = data['categories']
            categorylist = categories.split(', ')
            businessid = data['business_id']
            for category in categorylist:
                try:
                    cur.execute("INSERT INTO HasCategory(business_id, categoryname)"
                                + " VALUES (%s, %s)",
                                (businessid, category))
                except Exception as e:
                    print("Insert to HasCategory Table failed!", e)
                conn.commit()
                count_line += 1

            line = f.readline()

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2TipTable():
    # reading the JSON file
    with open('./yelp_tip.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # connect to yelpdb database on postgres server using psycopg2
        try:
            # TODO: update the database name, username, and password
            conn = psycopg2.connect(
                "dbname='yelpdbfinal' user='postgres' host='localhost' password='NA'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            try:
                cur.execute("INSERT INTO Tip(business_id, tipdate, likecount, tiptext, user_id)"
                            + " VALUES (%s, %s, %s, %s, %s)",
                            (data['business_id'], data['date'], data['likes'], data['text'], data['user_id']))
            except Exception as e:
                print("Insert to Tip Table failed!", e)
            conn.commit()
            count_line += 1

            line = f.readline()

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2CheckinTable():
    # reading the JSON file
    with open('./yelp_checkin.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # connect to yelpdb database on postgres server using psycopg2
        try:
            # TODO: update the database name, username, and password
            conn = psycopg2.connect(
                "dbname='yelpdbfinal' user='postgres' host='localhost' password='NA'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            checkins = data['date']
            checkinlist = checkins.split(',')
            businessid = data['business_id']
            for date in checkinlist:
                try:
                    year = str(date[0:4])
                    month = str(date[5:7])
                    day = str(date[8:10])
                    time = str(date[11:])
                    cur.execute("INSERT INTO Checkin(business_id, checkinyear, checkinmonth, checkinday, checkintime)"
                                + " VALUES (%s, %s, %s, %s, %s)",
                                (businessid, year, month, day, time))
                except Exception as e:
                    print("Insert to Checkin Table failed!", e)
            conn.commit()
            count_line += 1

            line = f.readline()

        cur.close()
        conn.close()

    print(count_line)
    f.close()


insert2BusinessTable()
insert2YelpUserTable()
insert2FriendshipTable()
insert2AttributeTable()
insert2BusinessHoursTable()
insert2CategoryTable()
insert2HasCategoryTable()
insert2TipTable()
insert2CheckinTable()
