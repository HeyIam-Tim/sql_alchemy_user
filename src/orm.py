from sqlalchemy import select, func, cast, Integer, and_, String, insert
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager

from .database import sync_engine, Base, session_factory, async_session_factory
from .models import Worker, Resume, Workload, Status, StatusStates, Vacancy
from .schemas import WorkersDTO, WorkersRelDTO, WorkloadAvgCompensationDTO, ResumesRelDTO


# def create_tables():
#     sync_engine.echo = False
#     Base.metadata.drop_all(sync_engine)
#     sync_engine.echo = True
#     Base.metadata.create_all(sync_engine)
#     # sync_engine.echo = True


# def insert_data():
#     with session_factory() as session:
#         worker1 = Worker(username='Ivan')
#         worker2 = Worker(username='Aman')
#         # session.add(worker1)
#         session.add_all([worker1, worker2])
#         session.commit()


# async def insert_data():
#     async with async_session_factory() as session:
#         worker1 = Worker(username='Ivan')
#         worker2 = Worker(username='Aman')
#         # session.add(worker1)
#         session.add_all([worker1, worker2])
#         await session.commit()


# from sqlalchemy import Integer, and_, text, insert, inspect, select, func, cast
# from database import sync_engine, async_engine, session_factory, async_session_factory, Base
# from models import WorkersOrm, ResumesOrm, Workload
#
#
class SyncORM:
    @staticmethod
    def create_tables():
        # sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker1 = Worker(username="Jack")
            worker2 = Worker(username="Johnathan")
            worker3 = Worker(username="Artem")
            worker4 = Worker(username="Roman")
            worker5 = Worker(username="Nurlan")
            worker6 = Worker(username="Kamal")

            session.add_all([worker1, worker2, worker3, worker4, worker5, worker6])
            # flush отправляет запрос в базу данных
            # После flush каждый из работников получает первичный ключ id, который отдала БД
            session.flush()
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            # worker_id = 1
            # worder1 = session.get(Worker, worker_id)
            query = select(Worker)
            result = session.execute(query)
            workers = result.all()
            print(f'{workers=}')

    @staticmethod
    def select_resumes():
        with session_factory() as session:
            query = select(Resume)
            result = session.execute(query)
            resumes = result.all()
            print(f'{resumes=}')

    @staticmethod
    def update_worker(worker_id: int = 1, new_username: str = 'Jackeb'):
        with session_factory() as session:
            worker1 = session.get(Worker, worker_id)
            worker1.username = new_username
            session.commit()

    #
    # @staticmethod
    # def update_worker(worker_id: int = 2, new_username: str = "Misha"):
    #     with session_factory() as session:
    #         worker_michael = session.get(WorkersOrm, worker_id)
    #         worker_michael.username = new_username
    #         # refresh нужен, если мы хотим заново подгрузить данные модели из базы.
    #         # Подходит, если мы давно получили модель и в это время
    #         # данные в базе данныхмогли быть изменены
    #         session.refresh(worker_michael)
    #         session.commit()
    #
    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_jack_1 = Resume(
                title="Python Junior Developer", compensation=50000, workload=Workload.fulltime, worker_id=1)

            status_new = Status(resume_id=1, state=StatusStates.new)
            status_pending = Status(resume_id=1, state=StatusStates.pending)

            resume_jack_2 = Resume(
                title="Python Разработчик", compensation=150000, workload=Workload.fulltime, worker_id=1)
            resume_michael_1 = Resume(
                title="Python Data Engineer", compensation=250000, workload=Workload.parttime, worker_id=2)
            resume_michael_2 = Resume(
                title="Data Scientist", compensation=300000, workload=Workload.fulltime, worker_id=2)
            session.add_all([resume_jack_1, resume_jack_2,
                             resume_michael_1, resume_michael_2, status_new, status_pending])
            session.commit()

    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "parttime", "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload": "parttime", "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload": "fulltime", "worker_id": 5},
            ]
            insert_resumes = insert(Resume).values(resumes)
            session.execute(insert_resumes)
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = 'Python'):
        with session_factory() as session:
            query = (
                select(
                    cast(Resume.workload, String).label('workload'),
                    cast(func.avg(Resume.compensation), Integer).label('avg_compensation'),
                )
                .select_from(Resume)
                .filter(and_(
                    Resume.title.contains(like_language),
                    Resume.compensation > 40000,
                ))
                .group_by(Resume.workload)
                .having(cast(func.avg(Resume.compensation), Integer) > 70000)
            )

            # print(query.compile(compile_kwargs={'literal_binds': True}))

            res = session.execute(query)
            result = res.all()
            print(f'{result=}')

            result_dto = [WorkloadAvgCompensationDTO.model_validate(row, from_attributes=True) for row in result]
            print(f'{result_dto=}')


