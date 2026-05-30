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

3. Configure `bridge.py` and Claude Desktop (see Configuration below).

## Configuration

`bridge.py` reads the endpoint URL from the `NEBIUS_ENDPOINT` environment variable, defaulting to `http://localhost:8000` if unset. Point it at your Nebius endpoint by setting the variable.

Run the bridge standalone:

```
export NEBIUS_ENDPOINT="http://<your-endpoint-host>:8000"
python3 bridge.py
```

Wire it into Claude Desktop by editing `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "nebius-serverless": {
      "command": "/Users/<you>/mcp-bridge-env/bin/python3",
      "args": ["/Users/<you>/mcp-bridge-env/bridge.py"],
      "env": {
        "NEBIUS_ENDPOINT": "http://<your-endpoint-host>:8000"
      }
    }
  }
}
```

Restart Claude Desktop after editing the config. Logs land at `~/Library/Logs/Claude/mcp-server-nebius-serverless.log`.

## Expected Output

embedding_dim: 4096, latency: ~139ms from Germany to eu-north1

## License

MIT
