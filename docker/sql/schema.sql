-- schema.sql

DROP DATABASE IF EXISTS posservice;

CREATE DATABASE posservice;

USE posservice;

GRANT SELECT, INSERT, UPDATE, DELETE ON posservice.* TO 'posservice'@'%' IDENTIFIED BY 'posservice';


CREATE TABLE dst_wallet_info (
  `id`            BIGINT      NOT NULL,
  `balance`       REAL(16,8)  NOT NULL,
  `stake`         REAL(16,8)  NOT NULL,
  `blocks`        BIGINT      NOT NULL,
  `update_at`     BIGINT      NOT NULL,
  `update_at_str` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8;

CREATE TABLE dst_transactions (
  `txid`        VARCHAR(80) NOT NULL,
  `idx`         BIGINT      NOT NULL,
  `category`    VARCHAR(20) NOT NULL,
  `amount`      REAL(16,8)  NOT NULL,
  `txtime`      BIGINT        NOT NULL,
  `txtime_str`  VARCHAR(50) NOT NULL,
  PRIMARY KEY (`txid`),
  KEY `idx_dst_transactions_txtime` (`txtime`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8;


CREATE TABLE users (
  `id`              VARCHAR(50)   NOT NULL,
  `name`            VARCHAR(50)   NOT NULL,
  `create_at`       REAL          NOT NULL,
  `create_at_time`  VARCHAR(50)   NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8;

INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('404504209241669642','dumh',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('402631387577974797','stevenwong2017','1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('401916285929127947','Parker Lee',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('396837819550662668','mako jr',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('411932460344016896','cat lmao',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('407552893806182411','lucky168',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('403478549379678211','baobao',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('403341228176965633','JWKY',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('385061500034875392','RAY',0,'1970-1-1 00:00:00');

CREATE TABLE dst_user_addr(
    `addr`              VARCHAR(50)   NOT NULL,
    `userid`            VARCHAR(50)   NOT NULL,
    `username`          VARCHAR(50)   NOT NULL,
    PRIMARY KEY (`addr`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8;

INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('fMZictACJc9dKhrMxCKRMkWNpq8Ni2ZBx8','404504209241669642','dumh');
-- 15.00
INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('F9Kb7kzVa8ormWWJMwoyvpBZmG5W1LqUrs','404504209241669642','dumh');
-- 2.00
INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('FCEj57L3DkVP2N8vccnZPQU6ciL4m3QrPZ','404504209241669642','dumh');
-- 10.00
INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('FLC3yVLsv2pUSof4w9uZzf3ZosgYxZLiW1','404504209241669642','dumh');
-- 2.00
INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('FFgiXPCVH47KwjqZjoV9cjpo2UfoVTnKyF','404504209241669642','dumh');
-- -1366.5001
-- INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('FCd1oY8aMH2daf8YvBnSfiFafunj85RZfT','404504209241669642','dumh');
-- 11
INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('FJaCXYHBd9gnWX4ZKvBmUWPqJatqD1X9aX','404504209241669642','dumh');
-- -3.5
INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('FNMHrHqz3D5BrZLGMZ8KFDsBiaHgX2QWUC','404504209241669642','dumh');

-- 10500
INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('FB1uuSzdh5mscz8KwzgFSN4TAe6rhz2xj2','402631387577974797','stevenwong2017');
-- 39
INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('F7pLR3gWjr4NQMMPLw3ZxBDC22q2ATmQwU','402631387577974797','stevenwong2017');

INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('F6AjHLwgL6Yn2pPpL3762AZ5ZqkFuGvjZ7','401916285929127947','Parker Lee');

INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('F6tyXagtuzhitN1Sjbg1PGedzTkDuVHDDp','396837819550662668','mako jr');

INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('FKokKAbCw6cTm2iwBe3hhDBrCAv1EvaND6','411932460344016896','cat lmao');

INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('F9TiwuFvp4oF6QksWBhA6qNpYFRkY2AS3n','407552893806182411','lucky168');

INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('FQC361sfYtNrLiQjBDonzgFVTbCPMGdVKK','403478549379678211','baobao');

INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('F8BcxZresqYT3pA1NugGdJ3VRqwd6ot3rR','403341228176965633','JWKY');

INSERT INTO `dst_user_addr` (`addr`,`userid`,`username`) VALUES('FTddbJCfWY6h5VfgZ1yzjbVCXhMuq5kx6X','385061500034875392','RAY');




CREATE TABLE dst_in_out_stake (
  `id`                  VARCHAR(50)   NOT NULL,
  `txid`                VARCHAR(80)   NOT NULL,
  `userid`              VARCHAR(50)   NOT NULL,
  `username`            VARCHAR(50)   NOT NULL,
  `change_amount`       REAL(16,8)    NOT NULL,
  `stake`               REAL(16,15)   NOT NULL,
  `start_amount`        REAL(16,8)    NOT NULL,
  `pos_profit`          REAL(16,8)    NOT NULL,
  `fix_amount`          REAL(16,8)    NOT NULL,
  `fix_stake`           REAL(16,15)    NOT NULL,
  `start_balance`       REAL(16,8)    NOT NULL,
  `stage_pos_profit`    REAL(16,8)    NOT NULL,
  `txtime`              BIGINT        NOT NULL,
  `txtime_str`          VARCHAR(50)   NOT NULL,
  `pos_time`            BIGINT        NOT NULL,
  `pos_time_str`        VARCHAR(50)   NOT NULL,
  `isprocess`           BOOLEAN       NOT NULL,
  `isonchain`           BOOLEAN       NOT NULL,
  `change_username`     VARCHAR(50)   NOT NULL,
  `comment`             VARCHAR(200),
  UNIQUE KEY `idx_dst_in_out_stake_txid` (`txid`),
  PRIMARY KEY (`id`),
  KEY `idx_dst_in_out_txtime` (`txtime`),
  KEY `idx_dst_in_out_pos_time` (`pos_time`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8;

CREATE TABLE dst_daily_profit(
  `id`                VARCHAR(50)   NOT NULL,
  `userid`            VARCHAR (50)  NOT NULL,
  `username`          VARCHAR (50)  NOT NULL,
  `daily_profit`      REAL(16,8)    NOT NULL,
  `stage_pos_profit`  REAL(16,8)    NOT NULL,
  `all_pos_profit`    REAL(16,8)    NOT NULL,
  `injection`         REAL(16,8)    NOT NULL,
  `start_amount`      REAL(16,8)    NOT NULL,
  `stake`             REAL(16,15)   NOT NULL,
  `pos_time`          BIGINT        NOT NULL,
  `isdailynode`       BOOLEAN       NOT NULL,
  `dailyflag`         BIGINT        NOT NULL,
  `dailyflag_str`     VARCHAR(50)   NOT NULL,
  `profit_time`       BIGINT        NOT NULL,
  `profit_time_str`   VARCHAR(50)   NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_dst_daily_profit_time` (`profit_time`),
  KEY `idx_dst_daily_profit_dailyflag` (`dailyflag`),
  KEY `idx_dst_daily_profit_pos_time` (`pos_time`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8;

CREATE TABLE dst_staking_info(
    `txid`              VARCHAR(80) NOT NULL,
    `vin_txid`          VARCHAR(80) NOT NULL,
    `vin_vout`          BIGINT      NOT NULL,
    `vin_amount`            REAL(16,8)  NOT NULL,
    `vin_tx_time`           BIGINT      NOT NULL,
    `vin_tx_time_str`       VARCHAR(50) NOT NULL,
    `staking_time`      BIGINT      NOT NULL,
    `staking_time_str`  VARCHAR(50) NOT NULL,
    `wait_time`         BIGINT      NOT NULL,
    `wait_time_str`     VARCHAR(50) NOT NULL,
    PRIMARY KEY (`vin_txid`,`vin_vout`),
    KEY `dst_staking_info_txid` (`txid`)

)
  ENGINE=innodb
  DEFAULT CHARSET = utf8;
