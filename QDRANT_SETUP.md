# Qdrant Setup Guide

This guide explains how to set up Qdrant as a separate service for the Revenue Leakage Detection System.

## Option 1: Qdrant Cloud (Recommended for Production)

### 1. Sign up for Qdrant Cloud
1. Go to [Qdrant Cloud](https://cloud.qdrant.io/)
2. Sign up for an account
3. Create a new cluster

### 2. Get Connection Details
After creating your cluster, you'll get:
- **Cluster URL**: `https://xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.region.aws.cloud.qdrant.io:6333`
- **API Key**: `your-api-key-here`

### 3. Configure Streamlit Cloud Secrets
In your Streamlit Cloud app settings, add these secrets:
```
QDRANT_HOST = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.region.aws.cloud.qdrant.io"
QDRANT_PORT = 6333
QDRANT_API_KEY = "your-api-key-here"
QDRANT_USE_HTTPS = true
```

## Option 2: Self-hosted Qdrant with Docker

### 1. Run Qdrant Container
```bash
docker run -p 6333:6333 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

### 2. Access Qdrant Dashboard
Open your browser and go to: http://localhost:6333/dashboard

### 3. Configure for Remote Access (Optional)
To make your self-hosted Qdrant accessible from Streamlit Cloud, you'll need to:
1. Expose your local Qdrant to the internet using a tunnel service like ngrok:
   ```bash
   ngrok http 6333
   ```
2. Use the ngrok URL as your QDRANT_HOST

## Option 3: Qdrant on Render (Free Tier)

### 1. Deploy Qdrant on Render
1. Go to [Render](https://render.com/)
2. Create a new Web Service
3. Use these settings:
   - **Public Git repository**: `https://github.com/qdrant/qdrant`
   - **Build command**: `cargo build --release`
   - **Start command**: `./target/release/qdrant`
   - **Instance type**: Free

### 2. Alternative: Use Render Blueprint
1. Fork this repository
2. Create a `render.yaml` file:
   ```yaml
   services:
     - type: web
       name: qdrant
       env: docker
       repo: https://github.com/qdrant/qdrant.git
       plan: free
       healthCheckPath: /
       envVars:
         - key: QDRANT__SERVICE__API_KEY
           sync: false
   ```

## Configuration for the Revenue Leakage Detection System

### Environment Variables
Set these environment variables in your deployment environment:

```bash
# For Qdrant Cloud
QDRANT_HOST=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.region.aws.cloud.qdrant.io
QDRANT_PORT=6333
QDRANT_API_KEY=your-api-key-here
QDRANT_USE_HTTPS=true

# For self-hosted (local)
QDRANT_HOST=localhost
QDRANT_PORT=6333
# QDRANT_API_KEY= (optional for local)
# QDRANT_USE_HTTPS=false (default)
```

### Testing the Connection
You can test your Qdrant connection with this Python script:

```python
from qdrant_client import QdrantClient

# For Qdrant Cloud
client = QdrantClient(
    host="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.region.aws.cloud.qdrant.io",
    port=6333,
    api_key="your-api-key-here",
    https=True
)

# For self-hosted
# client = QdrantClient(host="localhost", port=6333)

# Test connection
try:
    info = client.get_collections()
    print("Qdrant connection successful!")
    print(info)
except Exception as e:
    print(f"Connection failed: {e}")
```

## Integration with Revenue Leakage Detection System

The system is already configured to work with external Qdrant instances. Just set these environment variables:

```
QDRANT_HOST = "your-qdrant-host"
QDRANT_PORT = 6333
QDRANT_API_KEY = "your-api-key-if-required"  # Optional for self-hosted
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Network Security**: Restrict access to your Qdrant instance
3. **Encryption**: Use HTTPS for all connections in production
4. **Backups**: Regularly backup your Qdrant data