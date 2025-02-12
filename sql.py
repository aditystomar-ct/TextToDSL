import sqlite3

# Connect to SQLite
connection = sqlite3.connect("MovieDb.db")

# Create a cursor object
cursor = connection.cursor()

# Create table queries
# Create table queries
actor_table = """
CREATE TABLE IF NOT EXISTS ACTOR (
    ACTID INTEGER PRIMARY KEY,
    ACTNAME VARCHAR(20),
    ACTGENDER CHAR(1)
);
"""

director_table = """
CREATE TABLE IF NOT EXISTS DIRECTOR (
    DIRID INTEGER PRIMARY KEY,
    DIRNAME VARCHAR(20),
    DIRPHONE INTEGER
);
"""

movies_table = """
CREATE TABLE IF NOT EXISTS MOVIES (
    MOVID INTEGER PRIMARY KEY,
    MOVTITLE VARCHAR(25),
    MOVYEAR INTEGER,
    MOVLANG VARCHAR(12),
    DIRID INTEGER,
    FOREIGN KEY (DIRID) REFERENCES DIRECTOR(DIRID)
);
"""

moviecast_table = """
CREATE TABLE IF NOT EXISTS MOVIECAST (
    ACTID INTEGER,
    MOVID INTEGER,
    ROLE VARCHAR(10),
    PRIMARY KEY (ACTID, MOVID),
    FOREIGN KEY (ACTID) REFERENCES ACTOR(ACTID),
    FOREIGN KEY (MOVID) REFERENCES MOVIES(MOVID)
);
"""

rating_table = """
CREATE TABLE IF NOT EXISTS RATING (
    MOVID INTEGER PRIMARY KEY,
    REVSTARS VARCHAR(25),
    FOREIGN KEY (MOVID) REFERENCES MOVIES(MOVID)
);
"""

# Execute table creation
tables = [actor_table, director_table, movies_table, moviecast_table, rating_table]
for table in tables:
    cursor.execute(table)

# Insert 50 records into ACTOR table
actors = [
    (301, "ANUSHKA", "F"), (302, "PRABHAS", "M"), (303, "PUNITH", "M"), (304, "SUDEEP", "M"),
    (305, "RAVI", "M"), (306, "VIJAY", "M"), (307, "DEEPIKA", "F"), (308, "ALIA", "F"),
    (309, "SRK", "M"), (310, "SALMAN", "M"), (311, "AAMIR", "M"), (312, "HRITHIK", "M"),
    (313, "KATRINA", "F"), (314, "PRIYANKA", "F"), (315, "KAJOL", "F"), (316, "SAIF", "M"),
    (317, "JOHN", "M"), (318, "EMRAAN", "M"), (319, "AKSHAY", "M"), (320, "SUNNY", "M"),
    (321, "NANA", "M"), (322, "ANIL", "M"), (323, "VARUN", "M"), (324, "SIDDHARTH", "M"),
    (325, "TAPSEE", "F"), (326, "SONAKSHI", "F"), (327, "KRITI", "F"), (328, "JACQUELINE", "F"),
    (329, "DIA", "F"), (330, "KAREENA", "F"), (331, "MADHURI", "F"), (332, "REKHA", "F"),
    (333, "HEMANT", "M"), (334, "BIPASHA", "F"), (335, "NEHA", "F"), (336, "TARA", "F"),
    (337, "ARJUN", "M"), (338, "ADITYA", "M"), (339, "RANBIR", "M"), (340, "RANVEER", "M"),
    (341, "VICKY", "M"), (342, "RAJKUMMAR", "M"), (343, "AYUSHMANN", "M"), (344, "PAWAN", "M"),
    (345, "MAHESH", "M"), (346, "NTR", "M"), (347, "RAM", "M"), (348, "ALLU", "M"),
    (349, "YASH", "M"), (350, "DULQUER", "M")
]
cursor.executemany("INSERT INTO ACTOR VALUES (?, ?, ?)", actors)

