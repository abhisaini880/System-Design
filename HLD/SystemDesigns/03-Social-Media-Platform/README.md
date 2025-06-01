# 🐦 Social Media Platform System Design (Twitter)

## 📋 Problem Statement

Design a social media platform like Twitter that allows users to post tweets, follow other users, and view personalized timelines with high scalability and performance.

### Functional Requirements
1. **Tweet Operations**: Create, read, delete tweets (280 character limit)
2. **Timeline**: Home timeline (following users), user timeline (own tweets)
3. **Follow System**: Follow/unfollow users, followers/following lists
4. **Engagement**: Like, retweet, reply to tweets
5. **Search**: Search tweets by keywords, hashtags, users
6. **Trends**: Trending hashtags and topics

### Non-Functional Requirements
1. **Scale**: 300M users, 400M tweets/day, 100M daily active users
2. **Read Heavy**: 100:1 read/write ratio (40B timeline views/day)
3. **Availability**: 99.9% uptime
4. **Latency**: <200ms for timeline generation
5. **Consistency**: Eventually consistent timelines

## 📊 Capacity Estimation

### Traffic Estimates
- **Tweet Creation**: 400M tweets/day = 4,630 tweets/second
- **Timeline Reads**: 40B reads/day = 462,960 reads/second
- **Peak Traffic**: 3x average = 1.39M reads/second
- **Active Users**: 100M DAU, 50M peak concurrent users

### Storage Estimates
- **Tweet Size**: 280 chars + metadata = 500 bytes average
- **Daily Storage**: 400M × 500 bytes = 200GB/day
- **5 Year Storage**: 200GB × 365 × 5 = 365TB
- **Media Content**: 10% tweets have media, average 2MB = 80TB/day

### Timeline Generation
- **Fan-out**: Average user has 200 followers
- **Timeline Updates**: 400M tweets × 200 followers = 80B timeline updates/day
- **Timeline Cache**: Top 10% users cached = 10M timelines × 800 tweets × 500 bytes = 4TB

## 🏗️ System Architecture

### High-Level Components

```
[Clients] → [CDN] → [Load Balancer] → [API Gateway]
                                           ↓
[Tweet Service] ← → [Timeline Service] ← → [User Service]
       ↓                    ↓                    ↓
[Tweet DB] → [Message Queue] → [Timeline Cache] → [User DB]
       ↓                    ↓                    ↓
[Media Storage] → [Search Service] → [Analytics DB]
```

### Core Services
1. **User Service**: User management, follow/unfollow operations
2. **Tweet Service**: Tweet creation, storage, and retrieval
3. **Timeline Service**: Timeline generation and caching
4. **Notification Service**: Push notifications for interactions
5. **Search Service**: Tweet and user search functionality
6. **Media Service**: Image/video upload and processing
7. **Analytics Service**: Metrics, trends, and recommendations

## 🗄️ Database Design

### User Table
```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    bio TEXT,
    profile_image_url VARCHAR(512),
    verified BOOLEAN DEFAULT FALSE,
    followers_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    tweets_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_followers_count (followers_count DESC)
);
```

### Tweet Table (Sharded)
```sql
CREATE TABLE tweets (
    tweet_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    media_urls JSON,
    hashtags JSON,
    mentions JSON,
    reply_to_tweet_id BIGINT NULL,
    retweet_of_tweet_id BIGINT NULL,
    likes_count INT DEFAULT 0,
    retweets_count INT DEFAULT 0,
    replies_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PARTITION BY HASH(tweet_id) PARTITIONS 1000,
    INDEX idx_user_created (user_id, created_at DESC),
    INDEX idx_created_at (created_at DESC)
);
```

### Follow Relationship Table
```sql
CREATE TABLE follows (
    follower_id BIGINT,
    followee_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (follower_id, followee_id),
    INDEX idx_followee (followee_id, created_at DESC),
    INDEX idx_follower (follower_id, created_at DESC)
);
```

### Tweet Engagement Table
```sql
CREATE TABLE tweet_likes (
    tweet_id BIGINT,
    user_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (tweet_id, user_id),
    INDEX idx_user_likes (user_id, created_at DESC)
);

CREATE TABLE retweets (
    original_tweet_id BIGINT,
    user_id BIGINT,
    retweet_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (original_tweet_id, user_id),
    INDEX idx_user_retweets (user_id, created_at DESC)
);
```

