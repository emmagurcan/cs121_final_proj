CREATE USER 'vballadm'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'vballclt'@'localhost' IDENTIFIED BY 'clientpw';
GRANT ALL PRIVILEGES ON volleyball.* TO 'vballadm'@'localhost';
GRANT SELECT ON volleyball.* TO 'vballclt'@'localhost';
FLUSH PRIVILEGES;