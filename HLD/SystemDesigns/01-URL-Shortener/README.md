# 🔗 URL Shortener System Design (TinyURL)

## 📋 Problem Statement

Design a URL shortening service like TinyURL, bit.ly, or goo.gl that converts long URLs into short, shareable links.

### Functional Requirements
1. **URL Shortening**: Convert long URLs to short URLs
2. **URL Redirection**: Redirect short URLs to original URLs
3. **Custom Aliases**: Allow users to create custom short URLs
4. **Analytics**: Track click counts and basic analytics
5. **Expiration**: URLs can have expiration dates

### Non-Functional Requirements
1. **Scale**: 100M URLs shortened per day
2. **Read Heavy**: 100:1 read/write ratio (10B redirections/day)
3. **Availability**: 99.9% uptime
4. **Latency**: <100ms for redirection
5. **Storage**: 5 years of data retention

## 📊 Capacity Estimation

### Traffic Estimates
- **Write**: 100M URLs/day = 1,160 URLs/second
- **Read**: 10B redirections/day = 115,700 redirections/second
- **Peak Traffic**: 2x average = 231,400 redirections/second

### Storage Estimates
- **URL Data**: Average 500 chars per URL
- **Metadata**: 500 bytes per URL entry
- **Total per URL**: ~1KB
- **5 years storage**: 100M × 365 × 5 × 1KB = ~183TB

### Memory Estimates (Caching)
- **Cache hot URLs**: 20% of daily reads
- **Cache size**: 2B × 1KB = 2TB (distributed across cache servers)

## 🏗️ System Architecture

### High-Level Components

```
[Client] → [Load Balancer] → [Web Servers] → [Application Servers]
                                              ↓
[Cache Layer (Redis)] ← → [Database Cluster (Primary/Replica)]
                                              ↓
                           [Analytics Database] ← [Message Queue]
```

### Core Services
1. **URL Shortening Service**: Generates short URLs
2. **URL Redirection Service**: Handles redirections
3. **Analytics Service**: Tracks and processes metrics
4. **Cache Service**: High-speed URL lookups
5. **Database Service**: Persistent storage

## 🗄️ Database Design

### URL Table (Primary Database)
```sql
CREATE TABLE urls (
    short_url VARCHAR(7) PRIMARY KEY,
    long_url TEXT NOT NULL,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
```

### Analytics Table (Separate Database)
```sql
CREATE TABLE url_analytics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    short_url VARCHAR(7),
    ip_address VARCHAR(45),
    user_agent TEXT,
    referrer TEXT,
    country VARCHAR(2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_short_url_timestamp (short_url, timestamp)
);
```

### User Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    api_key VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_premium BOOLEAN DEFAULT FALSE
);
```

## 🔧 Algorithm Design

### Short URL Generation

#### Approach 1: Base62 Encoding
```python
import random
import string

class URLShortener:
    def __init__(self):
        self.alphabet = string.ascii_letters + string.digits  # 62 chars
        self.base = len(self.alphabet)
    
    def encode(self, num):
        """Convert number to base62 string"""
        if num == 0:
            return self.alphabet[0]
        
        result = []
        while num > 0:
            result.append(self.alphabet[num % self.base])
            num //= self.base
        
        return ''.join(reversed(result))
    
    def generate_short_url(self):
        """Generate 7-character short URL"""
        # Use timestamp + random for uniqueness
        timestamp = int(time.time())
        random_part = random.randint(1000, 9999)
        unique_id = timestamp * 10000 + random_part
        
        short_code = self.encode(unique_id)
        return short_code[:7].ljust(7, 'a')  # Ensure 7 chars
```

#### Approach 2: Counter-based with Sharding
```python
class CounterBasedShortener:
    def __init__(self, shard_id, total_shards):
        self.shard_id = shard_id
        self.total_shards = total_shards
        self.counter = self.load_counter()
    
    def generate_short_url(self):
        """Generate unique short URL using counter"""
        # Increment counter for this shard
        self.counter += self.total_shards
        self.save_counter(self.counter)
        
        # Encode counter to base62
        return self.encode(self.counter)
```

## 🚀 API Design

### REST Endpoints

#### 1. Shorten URL
```http
POST /api/v1/shorten
Content-Type: application/json

{
  "long_url": "https://example.com/very/long/url",
  "custom_alias": "my-link",  # optional
  "expires_at": "2024-12-31T23:59:59Z"  # optional
}

Response:
{
  "short_url": "https://tiny.ly/abc123",
  "long_url": "https://example.com/very/long/url",
  "expires_at": "2024-12-31T23:59:59Z",
  "created_at": "2024-06-01T10:00:00Z"
}
```

#### 2. Redirect URL
```http
GET /abc123

