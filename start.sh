#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Абсолютный путь к проекту (независимо от того откуда запущен скрипт)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo -e "${YELLOW}=== BarberBoss Dev Server ===${NC}"

# Убиваем старые процессы
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null
pkill -f "ngrok" 2>/dev/null
sleep 0.5

# Загружаем .env
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
else
    echo -e "${RED}Ошибка: файл .env не найден!${NC}"
    exit 1
fi

# Запускаем WebApp (порт 3000)
echo -e "${GREEN}[1/4] WebApp на порту 3000...${NC}"
python3 -m http.server 3000 --directory "$PROJECT_DIR/webapp" &>/dev/null &
WEBAPP_PID=$!

# Запускаем Django Admin (порт 8000)
echo -e "${GREEN}[2/4] Django Admin на порту 8000...${NC}"
(cd "$PROJECT_DIR/admin_panel" && python3 manage.py runserver 8000 &>/dev/null) &
DJANGO_PID=$!

# Запускаем ngrok
echo -e "${GREEN}[3/4] Запускаем ngrok...${NC}"
ngrok http 3000 --log=stdout &>/tmp/ngrok.log &
NGROK_PID=$!

# Ждём пока ngrok поднимется и получаем URL
echo -n "    Ждём ngrok URL"
NGROK_URL=""
for i in $(seq 1 15); do
    sleep 1
    echo -n "."
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tunnels = data.get('tunnels', [])
    for t in tunnels:
        if t.get('proto') == 'https':
            print(t['public_url'])
            break
except:
    pass
" 2>/dev/null)
    if [ -n "$NGROK_URL" ]; then
        break
    fi
done
echo ""

if [ -z "$NGROK_URL" ]; then
    echo -e "${RED}Не удалось получить ngrok URL. Проверь что ngrok установлен и авторизован.${NC}"
    echo -e "  Установка: brew install ngrok"
    echo -e "  Авторизация: ngrok config add-authtoken <твой_токен>"
    kill $WEBAPP_PID $DJANGO_PID $NGROK_PID 2>/dev/null
    exit 1
fi

# Обновляем WEBAPP_URL в .env
echo -e "${GREEN}    URL получен: ${NGROK_URL}${NC}"
if grep -q "WEBAPP_URL=" "$PROJECT_DIR/.env"; then
    sed -i '' "s|WEBAPP_URL=.*|WEBAPP_URL=${NGROK_URL}|" "$PROJECT_DIR/.env"
else
    echo "WEBAPP_URL=${NGROK_URL}" >> "$PROJECT_DIR/.env"
fi
export WEBAPP_URL="$NGROK_URL"

# Запускаем бота (уже с новым URL)
echo -e "${GREEN}[4/4] Telegram бот...${NC}"
python3 "$PROJECT_DIR/run_bot.py" &
BOT_PID=$!

echo ""
echo -e "${YELLOW}=============================${NC}"
echo -e "  WebApp:       ${GREEN}http://localhost:3000${NC}"
echo -e "  Публичный URL:${GREEN}${NGROK_URL}${NC}"
echo -e "  Django Admin: ${GREEN}http://localhost:8000/admin${NC}"
echo -e "  .env обновлён автоматически"
echo -e "${YELLOW}=============================${NC}"
echo -e "Нажми ${RED}Ctrl+C${NC} чтобы остановить всё"

trap "echo ''; echo -e '${RED}Останавливаем...${NC}'; kill $WEBAPP_PID $DJANGO_PID $NGROK_PID $BOT_PID 2>/dev/null; exit 0" INT

wait
