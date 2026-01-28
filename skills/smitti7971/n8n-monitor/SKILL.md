# Skill: n8n-monitor

Monitoramento operacional do N8N via Docker.

## Capabilities
- Verificar status dos containers N8N
- Ler logs recentes
- Checar saúde do container
- Analisar uso de CPU e memória

## Commands
- docker ps | grep n8n
- docker logs --tail 50 n8n
- docker inspect --format='{{.State.Health.Status}}' n8n
- docker stats --no-stream n8n

## Output
Respostas em Markdown, com tabelas simples e status claro.

## Status
active
