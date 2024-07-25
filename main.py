import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.models import Worker
from src.orm import SyncORM, AsyncORM
from src.core import SyncCore

# SyncCore.create_tables()
# SyncORM.create_tables()

# SyncCore.insert_workers()
# SyncORM.insert_workers()

# SyncCore.insert_resumes()
# SyncCore.insert_additional_resumes()

# SyncORM.insert_resumes()
# SyncORM.insert_additional_resumes()

# SyncCore.select_workers()
# SyncORM.select_workers()

# SyncCore.select_resumes()
# SyncORM.select_resumes()

# SyncORM.select_workers_with_lazy_relationship()
# SyncORM.select_workers_with_joined_relationship()
# SyncORM.select_workers_with_selectin_relationship()
# SyncORM.select_parttime_resumes()
# SyncORM.select_parttime_resumes_contains_eager()
# SyncORM.select_parttime_resumes_contains_eager_with_limit()
# SyncORM.select_without_relationship()
# SyncORM.select_with_relationship()
# SyncORM.select_with_relationship_resume_statuses()
# SyncORM.add_vacancies_and_replies()
# SyncORM.select_resumes_with_all_relationships()
# SyncORM.select_vacancy_with_all_relationships()

# SyncCore.update_worker()
# SyncORM.update_worker()

# SyncCore.select_resumes_avg_compensation()
# SyncORM.select_resumes_avg_compensation()

# asyncio.run(AsyncORM.join_cte_subquery_window_func())


def create_fastapi_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*']
    )

    @app.get('/workers')
    async def get_workers():
        # workers = SyncORM.select_with_relationship()
        # return workers

        # resumes = SyncORM.select_with_relationship_resume_statuses()
        resumes = SyncORM.select_vacancy_with_all_relationships()
        return resumes

    return app


app = create_fastapi_app()


if __name__ == '__main__':
    # asyncio.run()
    uvicorn.run(
        app='main:app',
        reload=True,
    )