# Insert 50 records into DIRECTOR table
directors = [
    (60, "RAJAMOULI", 9191919191), (61, "HITCHCOCK", 818181818), (62, "FARAN", 7171717171),
    (63, "SPIELBERG", 6161616161), (64, "CHRISTOPHER", 5151515151), (65, "JAMES", 4141414141),
    (66, "RIDLEY", 3131313131), (67, "QUENTIN", 2121212121), (68, "MARTIN", 1111111111),
    (69, "KUBRICK", 9999999999), (70, "COEN", 8888888888), (71, "DEL TORO", 7777777777),
    (72, "CAMERON", 6666666666), (73, "WES", 5555555555), (74, "SNYDER", 4444444444),
    (75, "TARANTINO", 3333333333), (76, "SPIKE", 2222222222), (77, "NOLAN", 1111222233),
    (78, "DE PALMA", 9988776655), (79, "BURTON", 8877665544)
]
cursor.executemany("INSERT INTO DIRECTOR VALUES (?, ?, ?)", directors)

# Insert 50 hardcoded records into MOVIES table
movies = [
    (1001, "BAHUBALI-2", 2017, "TELUGU", 60), (1002, "BAHUBALI-1", 2015, "TELUGU", 60),
    (1003, "AKASH", 2008, "KANNADA", 61), (1004, "WAR HORSE", 2011, "ENGLISH", 63),
    (1005, "TITANIC", 1997, "ENGLISH", 72), (1006, "INCEPTION", 2010, "ENGLISH", 77),
    (1007, "DHOOM", 2004, "HINDI", 78), (1008, "GHAJINI", 2008, "HINDI", 77),
    (1009, "AVATAR", 2009, "ENGLISH", 72), (1010, "INTERSTELLAR", 2014, "ENGLISH", 77),
    (1011, "THE DARK KNIGHT", 2008, "ENGLISH", 77), (1012, "GLADIATOR", 2000, "ENGLISH", 66),
    (1013, "JOKER", 2019, "ENGLISH", 75), (1014, "LAGAAN", 2001, "HINDI", 77),
    (1015, "FIGHT CLUB", 1999, "ENGLISH", 78), (1016, "THE GODFATHER", 1972, "ENGLISH", 68),
    (1017, "THE MATRIX", 1999, "ENGLISH", 69), (1018, "JOHN WICK", 2014, "ENGLISH", 70),
    (1019, "BLACK PANTHER", 2018, "ENGLISH", 71), (1020, "MISSION IMPOSSIBLE", 1996, "ENGLISH", 72),
    (1021, "KGF CHAPTER-1", 2018, "KANNADA", 78), (1022, "KGF CHAPTER-2", 2022, "KANNADA", 78),
    (1023, "ROCKY", 1976, "ENGLISH", 79), (1024, "SPIDER-MAN", 2002, "ENGLISH", 65),
    (1025, "WOLVERINE", 2013, "ENGLISH", 66), (1026, "X-MEN", 2000, "ENGLISH", 67),
    (1027, "FAST & FURIOUS", 2001, "ENGLISH", 68), (1028, "JURASSIC PARK", 1993, "ENGLISH", 69),
    (1029, "THE AVENGERS", 2012, "ENGLISH", 70), (1030, "SHAWSHANK REDEMPTION", 1994, "ENGLISH", 71),
    (1031, "HARRY POTTER", 2001, "ENGLISH", 72), (1032, "STAR WARS", 1977, "ENGLISH", 73),
    (1033, "DEADPOOL", 2016, "ENGLISH", 74), (1034, "DOCTOR STRANGE", 2016, "ENGLISH", 75),
    (1035, "CAPTAIN MARVEL", 2019, "ENGLISH", 76), (1036, "BLACK WIDOW", 2021, "ENGLISH", 77),
    (1037, "IRON MAN", 2008, "ENGLISH", 78), (1038, "THOR", 2011, "ENGLISH", 79),
    (1039, "HULK", 2003, "ENGLISH", 60), (1040, "SUPERMAN", 1978, "ENGLISH", 61),
    (1041, "LOGAN", 2017, "ENGLISH", 62), (1042, "THE BATMAN", 2022, "ENGLISH", 63),
    (1043, "MAN OF STEEL", 2013, "ENGLISH", 64), (1044, "JUSTICE LEAGUE", 2017, "ENGLISH", 65),
    (1045, "WONDER WOMAN", 2017, "ENGLISH", 66), (1046, "THE FLASH", 2023, "ENGLISH", 67),
    (1047, "AQUAMAN", 2018, "ENGLISH", 68), (1048, "SHANG-CHI", 2021, "ENGLISH", 69),
    (1049, "ETERNALS", 2021, "ENGLISH", 70), (1050, "MORBIUS", 2022, "ENGLISH", 71)
]
cursor.executemany("INSERT INTO MOVIES VALUES (?, ?, ?, ?, ?)", movies)