## 🔧 Timeline Generation Architecture

### Push vs Pull Model
```python
class TimelineService:
    def __init__(self):
        self.celebrity_threshold = 1000000  # 1M followers
        
    async def generate_timeline(self, user_id, limit=20):
        """Generate user's home timeline"""
        # Check if user follows any celebrities
        following = await self.get_user_following(user_id)
        celebrities = [u for u in following if u.followers_count > self.celebrity_threshold]
        regular_users = [u for u in following if u.followers_count <= self.celebrity_threshold]
        
        # Get cached timeline for regular users (push model)
        cached_tweets = await self.get_cached_timeline(user_id, limit)
        
        # Get recent tweets from celebrities (pull model)
        celebrity_tweets = []
        if celebrities:
            celebrity_tweets = await self.get_celebrity_tweets(celebrities, limit)
        
        # Merge and sort tweets
        timeline = self.merge_timelines(cached_tweets, celebrity_tweets, limit)
        return timeline
    
    async def fan_out_tweet(self, tweet):
        """Fan out tweet to followers (push model)"""
        author = await self.get_user(tweet['user_id'])
        
        if author.followers_count > self.celebrity_threshold:
            # Don't fan out for celebrities - use pull model
            return
            
        followers = await self.get_user_followers(tweet['user_id'])
        
        # Add tweet to followers' cached timelines
        for follower_id in followers:
            await self.add_to_timeline_cache(follower_id, tweet)
```

### Timeline Caching Strategy
```python
class TimelineCache:
    def __init__(self):
        self.redis_client = redis.Redis(decode_responses=True)
        self.cache_size = 800  # tweets per timeline
        
    async def get_timeline(self, user_id, limit=20):
        """Get cached timeline for user"""
        cache_key = f"timeline:{user_id}"
        tweets = await self.redis_client.lrange(cache_key, 0, limit-1)
        return [json.loads(tweet) for tweet in tweets]
    
    async def add_tweet_to_timeline(self, user_id, tweet):
        """Add new tweet to user's cached timeline"""
        cache_key = f"timeline:{user_id}"
        tweet_json = json.dumps(tweet)
        
        # Add to front of timeline
        await self.redis_client.lpush(cache_key, tweet_json)
        
        # Trim to keep only recent tweets
        await self.redis_client.ltrim(cache_key, 0, self.cache_size-1)
        
        # Set expiration
        await self.redis_client.expire(cache_key, 3600 * 24)  # 24 hours
```

## 🚀 API Design

### REST Endpoints

#### Create Tweet
```http
POST /api/v1/tweets
Content-Type: application/json
Authorization: Bearer <token>

{
  "content": "Hello world! #firsttweet",
  "media_urls": ["https://media.twitter.com/image1.jpg"],
  "reply_to": 12345
}

Response:
{
  "tweet_id": 98765,
  "user_id": 123,
  "username": "johndoe",
  "content": "Hello world! #firsttweet",
  "media_urls": ["https://media.twitter.com/image1.jpg"],
  "hashtags": ["firsttweet"],
  "created_at": "2024-06-01T10:30:00Z",
  "likes_count": 0,
  "retweets_count": 0,
  "replies_count": 0
}
```

#### Get Home Timeline
```http
GET /api/v1/timeline/home?limit=20&cursor=abc123
Authorization: Bearer <token>

Response:
{
  "tweets": [
    {
      "tweet_id": 98765,
      "user": {
        "user_id": 456,
        "username": "janedoe",
        "display_name": "Jane Doe",
        "verified": true
      },
      "content": "Great day for coding!",
      "created_at": "2024-06-01T10:30:00Z",
      "likes_count": 42,
      "retweets_count": 8,
      "replies_count": 5,
      "liked_by_user": false,
      "retweeted_by_user": false
    }
  ],
  "next_cursor": "def456",
  "has_more": true
}
```

#### Follow User
```http
POST /api/v1/users/456/follow
Authorization: Bearer <token>

Response:
{
  "following": true,
  "user": {
    "user_id": 456,
    "username": "janedoe",
    "followers_count": 1001
  }
}
```

#### Search Tweets
```http
GET /api/v1/search/tweets?q=machine%20learning&limit=20

Response:
{
  "tweets": [...],
  "query": "machine learning",
  "count": 20,
  "next_cursor": "search_cursor_123"
}
```

