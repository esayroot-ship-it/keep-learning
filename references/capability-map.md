# Capability Map

Use this map only as a pool of candidate directions, never as a default syllabus or an interview checklist. Select the stated role's common work and indispensable basic principles under `curriculum-quality.md`; put specialised branches outside the short core course. A broad subject name does not select an entire section. Listed terms still need a practical scenario and evidence when they become core.

## Fundamentals

- output, variables, literals, operators, control flow, functions.
- types, collections, strings, dates, errors, modules, packages.
- files, JSON, CSV, command line, environment variables, HTTP basics.

## Language And Framework

- syntax, idioms, standard library, dependency management, formatting, linting.
- project structure, lifecycle, configuration, routing/components/controllers, state, middleware/plugins, ORM/data access, validation, authentication.
- testing, debugging, logging, build, release, deployment.

## Algorithms

- arrays, strings, hash maps, linked lists, stacks, queues.
- recursion, trees, heaps, graphs.
- sorting, searching, sliding window, two pointers, dynamic programming.
- complexity analysis and tradeoffs.

## Database

For ordinary application development, consider connection and statement execution; tables, common types, NULL, keys and constraints; schema changes and CRUD; joins, grouping and common subqueries; basic transaction/rollback/isolation behaviour; practical indexes and EXPLAIN; parameterised application access and common error diagnosis. Select realistic scenarios rather than teaching every listed feature.

Specialist directions include B+ tree/page internals, optimizer algorithms, redo/undo and MVCC implementation, detailed locking, advanced migrations, DBA backup/recovery, replication, failover, capacity, partitioning and sharding. These are brief extensions unless explicitly selected or necessary for the stated work. For example, a named recovery-design task makes recovery mechanisms core; a generic MySQL development request does not.

## Middleware

- cache: Redis basics, TTL, invalidation, penetration, breakdown, avalanche, distributed locks.
- messaging: queue, topic, producer, consumer, retry, idempotency, dead letter, ordering.
- gateway/proxy: Nginx, routing, load balancing, TLS, rate limiting.
- search/storage/coordination: Elasticsearch, object storage, Etcd/ZooKeeper concepts when relevant.

## Server And Architecture

- HTTP, RPC, WebSocket, background jobs, schedulers.
- auth, permissions, sessions, tokens.
- logging, metrics, tracing, alerting.
- rate limiting, circuit breaking, graceful shutdown, retries, timeout, backpressure.
- layered architecture, DDD basics, microservices, event-driven design, CQRS when relevant.
- high availability, high concurrency, scalability, consistency, fault tolerance.

## Engineering Practice

- code organization, naming, interfaces, dependency injection.
- tests, mocks, fixtures, integration tests, regression tests.
- debugging, profiling, refactoring, code review.
- Docker, CI/CD, deployment, rollback, configuration and secrets.
