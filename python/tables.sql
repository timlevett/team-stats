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