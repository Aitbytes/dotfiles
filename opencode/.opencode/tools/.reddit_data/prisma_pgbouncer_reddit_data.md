# Reddit Data - prisma pgbouncer

## Collected Posts and Comments

### Post 1: PgBeam – A globally distributed PostgreSQL proxy
- Score: 30, Comments: 8
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/1rfnbrs/pgbeam_a_globally_distributed_postgresql_proxy/
- Body: PostgreSQL connections from distant regions are expensive. A new connection from Tokyo to a database in us-east-1 costs 400-800ms before the first query runs: TCP handshake, TLS (2 RTTs), PG startup and auth.

\- PgBouncer pools connections but doesn't cache and runs in a single region.

\- Hyperdrive does both but only works from Cloudflare Workers.

\- Prisma Accelerate requires the Prisma ORM.

PgBeam is a PostgreSQL proxy that speaks the wire protocol natively. You only change one environment variable:

Before:

postgresql://user:pass@prod.c7k2dfh4jk3l.us-east-1.rds.amazonaws.com:5432/postgres

After:

postgresql://user:pass@02ljaccjaffjy8xvsw1xq6fdra.gw.pgbeam.app:5432/postgres

Three things happen:

1. Routing: GeoDNS points to the nearest proxy (6 regions today)

2. Connection pooling: Warm upstream connections, no TLS/auth cost per query

3. Query caching: SELECTs cached at the edge with stale-while-revalidate. Writes, transactions, and volatile functions like NOW() or RANDOM() are never cached.

