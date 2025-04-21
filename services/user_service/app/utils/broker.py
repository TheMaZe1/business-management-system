import json

import aio_pika

from app.config import settings


RABBITMQ_URL = settings.RABBITMQ_URL

# Подключаемся к RabbitMQ
async def get_connection():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    return connection

# Метод для отправки события "пользователь создан"
async def publish_user_created_event(user_id: int):
    connection = await get_connection()
    async with connection:
        channel = await connection.channel()  # Открываем канал
        exchange = await channel.declare_exchange("user_events", aio_pika.ExchangeType.FANOUT)

        # Публикуем сообщение в обменник
        message = aio_pika.Message(
            body=json.dumps({"user_id": user_id}).encode()
        )

        await exchange.publish(message, routing_key="")  # Публикуем сообщение

# Тут можно добавить другие методы для работы с RabbitMQ, например:
# - подписка на события
# - отправка других типов сообщений (например, для meetings, calendars)