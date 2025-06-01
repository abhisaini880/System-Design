# 🗄️ Database Design & Sharding

## Overview
Database design and sharding are crucial for building scalable systems. As data grows, a single database becomes a bottleneck, requiring horizontal partitioning (sharding) to distribute load across multiple database instances.

## Database Design Principles

### 1. Normalization vs Denormalization

#### Normalization
- Reduces data redundancy
- Ensures data consistency
- Follows normal forms (1NF, 2NF, 3NF, BCNF)
- Good for write-heavy workloads

#### Denormalization
- Introduces controlled redundancy
- Optimizes for read performance
- Reduces complex joins
- Good for read-heavy workloads

### 2. ACID Properties
- **Atomicity**: All or nothing transactions
- **Consistency**: Data integrity maintained
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed data persists

### 3. CAP Theorem
- **Consistency**: All nodes see same data simultaneously
- **Availability**: System remains operational
- **Partition Tolerance**: System continues despite network failures
- **Reality**: Can only guarantee 2 out of 3

## Sharding Strategies

### 1. Horizontal Sharding (Most Common)
```python
class HorizontalSharding:
    def __init__(self, shards):
        self.shards = shards
    
    def get_shard_by_hash(self, key):
        shard_id = hash(key) % len(self.shards)
        return self.shards[shard_id]
    
    def get_shard_by_range(self, key):
        # Range-based sharding
        if key < 1000:
            return self.shards[0]
        elif key < 2000:
            return self.shards[1]
        else:
            return self.shards[2]
```

### 2. Vertical Sharding
- Split tables by features/domains
- User service gets user tables
- Order service gets order tables
- Good for microservices architecture

### 3. Directory-Based Sharding
```python
class DirectorySharding:
    def __init__(self):
        self.directory = {}  # key -> shard_id mapping
    
    def get_shard(self, key):
        shard_id = self.directory.get(key)
        return self.shards[shard_id] if shard_id else None
    
    def add_mapping(self, key, shard_id):
        self.directory[key] = shard_id
```

## Sharding Key Selection

### Good Sharding Keys
1. **High Cardinality**: Many unique values
2. **Even Distribution**: Avoids hot spots
3. **Query Friendly**: Supports common access patterns

### Bad Sharding Keys
1. **Timestamps**: Creates hot spots for recent data
2. **Sequential IDs**: Uneven distribution
3. **Geographic Data**: May create regional hot spots

## Consistent Hashing

```python
import hashlib
import bisect

class ConsistentHashing:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def add_node(self, node):
        for i in range(self.replicas):
            key = self.hash(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()
    
    def remove_node(self, node):
        for i in range(self.replicas):
            key = self.hash(f"{node}:{i}")
            del self.ring[key]
            self.sorted_keys.remove(key)
    
    def get_node(self, key):
        if not self.ring:
            return None
        
        hash_key = self.hash(key)
        idx = bisect.bisect_right(self.sorted_keys, hash_key)
        if idx == len(self.sorted_keys):
            idx = 0
        return self.ring[self.sorted_keys[idx]]
    
    def hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
```

## Database Types & Use Cases

### 1. Relational Databases (SQL)
- **Examples**: PostgreSQL, MySQL, Oracle
- **Use Cases**: ACID transactions, complex queries, structured data
- **Pros**: ACID compliance, mature ecosystem, SQL standardization
- **Cons**: Vertical scaling limitations, rigid schema

### 2. NoSQL Databases

#### Document Stores
- **Examples**: MongoDB, CouchDB
- **Use Cases**: Content management, catalogs, user profiles
- **Pros**: Flexible schema, natural data modeling
- **Cons**: Limited ACID, eventual consistency

#### Key-Value Stores
- **Examples**: Redis, DynamoDB, Riak
- **Use Cases**: Caching, session storage, real-time recommendations
- **Pros**: High performance, simple model, horizontal scaling
- **Cons**: Limited query capabilities, no ACID across keys

