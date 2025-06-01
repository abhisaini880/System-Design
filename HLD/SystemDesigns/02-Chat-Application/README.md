# 💬 Chat Application System Design (WhatsApp)

## 📋 Problem Statement

Design a real-time chat application like WhatsApp, Telegram, or Signal that supports one-on-one and group messaging with high availability and low latency.

### Functional Requirements
1. **Messaging**: Send/receive text messages in real-time
2. **Group Chat**: Create groups, add/remove members
3. **Media Sharing**: Send images, videos, documents
4. **User Status**: Online/offline, last seen, typing indicators
5. **Message Status**: Sent, delivered, read receipts
6. **Push Notifications**: Offline message notifications

### Non-Functional Requirements
1. **Scale**: 50M daily active users, 1B messages/day
2. **Latency**: <100ms message delivery
3. **Availability**: 99.9% uptime
4. **Consistency**: Eventually consistent message ordering
5. **Security**: End-to-end encryption

## 📊 Capacity Estimation

### Traffic Estimates
- **Daily Messages**: 1B messages/day = 11,570 messages/second
- **Peak Traffic**: 3x average = 34,710 messages/second
- **Active Connections**: 50M users × 40% online = 20M concurrent connections
- **Group Messages**: 20% of total messages (fan-out required)

### Storage Estimates
- **Message Size**: Average 100 bytes per text message
- **Media Messages**: 10% of messages, average 1MB each
- **Daily Storage**: 1B × 100 bytes + 100M × 1MB = 100TB/day
- **5 Year Storage**: 100TB × 365 × 5 = 182PB

### Bandwidth Estimates
- **Incoming**: 34,710 messages/sec × 100 bytes = 3.5 MB/s
- **Outgoing**: 3.5 MB/s × average fan-out of 2 = 7 MB/s
- **Media Traffic**: 100M × 1MB / (24×3600) = 1.2 GB/s

## 🏗️ System Architecture

### High-Level Components

```
[Mobile Clients] → [Load Balancer] → [Gateway Service]
                                           ↓
[WebSocket Servers] ← → [Message Service] → [Notification Service]
        ↓                       ↓                    ↓
[Connection Manager] → [Message Queue] → [Push Service]
        ↓                       ↓                    ↓
[User Session Store] → [Message Database] → [Media Storage]
```

### Core Services
1. **Gateway Service**: API gateway, authentication, rate limiting
2. **WebSocket Service**: Real-time connections, message routing
3. **Message Service**: Message processing, storage, delivery
4. **User Service**: User management, presence, contacts
5. **Group Service**: Group creation, membership management
6. **Notification Service**: Push notifications for offline users
7. **Media Service**: File upload, storage, and delivery

## 🗄️ Database Design

### Message Table (Partitioned by Chat ID)
```sql
CREATE TABLE messages (
    message_id BIGINT PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    sender_id BIGINT NOT NULL,
    content TEXT,
    message_type ENUM('text', 'image', 'video', 'document'),
    media_url VARCHAR(512),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited_at TIMESTAMP NULL,
    reply_to_message_id BIGINT NULL,
    
    PARTITION BY HASH(chat_id) PARTITIONS 100,
    INDEX idx_chat_timestamp (chat_id, timestamp DESC),
    INDEX idx_sender (sender_id, timestamp DESC)
);
```

### Chat Table
```sql
CREATE TABLE chats (
    chat_id BIGINT PRIMARY KEY,
    chat_type ENUM('one_on_one', 'group'),
    name VARCHAR(255), -- for group chats
    created_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_message_id BIGINT,
    last_activity TIMESTAMP,
    
    INDEX idx_created_by (created_by),
    INDEX idx_last_activity (last_activity DESC)
);
```

### Chat Participants Table
```sql
CREATE TABLE chat_participants (
    chat_id BIGINT,
    user_id BIGINT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    left_at TIMESTAMP NULL,
    role ENUM('admin', 'member') DEFAULT 'member',
    last_read_message_id BIGINT DEFAULT 0,
    
    PRIMARY KEY (chat_id, user_id),
    INDEX idx_user_chats (user_id, joined_at DESC)
);
```

### User Presence Table (Redis)
```sql
-- Redis Hash Structure
HSET user:presence:123 
    status "online"
    last_seen "2024-06-01T10:00:00Z"
    device "mobile"
    socket_id "ws_conn_456"
```

## 🔧 Real-Time Architecture

