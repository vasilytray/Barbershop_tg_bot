#!/bin/bash
# check-services.sh

echo "=== Проверка сервисов ==="

# Проверка портов
echo "1. Проверка доступности портов:"
for port in 3001 5050 9090 9187 9188 5434 5435; do
  if nc -z localhost $port 2>/dev/null; then
    echo "  ✓ Порт $port открыт"
  else
    echo "  ✗ Порт $port закрыт"
  fi
done

echo -e "\n2. Статус контейнеров:"
docker compose ps

echo -e "\n3. Доступ к базам данных:"
echo "   Основная БД:"
docker exec postgres-app psql -U ${POSTGRES_USER:-justes12} -d ${POSTGRES_DB:-manssalon_db} -c "SELECT version();" 2>/dev/null || echo "   Не удалось подключиться"

echo -e "\n   БД планировщика:"
docker exec postgres-scheduler psql -U ${SCHEDULER_DB_USER:-scheduler_user} -d ${SCHEDULER_DB_NAME:-scheduler_db} -c "SELECT version();" 2>/dev/null || echo "   Не удалось подключиться"

echo -e "\n4. URL для доступа:"
echo "   Grafana:     http://localhost:3001"
echo "   PgAdmin:     http://localhost:5050"
echo "   Prometheus:  http://localhost:9090"
echo "   Основная БД: localhost:5434"
echo "   БД планировщика: localhost:5435"