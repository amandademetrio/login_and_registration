/* Creating a user table */

CREATE TABLE regusers (
  id int(11) NOT NULL AUTO_INCREMENT,
  first_name char(35) NOT NULL DEFAULT '',
  flast_name char(35) NOT NULL DEFAULT '',
  email char(255) NOT NULL DEFAULT '',
  password_hash char(255) NOT NULL,
  PRIMARY KEY (id),
  created_at datetime,
  updated_at datetime
) ENGINE=InnoDB AUTO_INCREMENT=4080 DEFAULT CHARSET=latin1;

/* Fixing last name mispelling */

ALTER TABLE regusers CHANGE flast_name last_name char(255);

/* Inserting users into table */

INSERT INTO regusers (first_name,last_name,email,password_hash,created_at,updated_at)
VALUES ("Amanda","Demetrio","amandademetrio@gmail.com","password_hashed",now(),now());