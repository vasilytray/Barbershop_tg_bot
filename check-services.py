# check-services.py
import subprocess
import socket
import os
import sys

def check_port(host, port):
    """Проверяет доступность порта"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result == 0
    except:
        return False

def run_command(cmd):
    """Выполняет команду и возвращает результат"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def main():
    print("=== Проверка сервисов ===")
    
    # 1. Проверка портов
    print("\n1. Проверка доступности портов:")
    ports = [3001, 5050, 9090, 9187, 9188, 5434, 5435]
    for port in ports:
        if check_port('localhost', port):
            print(f"  ✓ Порт {port} открыт")
        else:
            print(f"  ✗ Порт {port} закрыт")
    
    # 2. Статус контейнеров
    print("\n2. Статус контейнеров:")
    code, output, error = run_command('docker compose ps')
    if code == 0:
        print(output)
    else:
        print(f"Ошибка: {error}")
    
    # 3. Проверка БД (используем переменные окружения)
    print("\n3. Проверка подключения к базам данных:")
    
    # Основная БД
    print("   Основная БД:")
    db_user = os.getenv('POSTGRES_USER', 'justes12')
    db_name = os.getenv('POSTGRES_DB', 'manssalon_db')
    cmd = f'docker exec postgres-app psql -U {db_user} -d {db_name} -c "SELECT version();"'
    code, output, error = run_command(cmd)
    if code == 0:
        print("   Подключение успешно:")
        for line in output.split('\n'):
            if line.strip():
                print(f"   {line}")
    else:
        print("   Не удалось подключиться")
    
    # БД планировщика
    print("\n   БД планировщика:")
    scheduler_user = os.getenv('SCHEDULER_DB_USER', 'scheduler_user')
    scheduler_db = os.getenv('SCHEDULER_DB_NAME', 'scheduler_db')
    cmd = f'docker exec postgres-scheduler psql -U {scheduler_user} -d {scheduler_db} -c "SELECT version();"'
    code, output, error = run_command(cmd)
    if code == 0:
        print("   Подключение успешно:")
        for line in output.split('\n'):
            if line.strip():
                print(f"   {line}")
    else:
        print("   Не удалось подключиться")
    
    # 4. URL
    print("\n4. URL для доступа:")
    urls = [
        ("Grafana", "http://localhost:3001"),
        ("PgAdmin", "http://localhost:5050"),
        ("Prometheus", "http://localhost:9090"),
        ("Основная БД", "localhost:5434"),
        ("БД планировщика", "localhost:5435")
    ]
    for name, url in urls:
        print(f"   {name}: {url}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()