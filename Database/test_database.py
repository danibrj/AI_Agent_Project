
# from database import get_db
# from models import Message, Conversation
# from sqlalchemy import select
# import sys

# sys.stdout.reconfigure(encoding="utf-8")



# db_generator = get_db()
# db = next(db_generator)

# try:
#     db.query(Message).delete(synchronize_session=False)
#     db.query(Conversation).delete(synchronize_session=False)

#     db.commit()

#     print("Database cleared successfully!")

# finally:
#     try:
#         next(db_generator)
#     except StopIteration:
#         pass


# # # def test(statement):
# # #     result = db.execute(statement)
# # #     messages = result.scalars().all()

# # #     message_list = []
# # #     for massage in messages:
# # #         l.append({
# # #             "role" : massage.role,
# # #             "content" : massage.content
# # #         })
# # #     return message_list


# # # try:

# # #     conversation_1 = (
# # #         db.query(Conversation)
# # #         .filter_by(test_key="history_test_1")
# # #         .first()
# # #     )

# # #     if conversation_1 is None:
# # #         conversation_1 = Conversation(
# # #             test_key="history_test_1",
# # #             created_at="12:13"
# # #         )
# # #         db.add(conversation_1)

# # #     conversation_2 = (
# # #         db.query(Conversation)
# # #         .filter_by(test_key="history_test_2")
# # #         .first()
# # #     )

# # #     if conversation_2 is None:
# # #         conversation_2 = Conversation(
# # #             test_key="history_test_2",
# # #             created_at="7:52"
# # #         )
# # #         db.add(conversation_2)

# # #     db.commit()


# # #     db.query(Message).filter(
# # #         Message.conversation_id.in_(
# # #             [conversation_1.id, conversation_2.id]
# # #         )
# # #     ).delete(synchronize_session=False)

# # #     db.commit()


# # #     messages = [
# # #         Message(
# # #             conversation_id=conversation_1.id,
# # #             role="user",
# # #             content="اسم من دانیال هست",
# # #             created_at="12:34"
# # #         ),
# # #         Message(
# # #             conversation_id=conversation_1.id,
# # #             role="assistant",
# # #             content="خوشبختم دانیال",
# # #             created_at="12:35"
# # #         ),
# # #         Message(
# # #             conversation_id=conversation_2.id,
# # #             role="user",
# # #             content="تو کی هستی",
# # #             created_at="8:02"
# # #         ),
# # #         Message(
# # #             conversation_id=conversation_1.id,
# # #             role="user",
# # #             content="اسم من چی بود؟",
# # #             created_at="12:36"
# # #         ),
# # #         Message(
# # #             conversation_id=conversation_2.id,
# # #             role="assistant",
# # #             content="من مدل هوش مصنوعی هستم",
# # #             created_at="9:06"
# # #         )
# # #     ]

# # #     db.add_all(messages)
# # #     db.commit()


# # #     statement0 = (
# # #         select(Message)
# # #         .where(
# # #             Message.conversation_id == conversation_1.id
# # #         )
# # #         .order_by(Message.id)
# # #     )

# # #     print(test(statement0))

# # #     print("-----")


# # #     statement1 = (
# # #         select(Message)
# # #         .where(
# # #             Message.conversation_id == conversation_2.id
# # #         )
# # #         .order_by(Message.id)
# # #     )

# # #     print(test(statement1))

# # # finally:

# # #     try:
# # #         next(db_generator)
# # #     except StopIteration:
# # #         pass
