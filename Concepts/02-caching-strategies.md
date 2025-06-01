# 🚀 Caching Strategies

## Overview
Caching is a technique to store frequently accessed data in fast storage to reduce latency and improve system performance. It's one of the most effective ways to scale systems.

## Cache Hierarchy

### 1. Browser Cache
- Client-side caching
- Stores static resources (CSS, JS, images)
- Controlled by HTTP headers

### 2. CDN (Content Delivery Network)
- Geographically distributed cache
- Reduces latency for global users
- Caches static and dynamic content

### 3. Reverse Proxy Cache
- Server-side caching layer
- Examples: Nginx, Varnish
- Caches responses before they reach application

### 4. Application Cache
- In-memory cache within application
- Examples: Redis, Memcached
- Fastest access for frequently used data

### 5. Database Cache
- Query result caching
- Reduces database load
- Can be at ORM level

## Caching Patterns

### 1. Cache-Aside (Lazy Loading)
```python
def get_user(user_id):
    # Check cache first
    user = cache.get(f"user:{user_id}")
    if user is None:
        # Cache miss - fetch from database
        user = database.get_user(user_id)
        # Store in cache for future requests
        cache.set(f"user:{user_id}", user, ttl=3600)
    return user
```

### 2. Write-Through
```python
def update_user(user_id, data):
    # Update database first
    user = database.update_user(user_id, data)
    # Then update cache
    cache.set(f"user:{user_id}", user, ttl=3600)
    return user
```

### 3. Write-Behind (Write-Back)
```python
def update_user_async(user_id, data):
    # Update cache immediately
    cache.set(f"user:{user_id}", data, ttl=3600)
    # Queue database update for later
    queue.enqueue('update_user_db', user_id, data)
```

### 4. Refresh-Ahead
```python
def get_user_with_refresh(user_id):
    user = cache.get(f"user:{user_id}")
    if user and cache.ttl(f"user:{user_id}") < 300:  # 5 min left
        # Async refresh before expiry
        queue.enqueue('refresh_user_cache', user_id)
    return user
```

## Cache Eviction Policies

### 1. LRU (Least Recently Used)
- Evicts least recently accessed items
- Good for temporal locality

### 2. LFU (Least Frequently Used)
- Evicts least frequently accessed items
- Good for frequency-based access patterns

### 3. FIFO (First In, First Out)
- Simple queue-based eviction
- Predictable but may not be optimal

### 4. TTL (Time To Live)
- Items expire after set time
- Prevents stale data issues

## Implementation Examples

### Redis Implementation
```python
import redis
import json
from typing import Optional, Any

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)
    
    def get(self, key: str) -> Optional[Any]:
        data = self.client.get(key)
        return json.loads(data) if data else None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        self.client.setex(key, ttl, json.dumps(value))
    
    def delete(self, key: str):
        self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        return self.client.exists(key)
```

### In-Memory LRU Cache
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def set(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used
            self.cache.popitem(last=False)
        self.cache[key] = value
```

## Cache Invalidation Strategies

### 1. TTL-Based
- Automatic expiration after set time
- Simple but may serve stale data

### 2. Event-Based
- Invalidate on data changes
- Complex but ensures consistency

### 3. Manual Invalidation
- Explicit cache clearing
- Full control but error-prone

### 4. Cache Tags
- Group related cache entries
- Invalidate by tags

## Distributed Caching Challenges

### 1. Cache Coherence
- Keeping multiple cache instances in sync
- Solutions: Pub/Sub, Event streaming

### 2. Hot Keys
- Popular keys overwhelming single cache node
- Solutions: Replication, Client-side caching

### 3. Cache Stampede
- Multiple requests fetching same expired data
- Solutions: Lock-based loading, Probabilistic expiry

## Performance Considerations

### Cache Hit Ratio
```python
def calculate_hit_ratio(hits, misses):
    total_requests = hits + misses
    return (hits / total_requests) * 100 if total_requests > 0 else 0
```

### Optimal Cache Size
- Pareto Principle: 80% requests from 20% data
- Monitor working set size
- Balance memory cost vs. hit ratio

## Real-World Examples
- **Facebook**: TAO (distributed cache for social graph)
- **Twitter**: Manhattan (distributed key-value store)
- **Netflix**: EVCache (distributed memcached)

## Common Pitfalls
1. **Over-caching**: Caching everything unnecessarily
2. **Under-invalidation**: Serving stale data too long
3. **Cache Avalanche**: Mass expiration causing overload
4. **Memory Leaks**: Unbounded cache growth

## Best Practices
1. Set appropriate TTL values
2. Monitor cache hit ratios
3. Use cache warming for critical data
4. Implement graceful degradation on cache failures
5. Consider data consistency requirements

## Metrics to Monitor
- **Hit Ratio**: Percentage of cache hits
- **Latency**: Cache response time
- **Memory Usage**: Cache size and utilization
- **Eviction Rate**: How often items are evicted

## Next Steps
- Study Database Design & Sharding
- Learn about Message Queues & Pub/Sub
- Understand API Design & Rate Limiting