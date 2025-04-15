import aio_pika
import json

from app.database.db import get_db_session
from app.services.calendar import CalendarService
from app.schemas.calendar import CalendarCreate
from app.config import settings

# Обработчик события, который создаёт календарь для пользователя
async def handle_user_created(message: aio_pika.IncomingMessage):
    async with message.process():  # Обрабатываем сообщение
        data = json.loads(message.body)  # Декодируем сообщение
        user_id = data.get("user_id")

        # Создаём календарь для пользователя в базе данных
        async with get_db_session() as db:
            service = CalendarService(db)
            await service.create_calendar(owner_id=user_id, calendar_data=CalendarCreate())

# Запуск слушателя
async def start_calendar_event_listener():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)  # Подключаемся к RabbitMQ
    channel = await connection.channel()  # Открываем канал
    exchange = await channel.declare_exchange("user_events", aio_pika.ExchangeType.FANOUT)  # Обменник событий
    queue = await channel.declare_queue("", exclusive=True)  # Создаём временную очередь
    await queue.bind(exchange)  # Привязываем очередь к обменнику

    # Подписываемся на события
    await queue.consume(handle_user_created)
