-- ./postgres/scheduler/init.sql
-- Настройки для БД планировщика
-- Упрощенные настройки для OLTP нагрузки
ALTER SYSTEM SET random_page_cost = 1.0;
ALTER SYSTEM SET effective_io_concurrency = 100;
SELECT 'Initializing scheduler database...';