#### Column-Family
- **Examples**: Cassandra, HBase
- **Use Cases**: Time-series data, IoT data, large-scale analytics
- **Pros**: High write throughput, compression, horizontal scaling
- **Cons**: Limited query flexibility, eventual consistency

#### Graph Databases
- **Examples**: Neo4j, Amazon Neptune
- **Use Cases**: Social networks, recommendation engines, fraud detection
- **Pros**: Relationship queries, graph algorithms
- **Cons**: Limited scalability, specialized use cases

## Replication Strategies

### 1. Master-Slave Replication
```python
class MasterSlaveReplication:
    def __init__(self, master, slaves):
        self.master = master
        self.slaves = slaves
        self.slave_index = 0
    
    def write(self, query):
        result = self.master.execute(query)
        # Async replication to slaves
        for slave in self.slaves:
            slave.replicate_async(query)
        return result
    
    def read(self, query):
        # Round-robin read from slaves
        slave = self.slaves[self.slave_index]
        self.slave_index = (self.slave_index + 1) % len(self.slaves)
        return slave.execute(query)
```

### 2. Master-Master Replication
- Multiple writable nodes
- Conflict resolution needed
- Higher availability but complex

### 3. Quorum-Based Replication
- Read/Write quorums ensure consistency
- Formula: R + W > N (where N = total replicas)

## Data Partitioning Challenges

### 1. Cross-Shard Queries
```python
class CrossShardQuery:
    def __init__(self, shards):
        self.shards = shards
    
    def aggregate_query(self, query):
        results = []
        for shard in self.shards:
            result = shard.execute(query)
            results.append(result)
        return self.merge_results(results)
    
    def join_across_shards(self, table1_key, table2_key):
        # Requires data co-location or application-level joins
        pass
```

### 2. Rebalancing
- Adding/removing shards
- Data migration without downtime
- Consistent hashing helps minimize movement

### 3. Hotspots
- Uneven data distribution
- Popular keys overwhelming single shard
- Solutions: Better sharding keys, data replication

## Implementation Example: User Sharding

```python
class UserShardingService:
    def __init__(self, database_shards):
        self.shards = database_shards
        self.shard_count = len(database_shards)
    
    def get_user_shard(self, user_id):
        shard_id = user_id % self.shard_count
        return self.shards[shard_id]
    
    def create_user(self, user_data):
        user_id = user_data['id']
        shard = self.get_user_shard(user_id)
        return shard.insert('users', user_data)
    
    def get_user(self, user_id):
        shard = self.get_user_shard(user_id)
        return shard.select('users', {'id': user_id})
    
    def get_users_by_range(self, start_id, end_id):
        # Cross-shard query - expensive!
        results = []
        for user_id in range(start_id, end_id + 1):
            shard = self.get_user_shard(user_id)
            user = shard.select('users', {'id': user_id})
            if user:
                results.append(user)
        return results
```

## Real-World Examples
- **Instagram**: Sharded PostgreSQL by user_id
- **Discord**: Partitioned by guild_id for chat messages
- **Uber**: Sharded by geographic region (geohash)
- **WhatsApp**: Sharded by phone number hash

## Common Pitfalls
1. **Over-sharding**: Too many small shards increase overhead
2. **Under-sharding**: Too few large shards create bottlenecks
3. **Poor Shard Key**: Uneven distribution or hotspots
4. **Cross-Shard Transactions**: Complex and expensive
5. **Resharding Complexity**: Difficult to change sharding strategy

## Best Practices
1. Plan sharding strategy early
2. Choose shard keys carefully
3. Monitor shard distribution and performance
4. Design for cross-shard query minimization
5. Use consistent hashing for flexibility
6. Implement proper monitoring and alerting
7. Plan for data migration and rebalancing

## Metrics to Monitor
- **Shard Size**: Data distribution across shards
- **Query Performance**: Response times per shard
- **Hot Shard Detection**: Uneven load distribution
- **Cross-Shard Query Ratio**: Percentage of expensive queries
- **Replication Lag**: Delay between master and slaves

## Next Steps
- Study Microservices Architecture
- Learn about Message Queues & Pub/Sub
- Understand Consistency & CAP Theorem