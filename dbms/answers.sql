select md.acct_number, md.join_date, me.earn_type_code, me.earn_timestamp, me.earn_value,
et.earn_type_name from member_details md JOIN member_earn me on md.acct_number = me.acct_number
JOIN earn_type et on me.earn_type_code = et.earn_type_code;


1.  select md.acct_number, md.join_date, me.earn_type_code, me.earn_timestamp, me.earn_value, et.earn_type_name from member_details md 
JOIN member_earn me on md.acct_number = me.acct_number JOIN earn_type et on me.earn_type_code = et.earn_type_code 
where me.earn_timestamp > DATE_SUB(now(), INTERVAL 10 DAY);


/*2. select distinct et.earn_type_name, et.earn_type_code as earn_type_code, me.acct_number from member_details md 
    JOIN member_earn me on md.acct_number = me.acct_number JOIN earn_type et on me.earn_type_code = et.earn_type_code;*/


    2.
     CREATE OR REPLACE VIEW EARN_FREQUENCY AS (SELECT DISTINCT *
    FROM  earn_type et
    INNER JOIN  (
        SELECT   EARN_TYPE_CODE as EARN_TYPE_CODE_DUPLICATE,
        COUNT(*) AS Count
        FROM   member_earn
        GROUP  BY earn_type_code
        ) me ON EARN_TYPE_CODE_DUPLICATE = et.earn_type_code);




       3. SELECT DISTINCT *
    FROM  earn_type et
    INNER JOIN  (
        SELECT   EARN_TYPE_CODE,
        COUNT(*) AS Count
        FROM   member_earn
        GROUP  BY earn_type_code
        ) me ON me.earn_type_code = et.earn_type_code
    ORDER BY Count DESC LIMIT 2, 1;



4. /*CREATE VIEW code_value as SELECT distinct me.earn_type_code, earn_value
    FROM  member_earn me
    INNER JOIN  (
        SELECT   earn_type_code, earn_type_name
        FROM   earn_type
        GROUP BY earn_type_code, earn_type_name
        ) et ON me.earn_type_code = et.earn_type_code
        where earn_type_name like 'TRAVEL%' order by earn_type_code;*/

        SELECT earn_type_code, AVG(earn_value) from (
    SELECT distinct me.earn_type_code, earn_value
    FROM  member_earn me
    INNER JOIN  (
        SELECT   earn_type_code, earn_type_name
        FROM   earn_type
        GROUP BY earn_type_code, earn_type_name
        ) et ON me.earn_type_code = et.earn_type_code
        where earn_type_name like 'TRAVEL%' order by earn_type_code
) code_value group by earn_type_code;


5. Select distinct * from member_earn where earn_value in (select MAX(earn_value) from member_earn);

6. SELECT * from member_details md join (select acct_number, join_date from member_details group by acct_number, join_date having count(*) > 1) md1
on md.acct_number = md1.acct_number and md.join_date = md1.join_date;
    

select * from member_details where NOT EXISTS (SELECT acct_number, count(acct_number)                       
FROM   member_details    
GROUP BY acct_number             
HAVING COUNT(acct_number) = 1);

        









        






         



/*
1. Return a list of account numbers and the associated earn details, for
members that were less than 10 days old at the time of that earn.
2. Create a view that will return all earn type names, along with a count of the
number of unique members associated with that earn.
3. Return the earn type name associated with the third highest count of
unique members.
4. Where the earn type name starts with "TRAVEL", calculate the average
earn value for each type of earn. Sort by the average earn value from
largest to smallest.
5. Return members and the earn type, where the member has an unusually
high earn for that earn type.
6. Where a member has multiple join dates, keep the oldest date, and delete the rest
*/