CREATE TABLE colleges (
    college_id INTEGER PRIMARY KEY,
    college_name TEXT NOT NULL UNIQUE,
    college_link TEXT
);

CREATE TABLE subjects (
    subject_id INTEGER PRIMARY KEY,
    subject_name TEXT NOT NULL
);

CREATE TABLE programs (
    program_id INTEGER PRIMARY KEY,
    program_name TEXT NOT NULL,
    program_link TEXT,
    score INTEGER,
    additional BOOL,
    college_id INTEGER,
    FOREIGN KEY (college_id) REFERENCES colleges(college_id)
);

CREATE TABLE subjects_for_program (
    subject_id INTEGER,
    program_id INTEGER,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
