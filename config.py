import os

class Config:
    DATABASE_URL="postgresql://nacp_user:lvZjFz6BVT2kDEv3KKKKZ8J7mnJi30bb@dpg-d24s71fgi27c73bcq4l0-a.oregon-postgres.render.com/nacp"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("NoMoreAntiSocialPartyInTheFreeKorea!!20250836", "dev")
