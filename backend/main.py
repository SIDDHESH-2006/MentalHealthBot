from fastapi import FastAPI
from routes import user_routes, journal_routes, analysis_routes
from routes.auth_routes import router as auth_router
from routes.journal_routes import router as journal_router
from routes.user_routes import router as user_router
from routes.analysis_routes import router as analysis_router
app.include_router(user_router)
app.include_router(journal_router)
app.include_router(auth_router)
app = FastAPI(title="MoodJournal.AI API")
app.include_router(user_routes.router)
app.include_router(journal_routes.router)
app.include_router(analysis_routes.router)