### WebSocket Connection Management
```python
import asyncio
import websockets
import json
import redis

class WebSocketHandler:
    def __init__(self):
        self.connections = {}  # user_id -> websocket
        self.redis_client = redis.Redis()
        
    async def handle_connection(self, websocket, user_id):
        """Handle new WebSocket connection"""
        self.connections[user_id] = websocket
        await self.update_user_presence(user_id, "online")
        
        try:
            async for message in websocket:
                await self.handle_message(user_id, json.loads(message))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            del self.connections[user_id]
            await self.update_user_presence(user_id, "offline")
    
    async def handle_message(self, sender_id, message_data):
        """Process incoming message"""
        message = {
            'message_id': self.generate_message_id(),
            'chat_id': message_data['chat_id'],
            'sender_id': sender_id,
            'content': message_data['content'],
            'timestamp': time.time()
        }
        
        # Store message
        await self.store_message(message)
        
        # Get chat participants
        participants = await self.get_chat_participants(message['chat_id'])
        
        # Send to online participants
        for participant_id in participants:
            if participant_id in self.connections:
                await self.send_message(participant_id, message)
            else:
                # Queue for offline delivery
                await self.queue_offline_message(participant_id, message)
```

### Message Delivery System
```python
class MessageDeliveryService:
    def __init__(self):
        self.message_queue = MessageQueue()
        self.notification_service = NotificationService()
    
    async def deliver_message(self, message, recipients):
        """Deliver message to all recipients"""
        online_users = []
        offline_users = []
        
        for user_id in recipients:
            if await self.is_user_online(user_id):
                online_users.append(user_id)
            else:
                offline_users.append(user_id)
        
        # Real-time delivery to online users
        await self.deliver_to_online_users(message, online_users)
        
        # Push notifications for offline users
        await self.send_push_notifications(message, offline_users)
        
        # Update message status
        await self.update_message_status(message['message_id'], 'delivered')
```

## 🚀 API Design

### WebSocket Message Protocol

#### Send Message
```json
{
  "type": "send_message",
  "data": {
    "chat_id": 12345,
    "content": "Hello, how are you?",
    "message_type": "text",
    "reply_to": 67890
  }
}
```

#### Receive Message
```json
{
  "type": "new_message",
  "data": {
    "message_id": 98765,
    "chat_id": 12345,
    "sender_id": 456,
    "sender_name": "John Doe",
    "content": "I'm doing great, thanks!",
    "timestamp": "2024-06-01T10:30:00Z",
    "message_type": "text"
  }
}
```

### REST API Endpoints

#### Get Chat History
```http
GET /api/v1/chats/12345/messages?limit=50&before=98765

Response:
{
  "messages": [
    {
      "message_id": 98765,
      "sender_id": 456,
      "content": "Hello!",
      "timestamp": "2024-06-01T10:30:00Z",
      "message_type": "text",
      "status": "read"
    }
  ],
  "has_more": true,
  "next_cursor": 98700
}
```

#### Create Group Chat
```http
POST /api/v1/chats
Content-Type: application/json

{
  "chat_type": "group",
  "name": "Project Team",
  "participants": [123, 456, 789]
}

Response:
{
  "chat_id": 12345,
  "name": "Project Team",
  "participants": [123, 456, 789],
  "created_at": "2024-06-01T10:00:00Z"
}
```

## ⚡ Scalability Strategies

### Message Sharding
```python
class MessageSharding:
    def __init__(self, num_shards=1000):
        self.num_shards = num_shards
    
    def get_shard(self, chat_id):
        """Determine message shard based on chat_id"""
        return chat_id % self.num_shards
    
    def store_message(self, message):
        shard = self.get_shard(message['chat_id'])
        return self.message_stores[shard].insert(message)
```

### Connection Load Balancing
```python
class ConnectionBalancer:
    def __init__(self, websocket_servers):
        self.servers = websocket_servers
        self.user_server_map = {}  # user_id -> server_id
    
    def assign_server(self, user_id):
        """Assign user to least loaded server"""
        server = min(self.servers, key=lambda s: s.connection_count)
        self.user_server_map[user_id] = server.id
        return server
    
    def route_message(self, recipient_id, message):
        """Route message to correct server"""
        server_id = self.user_server_map.get(recipient_id)
        if server_id:
            return self.servers[server_id].send_message(recipient_id, message)
```

### Message Queue Architecture
```python
# Using Apache Kafka for message queuing
class MessageQueue:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['kafka1:9092', 'kafka2:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    async def publish_message(self, message):
        """Publish message to appropriate topic"""
        topic = f"chat_{message['chat_id'] % 100}"  # 100 partitions
        await self.producer.send(topic, message)
    
    async def process_messages(self):
        """Consumer to process queued messages"""
        consumer = KafkaConsumer(
            'chat_*',
            bootstrap_servers=['kafka1:9092', 'kafka2:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        async for message in consumer:
            await self.deliver_message(message.value)
```

