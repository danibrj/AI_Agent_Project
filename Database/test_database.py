from database import get_db
from models import Message, Conversation
from sqlalchemy import select
import sys

sys.stdout.reconfigure(encoding="utf-8")

db = get_db()

#----------------general test----------------
# conversations = db.query(Conversation).all()

# print("=== Conversations ===")

# for conversation in conversations:
#     print(conversation.__dict__)


# messages = db.query(Message).all()

# print("\n=== Messages ===")

# for message in messages:
#     print(message.__dict__)
#--------------------------------------------

def test(statement):

    result = db.execute(statement)

    messages = result.scalars().all()

    for message in messages:
        print(message.role + " : " + message.content)

# create conversation
conversation_1 = Conversation(created_at="12:13")
conversation_2 = Conversation(created_at="7:52")



db.add(conversation_1)
db.add(conversation_2)
db.commit()

# save the messages
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
    conversation_id=conversation_2.id,
    role="user",
    content="تو کی هستی",
    created_at="8:02"
)
message3 = Message(
    conversation_id=conversation_1.id,
    role="user",
    content="اسم من چی بود؟",
    created_at="12:36"
)
message4 = Message(
    conversation_id=conversation_2.id,
    role="assistant",
    content="من مدل هوش مصنوعی هستم",
    created_at="9:06"
)


db.add(message0)
db.add(message1)
db.add(message2)
db.add(message3)
db.add(message4)
db.commit()

# read history
#test1:
statement0 = select(Message).where(Message.conversation_id == conversation_1.id)

test(statement0)

print("-----")
#test2:
statement1 = select(Message).where(Message.conversation_id == conversation_2.id)

test(statement1)

