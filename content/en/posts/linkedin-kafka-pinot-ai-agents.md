---
title: "4 Lessons from LinkedIn: How 'Who Viewed Your Profile' Spawned Apache Kafka and Pinot (And Why It Matters for AI Agents)"
date: 2025-09-15T10:00:00+03:00
tags:
  - Apache Kafka
  - Apache Pinot
  - LinkedIn
  - AI Agents
  - Real-time Analytics
  - User-facing Analytics
  - Vector Search
  - Big Data
  - Data Architecture
categories:
  - System Architecture
  - AI and Machine Learning
  - Data Engineering
description: "The story of how one simple LinkedIn feature sparked a data processing revolution. We explore the creation of Apache Kafka and Pinot, and why these technologies are critical for the AI agent era."
keywords: "Apache Kafka, Apache Pinot, LinkedIn, AI agents, real-time analytics, user-facing analytics, vector search, real-time data processing"
summary: "How did LinkedIn's 'Who Viewed Your Profile' feature lead to Apache Kafka and Pinot? And why is this 10-year-old architecture critical for AI agents? 4 key lessons from the data processing revolution."
---

# How LinkedIn Accidentally Created the Perfect Architecture for AI Agents (The Apache Kafka and Pinot Story)

> **TL;DR:**
> LinkedIn created "Who viewed your profile" → Spawned Apache Kafka and Pinot → Accidentally solved AI agent problems 10 years before they existed.
> **Key insight:** Your database isn't ready for an AI agent running 100 parallel queries instead of one.

---

## Introduction: From Simple Counter to Data Revolution

Imagine: You log into LinkedIn and see "23 people viewed your profile." Simple number, right?

Wrong.

Behind that number lies an architecture that:
- Processes **10,000 requests per second**
- Responds in **100 milliseconds**
- Spawned **two open-source giants** (Apache Kafka and Pinot)
- Accidentally solved AI agent problems **10 years before they appeared**

This feature's story isn't just another Silicon Valley tech tale. It's a **blueprint** for a future where your primary users aren't humans, but autonomous AI agents.

Let's break down 4 key lessons.

---

## Lesson 1: One Feature → Two Open-Source Giants

### LinkedIn's Problem (2010)

In 2010, LinkedIn was a "resume graveyard." People uploaded profiles and... that was it. No activity, no engagement.

The team launched an experiment: **"Who Viewed Your Profile?"**

Result? 💥 **Explosive growth in activity.**