# Insert 50 hardcoded records into MOVIECAST table
moviecast = [
    (301, 1001, "HERO"), (302, 1002, "HEROINE"), (303, 1003, "VILLAIN"), (304, 1004, "HERO"),
    (305, 1005, "SUPPORT"), (306, 1006, "HERO"), (307, 1007, "HEROINE"), (308, 1008, "VILLAIN"),
    (309, 1009, "HERO"), (310, 1010, "HERO"), (311, 1011, "HERO"), (312, 1012, "SUPPORT"),
    (313, 1013, "HEROINE"), (314, 1014, "HERO"), (315, 1015, "SUPPORT"), (316, 1016, "VILLAIN"),
    (317, 1017, "HERO"), (318, 1018, "HERO"), (319, 1019, "HERO"), (320, 1020, "HEROINE"),
    (321, 1021, "HERO"), (322, 1022, "HERO"), (323, 1023, "SUPPORT"), (324, 1024, "VILLAIN"),
    (325, 1025, "HEROINE"), (326, 1026, "HERO"), (327, 1027, "HERO"), (328, 1028, "HERO"),
    (329, 1029, "HEROINE"), (330, 1030, "VILLAIN"), (331, 1031, "HERO"), (332, 1032, "HERO"),
    (333, 1033, "HEROINE"), (334, 1034, "SUPPORT"), (335, 1035, "HERO"), (336, 1036, "HERO"),
    (337, 1037, "VILLAIN"), (338, 1038, "HERO"), (339, 1039, "HERO"), (340, 1040, "HEROINE"),
    (341, 1041, "SUPPORT"), (342, 1042, "HERO"), (343, 1043, "HERO"), (344, 1044, "VILLAIN"),
    (345, 1045, "HERO"), (346, 1046, "SUPPORT"), (347, 1047, "HERO"), (348, 1048, "HERO"),
    (349, 1049, "HERO"), (350, 1050, "HEROINE")
]
cursor.executemany("INSERT INTO MOVIECAST VALUES (?, ?, ?)", moviecast)

# Insert 50 hardcoded records into RATING table
ratings = [
    (1001, "4"), (1002, "5"), (1003, "3"), (1004, "4"), (1005, "5"), (1006, "4"), (1007, "3"),
    (1008, "5"), (1009, "2"), (1010, "5"), (1011, "4"), (1012, "5"), (1013, "3"), (1014, "4"),
    (1015, "5"), (1016, "4"), (1017, "3"), (1018, "5"), (1019, "2"), (1020, "5")
]
cursor.executemany("INSERT INTO RATING VALUES (?, ?)", ratings)

# Display all the records from a table (change "STUDENT" to an actual table name, like ACTOR)
print("The inserted records are:")
# data = cursor.execute('SELECT * FROM ACTOR')  # Change to relevant table like ACTOR, DIRECTOR, etc.
# for row in data:
#     print(row)

# Commit changes and close the connection
connection.commit()
connection.close()