from database import make_session
from models import Message, Conversation
from sqlalchemy import select

db = make_session()

conversation_1 = Conversation(created_at="12:13")

db.add(conversation_1)
db.commit()

message0 = Message(
    conversation_id=conversation_1.id,
    role="user",
    content="اسم من دانیال هست",
    created_at="12:34"
)
message1 = Message(
    conversation_id=conversation_1.id,
    role="assistant",
    content="خوشبختم دانیال",
    created_at="12:35"
)
message2 = Message(
    conversation_id=conversation_1.id,
    role="user",
    content="اسم من چی بود؟",
    created_at="12:36"
)

db.add(message0)
db.add(message1)
db.add(message2)
db.commit()

statement = select(Message).where(Message.conversation_id == conversation_1.id)

result = db.execute(statement)

messages = result.scalars().all()

for message in messages:
    print(message.role + " : " + message.content)