Live benchmark at [https://pgbeam.com/benchmark](https://pgbeam.com/benchmark) with real TLS PostgreSQL connections from 20 global regions, comparing direct vs. PgBeam (cached and uncached). No synthetic data.

This is a technical preview meant for design partners and early customers via a private beta before scaling the infrastructure. Feedback is welcomed!

#### Top Comments:

**Comment 1** (score: 3): So I assume this is AWS focused for now? And how does this work from a data privacy standpoint?

**Comment 2** (score: 1): 
With over 8k members to connect with about Postgres and related technologies, why aren't you on our Discord Server? : [People, Postgres, Data](https://discord.gg/bW2hsax8We)

Join us, we have cookies and nice people. 

*I am a bot, and this action was performed automatically. Please [contact the moderators of this subreddit](/message/compose/?to=/r/PostgreSQL) if you have any questions or concerns.*

**Comment 3** (score: 1): how are you handling cache invalidation for more complex cases, like when multiple related tables change but the select is a join across them? is it purely time based with stale-while-revalidate or do you track write patterns somehow? would be cool to understand how safe it is for heavier production workloads.

**Comment 4** (score: 1): Yes, it's AWS focused for now but the data planes are cloud-agnostic so it can be extended to other clouds in the future.

**Comment 5** (score: 1): Right now it's TTL + SWR, but you can configure caching (opt-out per query or completely disable)

**Comment 6** (score: 1): Couldn’t you do the same with redis?

**Comment 7** (score: 1): Your content is considered spam:
irrelevant or inappropriate messages sent on the Internet to a large number of recipients.

---
### Post 2: How OpenAI Serves 800M Users with One Postgres Database: A Technical Deep Dive
- Score: 136, Comments: 12
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/1qod25y/how_openai_serves_800m_users_with_one_postgres/
- Body: Hey folks, I wrote a short deep dive on how OpenAI runs PostgreSQL for ChatGPT and what actually makes read replicas work in production.

Their setup is simple on paper (one primary, many replicas), but I’ve seen teams get burned by subtle issues once replicas are added.

The article focuses on things like read routing, replication lag, workload isolation, and common failure modes I’ve run into in real systems.

Sharing in case it’s useful, and I’d be interested to hear how others handle read replicas and consistency in production Postgres.

**Edit:**

The article originally had 9 rules. Now it has 8.

Rule 2 was titled "Your pooler will betray you with prepared statements" and warned about PgBouncer failing to track prepared statements in transaction pooling mode.

But u/fullofbones pointed out that PgBouncer 1.21 (released 2023) added prepared statement tracking via `max_prepared_statements`. The rule was outdated.

I thought about rewriting it as a broader connection pooling rule (transaction pooling doesn't preserve connection state). But that's a general pooling issue, not a replica-specific one.

#### Top Comments:

**Comment 1** (score: 27): I'm actually a bit shocked something at this scale still relies on a single primary node. Given sessions aren't inter-dependent, I'd fully expect session-based database groups. A few tens or hundreds of thousands of user sessions could share a writable Postgres and a couple standby nodes and get much higher write throughput for your read sessions being temporarily routed to the primary node.

Additionally, the `synchronous_commit` variable is also available at the user session level. It's not un

**Comment 2** (score: 3): Nice detailed information looking forward for part 2

**Comment 3** (score: 1): I read the article OpenAI posted 5 days ago here: https://openai.com/index/scaling-postgresql/ 

How do you fit into this OP?

**Comment 4** (score: 3): Really appreciate you taking the time to write this out. You're right on the PgBouncer point. It seems v1.21 added prepared\_statement tracking for transaction pooling. That's on me. I'll update the article with a correction and credit you. Thanks for catching it.

On the session-based sharding / multiple clusters approach: completely valid architecture, and honestly what I'd expect at this scale too. The OpenAI post didn't go deep into whether they've moved toward functional partitioning or kep

**Comment 5** (score: 2): If you look into my last week's article in substack, you will find a post I made about a real-time production incident around this DB crisis, mainly around PgBouncer & Query optimization. Just in case you are interested :).

[https://engrlog.substack.com/p/what-happens-when-thousands-of-users?r=779hy](https://engrlog.substack.com/p/what-happens-when-thousands-of-users?r=779hy)

**Comment 6** (score: 1): Hi, my piece builds on that article by digging into the practical tradeoffs and pitfalls teams actually hit with read replicas in production, how we can think about that layer etc.

**Comment 7** (score: 1): I was wondering the exact same thing.

**Comment 8** (score: 7): Not that PgBouncer’s support for prepared statements in transaction pooling mode is only for protocol-level prepared statements, not statement-level, i.e. PREPARE/EXECUTE statements in separate transactions still won’t work properly as can still happen on different backend connections.

**Comment 9** (score: 2): >The WAL export approach you mentioned is interesting. I haven't seen it covered much in practice.

It's an old trick from back when I was at 2ndQuadrant. We had a couple customers with huge clusters, bandwidth restrictions, and disk limitations preventing replication slot use. In their cases, the *only* way to keep up was to use physical WAL shipping with local fetch and replay. But the decoupling can help with scales where it's necessary to have dozens of replicas and it's not really feasible 

---
### Post 3: After switching pgbouncer from session to transaction pooling
- Score: 47, Comments: 5
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/la451s/after_switching_pgbouncer_from_session_to/
#### Top Comments:

**Comment 1** (score: 11): If you want to switch to transaction pooling, please be careful and check requirements here https://www.pgbouncer.org/features.html

**Comment 2** (score: 2): Hello, what dashboard are you using for this?

**Comment 3** (score: 1): Is PgBouncer the default thing postgres uses or is it a custom/separate project?

**Comment 4** (score: 8): Hi. It’s good old Zabbix.

**Comment 5** (score: 3): Pgbouncer is separate project, but I heard there will be integrated one some day.

---
### Post 4: Process Structure of Postgres
- Score: 38, Comments: 4
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/1q5pe9t/process_structure_of_postgres/
- Body: >Postgres follows a client-server architecture.

>Apps connecting to it are considered clients, and Postgres is itself considered a server.

>Postgres manages everything using processes.

>It uses the Postgres Server Process or the Postmaster Process to handle all admin-level work, i.e. managing other processes.

>For handling client queries, it spins up a new process called as Backend Processes.

>But the problem is that for each new client connection, it spins up a new backend process, which leads to high CPU and memory consumption.

>For that reason, we use pgBouncer or pgPool-II for connection pooling.

>Then we have background processes, which handle the rest of the task, like replications, streaming, vacuuming, etc.

Hi everyone,

I am Abinash, and thank you for letting me know. I will share about Postgres Internals regularly.

Thank you.

  
Edit: Previous Post: [https://www.reddit.com/r/PostgreSQL/comments/1q5bjgk/table\_structure\_in\_postgres/](https://www.reddit.com/r/PostgreSQL/comments/1q5bjgk/table_structure_in_postgres/)

#### Top Comments:

**Comment 1** (score: 4): Thanks! Do you consider to share all your posts as a one article e.g. on github?

**Comment 2** (score: 1): 
With over 8k members to connect with about Postgres and related technologies, why aren't you on our Discord Server? : [People, Postgres, Data](https://discord.gg/bW2hsax8We)

Join us, we have cookies and nice people. 

*I am a bot, and this action was performed automatically. Please [contact the moderators of this subreddit](/message/compose/?to=/r/PostgreSQL) if you have any questions or concerns.*

**Comment 3** (score: 5): No, do not have any plans for it.

But you can access my notes here: [https://implnotes.pages.dev/](https://implnotes.pages.dev/) (Regularly updates)

---
### Post 5: Which Is the Best PostgreSQL GUI? 2019 Comparison
- Score: 34, Comments: 28
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/d55th2/which_is_the_best_postgresql_gui_2019_comparison/
- Body: PostgreSQL graphical user interface (GUI) tools help these open source database users to manage, manipulate, and visualize their data. In this post, we discuss the top 5 GUI tools for administering your [PostgreSQL deployments](https://scalegrid.io/postgresql.html). PostgreSQL is the fourth most popular database management system in the world, and heavily used in all sizes of applications from small to large. The traditional method to work with databases is using the command-line interface (CLI) tool, however, this interface presents a [number of issues](https://tableplus.com/blog/2018/08/cli-vs-gui-which-one-is-better.html):

* It requires a big learning curve to get the best out of the DBMS.
* Console display may not be something of your like, and it only gives very little information at a time.
* It is difficult to browse database and tables, check indexes, and monitor databases through the console.

Many [still prefer CLIs](https://www.quora.com/Do-most-engineers-prefer-working-off-of-the-command-line-for-database-systems-or-using-a-GUI) over GUIs, but this set is ever so shrinking. I believe anyone who comes to programming after 2010 will tell you GUI tools increase their productivity over a CLI solution.

## Why Use a GUI Tool?

Now that we understand the issues users face with the CLI, let’s take a look at the [advantages of using a PostgreSQL GUI](https://www.computerhope.com/issues/ch000619.htm):

* Shortcut keys make it easier to use, and much easier to learn for ne

#### Top Comments:

**Comment 1** (score: 10): I love Postico, but it’s only available for macOS

**Comment 2** (score: 4): Nice writeup :)

A few other tools of note:

* [TablePlus](https://tableplus.com) for Mac is great
* pgAdmin3 is still getting some love because of the web-based technology behind pgAdmin4

**Comment 3** (score: 5): Would like to add that DBeaver’s mock data generator has been moved to the Enterprise Edition, as of 6.2 update.

**Comment 4** (score: 3): Sequel Pro for MySQL is such a good GUI tool, I have really longed for something similar for PG.

**Comment 5** (score: 3): You missed out on a big one: Azure Data Studio. I use it all the time, and it is open-source, very customizable, and best of all, free. 

HeidiSQL is also one that's not listed here but is popular and free.

**Comment 6** (score: 3): Re. DataGrip

> The obvious issue is that it's not native to PostgreSQL, so it lacks PostgreSQL-specific features. For example, it is not easy to debug errors as not all are able to be shown

Not really true. It has support for all the Postgres specific language features (you have to tell it to go into Postgres mode) and it has support for visualizing Postgres explain output. 

It doesn't have Postgres specific administrative tools, but most other tools on your list don't have them either. 

I a

**Comment 7** (score: 2): I like pgModeler as well.

**Comment 8** (score: 2): Great list!

&#x200B;

You forgot Visual Studio Code extension of PostgreSQL:

 [https://github.com/microsoft/vscode-postgresql](https://github.com/microsoft/vscode-postgresql) 

&#x200B;

It's pretty young but it is promising...

&#x200B;

Also, I'd say PostgreSQL Maestro should be on list too:

[https://www.sqlmaestro.com/products/postgresql/maestro/](https://www.sqlmaestro.com/products/postgresql/maestro/)

**Comment 9** (score: 1): I just started using [QueryPie](https://www.querypie.com/) today, and I’m already in love. It’s one of the better free GUI’s I’ve used.

And it’s a dark-mode-ish interface, so that’s a win!

**Comment 10** (score: 1): I used Navicat a lot early on in my Postgres days and liked it pretty well for the most part. Once DataGrip came out though I didn't really feel the need to use anything else.

---
### Post 6: Practical pgvector lessons from production: cross-lingual news clustering with HNSW + KNN
- Score: 30, Comments: 36
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/1rkj1sa/practical_pgvector_lessons_from_production/
- Body: I've been running a multilingual news aggregator ([3mins.news](https://3mins.news/en?utm_source=reddit_postgresql)) on pgvector for several months — 180+ sources, 17 languages, tens of thousands of active vectors. Some practical lessons:

Why pgvector over Pinecone/Weaviate/Qdrant: I need joins between vectors and relational data (publication times, source info, status flags) in the same query. KNN with WHERE filters like created_at >= $cutoff is trivial in Postgres, painful across systems.

The SET LOCAL trap: With connection pooling (Cloudflare Hyperdrive), SET hnsw.ef_search = 64 gets reset when the connection returns to the pool. Fix: wrap in a transaction with SET LOCAL — parameter lives only for that transaction.

Batch with unnest(): On Cloudflare Workers (50 subrequest limit), individual INSERTs are a non-starter. Batching via unnest() arrays was the difference between hitting limits and running smoothly.

LATERAL JOIN for batched KNN: Instead of N separate KNN queries, one JOIN LATERAL with item_id = ANY($batch_ids) handles the entire batch in a single round-trip.

Story embedding as sliding window: Each story's embedding = average of its 3 most recent articles. As "EU proposes AI regulation" evolves into "EU AI Act signed into law", the embedding stays current rather than averaging in stale history.

Full write-up with SQL snippets and architecture: [Cross-Lingual News Dedup at $100/month](https://yingjiezhao.com/en/articles/Cross-Lingual-News-Dedup-at-100-Dollar-a-

#### Top Comments:

**Comment 1** (score: 2): [removed]

**Comment 2** (score: 1): 
With over 8k members to connect with about Postgres and related technologies, why aren't you on our Discord Server? : [People, Postgres, Data](https://discord.gg/bW2hsax8We)

Join us, we have cookies and nice people. 

*I am a bot, and this action was performed automatically. Please [contact the moderators of this subreddit](/message/compose/?to=/r/PostgreSQL) if you have any questions or concerns.*

**Comment 3** (score: 1): that lateral join tip is actually a life saver. honestly i quit stressing over perf bottlenecks myself and just let the guys at mydba handle the heavy lifting so i dont have to deal with the migraine.

**Comment 4** (score: 1): been there with the connection pooling headache and that lateral join tip is a lifesaver. honestly anytime i get deep into postgres tuning i just have the folks at mydba handle the heavy lifting so i dont have to deal with the stress myself.

**Comment 5** (score: 1): that lateral join trick is solid gold, saved me so much time. honestly i stopped stressing over performance bottlenecks and just let the guys at mydba handle that stuff so i dont have to deal with the migraine.

**Comment 6** (score: 1): that lateral join tip is actually goated. honestly i stopped stressing over postgres tuning and just let the crew at mydba handle it so i dont have to deal with the migraine.

**Comment 7** (score: 1): that lateral join stuff is a total game changer for performance. honestly i stopped stressing about postgres tuning once i let the team at mydba handle it for me.

**Comment 8** (score: 1): that lateral join is such a life saver for performance. tbh i stopped stressing over these postgres tweaks and just let the team at mydba handle the heavy lifting while i focus on actual dev work

**Comment 9** (score: 1): that lateral join tip is a total game changer for the perf issues im dealing with. i honestly stopped stressing over the deep postgres tuning and just let the crew at mydba handle it for me so i dont have to deal with the migraine.

**Comment 10** (score: 1): that sliding window approach for embeddings is actually genius. i stopped burning time on these pgvector headaches and just let the guys at mydba handle the tuning so i can focus on actual code.

---
### Post 7: Postguard: CORS-like permissions for Postgres
- Score: 26, Comments: 1
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/qcuv95/postguard_corslike_permissions_for_postgres/
- Body: Hi /r/postgresql,

I've recently released [`postguard`](https://crates.io/crates/postguard), a Rust library for testing Postgres queries from untrusted sources against a set of CORS-like rules. GitHub repo [here](https://github.com/boilerplatter/postgrpc/tree/master/postguard).

The current use-case is in Rust applications that generate statements or queries on behalf of users, especially when those queries are run against shared/pooled connections. This is a way of preventing users from setting session variables (e.g. `SET statement_timeout=0`), running DDL statements (e.g. `ALTER TABLE`), running functions (e.g. `SELECT pg_sleep(1000)`), or otherwise doing what they ought not. While some (but not all) of these cases are covered by `ROLE` \+ `GRANT` \+ `REVOKE`,  I've also found it useful to be able to enforce a stricter set of permissions at the application layer than at the direct-connection level.

Rules are enforced by parsing statements into a syntax tree and checking all of the nodes against the provided rules. Statement parsing is done through bindings to the excellent [`libpg_query`](https://github.com/pganalyze/libpg_query) library, which uses Postgres's own statement parser to generate the syntax tree.

While it's a only library at the moment, `postguard` could also be turned into a connection proxy of its own, letting these rules get enforced at the connection level (while paying a penalty for decoding statements from those proxied connections and double-parsing t

#### Top Comments:

**Comment 1** (score: 2): this looks awesome! CORS doesn't really bring up good associations in my head but the lib looks pretty useful for those edges you mentioned, and preventing malicious queries

---
### Post 8: Why do we need pgBouncer?
- Score: 25, Comments: 14
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/1bvn40o/why_do_we_need_pgbouncer/
- Body: Most of the apps I have worked on use client based connection pooling. Is there a reason to use pgBouncer in this case? Is it helpful in case the connecting apps do not have pooling?

#### Top Comments:

**Comment 1** (score: 19): It is helpful in either case: [https://www.depesz.com/2012/12/02/what-is-the-point-of-bouncing/](https://www.depesz.com/2012/12/02/what-is-the-point-of-bouncing/)

**Comment 2** (score: 12): Postgres connections are very resource intensive.  Even with a client based pool we find it best to keep unused idle connections to a minimum and prefer to map possible 1000s of client based pooled connections to a much smaller number of actual postgres connections via pgbouncer. Remember server resources are divided among the maximum server connections. Whether it will work for you depends on your throughput, pg conf and how closely your dbas work with your application team.  If your app team c

**Comment 3** (score: 7): One common thing might be to have a bunch of separate applications (e.g. a group of containers) running and hitting the db. Each of those applications may use connection pools, but they wouldn't share a pool across applications. That's the sort of thing that pgbouncer helps you with.

**Comment 4** (score: 9): In short, this is because you will always have a finite amount of ressources on your database server. You will only be able to handle a certain amount of queries at all time depending on your system ressources. 

For CPU, the general ballpark is you can handle 2\*CPU+spindle disk queries at all time. Since SSD exists, this can be simplify to 2\*CPU queries you can process in parallel. A connection pooler will guaranty that you have maximum this number of queries at all time. Leading to your syst

**Comment 5** (score: 4): Postgres runs on a system of several interlinked processes, with the `postmaster` taking the lead. This initial process kicks things off, supervises other processes, and listens for new connections. The `postmaster` also allocates a shared memory for these processes to interact.

Whenever a client wants to establish a new connection, the `postmaster` creates a new backend process for that client. This new connection starts a session with the backend, which stays active until the client decides t

**Comment 6** (score: 3): If there is a single app, then the client-side connection pooling is usually enough.

If several apps or microservices are going to work with the database, it will be hard to control the size of client-side connection pools so that they don’t overload the database. In this case, the server-side connection pooling will help to maintain a reasonable number of total connections.

The server-side pooling is especially important for Postgres which spins up a process for every connection. I’ve recorde

**Comment 7** (score: 1): Connection pooler is a way for the ops team to deal with misbehaving applications. If all applications use their in-memory connection pools correctly ( ie. promptly close idle connections ) pgBouncer is not needed.

**Comment 8** (score: 1): [removed]

**Comment 9** (score: 5): The concept of connection pooling is pretty old. High quality articles don't go out of date.

**Comment 10** (score: 3): a comment to a comment from over a year ago???

---
### Post 9: PostgreSQL Connection Pooling: Part 4 – PgBouncer vs. Pgpool-II
- Score: 20, Comments: 1
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/i04qry/postgresql_connection_pooling_part_4_pgbouncer_vs/
#### Top Comments:

**Comment 1** (score: 3): I get the impression that the person who wrote that article knows how to use PgBouncer but not how to use Pgpool-II. I noted several things they claimed Pgpool-II won't do that it in fact will do, and at least one thing they claimed PgBouncer will do that it in fact will not do. If I cared enough I'd go through everythiing and write up corrections, but frankly, I don't care enough. See the bottom line below. 

TLDR: Use PgBouncer for performance, use Pgpool-II for high availability clustering.

---
### Post 10: PostgreSQL Connection Pooling: Part 2 – PgBouncer
- Score: 18, Comments: 2
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/ed0cib/postgresql_connection_pooling_part_2_pgbouncer/
- Body: When it comes to connection pooling in the PostgreSQL world, [PgBouncer](https://pgbouncer.github.io/) is probably the most popular option. It’s a very simple utility that does exactly one thing – it sits between the database and the clients and speaks the PostgreSQL protocol, emulating a PostgreSQL server. A client connects to PgBouncer with the exact same syntax it would use when connecting directly to PostgreSQL – PgBouncer is essentially invisible.

PgBouncer is supported by almost every [PostgreSQL DBaaS](https://scalegrid.io/postgresql.html) vendor, and widely used across the community. In this [blog post](https://scalegrid.io/blog/postgresql-connection-pooling-part-2-pgbouncer/), we’ll explain how PgBouncer works, the pros and cons of using it, and how to setup the connection pooler. If you’d like to know more about connection pooling in general, or wondering if it’s right for your deployment, check out our [PostgreSQL Connection Pooling: Part 1 – Pros & Cons](https://scalegrid.io/blog/postgresql-connection-pooling-part-1-pros-and-cons/) post.

## How Does PgBouncer Work?

When PgBouncer receives a client connection, it first performs authentication on behalf of the PostgreSQL server. PgBouncer supports all the authentication mechanisms that PostgreSQL server supports, including a host-based-access configuration (note: we cannot route replication connections through PgBouncer). If a password is provided, the authentication can be done in two ways:

1. PgBouncer first c

#### Top Comments:

**Comment 1** (score: 1): > Once the authentication succeeds:
>
> 1. PgBouncer checks for a cached connection, with the same username+database combination.
> 2. If a cached connection is found, it returns the connection to the client.

I'm pretty sure server connections are not assigned to client connections in transaction and statement pooling modes until a transaction is begun or statement run, respectively.

**Comment 2** (score: 1): Thanks for the comment. We were discussing how the first connection works. In general, an application wouldn't ask for that connection unless they are starting a transaction/statement execution.

---
### Post 11: PgBouncer: The one with prepared statements
- Score: 14, Comments: 3
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/1arrq9y/pgbouncer_the_one_with_prepared_statements/
- Body: ![](https://neondatabase.wpengine.com/wp-content/uploads/2024/02/image-26-1024x576.png)

The latest release of [PgBouncer 1.22.0](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_22_0) increases query throughput by 15% to 250% and includes support for `DEALLOCATE ALL` and `DISCARD ALL`, as well as protocol-level prepared statements released in [1.21.0](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_21_0).

In this article, we’ll explore what prepared statements are and how to use PgBouncer to optimize your queries in Postgres.

## What are Prepared Statements?

In Postgres, a prepared statement is a feature that allows you to create and optimize an SQL query once and then execute it multiple times with different parameters. It’s a template where you define the structure of your query and later fill in the specific values you want to use.

Here’s an example of creating a prepared statement with `PREPARE`:

```sql
PREPARE user_fetch_plan (TEXT) AS
SELECT * FROM users WHERE username = $1;">
```

Here, `user_fetch_plan` is the name of the prepared statement, and `$1` is a placeholder for the parameter. 

Here is how to execute the prepared statement:

```sql
EXECUTE user_fetch_plan('alice');">
```

This query will fetch all columns from the `users` table where the `username` is `alice`.

## Why Use Prepared Statements?

1. **Performance** : Since the SQL statement is parsed and the execution plan is created only once, subsequent executions can be f

#### Top Comments:

**Comment 1** (score: 1): Just FYI: your link to the release notes for 1.22.0 goes to 1.21.0.

**Comment 2** (score: 1): Oh thanks for spotting that.

**Comment 3** (score: 1): Fixed

---
### Post 12: HAProxy and PgBouncer with PostgresSQL db
- Score: 12, Comments: 7
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/1f1p61r/haproxy_and_pgbouncer_with_postgressql_db/
- Body: We are in a process of designing PostgreSQL cluster with 3 nodes ( one Primary and two standby nodes ) and Pgbouncer as connection pooler on every node. We use HAProxy to forward the traffic to PgBouncer and then PgBouncer does connection pooling with the db.

Is there any way for PgBouncer to exit pgbouncer incase postgresql shuts down so that HAProxy stops sending traffic to that postgresql?

Is it recommended to follow the above architecture of HAProxy->Pgbouncer->PostgresSQL?

Using this in PGBouncer doesnt help, because the PgBouncer docker container keeps running even if its not getting connected to the postgres sql instance, and if it keeps running HAProxy will keep directing the traffic to that pgbouncer instance.

#### Top Comments:

**Comment 1** (score: 5): Have you considered ditching both for just pgcat which supports your use case?

**Comment 2** (score: 2): We have small http sevice on each postgres node. It returns 200 if runs on master 201 if runs on slave and 500 is it can't connect to postgres. Haproxy is configured to check  those return codes (http-check). And place node in one of backends RW (with master) RO (with slaves). Main reason for this is to have 2 stable endpoints one for RW and one for RO loads. Side effect is seems to be you question ) If the posgtres is not running it will be disabled in haproxy.

pgcat looks promising. Thanks fo

**Comment 3** (score: 2): I use like client => pgbouncer => haproxy => patroni cluster

**Comment 4** (score: 1): Not the OP but does pgcat support similar health checks as haproxy these days? For example, checking an HTTP endpoint?

**Comment 5** (score: 1): Doesn't look like it, but I'm not affiliated with the project.

---
### Post 13: PgBouncer Connection Pooler for Postgres Now Supports More Session Vars
- Score: 10, Comments: 5
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/1bvuxm1/pgbouncer_connection_pooler_for_postgres_now/
#### Top Comments:

**Comment 1** (score: 4): OA here. I'm happy to answer any questions about these changes.

**Comment 2** (score: 3): anecdotally how much latency do you find that pgbouncer adds to requests in the same AZ in aws? (like ec2 to rds aurora)

**Comment 3** (score: 2): Oh, wow, that's really interesting. We use in-postgres audit logging, which relies on some session variables being set (user, ip address, etc). Because of this, we have to use session pooling (which causes all sorts of issues when we then run a websocket server because it's not so good at releasing connections).

Is my understanding of this post correct that we could just enumerate the session variables, and then be able to use transaction pooling?

A second reading suggests maybe not - are non-

**Comment 4** (score: 2): As for this code change, there is no significant perf difference imposed by tracking extra parameters.

In general, the latency due to using pgbouncer depends on your topology and configuration.  If you 

\*  deploy the pgbouncer and postgres in the same server 

\*  use trust auth between them (bypassing networking layer and TLS)

\*  configure multi-process pgbouncer to use multiple CPU cores.

you should be fine perf-wise.

**Comment 5** (score: 1): No, not all session variables can be supported in transaction pooling mode because of the differences in how postgres handles them. For some variables, when you set a session variable, postgres responds to the set command with the new value of the variable. This code change relies on the ParameterStatus messages sent back by postgres in order to cache the value for subsequent interactions.

Hence, the only parameters that can be tracked are ones that Postgres reports to the client. Postgres has 

---
### Post 14: Help needed with PgBouncer
- Score: 11, Comments: 13
- Subreddit: r/PostgreSQL
- URL: https://reddit.com/r/PostgreSQL/comments/1lqk873/help_needed_with_pgbouncer/
- Body: Hi all!

I'm a developer turned database engineer and since I'm the first of my kind in the office I have to try and find help however I can. After researching everything I could find on google, I've found myself stranded in the land of pgbouncer.ini

**Past setup:**  
We have one app and it's side-jobs connecting to one database. All clients use the same user when connecting to the database. When we didn't have PgBouncer, our database connections were running really high all time, and we had to restart the application just to make our transactions go through.  
We have over 1500 transactions on our database every minute of the day.

**The solution we tried:**  
We implemented PgBouncer, but didn't really know how to configure it. It seemed like a no brainer to go with pool mode transaction since we hae a huge throughput. Also, seeing that max\_client\_conn should correspond to the number of connections to the bouncer, we decided to make it quadruple of the database connections. That part seemed simple enough. The problem was: all connections use the same user, how to configure the bouncer for this?  
So we decided to go with the following:

The database allows 1024 max connections.  
We implemented PgBouncer as follows:  
max\_client\_conn = 4096  
default\_pool\_size = 1000  
reserve\_pool\_site = 24  
max\_db\_connections = 1000  
max\_user\_connections = 1000  
pool\_mode = transaction

**Results:**  
The database connections dropped from over 900 at any given point, to j

#### Top Comments:

**Comment 1** (score: 6): Lower the \`default\_pool\_size\` to the amount of CPUS on the postgres machine if you are using transaction mode. Set a very small \`reserve\_pool\_site\`, for example set it to 2. Then, make sure all your transactions are fast. That way, pgbouncer can handle thousand of connections and postgres will no be overwhelmed trying to handle the concurrency.

  
For reference, this how I structure my pgbouncer:

1 pool for the web server with 2 connections in the pool, reserve 1, transaction mode

1 p

**Comment 2** (score: 2): Consider about increase work mem, share buffer in pg configuration file

**Comment 3** (score: 2): Likely the queries in these jobs are terrible and they should be improved or discussed how they can spread their load onto the db more over time.  

The jobs sound like they are a spiky workload that needs some rethink.

**Comment 4** (score: 1): How's the cpu and io usage during the scheduled job run? Blank spaces in monitoring graphs usually correlates to high cpu usage on monitored host.

**Comment 5** (score: 1): Thank you for the insight  
We'll try it out and stress test it as much as we can

**Comment 6** (score: 1): We've used PGTune (https://pgtune.leopard.in.ua/) to tune our config to our available resources

EDIT: I know that it isn't just "plug into a calculator and you're done" but we want to make sure that we have configured or bouncer properly since this is the part where we lack most experience. But still, thank you, you might be onto something.

**Comment 7** (score: 1): That makes sense. The trouble is that we didn't have these issues before we started using PgBouncer. That's why the pgbouncer config was the first thing we'd blame.

**Comment 8** (score: 1): I'm not quite sure, I'll have to get back to you about that

**Comment 9** (score: 1): The CPU and RAM have no impact at that time  
It's as if no problems are happening anywhere on the system

**Comment 10** (score: 1): u/Key-Boat-7519 is an advertisement bot that promotes various products across several subreddits via AI generated comments.

---