Response:
HTTP 301 Moved Permanently
Location: https://example.com/very/long/url
```

#### 3. Get Analytics
```http
GET /api/v1/analytics/abc123

Response:
{
  "short_url": "abc123",
  "total_clicks": 1500,
  "daily_clicks": [
    {"date": "2024-06-01", "clicks": 100},
    {"date": "2024-06-02", "clicks": 150}
  ],
  "top_countries": [
    {"country": "US", "clicks": 800},
    {"country": "IN", "clicks": 400}
  ]
}
```

## ⚡ Caching Strategy

### Cache Architecture
```python
class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(host='redis-cluster')
        self.ttl = 3600  # 1 hour
    
    def get_url(self, short_code):
        """Get long URL from cache"""
        cached = self.redis_client.get(f"url:{short_code}")
        if cached:
            return json.loads(cached)
        return None
    
    def set_url(self, short_code, url_data):
        """Cache URL data"""
        self.redis_client.setex(
            f"url:{short_code}",
            self.ttl,
            json.dumps(url_data)
        )
    
    def invalidate_url(self, short_code):
        """Remove from cache"""
        self.redis_client.delete(f"url:{short_code}")
```

### Cache Policies
1. **Cache-Aside**: Application manages cache
2. **TTL**: 1 hour for active URLs
3. **LRU Eviction**: Remove least recently used
4. **Write-Through**: Update cache on URL updates

## 📈 Scalability Considerations

### Database Sharding
```python
class DatabaseSharding:
    def __init__(self, shards):
        self.shards = shards
        self.shard_count = len(shards)
    
    def get_shard(self, short_code):
        """Determine shard based on short code"""
        shard_id = hash(short_code) % self.shard_count
        return self.shards[shard_id]
    
    def store_url(self, short_code, url_data):
        shard = self.get_shard(short_code)
        return shard.insert('urls', url_data)
```

### Load Balancing
- **Application Servers**: Round-robin with health checks
- **Database Reads**: Route to read replicas
- **Cache**: Consistent hashing for Redis cluster

### CDN Integration
- Cache redirection responses at edge locations
- Reduce latency for global users
- Handle 80% of traffic at CDN level

## 🔒 Security & Reliability

### Security Measures
1. **Rate Limiting**: Prevent abuse
2. **URL Validation**: Check for malicious URLs
3. **Authentication**: API keys for premium features
4. **Input Sanitization**: Prevent injection attacks

### Reliability Features
1. **Health Checks**: Monitor service availability
2. **Circuit Breakers**: Prevent cascade failures
3. **Graceful Degradation**: Return cached data on DB failure
4. **Monitoring**: Real-time alerts and metrics

## 📊 Monitoring & Analytics

### Key Metrics
- **Request Rate**: URLs/second
- **Response Time**: P95, P99 latencies
- **Error Rate**: Failed requests percentage
- **Cache Hit Ratio**: Cache effectiveness
- **Database Performance**: Query times

### Analytics Pipeline
```
[Click Events] → [Message Queue] → [Stream Processor] → [Analytics DB]
                                        ↓
[Real-time Dashboard] ← [Batch Analytics] ← [Data Warehouse]
```

## 🚀 Future Enhancements

### Phase 2 Features
1. **QR Code Generation**: Visual URL sharing
2. **Link Preview**: Show page metadata
3. **Bulk Operations**: API for multiple URLs
4. **A/B Testing**: Multiple destinations per short URL

### Advanced Analytics
1. **Real-time Analytics**: Live click tracking
2. **Fraud Detection**: Identify suspicious activity
3. **Performance Insights**: Page load time tracking
4. **Conversion Tracking**: Business metrics

## 💡 Design Trade-offs

### Consistency vs Availability
- **Choice**: Eventual consistency for better availability
- **Reason**: URL shortening can tolerate slight delays
- **Implementation**: Async replication to read replicas

### Storage vs Performance
- **Choice**: Denormalized analytics for fast queries
- **Reason**: Analytics queries are complex and frequent
- **Implementation**: Separate OLAP database for analytics

### Complexity vs Maintainability
- **Choice**: Simple base62 encoding over complex algorithms
- **Reason**: Easier to debug and maintain
- **Implementation**: Counter-based approach with collision handling

---

## ✅ Success Criteria

This design successfully handles:
- ✅ **Scale**: 100M URLs/day, 10B redirections/day
- ✅ **Performance**: <100ms redirection latency
- ✅ **Availability**: 99.9% uptime with redundancy
- ✅ **Storage**: Efficient storage for 5 years of data
- ✅ **Analytics**: Real-time and historical insights

**Next Steps**: Implement URL Shortener prototype and move to Chat Application design.