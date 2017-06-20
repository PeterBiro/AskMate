--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;

DROP TABLE IF EXISTS public.question;
DROP SEQUENCE IF EXISTS public.question_id_seq;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time char(16) default to_char(LOCALTIMESTAMP, 'YYYY-MM-DD HH24:MI'),
    view_number integer DEFAULT 0, 
    vote_number integer DEFAULT 0,
    title text,
    message text,
    image text,
    users_id integer
);

DROP TABLE IF EXISTS public.answer;
DROP SEQUENCE IF EXISTS public.answer_id_seq;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time char(16) default to_char(LOCALTIMESTAMP, 'YYYY-MM-DD HH24:MI'),
    vote_number integer DEFAULT 0,
    question_id integer,
    message text,
    image text,
    accepted boolean default FALSE,
    users_id integer
);

DROP TABLE IF EXISTS public.comment;
DROP SEQUENCE IF EXISTS public.comment_id_seq;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time char(16) default to_char(LOCALTIMESTAMP, 'YYYY-MM-DD HH24:MI'),
    edited_count integer DEFAULT 0,
    users_id integer
);

DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.users_id_seq;
CREATE TABLE users (
    id serial NOT NULL,
    name text NOT NULL UNIQUE,
    password text default '123456',
    rank integer default 0,
    submission_time char(16) default to_char(LOCALTIMESTAMP, 'YYYY-MM-DD HH24:MI')
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
DROP SEQUENCE IF EXISTS public.tag_id_seq;
CREATE TABLE tag (
    id serial NOT NULL,
    name text,
    color varchar
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_users_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id)
    ON DELETE CASCADE;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_users_id FOREIGN KEY (users_id) REFERENCES users(id)
    ON DELETE CASCADE;

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_users_id FOREIGN KEY (users_id) REFERENCES users(id)
    ON DELETE CASCADE;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id)
    ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id)
    ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id)
    ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_users_id FOREIGN KEY (users_id) REFERENCES users(id)
    ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id)
    ON DELETE CASCADE;


INSERT INTO users (name) VALUES ('Jeannie');
INSERT INTO users (name) VALUES ('Greg');
INSERT INTO users (name) VALUES ('Peter');
INSERT INTO users (name) VALUES ('Attila');
INSERT INTO users (name) VALUES ('Helga');
INSERT INTO users (name) VALUES ('Barna');
SELECT pg_catalog.setval('users_id_seq', 6, true);


INSERT INTO question VALUES (0, '2017-04-28 08:29', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL, 2);
INSERT INTO question VALUES (1, '2017-04-29 09:19', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'images/image1.png', 1);
INSERT INTO question VALUES (2, '2017-05-01 16:24', 4, 0, 'PostgreSQL: Difference between text and varchar (character varying)
', 'What''s the difference between the text data type and the character varying (varchar) data types?

According to the documentation: If character varying is used without length specifier, the type accepts strings of any size. The latter is a PostgreSQL extension.
and in addition, PostgreSQL provides the text type, which stores strings of any length. Although the type text is not in the SQL standard, several other SQL database management systems have it as well.
So what''s the difference?', NULL, 2);
INSERT INTO question VALUES (3, '2017-05-01 1:01', 36, 0, 'PostgreSQL digit matching regex strange behavior

', 'So I''m having this problem where a PostgreSQL regular expression doesn''t behave the same way in two different contexts - as a CONSTRAINT and with a regex_matches() function.

I want the regex to work as it does demonstrated with SELECT statements below but as a table CONSTRAINT, which for some reason it doesn''t.

Has anyone else experienced this kind of behavior or does anyone have any insight on this?

Thanks!', NULL, 1);
INSERT INTO question VALUES (4, '2017-05-01 04:34', 14, 0, 'Show tables in PostgreSQL

', 'From the psql command line interface:

\dt
Programmatically (or from the psql interface too, of course):

SELECT * FROM pg_catalog.pg_tables
The system tables live in the pg_catalog database.', NULL, 3);

SELECT pg_catalog.setval('question_id_seq', 4, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49', 4, 0, 'You need to use brackets: my_list = []', NULL, FALSE, 1);
INSERT INTO answer VALUES (2, '2017-04-27 14:42', 35, 0, 'Look it up in the Python docs', 'images/image2.jpg', FALSE, 3);
INSERT INTO answer VALUES (3, '2017-04-21 12:25', 0, 0, 'Notice how I am creating an empty array (list500steps) each time in the first for loop? Then, after creating all the steps I append that array (Which is now NOT empty) to the array of walks.', NULL, FALSE, 2);
INSERT INTO answer VALUES (4, '2017-04-25 19:05', 0, 1, 'Do you really need to use multiple versions of jQuery? Doing that normally creates more problems than it solves', NULL, FALSE, 2);
INSERT INTO answer VALUES (5, '2017-04-24 16:21', 0, 1, 'no, no, no exactly BECAUSE i have multiple versions (wordpress loads jquery and my theme loads jquery) it causes problems', NULL, FALSE, 2);
INSERT INTO answer VALUES (6, '2017-04-23 08:56', 0, 2, 'There is no difference, under the hood it''s all varlena', NULL, FALSE, 2);
INSERT INTO answer VALUES (7, '2017-04-26 02:48', 0, 3, 'varchar(5) is better, note however that you''ve already limited the length of string using check. On a side note I''m using solely text. In the quoted post you can find some benchmarks as well.', NULL, FALSE, 2);
INSERT INTO answer VALUES (8, '2017-04-22 10:19', 0, 4, 'Login as superuser: sudo -u postgres psql. You can list all databases and users by \l command, (list other commands by \?). Now if you want to see other databases you can change user/database by \c command like \c template1, \c postgres postgres and use \d, \dt or \dS to see tables/views/etc.', NULL, FALSE, 2);
SELECT pg_catalog.setval('answer_id_seq', 8, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49', 1, 2);
INSERT INTO comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55', 3, 2);
INSERT INTO comment VALUES (3, 2, NULL, 'That makes sense. Thanks a lot', '2017-05-21 08:24', 1, 2);
INSERT INTO comment VALUES (4, NULL, 8, 'Can you use the in operator?', '2017-05-24 12:15', 3, 2);
INSERT INTO comment VALUES (5, NULL, 2, 'Thanks, Captain Obvious', '2017-05-26 13:15', 3, 2);
INSERT INTO comment VALUES (6, NULL, 3, 'Yep you are right. I forgot empty lists.', '2017-05-26 15:14', 3, 2);
SELECT pg_catalog.setval('comment_id_seq', 4, true);

INSERT INTO tag VALUES (1, 'python', 'rgb(0, 128, 255)');
INSERT INTO tag VALUES (2, 'sql', 'rgb(0, 255, 64)');
INSERT INTO tag VALUES (3, 'css', 'rgb(255, 128, 0)');
INSERT INTO tag VALUES (4, 'BIOHAZARD', 'rgb(255, 255, 0)');
SELECT pg_catalog.setval('tag_id_seq', 4, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);
