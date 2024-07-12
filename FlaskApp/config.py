import uuid

class Config:
    SECRET_KEY = str(hex(uuid.getnode())) + str(uuid.uuid4().hex) 
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 1800