## ⚡ Scalability Strategies

### Database Sharding
```python
class TweetSharding:
    def __init__(self, num_shards=1000):
        self.num_shards = num_shards
        
    def get_shard(self, tweet_id):
        """Determine shard based on tweet_id"""
        return tweet_id % self.num_shards
    
    def get_user_timeline_shard(self, user_id):
        """Get shard for user's tweets"""
        return user_id % self.num_shards
    
    async def store_tweet(self, tweet):
        shard = self.get_shard(tweet['tweet_id'])
        return await self.tweet_stores[shard].insert(tweet)
```

### Read Replica Strategy
```python
class DatabaseRouter:
    def __init__(self):
        self.primary_db = PrimaryDatabase()
        self.read_replicas = [ReadReplica1(), ReadReplica2(), ReadReplica3()]
        
    async def write_operation(self, query):
        """Route write operations to primary"""
        return await self.primary_db.execute(query)
    
    async def read_operation(self, query):
        """Route read operations to replicas"""
        replica = random.choice(self.read_replicas)
        return await replica.execute(query)
```

### Message Queue for Async Processing
```python
class TweetProcessor:
    def __init__(self):
        self.kafka_producer = KafkaProducer()
        
    async def process_new_tweet(self, tweet):
        """Async processing pipeline for new tweets"""
        tasks = [
            'extract_hashtags',
            'extract_mentions', 
            'detect_language',
            'moderate_content',
            'update_search_index',
            'fan_out_to_followers',
            'update_analytics'
        ]
        
        for task in tasks:
            await self.kafka_producer.send(f'tweet_{task}', tweet)
```

## 🔍 Search and Discovery

### Tweet Search Service
```python
class TweetSearchService:
    def __init__(self):
        self.elasticsearch = Elasticsearch()
        
    async def index_tweet(self, tweet):
        """Index tweet for search"""
        doc = {
            'tweet_id': tweet['tweet_id'],
            'content': tweet['content'],
            'hashtags': tweet['hashtags'],
            'user_id': tweet['user_id'],
            'username': tweet['username'],
            'created_at': tweet['created_at'],
            'likes_count': tweet['likes_count'],
            'retweets_count': tweet['retweets_count']
        }
        
        await self.elasticsearch.index(
            index='tweets',
            id=tweet['tweet_id'],
            body=doc
        )
    
    async def search_tweets(self, query, filters=None):
        """Search tweets with various filters"""
        search_body = {
            'query': {
                'multi_match': {
                    'query': query,
                    'fields': ['content', 'hashtags']
                }
            },
            'sort': [
                {'created_at': {'order': 'desc'}},
                {'_score': {'order': 'desc'}}
            ]
        }
        
        if filters:
            search_body['filter'] = filters
            
        result = await self.elasticsearch.search(
            index='tweets',
            body=search_body
        )
        
        return [hit['_source'] for hit in result['hits']['hits']]
```

### Trending Topics
```python
class TrendingService:
    def __init__(self):
        self.redis_client = redis.Redis()
        
    async def update_hashtag_count(self, hashtag):
        """Update hashtag trending score"""
        now = int(time.time())
        hour_bucket = now // 3600  # Hourly buckets
        
        # Increment count for current hour
        key = f"hashtag:{hashtag}:{hour_bucket}"
        await self.redis_client.incr(key)
        await self.redis_client.expire(key, 3600 * 24)  # 24 hour expiry
        
    async def get_trending_hashtags(self, limit=10):
        """Get currently trending hashtags"""
        now = int(time.time())
        current_hour = now // 3600
        
        # Get hashtag counts for last few hours
        trending_scores = {}
        for hour_offset in range(6):  # Last 6 hours
            hour = current_hour - hour_offset
            pattern = f"hashtag:*:{hour}"
            
            for key in await self.redis_client.keys(pattern):
                hashtag = key.split(':')[1]
                count = await self.redis_client.get(key)
                
                if hashtag not in trending_scores:
                    trending_scores[hashtag] = 0
                trending_scores[hashtag] += int(count) * (6 - hour_offset)  # Recent hours weighted more
        
        # Return top trending hashtags
        return sorted(trending_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
```

## 📊 Analytics and Monitoring

