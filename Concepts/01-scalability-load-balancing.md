# 📈 Scalability & Load Balancing

## Overview
Scalability is the ability of a system to handle increased load by adding resources. Load balancing distributes incoming requests across multiple servers to ensure no single server becomes overwhelmed.

## Key Concepts

### Types of Scalability
1. **Vertical Scaling (Scale Up)**
   - Adding more power to existing machines
   - Pros: Simple, no code changes
   - Cons: Hardware limits, single point of failure

2. **Horizontal Scaling (Scale Out)**
   - Adding more machines to the pool
   - Pros: No hardware limits, fault tolerant
   - Cons: Complex, requires load balancing

### Load Balancing Strategies

#### 1. Round Robin
- Requests distributed sequentially
- Simple but doesn't consider server load

#### 2. Weighted Round Robin
- Servers assigned weights based on capacity
- Better for heterogeneous servers

#### 3. Least Connections
- Routes to server with fewest active connections
- Good for varying request processing times

#### 4. IP Hash
- Routes based on client IP hash
- Ensures session stickiness

#### 5. Geographic/Latency-based
- Routes to nearest server
- Reduces latency for users

### Load Balancer Types

#### Layer 4 (Transport Layer)
- Routes based on IP and port
- Faster, lower overhead
- No visibility into application data

#### Layer 7 (Application Layer)
- Routes based on content (HTTP headers, URLs)
- More intelligent routing
- Higher overhead but more flexible

## Implementation Patterns

### Database Scaling
```python
# Master-Slave Replication
class DatabaseCluster:
    def __init__(self):
        self.master = MasterDB()
        self.slaves = [SlaveDB() for _ in range(3)]
    
    def write(self, query):
        return self.master.execute(query)
    
    def read(self, query):
        slave = self.get_least_loaded_slave()
        return slave.execute(query)
```

### Horizontal Partitioning (Sharding)
```python
class ShardedDatabase:
    def __init__(self, shards):
        self.shards = shards
    
    def get_shard(self, key):
        shard_id = hash(key) % len(self.shards)
        return self.shards[shard_id]
    
    def query(self, key, query):
        shard = self.get_shard(key)
        return shard.execute(query)
```

## Real-World Examples
- **Netflix**: Uses AWS Auto Scaling + ELB
- **Google**: Global load balancing with health checks
- **Facebook**: Sharded MySQL with read replicas

## Common Pitfalls
1. **Hot Spots**: Uneven data distribution
2. **Session Stickiness**: Limits load balancing effectiveness
3. **Cascading Failures**: One failure causing others

## Best Practices
1. Use health checks for automatic failover
2. Implement circuit breakers
3. Monitor key metrics (latency, throughput, error rates)
4. Plan for capacity ahead of time
5. Use CDNs for static content

## Metrics to Monitor
- **Throughput**: Requests per second
- **Latency**: Response time percentiles
- **Error Rate**: Failed requests percentage
- **Resource Utilization**: CPU, memory, disk usage

## Next Steps
- Study Caching Strategies
- Learn about Database Design & Sharding
- Understand Microservices Architecture