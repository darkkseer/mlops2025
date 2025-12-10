# RAG Animation System (Step 3)

Генерация анимаций по текстовому описанию с использованием RAG.

## Как работает
1. Получает запрос: `"танец макарена"`
2. Ищет релевантные позы в `data/poses_database.json`
3. LLM (через Ollama/vLLM на порту 11434) формирует последовательность
4. Pose API (порт 8001) рисует кадры
5. Кадры собираются в GIF

## Зависимости
- Запущенный **LLM сервер** на `http://localhost:11434` (Ollama/vLLM)
- Запущенный **Pose API** на `http://localhost:8001`
- Python ≥ 3.10, Poetry

## Установка и запуск

```bash
make install
make run
# Результат: outputs/macarena_dance.gif
```

## Выход

GIF-анимация по запросу (по умолчанию — "танец макарена").
