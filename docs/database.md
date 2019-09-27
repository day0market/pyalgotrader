#  database configuration 

VN Trader currently supports the following four database ：  

 * [SQLite](#sqlite)（ default ）
 * [MySQL](#sqlmysqlpostgresql)
 * [PostgreSQL](#sqlmysqlpostgresql)
 * [MongoDB](#mongodb)
 
 if you need to configure the database ， click configuration .  then follow the desired values ​​can be filled in the respective database field corresponding to the . 

---
## SQLite
 you need to fill in the following fields ：

|  field name             |  value  |
|---------           |---- |
|database.driver     | sqlite |
|database.database   |  database files （ with respect trader table of contents ） |
 
SQLite example of ：

|  field name             |  value  |
|---------           |---- |
|database.driver     | sqlite |
|database.database   | database.db |


---
## SQL(MySQL,PostgreSQL)

 you need to fill in the following fields ：

|  field name             |  value  |
|---------           |---- |
|database.driver     | "mysql" or "postgresql" |
|database.host       |  address  |
|database.port       |  port  |
|database.database   |  data storage name  |
|database.user       |  username  |
|database.password   |  password  |
 
MySQL example of ：

|  field name             |  value  |
|---------           |----  |
|database.driver     | mysql |
|database.host       | localhost |
|database.port       | 3306 |
|database.database   | vnpy |
|database.user       | root |
|database.password   | .... |

> vnpy not take the initiative to create a database to a relational database ， so make sure you filled in database.database field corresponds to the database has been created   
>  if you do not create a database ， please manually connect to the database and run the command ：```create database < you fill database.database>;```   

---
## MongoDB

 you need to fill in the following fields ：

|  field name             |  value  |           required |
|---------           |---- |  ---|
|database.driver     | "mysql" or "postgresql" |  mandatory  |
|database.host       |  address |  mandatory  |
|database.port       |  port |  mandatory  |
|database.database   |  data storage name |  mandatory  |
|database.user       |  username |  optional  |
|database.password   |  password |  optional  |
|database.authentication_source   | [ create a database used by the user ][AuthSource]|  optional  |
 
MongoDB with examples of certification ：

|  field name             |  value  |
|---------           |----  |
|database.driver     | mongodb |
|database.host       | localhost |
|database.port       | 27017 |
|database.database   | vnpy |
|database.user       | root |
|database.password   | .... |
|database.authentication_source   | vnpy |


[AuthSource]: https://docs.mongodb.com/manual/core/security-users/#user-authentication-database