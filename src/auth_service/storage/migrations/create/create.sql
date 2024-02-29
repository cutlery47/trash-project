--NOT A FINAL VERSION--
CREATE TABLE Roles (
    id          INT NOT NULL,
    name        VARCHAR(32) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Users (
    id          INT NOT NULL,
    role_id     INT NOT NULL,
    mail        VARCHAR(128) NOT NULL,
    password    VARCHAR(128) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(role_id) REFERENCES Roles(id)
);

CREATE TABLE UserRoles (
    user_id     INT NOT NULL,
    role_id     INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(role_id) REFERENCES Roles(id)
);