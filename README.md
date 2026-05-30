# mcp-serverless

An MCP server running on Nebius Serverless Endpoints. Receives tool calls from Claude Desktop and forwards them to Nebius Token Factory for text embeddings.

## Architecture

Claude Desktop -> bridge.py (stdio) -> Nebius Endpoint (HTTP) -> Token Factory (Qwen3-Embedding-8B)

## Hardware

- Endpoint: Non-GPU AMD Epyc Genoa, 4 vCPU, 16 GiB RAM
- Region: eu-north1
- Approximate cost: $0.14/hour

## Setup

1. Build and push the image:

```
docker build -t mcp-server .
docker tag mcp-server mesutoezdil/mcp-server:latest
docker push mesutoezdil/mcp-server:latest
```

2. Create the Nebius endpoint:

```
nebius ai endpoint create \
  --name mcp-server-endpoint \
  --image docker.io/mesutoezdil/mcp-server:latest \
  --container-port 8000 \
  --env "name=NEBIUS_API_KEY,value=<your-token-factory-key>" \
  --platform cpu-d3 \
  --preset 4vcpu-16gb \
  --public
```

3. Set the endpoint URL in bridge.py and add to Claude Desktop config.

## Expected Output

embedding_dim: 4096, latency: ~139ms from Germany to eu-north1

## License

MIT
