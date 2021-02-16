-- AIP SQL statements

create table invoice 
(Company_Name VARCHAR(50),
Client_Name VARCHAR(50),
Client_Address VARCHAR(50),
SOW_Number VARCHAR(50),
Project_ID VARCHAR(50),
Invoice_Number VARCHAR(50),
Invoice_Date DATE,
Billing_Period DATE,
Developer VARCHAR(255),
Rate VARCHAR(50),
Hours INT,
Subtotal VARCHAR(50),
Balance_Due VARCHAR(50),
Bank_Account_Number INT,
Bank_Name VARCHAR(50));

create table timesheet 
(Company_Name VARCHAR(50),
SOW_Number VARCHAR(50),
Project_ID VARCHAR(50),
Invoice_Number VARCHAR(50),
Invoice_Date DATE,
Billing_Period DATE,
Developer VARCHAR(255),
Rate VARCHAR(50),
Hours INT,
Bank_Account_Number INT,
Bank_Name VARCHAR(50));

insert into timesheet (Company_Name, SOW_Number, Project_ID, Invoice_Number, Invoice_Date, Billing_Period, Developer, Rate, Hours, Bank_Account_Number, Bank_name)
values ('Vsquare Systems', '001', '002', '030', '2020-01-31', '2020-01-31', 'Developer1', '$185', 160, 000000001, 'Payment Bank');

insert into timesheet (Company_Name, SOW_Number, Project_ID, Invoice_Number, Invoice_Date, Billing_Period, Developer, Rate, Hours, Bank_Account_Number, Bank_name)
values ('Vsquare Systems', '001', '002', '030', '2020-01-31', '2020-01-31', 'Developer2', '$150', 152, 000000001, 'Payment Bank');

insert into timesheet (Company_Name, SOW_Number, Project_ID, Invoice_Number, Invoice_Date, Billing_Period, Developer, Rate, Hours, Bank_Account_Number, Bank_name)
values ('Vsquare Systems', '001', '002', '030', '2020-01-31', '2020-01-31', 'Developer3', '$140', 168, 000000001, 'Payment Bank');
