INSERT INTO users (login, hashed_password) VALUES ('user1', 'pbkdf2:sha256:260000$1upAQJtGclR7mNP3$875487796bf76dc5602c6459b870b5c20f98b082d4d281cf4dbc8fb73d5ae3f4');
INSERT INTO users (login, hashed_password) VALUES ('user2', 'pbkdf2:sha256:260000$AFrzWpOKUIEjtLGX$a933866087570e44328d7ed8ee3b6e2594ecc12c06289c58a3b44333fad5c6c9');
INSERT INTO users (login, hashed_password) VALUES ('user3', 'pbkdf2:sha256:260000$AFrzWpOKUIEjtLGX$a933866087570e44328d7ed8ee3b6e2594ecc12c06289c58a3b44333fad5c6c9');
INSERT INTO users (login, hashed_password) VALUES ('user4', 'pbkdf2:sha256:260000$AFrzWpOKUIEjtLGX$a933866087570e44328d7ed8ee3b6e2594ecc12c06289c58a3b44333fad5c6c9');

INSERT INTO bookmarks (url, owner_id) VALUES ('https://test.com', 2);
INSERT INTO bookmarks (url, owner_id) VALUES ('https://test2.com', 2);
INSERT INTO bookmarks (url, owner_id) VALUES ('https://test3.com', 2);