-- @BLOCK
USE bc3wmkwevexrh8ydz7ix;

-- @BLOCK
SHOW TABLES;

-- @BLOCK
CREATE TABLE USERS (
    UserName VARCHAR(255) PRIMARY KEY,
    PWD VARCHAR(20)
);

-- @BLOCK
ALTER TABLE USERS MODIFY COLUMN PWD VARCHAR(20) NOT NULL; 

-- @BLOCK
INSERT INTO USERS(UserName, PWD) VALUES ("ferbfletcher", "12345678");

-- @BLOCK
SELECT * FROM USERS;

-- @BLOCK
CREATE TABLE PRODUCT (
    ASIN VARCHAR(15) PRIMARY KEY,
    NAME VARCHAR(255),
    Link VARCHAR(255)
);

-- @BLOCK
INSERT INTO PRODUCT VALUES (
    "B08B44K4YS",
    "Saffola Honey, 100% Pure NMR tested Honey, (1kg +200g)",
    "https://www.amazon.in/dp/B08B44K4YS"
);




-- @BLOCK
SELECT * FROM PRODUCT WHERE ASIN = "B077X87TTS";

-- @BLOCK
SELECT COUNT(ASIN) FROM PRODUCT WHERE ASIN = "B071Z8M4KX";


-- @BLOCK
CREATE TABLE FLUCTUATIONS (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ASIN VARCHAR(15),
    Date DATE,
    Price DECIMAL(65, 10)
);

-- @BLOCK
INSERT INTO FLUCTUATIONS (ASIN, Date, Price) 
VALUES (
    "B071Z8M4KX",
    "2022-01-14",
    299.0
);

-- @BLOCK
SELECT * FROM FLUCTUATIONS WHERE ASIN = "B09C6LJF3W" ORDER BY Date DESC ;

-- @BLOCK
SELECT * FROM FLUCTUATIONS;

-- @BLOCK
SELECT COUNT(*) FROM FLUCTUATIONS WHERE Date = '2022-02-02';

-- @BLOCK
SELECT * FROM FLUCTUATIONS WHERE Date = '2022-02-09';

-- @BLOCK
SELECT * FROM FLUCTUATIONS WHERE ASIN = "B00YGMM2MM" AND Date = '2022-02-01';

-- @BLOCK
SELECT * FROM FLUCTUATIONS WHERE ASIN = 'B077X87TTS' ORDER BY Date;



-- @BLOCK
-- these products are not recorded in fluctuations on '2022-01-25'
SELECT PRODUCT.ASIN, PRODUCT.Name, PRODUCT.Link FROM PRODUCT WHERE PRODUCT.ASIN != ALL(SELECT FLUCTUATIONS.ASIN FROM FLUCTUATIONS WHERE Date = '2022-02-01');

-- @BLOCK
SELECT EXISTS(SELECT * FROM USERS WHERE UserName = "perrytheplatypus" AND PWD = "12345678");

-- @BLOCK
SELECT Name, Date, Price FROM FLUCTUATIONS, PRODUCT WHERE FLUCTUATIONS.ASIN = 'B071Z8M4KX' AND FLUCTUATIONS.ASIN = PRODUCT.ASIN ORDER BY Price DESC; 

-- @BLOCK
CREATE TABLE USERSPRODUCT (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(255),
    ASIN VARCHAR(15) NOT NULL,
    FOREIGN KEY (UserName) REFERENCES USERS(UserName),
    FOREIGN KEY (ASIN) REFERENCES PRODUCT(ASIN)
);

-- @BLOCK
INSERT INTO USERSPRODUCT (UserName, ASIN)
VALUES (
    "perrytheplatypus",
    "B071Z8M4KX"
);

-- @BLOCK
SELECT EXISTS(SELECT * FROM USERSPRODUCT WHERE UserName = "perrythepatypus" AND ASIN = "B08B44K4YS");

-- @BLOCK
SELECT * FROM USERSPRODUCT;


-- @BLOCK
SELECT PRODUCT.ASIN, PRODUCT.Name FROM PRODUCT, USERSPRODUCT WHERE PRODUCT.ASIN = USERSPRODUCT.ASIN AND USERSPRODUCT.UserName = "perrytheplatypus";