#     @staticmethod
#     def select_resumes_avg_compensation(like_language: str = "Python"):
#         """
#         select workload, avg(compensation)::int as avg_compensation
#         from resumes
#         where title like '%Python%' and compensation > 40000
#         group by workload
#         having avg(compensation) > 70000
#         """
#         with session_factory() as session:
#             query = (
#                 select(
#                     ResumesOrm.workload,
#                     # 1 вариант использования cast
#                     # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
#                     # 2 вариант использования cast (предпочтительный способ)
#                     func.avg(ResumesOrm.compensation).cast(Integer).label("avg_compensation"),
#                 )
#                 .select_from(ResumesOrm)
#                 .filter(and_(
#                     ResumesOrm.title.contains(like_language),
#                     ResumesOrm.compensation > 40000,
#                 ))
#                 .group_by(ResumesOrm.workload)
#                 .having(func.avg(ResumesOrm.compensation) > 70000)
#             )
#             print(query.compile(compile_kwargs={"literal_binds": True}))
#             res = session.execute(query)
#             result = res.all()
#             print(result[0].avg_compensation)


    @staticmethod
    def select_workers_with_lazy_relationship():
        with session_factory() as session:
            query = (
                select(Worker)
            )
            result = session.execute(query)

            # result = result.all()
            # print(type(result), result)

            # result = result.scalars()
            # print(type(result), result)

            result = result.scalars().all()
            print(type(result), result)

            # worker_1_resumes = result[0].resumes
            # print(f'{worker_1_resumes=}')
            #
            # worker_2_resumes = result[1].resumes
            # print(f'{worker_2_resumes=}')

    @staticmethod
    def select_workers_with_joined_relationship():
        with session_factory() as session:
            query = (
                select(Worker)
                .options(joinedload(Worker.resumes))
            )
            result = session.execute(query)
            result = result.unique().scalars().all()

            worker_1_resumes = result[0].resumes
            print(f'{worker_1_resumes=}')

            worker_2_resumes = result[1].resumes
            print(f'{worker_2_resumes=}')

    @staticmethod
    def select_workers_with_selectin_relationship():
        with session_factory() as session:
            query = (
                select(Worker)
                .options(selectinload(Worker.resumes))
            )
            result = session.execute(query)
            result = result.unique().scalars().all()

            worker_1_resumes = result[0].resumes
            print(f'{worker_1_resumes=}')

            worker_2_resumes = result[1].resumes
            print(f'{worker_2_resumes=}')

    @staticmethod
    def select_parttime_resumes():
        with session_factory() as session:
            query = (
                select(Worker)
                .options(selectinload(Worker.resumes_parttime))
            )
            res = session.execute(query)
            result = res.scalars().all()
            print(result)

    @staticmethod
    def select_parttime_resumes_contains_eager():
        with session_factory() as session:
            query = (
                select(Worker)
                .join(Worker.resumes)
                .options(contains_eager(Worker.resumes))
                .filter(Resume.workload == 'parttime')
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)

    @staticmethod
    def select_parttime_resumes_contains_eager_with_limit():
        with session_factory() as session:
            subquery = (
                select(Resume.id.label('parttime_resume_id'))
                .filter(Resume.worker_id == Worker.id)
                .order_by(Worker.id.desc())
                .limit(1)
                .scalar_subquery()
                .correlate(Worker)
            )
            query = (
                select(Worker)
                .join(Resume, Resume.id.in_(subquery))
                .options(contains_eager(Worker.resumes))
                # .filter(Resume.workload == 'parttime')
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)

    @staticmethod
    def select_without_relationship():
        with session_factory() as session:
            query = (
                select(Worker)
                .limit(2)
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(f'{result=}')

            result_dto = [WorkersDTO.model_validate(row, from_attributes=True) for row in result]
            print(f'{result_dto=}')

    @staticmethod
    def select_with_relationship():
        with session_factory() as session:
            query = (
                select(Worker)
                .options(selectinload(Worker.resumes))
                .limit(2)
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(f'{result=}')

            result_dto = [WorkersRelDTO.model_validate(row, from_attributes=True) for row in result]
            print(f'{result_dto=}')
            return result_dto

    @staticmethod
    def select_with_relationship_resume_statuses():
        with session_factory() as session:
            query = (
                select(Resume)
                .options(selectinload(Resume.statuses))
                .limit(2)
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(f'{result=}')

            result_dto = [ResumesRelDTO.model_validate(row, from_attributes=True) for row in result]
            print(f'{result_dto=}')
            return result_dto

    @staticmethod
    def select_with_dto():
        with session_factory() as session:
            query = (
                select(Worker)
                .options(selectinload(Worker.resumes))
                .limit(2)
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(f'{result=}')

            result_dto = [WorkersRelDTO.model_validate(row, from_attributes=True) for row in result]
            print(f'{result_dto=}')
            return result_dto

    @staticmethod
    def add_vacancies_and_replies():
        with session_factory() as session:
            new_vacancy = Vacancy(title='Python Developer', compensation=100000)
            resume1 = session.get(Resume, 1)
            resume2 = session.get(Resume, 2)
            resume1.vacancies_replied.append(new_vacancy)
            resume2.vacancies_replied.append(new_vacancy)
            session.commit()

    @staticmethod
    def select_resumes_with_all_relationships():
        with session_factory() as session:
            query = (
                select(Resume)
                .options(joinedload(Resume.worker))
                .options(selectinload(Resume.vacancies_replied).load_only(Vacancy.title))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()
            print(f'{result=}')


    @staticmethod
    def select_vacancy_with_all_relationships():
        with session_factory() as session:
            query = (
                select(Vacancy)
                # .options(joinedload(Resume.worker))
                .options(selectinload(Vacancy.resumes_replied))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()
            print(f'{result=}')
            return result

class AsyncORM:
    @staticmethod
    async def join_cte_subquery_window_func(like_language: str = 'Python'):
        """
        with comp_window_avg as (
        select *, compensation - avg_workload_compensation as compensation_differ
        from
            (select
                w.id,
                w.username,
                r.compensation,
                r.workload,
                avg(r.compensation) over (partition by r.workload)::int as avg_workload_compensation
            from worker w
            join resume r on r.worker_id = w.id
            ) as resumes_avg
        )

        select * from comp_window_avg
        order by compensation_differ;
        :param like_language:
        :return:
        """

        async with async_session_factory() as session:

            r = aliased(Resume)
            w = aliased(Worker)

            subquery = (
                select(
                    r,
                    w,
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label('avg_workload_compensation')
                )
                # .select_from(r)
                .join(r, r.worker_id == w.id).subquery('subquery')
            )
            cte = (
                select(
                    subquery.c.worker_id,
                    subquery.c.username,
                    subquery.c.compensation,
                    subquery.c.workload,
                    subquery.c.avg_workload_compensation,
                    (subquery.c.compensation - subquery.c.avg_workload_compensation).label('compensation_differ')
                )
                .cte('cte')
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_differ.desc())
            )

            # print(query.compile(compile_kwargs={"literal_binds": True}))

            result = await session.execute(query)
            res = result.all()
            print(f'{res=}, {len(res)}')

#     # Асинхронный вариант, не показанный в видео
#     @staticmethod
#     async def create_tables():
#         async with async_engine.begin() as conn:
#             await conn.run_sync(Base.metadata.drop_all)
#             await conn.run_sync(Base.metadata.create_all)
#
#     @staticmethod
#     async def insert_workers():
#         async with async_session_factory() as session:
#             worker_jack = WorkersOrm(username="Jack")
#             worker_michael = WorkersOrm(username="Michael")
#             session.add_all([worker_jack, worker_michael])
#             # flush взаимодействует с БД, поэтому пишем await
#             await session.flush()
#             await session.commit()
#
#     @staticmethod
#     async def select_workers():
#         async with async_session_factory() as session:
#             query = select(WorkersOrm)
#             result = await session.execute(query)
#             workers = result.scalars().all()
#             print(f"{workers=}")
#
#     @staticmethod
#     async def update_worker(worker_id: int = 2, new_username: str = "Misha"):
#         async with async_session_factory() as session:
#             worker_michael = await session.get(WorkersOrm, worker_id)
#             worker_michael.username = new_username
#             await session.refresh(worker_michael)
#             await session.commit()
#
#     @staticmethod
#     async def insert_resumes():
#         async with async_session_factory() as session:
#             resume_jack_1 = ResumesOrm(
#                 title="Python Junior Developer", compensation=50000, workload=Workload.fulltime, worker_id=1)
#             resume_jack_2 = ResumesOrm(
#                 title="Python Разработчик", compensation=150000, workload=Workload.fulltime, worker_id=1)
#             resume_michael_1 = ResumesOrm(
#                 title="Python Data Engineer", compensation=250000, workload=Workload.parttime, worker_id=2)
#             resume_michael_2 = ResumesOrm(
#                 title="Data Scientist", compensation=300000, workload=Workload.fulltime, worker_id=2)
#             session.add_all([resume_jack_1, resume_jack_2,
#                              resume_michael_1, resume_michael_2])
#             await session.commit()
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
#         async with async_session_factory() as session:
#             query = (
#                 select(
#                     ResumesOrm.workload,
#                     # 1 вариант использования cast
#                     # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
#                     # 2 вариант использования cast (предпочтительный способ)
#                     func.avg(ResumesOrm.compensation).cast(Integer).label("avg_compensation"),
#                 )
#                 .select_from(ResumesOrm)
#                 .filter(and_(
#                     ResumesOrm.title.contains(like_language),
#                     ResumesOrm.compensation > 40000,
#                 ))
#                 .group_by(ResumesOrm.workload)
#                 .having(func.avg(ResumesOrm.compensation) > 70000)
#             )
#             print(query.compile(compile_kwargs={"literal_binds": True}))
#             res = await session.execute(query)
#             result = res.all()
#             print(result[0].avg_compensation)