But a technical problem emerged:
- **1 billion users** want to know who viewed them
- **10,000 requests per second** at peak hours
- Latency must be **< 100ms** (or the app "lags")
- Data must be **fresh** (not yesterday's)

### Birth of Apache Kafka (2010)

Existing message queue systems couldn't handle it. LinkedIn created **Kafka** — a distributed streaming platform.

**Kafka's Key Principles:**
```
1. Events as first-class citizens
2. Horizontal scaling
3. Built-in fault-tolerance
4. Throughput > 1M events/sec
```

Every click, view, like — it's an event in Kafka. The system became LinkedIn's "central nervous system."

### Birth of Apache Pinot (2013)

Kafka collected events, but how to **instantly** analyze them?

Traditional OLAP systems:
- ❌ Too slow (seconds, not milliseconds)
- ❌ Can't handle concurrency (1000+ parallel queries)
- ❌ Batch-oriented (data gets stale)

LinkedIn created **Pinot** — a real-time OLAP database.

**Pinot Architecture:**
```yaml
Ingestion:
  - Real-time: directly from Kafka
  - Batch: historical data

Indexing:
  - Inverted Index: text search
  - Range Index: numeric ranges
  - JSON Index: nested structures
  - Vector Index: semantic search (new!)

Query:
  - Latency: < 100ms at 99th percentile
  - Concurrency: 10K+ QPS
  - Freshness: seconds from event to query
```

**Result:** One user-facing feature spawned two technologies now used by Uber, Stripe, Walmart, and dozens of other companies.

---

## Lesson 2: Best Analytics Are Customer-Facing

### Two Worlds of Analytics

**World 1: Internal Analytics (for managers)**
```python
# Typical scenario
analyst.run_query("SELECT revenue FROM sales WHERE date = yesterday")
analyst.go_get_coffee()  # Query runs for 30 seconds
analyst.view_dashboard()  # T+1 data (yesterday's)
```

**World 2: User-Facing Analytics (for customers)**
```python
# LinkedIn scenario
user.clicks("Who viewed my profile")
# Expectation: < 100ms
# Freshness: real-time
# Concurrency: 1M+ users simultaneously
```

### The Trinity Challenge of User-Facing Analytics

**1. Data Freshness**
- Internal: "Yesterday's data? Fine."
- User-facing: "Someone viewed my profile? I want to know NOW."

**2. Query Latency**
- Internal: "30 seconds? I'll get coffee."
- User-facing: "100ms or the user leaves."

**3. Concurrency**
- Internal: 10-100 analysts
- User-facing: 1M+ users **simultaneously**

### Why This Is Revolutionary

> "Data's true value is revealed when you **return it to customers**, not lock it in manager dashboards."

Examples of user-facing analytics today:
- **Spotify Wrapped**: Your music statistics
- **Strava**: Real-time workout analysis
- **Uber**: "Your driver arrives in 3 minutes"
- **Trading apps**: Real-time quotes and portfolio

---

## Lesson 3: AI Agents Are Machines, Not Humans (And Your DB Isn't Ready)

### Human vs AI Agent: Query Patterns

**Human:**
```sql
-- One query, wait for response
SELECT * FROM users WHERE country = 'USA'
-- Think...
-- Another query
SELECT avg(age) FROM users WHERE country = 'USA'
```

**AI Agent:**
```python
# Task: "Find anomalies in data"
# Agent generates 20 queries IN PARALLEL:

queries = [
    "SELECT * FROM posts WHERE likes > 10000 AND comments < 10",
    "SELECT user_id, follower_growth FROM users WHERE growth_rate > 1000%",
    "SELECT content FROM posts WHERE created_at - user_created_at < 1_day",
    # ... 17 more queries
]

# Execute all simultaneously
results = parallel_execute(queries)
# Analyze correlations
find_patterns(results)
```

### Real Example from Demo

In one demonstration, an AI agent was given the task: **"Find suspicious accounts in social network"**

The agent independently:
1. Generated **15-20 SQL queries**
2. Looked for patterns:
   - "Posts with 10K+ likes but < 10 comments"
   - "Follower growth > 1000% per day"
   - "Accounts created yesterday with 100K followers"
3. Executed all queries **in parallel**
4. Found correlations between results

### What This Means for Your Architecture

```yaml
Traditional DB:
  Optimized for: Sequential queries from humans
  Concurrency: 10-100 users
  Pattern: Query → Wait → Query

AI Agent Requirements:
  Optimized for: Parallel burst queries
  Concurrency: 1000+ queries from ONE agent
  Pattern: 100 queries simultaneously → Analyze

Solution: Apache Pinot
  - Designed for 10K+ QPS
  - Sub-100ms latency at 99%
  - Real-time freshness
```

> **Key insight:** If your DB struggles with 10 analysts, imagine when 100 AI agents start firing 100 queries each.

---

## Lesson 4: Future = Vector Search + Real-time Filters

### Why Pure Vector Search Isn't Enough

**Typical vector search:**
```python
# Find documents similar in meaning to "authentication failure"
vector_db.search("authentication failure", k=10)
```

**Real business query:**
```python
# Find similar to "authentication failure", BUT:
# - Only from last hour
# - Only for Enterprise customers
# - Only in EU region
# - Sort by severity

vector_db.search(
    query="authentication failure",
    filters={
        "timestamp": "> now() - 1h",
        "plan": "Enterprise",
        "region": "EU"
    },
    order_by="severity DESC"
)
```

### Problem with Vector DBs

Pure vector DBs (Pinecone, Weaviate) **struggle** with hybrid queries:
1. First vector search (slow on large volume)
2. Then filtering (inefficient)
3. Performance degrades with more filters

### Pinot's Solution: Hybrid Architecture

```yaml
Apache Pinot Indexes:
  Inverted Index: Text search
  Range Index: Numeric ranges
  JSON Index: Nested structures
  Timestamp Index: Time-series data
  Vector Index: Semantic search (NEW!)

Magic: ALL indexes work TOGETHER in one query
```

**Example hybrid query in Pinot:**
```sql
SELECT
  log_message,
  COSINE_DISTANCE(embedding, [0.1, 0.2, ...]) as similarity
FROM logs
WHERE
  timestamp > NOW() - INTERVAL '1' HOUR
  AND customer_tier = 'Enterprise'
  AND region = 'EU'
  AND TEXT_MATCH(log_message, 'error OR failure')
ORDER BY similarity ASC
LIMIT 100
```

**Result:**
- ⚡ 10-100x faster than pure vector DBs on hybrid queries
- ✅ One engine for all search types
- 🔄 Real-time ingestion from Kafka

---

## Practical Takeaways: What to Do Right Now

### If You're Building a User-Facing Product:

1. **Rethink analytics**
   - Not "dashboards for managers"
   - But "insights for users"

2. **Check real-time readiness**
   ```bash
   # Your checklist:
   □ Data freshness < 1 second?
   □ Query latency < 100ms?
   □ Concurrency > 1000 QPS?

   If any "no" → explore Kafka + Pinot
   ```

### If You're Implementing AI Agents:

1. **Test the load**
   ```python
   # Simulate AI agent
   for _ in range(100):
       thread.start(run_random_query)
   # Did your DB survive?
   ```

2. **Prepare architecture**
   - Event streaming (Kafka) for data collection
   - Real-time OLAP (Pinot) for analytics
   - Hybrid indexes for vector + structured search

### If You're a Data Engineer:

1. **Study LinkedIn's stack**
   - [Apache Kafka](https://kafka.apache.org/) — already industry standard
   - [Apache Pinot](https://pinot.apache.org/) — gaining momentum

2. **Try in sandbox**
   ```bash
   # Quick start with Docker
   docker run -p 9000:9000 apachepinot/pinot:latest \
     QuickStart -type hybrid
   ```

---

## Conclusion: History Repeats Itself

**2010:** LinkedIn created user-facing analytics → Spawned Kafka and Pinot

**2025:** AI agents become new "users" → Require the same architecture

LinkedIn's story teaches us the main thing:

> **Technologies created to solve real user problems outlive their creators and find applications in areas no one could dream of.**

The "Who viewed your profile" feature was created to increase engagement.

But it accidentally solved problems that would appear 15 years later — when AI agents start "viewing" our data at 10,000 requests per second.

**The question isn't whether your infrastructure is ready for AI agents.**

**The question is whether you'll be ready before your competitors launch theirs.**

---

## Useful Links

### Technologies
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Pinot Getting Started](https://docs.pinot.apache.org/basics/getting-started)
- [Kafka + Pinot Integration Guide](https://docs.pinot.apache.org/basics/data-import/from-apache-kafka)

### Use Cases
- [How LinkedIn uses Kafka and Pinot](https://engineering.linkedin.com/blog/topic/pinot)
- [Uber's real-time analytics with Pinot](https://www.uber.com/blog/uber-real-time-analytics/)
- [Stripe's data infrastructure](https://stripe.com/blog/online-migrations)

### For Developers
- [Pinot Vector Index (beta)](https://docs.pinot.apache.org/basics/indexing/vector-index)
- [Building User-Facing Analytics](https://www.startree.ai/blog/user-facing-analytics-guide)
- [Real-time ML Feature Store with Kafka + Pinot](https://github.com/apache/pinot/tree/master/pinot-contrib/pinot-ml)

---

*Have experience with Kafka or Pinot? Implementing AI agents? Share in comments or reach me on [Telegram](https://t.me/vitnm)!*