-- schema.sql

DROP DATABASE IF EXISTS posservice;

CREATE DATABASE posservice;

USE posservice;

GRANT SELECT, INSERT, UPDATE, DELETE ON posservice.* TO ''@'%' IDENTIFIED BY 'posservice';


CREATE TABLE dst_wallet_balance (
  `id`            BIGINT      NOT NULL,
  `balance`       REAL(16,8)  NOT NULL,
  `stake`         REAL(16,8)  NOT NULL,
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
  `create_at`      REAL          NOT NULL,
  `create_at_time` VARCHAR(50)   NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8;

INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('404504209241669642','dumh',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('402631387577974797','stevenwong2017',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('401916285929127947','Parker Lee',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('396837819550662668','mako jr',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('411932460344016896','cat lmao',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('407552893806182411','lucky168',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('403478549379678211','baobao',0,'1970-1-1 00:00:00');
INSERT INTO `users` (`id`,`name`,`create_at`,`create_at_time`) VALUES ('403341228176965633','JWKY',0,'1970-1-1 00:00:00');

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
  UNIQUE KEY `idx_dst_daily_profit_id` (`id`),
  KEY `idx_dst_daily_profit_time` (`profit_time`),
  KEY `idx_dst_daily_profit_dailyflag` (`dailyflag`),
  KEY `idx_dst_daily_profit_pos_time` (`pos_time`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8;

