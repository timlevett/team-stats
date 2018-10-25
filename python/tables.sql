Create database testing;

CREATE TABLE If not exists `time_in_status` (
  `version` varchar(30) NOT NULL,
  `issue_type` varchar(30) NOT NULL,
  `team` int(11) NOT NULL,
  `status_name` varchar(30) NOT NULL,
  `count` int(11) NOT NULL,
  `sum` mediumtext NOT NULL,
  `max` int(11) NOT NULL,
  `median` int(11) NOT NULL,
  `std_diff` float NOT NULL,
  PRIMARY KEY (`version`,`team`,`issue_type`,`status_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE If not exists `transitions` (
  `version` varchar(30) NOT NULL,
  `team` int(11) NOT NULL,
  `issueType` varchar(30) NOT NULL,
  `tFrom` varchar(30) NOT NULL,
  `tTo` varchar(30) NOT NULL,
  `count` int(11) NOT NULL,
  `total_in_category` int(11) NOT NULL,
  PRIMARY KEY (`version`,`team`,`issueType`,`tFrom`,`tTo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists `issue_duration_in_status` (
  id int unsigned not null auto_increment primary key,
  planning_period varchar(30) not null,
  issue_id varchar(30) not null,
  issue_type varchar(30) not null,
  status_name varchar(40) not null,
  status_start timestamp DEFAULT '1970-01-01 00:00:01' not null,
  status_end timestamp DEFAULT '1970-01-01 00:00:01' not null,
  status_duration_hours int not null,
  team int not null
);