--
-- PostgreSQL database dump
--

\restrict NXKoj2TyfQWxbTXhpAWoLZ8bPBc4kdZRhfHI58SEtkaWeLPFgdHvDXaA2rpeD9N

-- Dumped from database version 18.3 (Debian 18.3-1.pgdg12+1)
-- Dumped by pg_dump version 18.4 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: voltedge_db_su9j_user
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO voltedge_db_su9j_user;

--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA public;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_stat_statements IS 'track planning and execution statistics of all SQL statements executed';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: charger; Type: TABLE; Schema: public; Owner: voltedge_db_su9j_user
--

CREATE TABLE public.charger (
    id integer NOT NULL,
    location character varying(100),
    status character varying(50),
    power_kw double precision
);


ALTER TABLE public.charger OWNER TO voltedge_db_su9j_user;

--
-- Name: charger_id_seq; Type: SEQUENCE; Schema: public; Owner: voltedge_db_su9j_user
--

CREATE SEQUENCE public.charger_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.charger_id_seq OWNER TO voltedge_db_su9j_user;

--
-- Name: charger_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER SEQUENCE public.charger_id_seq OWNED BY public.charger.id;


--
-- Name: invoice; Type: TABLE; Schema: public; Owner: voltedge_db_su9j_user
--

CREATE TABLE public.invoice (
    id integer NOT NULL,
    session_id integer,
    amount double precision,
    currency character varying(10),
    status character varying(50)
);


ALTER TABLE public.invoice OWNER TO voltedge_db_su9j_user;

--
-- Name: invoice_id_seq; Type: SEQUENCE; Schema: public; Owner: voltedge_db_su9j_user
--

CREATE SEQUENCE public.invoice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.invoice_id_seq OWNER TO voltedge_db_su9j_user;

--
-- Name: invoice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER SEQUENCE public.invoice_id_seq OWNED BY public.invoice.id;


--
-- Name: session; Type: TABLE; Schema: public; Owner: voltedge_db_su9j_user
--

CREATE TABLE public.session (
    id integer NOT NULL,
    charger_id integer,
    user_id character varying(50),
    energy_kwh double precision,
    status character varying(50)
);


ALTER TABLE public.session OWNER TO voltedge_db_su9j_user;

--
-- Name: session_id_seq; Type: SEQUENCE; Schema: public; Owner: voltedge_db_su9j_user
--

CREATE SEQUENCE public.session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.session_id_seq OWNER TO voltedge_db_su9j_user;

--
-- Name: session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER SEQUENCE public.session_id_seq OWNED BY public.session.id;


--
-- Name: charger id; Type: DEFAULT; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER TABLE ONLY public.charger ALTER COLUMN id SET DEFAULT nextval('public.charger_id_seq'::regclass);


--
-- Name: invoice id; Type: DEFAULT; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER TABLE ONLY public.invoice ALTER COLUMN id SET DEFAULT nextval('public.invoice_id_seq'::regclass);


--
-- Name: session id; Type: DEFAULT; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER TABLE ONLY public.session ALTER COLUMN id SET DEFAULT nextval('public.session_id_seq'::regclass);


--
-- Data for Name: charger; Type: TABLE DATA; Schema: public; Owner: voltedge_db_su9j_user
--

COPY public.charger (id, location, status, power_kw) FROM stdin;
1	København N	available	22
2	Aarhus C	occupied	50
3	stockholm	available	101
\.


--
-- Data for Name: invoice; Type: TABLE DATA; Schema: public; Owner: voltedge_db_su9j_user
--

COPY public.invoice (id, session_id, amount, currency, status) FROM stdin;
1	1	100	dkk	Paid
\.


--
-- Data for Name: session; Type: TABLE DATA; Schema: public; Owner: voltedge_db_su9j_user
--

COPY public.session (id, charger_id, user_id, energy_kwh, status) FROM stdin;
1	1	test	101	test
2	1	test	101	test
3	1	11	15.1	Active
4	2	12	20	Active
5	3	13	8.7	Active
11	2	14	32	Completed
12	2	15	27	Completed
\.


--
-- Name: charger_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltedge_db_su9j_user
--

SELECT pg_catalog.setval('public.charger_id_seq', 3, true);


--
-- Name: invoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltedge_db_su9j_user
--

SELECT pg_catalog.setval('public.invoice_id_seq', 1, true);


--
-- Name: session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltedge_db_su9j_user
--

SELECT pg_catalog.setval('public.session_id_seq', 12, true);


--
-- Name: charger charger_pkey; Type: CONSTRAINT; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER TABLE ONLY public.charger
    ADD CONSTRAINT charger_pkey PRIMARY KEY (id);


--
-- Name: invoice invoice_pkey; Type: CONSTRAINT; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_pkey PRIMARY KEY (id);


--
-- Name: session session_pkey; Type: CONSTRAINT; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER TABLE ONLY public.session
    ADD CONSTRAINT session_pkey PRIMARY KEY (id);


--
-- Name: invoice invoice_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.session(id);


--
-- Name: session session_charger_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: voltedge_db_su9j_user
--

ALTER TABLE ONLY public.session
    ADD CONSTRAINT session_charger_id_fkey FOREIGN KEY (charger_id) REFERENCES public.charger(id);


--
-- Name: FUNCTION pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT wal_buffers_full bigint, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT parallel_workers_to_launch bigint, OUT parallel_workers_launched bigint, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON FUNCTION public.pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT wal_buffers_full bigint, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT parallel_workers_to_launch bigint, OUT parallel_workers_launched bigint, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone) TO voltedge_db_su9j_user;


--
-- Name: FUNCTION pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON FUNCTION public.pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone) TO voltedge_db_su9j_user;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO voltedge_db_su9j_user;


--
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO voltedge_db_su9j_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO voltedge_db_su9j_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO voltedge_db_su9j_user;


--
-- PostgreSQL database dump complete
--

\unrestrict NXKoj2TyfQWxbTXhpAWoLZ8bPBc4kdZRhfHI58SEtkaWeLPFgdHvDXaA2rpeD9N

