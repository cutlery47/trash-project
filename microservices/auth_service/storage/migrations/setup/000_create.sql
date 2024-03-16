CREATE TABLE "Roles" (
    id          INT NOT NULL,
    name        VARCHAR(32) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE "Users" (
    id          INT NOT NULL,
    role_id     INT NOT NULL,
    email       VARCHAR(128) NOT NULL,
    password    VARCHAR(128) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(role_id) REFERENCES "Roles"(id)
);

CREATE TABLE "Permissions" (
    id          INT NOT NULL,
    permission  VARCHAR(128) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE "RolePermissions" (
    role_id     INT NOT NULL,
    perm_id     INT NOT NULL,
    FOREIGN KEY(role_id) REFERENCES "Roles"(id),
    FOREIGN KEY(perm_id) REFERENCES "Permissions"(id)
);

END;

