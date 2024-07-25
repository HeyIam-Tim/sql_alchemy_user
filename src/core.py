from sqlalchemy import Integer, and_, func, text, insert, select, update
from .database import sync_engine, async_engine
from .models import metadata_obj, worker_table, resume_table, Workload


class SyncCore:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        """Insert data"""

        with sync_engine.connect() as conn:
            # stmt = """INSERT INTO workers (username) VALUES
            #     ('Jack'),
            #     ('Michael');"""
            stmt = insert(worker_table).values(
                [
                    {"username": "Jack"},
                    {"username": "Michael"},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(worker_table)
            result = conn.execute(query)
            workers = result.all()
            print(f'{workers=}')

    @staticmethod
    def select_resumes():
        with sync_engine.connect() as session:
            query = select(resume_table)
            result = session.execute(query)
            resumes = result.all()
            print(f'{resumes=}')

    # @staticmethod
    # def select_workers():
    #     with sync_engine.connect() as conn:
    #         query = select(workers_table)  # SELECT * FROM workers
    #         result = conn.execute(query)
    #         workers = result.all()
    #         print(f"{workers=}")

    @staticmethod
    def update_worker(worker_id: int = 1, new_username: str = 'John'):
        with sync_engine.connect() as conn:
            # stmt = text("""UPDATE worker SET username=:username WHERE id=:id""")
            # stmt = stmt.bindparams(username=new_username, id=worker_id)

            stmt = (
                update(worker_table)
                .values(username=f'{new_username}/CORE')
                .filter_by(id=worker_id)
            )
            conn.execute(stmt)
            conn.commit()

    # @staticmethod
    # def update_worker(worker_id: int = 2, new_username: str = "Misha"):
    #     with sync_engine.connect() as conn:
    #         # stmt = text("UPDATE workers SET username=:username WHERE id=:id")
    #         # stmt = stmt.bindparams(username=new_username, id=worker_id)
    #         stmt = (
    #             update(workers_table)
    #             .values(username=new_username)
    #             # .where(workers_table.c.id==worker_id)
    #             .filter_by(id=worker_id)
    #         )
    #         conn.execute(stmt)
    #         conn.commit()

    @staticmethod
    def insert_resumes():
        with sync_engine.connect() as conn:
            resumes = [
                {"title": "Python Junior Developer", "compensation": 50000, "workload": Workload.fulltime,
                 "worker_id": 1},
                {"title": "Python Разработчик", "compensation": 150000, "workload": Workload.fulltime, "worker_id": 1},
                {"title": "Python Data Engineer", "compensation": 250000, "workload": Workload.parttime,
                 "worker_id": 2},
                {"title": "Data Scientist", "compensation": 300000, "workload": Workload.fulltime, "worker_id": 2},
            ]
            stmt = insert(resume_table).values(resumes)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        having avg(compensation) > 70000
        """
        with sync_engine.connect() as conn:
            query = (
                select(
                    resume_table.c.workload,
                    # 1 вариант использования cast
                    # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
                    # 2 вариант использования cast (предпочтительный способ)
                    func.avg(resume_table.c.compensation).cast(Integer).label("avg_compensation"),
                )
                .select_from(resume_table)
                .filter(and_(
                    resume_table.c.title.contains(like_language),
                    resume_table.c.compensation > 40000,
                ))
                .group_by(resume_table.c.workload)
                .having(func.avg(resume_table.c.compensation) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = conn.execute(query)
            result = res.all()
            print(result[0].avg_compensation)

    @staticmethod
    def insert_additional_resumes():
        with sync_engine.connect() as conn:
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},   # id 5
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "parttime", "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload": "parttime", "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload": "fulltime", "worker_id": 5},
            ]
            insert_workers = insert(worker_table).values(workers)
            insert_resumes = insert(resume_table).values(resumes)
            conn.execute(insert_workers)
            conn.execute(insert_resumes)
            conn.commit()


# class AsyncCore:
#     # Асинхронный вариант, не показанный в видео
#     @staticmethod
#     async def create_tables():
#         async with async_engine.begin() as conn:
#             await conn.run_sync(metadata_obj.drop_all)
#             await conn.run_sync(metadata_obj.create_all)
#
#     @staticmethod
#     async def insert_workers():
#         async with async_engine.connect() as conn:
#             # stmt = """INSERT INTO workers (username) VALUES
#             #     ('Jack'),
#             #     ('Michael');"""
#             stmt = insert(workers_table).values(
#                 [
#                     {"username": "Jack"},
#                     {"username": "Michael"},
#                 ]
#             )
#             await conn.execute(stmt)
#             await conn.commit()
#
#     @staticmethod
#     async def select_workers():
#         async with async_engine.connect() as conn:
#             query = select(workers_table)  # SELECT * FROM workers
#             result = await conn.execute(query)
#             workers = result.all()
#             print(f"{workers=}")
#
#     @staticmethod
#     async def update_worker(worker_id: int = 2, new_username: str = "Misha"):
#         async with async_engine.connect() as conn:
#             # stmt = text("UPDATE workers SET username=:username WHERE id=:id")
#             # stmt = stmt.bindparams(username=new_username, id=worker_id)
#             stmt = (
#                 update(workers_table)
#                 .values(username=new_username)
#                 # .where(workers_table.c.id==worker_id)
#                 .filter_by(id=worker_id)
#             )
#             await conn.execute(stmt)
#             await conn.commit()
#
#     @staticmethod
#     async def insert_resumes():
#         async with async_engine.connect() as conn:
#             resumes = [
#                 {"title": "Python Junior Developer", "compensation": 50000, "workload": Workload.fulltime,
#                  "worker_id": 1},
#                 {"title": "Python Разработчик", "compensation": 150000, "workload": Workload.fulltime, "worker_id": 1},
#                 {"title": "Python Data Engineer", "compensation": 250000, "workload": Workload.parttime,
#                  "worker_id": 2},
#                 {"title": "Data Scientist", "compensation": 300000, "workload": Workload.fulltime, "worker_id": 2},
#             ]
#             stmt = insert(resumes_table).values(resumes)
#             await conn.execute(stmt)
#             await conn.commit()
#
#     @staticmethod
#     async def select_resumes_avg_compensation(like_language: str = "Python"):
#         """
#         select workload, avg(compensation)::int as avg_compensation
#         from resumes
#         where title like '%Python%' and compensation > 40000
#         group by workload
#         having avg(compensation) > 70000
#         """
#         async with async_engine.connect() as conn:
#             query = (
#                 select(
#                     resumes_table.c.workload,
#                     # 1 вариант использования cast
#                     # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
#                     # 2 вариант использования cast (предпочтительный способ)
#                     func.avg(resumes_table.c.compensation).cast(Integer).label("avg_compensation"),
#                 )
#                 .select_from(resumes_table)
#                 .filter(and_(
#                     resumes_table.c.title.contains(like_language),
#                     resumes_table.c.compensation > 40000,
#                 ))
#                 .group_by(resumes_table.c.workload)
#                 .having(func.avg(resumes_table.c.compensation) > 70000)
#             )
#             print(query.compile(compile_kwargs={"literal_binds": True}))
#             res = await conn.execute(query)
#             result = res.all()
#             print(result[0].avg_compensation)
