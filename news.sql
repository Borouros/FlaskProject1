CREATE TABLE News (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO News (title, summary, content)
VALUES (
    'Welcome to the Portal',
    'This is the first article.',
    'We’re excited to launch our new news platform powered by Flask and SQL!'
);
