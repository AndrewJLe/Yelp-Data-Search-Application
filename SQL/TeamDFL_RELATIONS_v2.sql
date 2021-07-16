-- Andrew Le, Hien Duong, Eric Furukawa
-- CS 451
-- Milestone 2

-- ENTITIES
CREATE TABLE YelpUser (
    user_id CHAR(22) UNIQUE,
	username VARCHAR NOT NULL,
    joindate DATE NOT NULL, 
    tipcount INTEGER DEFAULT 0,
    CHECK (tipcount>=0),
    tipLikeCount INTEGER DEFAULT 0,
    CHECK (tipLikeCount>=0),
    votecount INTEGER,
    CHECK (votecount>=0),
    fancount INTEGER,
    CHECK (fancount>=0),
    averagestars FLOAT,
    CHECK (averagestars>=0 AND averagestars<=5),
    latitude FLOAT,
    CHECK (latitude >= -90 AND latitude <= 90),
    longitude FLOAT,
    CHECK (longitude >= -180 AND longitude <= 180),
    latesttip VARCHAR, -- DELETE?
    funny INTEGER,
    CHECK (funny>=0),
    cool INTEGER,
    CHECK (cool>=0),
    useful INTEGER,
    CHECK (useful>=0),
    PRIMARY KEY (user_id)
);

-- Businesses have categories that they are in.
-- Example: ['Beauty & Spas', 'Hair Salons'].
CREATE TABLE Category(
  categoryname VARCHAR UNIQUE,
  PRIMARY KEY (categoryname)
);

-- Businesses have attributes about their business.
-- Example: attributes: [('HasTV', 'True'), ('RestaurantsDelivery', 'False'), ('Caters', 'True')].
CREATE TABLE Attribute(
    business_id CHAR(22),
    attributename VARCHAR,
    attributevalue VARCHAR NOT NULL,
    PRIMARY KEY (business_id, attributename),
    FOREIGN KEY (business_id) REFERENCES Business (business_id)
);

CREATE TABLE Business(
    business_id CHAR(22) UNIQUE,
	businessname VARCHAR NOT NULL,
    address VARCHAR,
    state CHAR(2),
    city VARCHAR,
    zipcode VARCHAR,
    latitude FLOAT,-- Composite with longitude but we flatten for this representation, Technically there are limits on lat and long
    CHECK (latitude >= -90 AND latitude <= 90),
    longitude FLOAT,
    CHECK (longitude >= -180 AND longitude <= 180),
    rating FLOAT,
    CHECK (rating>=0 AND rating<=5),
    tipcount INTEGER DEFAULT 0,
    CHECK (tipcount>=0),
    checkincount INTEGER DEFAULT 0,
    CHECK (checkincount>=0),
    categoryname VARCHAR,  -- DELETE?
    attributename VARCHAR, -- DELETE?
    is_open BOOLEAN,
    PRIMARY KEY (business_id),
    FOREIGN KEY (categoryname) REFERENCES Category (categoryname),      -- DELETE?
    FOREIGN KEY (attributename) REFERENCES Attribute (attributename)    -- DELETE?
);

-- Users can create tips for restaurants and like other tips.
-- Liking a tip increments the likeCount.
CREATE TABLE Tip(
    business_id CHAR(22),
	tipdate TIMESTAMP,
    likecount INTEGER,
    CHECK (likecount>=0),
    tiptext VARCHAR,
	user_id CHAR(22),
    PRIMARY KEY (tipdate, user_id, business_id),
    FOREIGN KEY (user_id) REFERENCES YelpUser (user_id),
    FOREIGN KEY (business_id) REFERENCES Business (business_id)
); 

-- WEAK ENTITY SET
-- A list of days a business is open and their opening-closing hours.
-- example: hours[0] = opening time, hours[1] = closing time).
-- NOTE: no relation for the identifying relationship 'isOpenDuring'.
CREATE TABLE BusinessHours(
	business_id CHAR(22),
    weekday VARCHAR,
    openingtime TIME,
    closingtime TIME,
    PRIMARY KEY (business_id, weekday),
    FOREIGN KEY (business_id) REFERENCES Business (business_id)
);

-- YelpUser Check in dates (year, month, day, time) for businesses
CREATE TABLE CheckIn(
	business_id CHAR(22),
	checkinyear CHAR(4),
    checkinmonth CHAR(2),
    checkinday CHAR(2),
    checkintime CHAR(8),
  	PRIMARY KEY (business_id, checkinyear, checkinmonth, checkinday, checkintime),
  	FOREIGN KEY (business_id) REFERENCES Business (business_id)
);


-- RELATIONS

-- Friender is friends with Friend.
-- Friender and Friend are both users.
CREATE TABLE Friendship (
    friender_id CHAR(22) NOT NULL,
    friend_id CHAR(22) NOT NULL,
    PRIMARY KEY (friender_id, friend_id),
    FOREIGN KEY (friender_id) REFERENCES YelpUser (user_id),
    FOREIGN KEY (friend_id) REFERENCES YelpUser (user_id)
);

-- Associates businesses with categories
CREATE TABLE HasCategory(
    business_id CHAR(22),
    categoryname VARCHAR,
    PRIMARY KEY (business_id, categoryname),
    FOREIGN KEY (business_id) REFERENCES Business (business_id),
    FOREIGN KEY (categoryname) REFERENCES Category (categoryname)
);