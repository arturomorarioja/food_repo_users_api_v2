DROP TABLE IF EXISTS user;

CREATE TABLE user (
    nUserID INTEGER PRIMARY KEY AUTOINCREMENT,
    cFirstName TEXT NOT NULL,
    cLastName TEXT NOT NULL,
    cEmail TEXT NOT NULL,
    cPassword TEXT NOT NULL,
    cToken TEXT,
    dTokenExpiration TEXT
);

DROP TABLE IF EXISTS user_favourites;

CREATE TABLE user_favourites (
    nUserID INTEGER NOT NULL,
    nRecipeID INTEGER NOT NULL,
    PRIMARY KEY (nUserID, nRecipeID)
);