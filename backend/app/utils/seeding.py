import asyncio

from faker import Faker

from app import crud
from app.utils.dependencies import get_db

fake = Faker()


def create_user():
    return crud.Users.create(
        username=fake.user_name(),
        password="pass",
        email=fake.safe_email()
    )


def create_chat():
    return crud.Chats.create(
        name=fake.user_name()
    )


def create_message(sender_id: int, chat_id: int = None):
    return crud.Messages.create(
        user_id=sender_id,
        body=fake.text(),
        chat_id=chat_id
    )


async def user_join_chat(chat_id: int, user_id: int):
    return await crud.ChatUsers.create(chat_id=chat_id, user_id=user_id)


async def create_chat_with_users_and_messages():
    users_from_others_chat = await crud.Users.get_many()
    chat = await create_chat()
    users_ids = []
    # add some existing users to chat
    if users_from_others_chat:
        for user in fake.random_choices(users_from_others_chat, 30):
            users_ids.append(user.id)
            await user_join_chat(chat_id=chat.id, user_id=user.id)
    # create new users and add them to chat
    for _ in range(fake.random_int(10, 20)):
        user = await create_user()
        users_ids.append(user.id)
        await user_join_chat(chat_id=chat.id, user_id=user.id)
    # create random messages
    for user_id in fake.random_choices(users_ids, 100):
        await create_message(sender_id=user_id, chat_id=chat.id)


async def create_filled_chats():
    for _ in range(fake.random_int(3, 7)):
        await create_chat_with_users_and_messages()


def main():
    async def db_seeding():
        async for _ in get_db():
            await create_filled_chats()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(db_seeding())


if __name__ == '__main__':
    main()
