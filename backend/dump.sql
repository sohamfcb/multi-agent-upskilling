--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4 (Debian 15.4-2.pgdg120+1)
-- Dumped by pg_dump version 15.4 (Debian 15.4-2.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: soham
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO soham;

--
-- Name: user_profiles; Type: TABLE; Schema: public; Owner: soham
--

CREATE TABLE public.user_profiles (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    highest_qualification character varying(120),
    degree character varying(120),
    institution character varying(120),
    graduation_year integer,
    years_experience integer,
    current_job_title character varying(120),
    current_company character varying(120),
    skills text[],
    career_goal_short text,
    career_goal_long text,
    resume_url text
);


ALTER TABLE public.user_profiles OWNER TO soham;

--
-- Name: users; Type: TABLE; Schema: public; Owner: soham
--

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    first_name character varying(20) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(50) NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    last_login timestamp without time zone,
    token_version integer NOT NULL,
    is_verified boolean NOT NULL
);


ALTER TABLE public.users OWNER TO soham;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: soham
--

COPY public.alembic_version (version_num) FROM stdin;
92454ca6a424
\.


--
-- Data for Name: user_profiles; Type: TABLE DATA; Schema: public; Owner: soham
--

COPY public.user_profiles (id, user_id, highest_qualification, degree, institution, graduation_year, years_experience, current_job_title, current_company, skills, career_goal_short, career_goal_long, resume_url) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: soham
--

COPY public.users (id, first_name, last_name, email, username, password, created_at, updated_at, last_login, token_version, is_verified) FROM stdin;
ec3c9912-39be-4f12-b22e-386366311dab	Soham	Mukherjee	soumyapu31@gmail.com	__.you_know_who	scrypt:32768:8:1$jGAaOWemZJstt6sO$aca2946e02fd72c7f19744c523abb0623a1848fe5a80398538773982b5bd63be1075d16b060a0292a223a53c3da31e0d4a1c718a85fd1379ed05a01377b7544c	2025-08-26 15:32:57.551647	2025-08-26 15:32:57.551647	\N	0	t
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: soham
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: users uq_users_email; Type: CONSTRAINT; Schema: public; Owner: soham
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_users_email UNIQUE (email);


--
-- Name: users uq_users_username; Type: CONSTRAINT; Schema: public; Owner: soham
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_users_username UNIQUE (username);


--
-- Name: user_profiles user_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: soham
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: soham
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: soham
--

CREATE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: soham
--

CREATE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: user_profiles user_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soham
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

