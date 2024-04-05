INSERT INTO
    "Roles" (id, name)
VALUES
    (0, 'user'),
    (1, 'admin');

INSERT INTO
    "Permissions" (id, permission)
VALUES
    (0, 'GET SINGLE USER DATA'),
    (1, 'GET MULTIPLE USERS DATA'),
    (2, 'UPDATE ANY USER DATA'),
    (3, 'DELETE ANY USER'),
    (4, 'GET ANY USER ROLE'),
    (5, 'GET ANY USER PERMISSION'),
    (6, 'CREATE ADMIN'),
    (7, 'PROMOTE TO ADMIN');

INSERT INTO
    "RolePermissions" (role_id, perm_id)
VALUES
    (0, 0),
    (1, 0),
    (0, 1),
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5);

END;