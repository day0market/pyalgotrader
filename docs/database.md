# Database Configuration

VN TraderCurrently supports the following four database：  

 * [SQLite](#sqlite)（default）
 * [MySQL](#sqlmysqlpostgresql)
 * [PostgreSQL](#sqlmysqlpostgresql)
 * [MongoDB](#mongodb)
 
If you need to configure the database，Click Configuration。Then follow the desired values ​​can be filled in the respective database field corresponding to the。

---
## SQLite
You need to fill in the following fields：

| Field name            | value |
|---------           |---- |
|database.driver     | sqlite |
|database.database   | Database files（With respecttradertable of Contents） |
 
SQLiteexample of：

| Field name            | value |
|---------           |---- |
|database.driver     | sqlite |
|database.database   | database.db |


---
## SQL(MySQL,PostgreSQL)

You need to fill in the following fields：

| Field name            | value |
|---------           |---- |
|database.driver     | "mysql"or"postgresql" |
|database.host       | address |
|database.port       | port |
|database.database   | data storage name |
|database.user       | username |
|database.password   | password |
 
MySQLexample of：

| Field name            | value |
|---------           |----  |
|database.driver     | mysql |
|database.host       | localhost |
|database.port       | 3306 |
|database.database   | vnpy |
|database.user       | root |
|database.password   | .... |

> vnpyNot take the initiative to create a database to a relational database，So make sure you filled indatabase.databaseField corresponds to the database has been created  
> If you do not create a database，Please manually connect to the database and run the command：```create database <You filldatabase.database>;```   

---
## MongoDB

You need to fill in the following fields：

| Field name            | value |          Required|
|---------           |---- |  ---|
|database.driver     | "mysql"or"postgresql" | Mandatory |
|database.host       | address| Mandatory |
|database.port       | port| Mandatory |
|database.database   | data storage name| Mandatory |
|database.user       | username| Optional |
|database.password   | password| Optional |
|database.authentication_source   | [Create a database used by the user][AuthSource]| Optional |
 
MongoDBWith examples of certification：

| Field name            | value |
|---------           |----  |
|database.driver     | mongodb |
|database.host       | localhost |
|database.port       | 27017 |
|database.database   | vnpy |
|database.user       | root |
|database.password   | .... |
|database.authentication_source   | vnpy |


[AuthSource]: https://docs.mongodb.com/manual/core/security-users/#user-authentication-database