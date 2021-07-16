-- Andrew Le, Hien Duong, Eric Furukawa
-- CS 451
-- Milestone 2
-- Update statements

-- numCheckins
UPDATE Business
SET checkincount = t1.numcheckins
FROM (SELECT business_id, Count(business_id) AS numcheckins FROM checkin GROUP BY business_id ) AS t1 
WHERE Business.business_id = t1.business_id

-- numTips
UPDATE Business
SET tipcount = t1.numTips
FROM (SELECT business_id, Count(tipdate) AS numTips FROM Tip GROUP BY business_id) AS t1 
WHERE Business.business_id = t1.business_id

-- totalLikes
UPDATE YelpUser
SET tiplikecount = t1.totalLikes
FROM (SELECT user_id, Sum(likecount) AS totalLikes FROM Tip GROUP BY user_id) AS t1 
WHERE YelpUser.user_id = t1.user_id

-- tipCount
UPDATE YelpUser
SET tipcount = t1.tipCount
FROM (SELECT user_id, Count(tipdate) AS tipCount FROM Tip GROUP BY user_id) AS t1 
WHERE YelpUser.user_id = t1.user_id