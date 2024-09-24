docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -e OPENAI_API_KEY=token-abc123 -e OPENAI_API_BASE_URL=https://hoangpn.hungphu.org/v1 -e WEBUI_AUTH=False -v ./backend/data:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main


docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -e WEBUI_AUTH=False -v ./backend/data:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main


docker compose -f docker-compose-ui-be.yaml up -d --build