### Real-time Analytics
```python
class AnalyticsService:
    def __init__(self):
        self.time_series_db = InfluxDB()
        
    async def track_tweet_engagement(self, tweet_id, action, user_id):
        """Track engagement metrics"""
        metrics = {
            'measurement': 'tweet_engagement',
            'tags': {
                'tweet_id': tweet_id,
                'action': action,  # like, retweet, reply
                'user_id': user_id
            },
            'fields': {
                'count': 1
            },
            'time': datetime.utcnow()
        }
        
        await self.time_series_db.write(metrics)
    
    async def get_tweet_analytics(self, tweet_id, time_range='24h'):
        """Get analytics for specific tweet"""
        query = f"""
        SELECT sum(count) as total_engagement
        FROM tweet_engagement 
        WHERE tweet_id = '{tweet_id}' 
        AND time >= now() - {time_range}
        GROUP BY action
        """
        
        return await self.time_series_db.query(query)
```

### Performance Monitoring
```python
class SystemMonitor:
    def __init__(self):
        self.prometheus_client = PrometheusClient()
        
    async def monitor_timeline_latency(self):
        """Monitor timeline generation performance"""
        start_time = time.time()
        
        # Generate sample timeline
        timeline = await self.timeline_service.generate_timeline(sample_user_id)
        
        latency = time.time() - start_time
        
        # Record metric
        await self.prometheus_client.histogram(
            'timeline_generation_latency_seconds',
            latency,
            labels={'service': 'timeline'}
        )
        
        if latency > 0.2:  # Alert if >200ms
            await self.send_alert(f'High timeline latency: {latency:.3f}s')
```

## 🔒 Security and Privacy

### Rate Limiting
```python
class RateLimiter:
    def __init__(self):
        self.redis_client = redis.Redis()
        
    async def check_rate_limit(self, user_id, action, limit, window):
        """Check if user has exceeded rate limit"""
        key = f"rate_limit:{user_id}:{action}"
        current = await self.redis_client.get(key)
        
        if current is None:
            # First request in window
            await self.redis_client.setex(key, window, 1)
            return True
        elif int(current) < limit:
            # Within limit
            await self.redis_client.incr(key)
            return True
        else:
            # Rate limit exceeded
            return False

# Usage in API endpoint
@app.route('/api/v1/tweets', methods=['POST'])
async def create_tweet():
    user_id = get_current_user_id()
    
    # Check rate limit: 100 tweets per hour
    if not await rate_limiter.check_rate_limit(user_id, 'tweet', 100, 3600):
        return {'error': 'Rate limit exceeded'}, 429
    
    # Process tweet creation
    # ...existing code...
```

## 🚀 Future Enhancements

### Advanced Features
1. **Spaces (Audio Rooms)**: Live audio conversations
2. **Fleets/Stories**: Temporary content that disappears
3. **Communities**: Topic-based discussion groups
4. **Creator Monetization**: Super follows, tips, subscriptions
5. **Advanced Analytics**: Detailed engagement insights

### AI/ML Enhancements
1. **Content Recommendation**: Personalized timeline algorithms
2. **Sentiment Analysis**: Tweet sentiment scoring
3. **Spam Detection**: Automated content moderation
4. **Topic Modeling**: Automatic content categorization
5. **Personalized Trends**: User-specific trending topics

## 💡 Design Trade-offs

### Push vs Pull Timeline Generation
- **Push Model**: Fast reads, expensive writes, good for regular users
- **Pull Model**: Expensive reads, cheap writes, good for celebrities
- **Hybrid**: Use push for regular users, pull for celebrities

### Consistency vs Performance
- **Choice**: Eventual consistency for better performance
- **Reason**: Users can tolerate slight delays in timeline updates
- **Implementation**: Async processing with message queues

### Storage vs Query Performance
- **Choice**: Denormalized data for faster queries
- **Reason**: Read-heavy workload requires optimization
- **Implementation**: Duplicate user info in tweet records

---

## ✅ Success Criteria

This design successfully handles:
- ✅ **Scale**: 300M users, 400M tweets/day
- ✅ **Performance**: <200ms timeline generation
- ✅ **Availability**: 99.9% uptime with proper redundancy
- ✅ **Engagement**: Real-time likes, retweets, replies
- ✅ **Discovery**: Search and trending functionality

**Next Steps**: Implement social media prototype and explore advanced scaling techniques.