## 📱 Push Notification System

### Notification Service
```python
class NotificationService:
    def __init__(self):
        self.fcm_client = FCMClient()  # Firebase Cloud Messaging
        self.apns_client = APNSClient()  # Apple Push Notification
    
    async def send_push_notification(self, user_id, message):
        """Send push notification to offline user"""
        user_devices = await self.get_user_devices(user_id)
        
        notification_data = {
            'title': message['sender_name'],
            'body': message['content'][:100],
            'chat_id': message['chat_id'],
            'message_id': message['message_id']
        }
        
        for device in user_devices:
            if device['platform'] == 'ios':
                await self.apns_client.send(device['token'], notification_data)
            elif device['platform'] == 'android':
                await self.fcm_client.send(device['token'], notification_data)
```

## 🔒 Security & Encryption

### End-to-End Encryption
```python
class MessageEncryption:
    def __init__(self):
        self.key_exchange = ECDHKeyExchange()
    
    def encrypt_message(self, message, recipient_public_key):
        """Encrypt message using recipient's public key"""
        shared_secret = self.key_exchange.generate_shared_secret(recipient_public_key)
        cipher = AES.new(shared_secret, AES.MODE_GCM)
        encrypted_content = cipher.encrypt(message['content'].encode())
        
        return {
            **message,
            'content': base64.b64encode(encrypted_content).decode(),
            'nonce': base64.b64encode(cipher.nonce).decode()
        }
    
    def decrypt_message(self, encrypted_message, sender_public_key):
        """Decrypt message using sender's public key"""
        shared_secret = self.key_exchange.generate_shared_secret(sender_public_key)
        cipher = AES.new(shared_secret, AES.MODE_GCM, 
                        nonce=base64.b64decode(encrypted_message['nonce']))
        
        decrypted_content = cipher.decrypt(
            base64.b64decode(encrypted_message['content'])
        )
        
        return {
            **encrypted_message,
            'content': decrypted_content.decode()
        }
```

## 📊 Monitoring & Analytics

### Key Metrics
- **Message Delivery Rate**: Percentage of messages delivered successfully
- **Connection Latency**: WebSocket connection establishment time
- **Message Latency**: Time from send to receive
- **Active Connections**: Number of concurrent WebSocket connections
- **Push Notification Delivery Rate**: Offline notification success

### Health Monitoring
```python
class HealthMonitor:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
    
    async def monitor_message_latency(self):
        """Monitor end-to-end message delivery latency"""
        start_time = time.time()
        # Send test message
        await self.send_test_message()
        # Measure delivery time
        latency = time.time() - start_time
        
        self.metrics_collector.record('message_latency', latency)
        
        if latency > 0.1:  # Alert if >100ms
            await self.send_alert('High message latency detected')
```

## 🚀 Future Enhancements

### Advanced Features
1. **Voice/Video Calls**: WebRTC integration for real-time communication
2. **Message Reactions**: Emoji reactions to messages
3. **Message Threading**: Reply chains and conversations
4. **Bot Integration**: Automated responses and commands
5. **Message Scheduling**: Send messages at specific times

### Performance Optimizations
1. **Message Caching**: Cache recent messages in Redis
2. **Connection Pooling**: Optimize WebSocket connection management
3. **Geographic Distribution**: Deploy servers closer to users
4. **Compression**: Compress message payloads for bandwidth efficiency

## 💡 Design Trade-offs

### Consistency vs Availability
- **Choice**: Eventual consistency for better availability
- **Reason**: Users prefer fast message delivery over perfect ordering
- **Implementation**: Use vector clocks for message ordering

### Storage vs Performance
- **Choice**: Denormalized data for faster queries
- **Reason**: Read-heavy workload requires optimized retrieval
- **Implementation**: Duplicate user data in message records

### Security vs Performance
- **Choice**: End-to-end encryption with performance optimization
- **Reason**: Privacy is critical but shouldn't impact user experience
- **Implementation**: Efficient crypto libraries and key caching

---

## ✅ Success Criteria

This design successfully handles:
- ✅ **Scale**: 50M DAU, 1B messages/day
- ✅ **Performance**: <100ms message delivery
- ✅ **Availability**: 99.9% uptime with redundancy
- ✅ **Security**: End-to-end encryption
- ✅ **Real-time**: WebSocket-based instant messaging

**Next Steps**: Study Social Media Platform design and implement chat prototype.