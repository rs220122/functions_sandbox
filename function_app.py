import logging
import os
import time

import azure.durable_functions as durable_functions
import azure.functions as func
from azure.durable_functions import DurableOrchestrationClient

from libs.dataclasses import TaskWithFile
from libs.sql_handler import Task
from libs.sql_usecase import DBUseCase

dfApp = durable_functions.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# @dfApp.timer_trigger(
#     schedule="0 */1 * * * *",
#     arg_name="myTimer",
#     run_on_startup=False,
#     use_monitor=False,
# )
# @dfApp.durable_client_input(client_name="client")
# async def timer_trigger(
#     myTimer: func.TimerRequest, client: DurableOrchestrationClient
# ) -> None:

#     if myTimer.past_due:
#         logging.info("The timer is past due!")

#     logging.info("Python timer trigger function executed.")

#     instance_id = await client.start_new("hello_orchestrator")
#     logging.info(f"instance id: {instance_id}")


# クライアント関数
@dfApp.route(route="start-batch")
@dfApp.durable_client_input(client_name="client")
async def start_batch(
    req: func.HttpRequest, client: durable_functions.DurableOrchestrationClient
):
    try:
        instance_id = await client.start_new(
            orchestration_function_name="hello_orchestrator"
        )
        response = client.create_check_status_response(req, instance_id)
        return func.HttpResponse("バッチを正常に開始しました。", status_code=200)
    except Exception as e:
        return func.HttpResponse(
            f"バッチの開始に失敗しました: {str(e)}", status_code=500
        )


# Orchestrator
@dfApp.orchestration_trigger(context_name="context")
def hello_orchestrator(context):

    # タスク一覧を取得する
    tasks = yield context.call_activity("get_ready_tasks", None)
    tasks = [Task]
    time.sleep(10)

    logging.info("Orchestrator End")

    # jsonシリアライズできないといけない
    return [tasks]


@dfApp.activity_trigger(input_name="none")
def get_ready_tasks(none: str) -> list[Task]:
    db_usecase = DBUseCase(os.environ["DATABASE_URL"])

    tasks = [
        TaskWithFile.from_sqlalchemy(t).to_dict() for t in db_usecase.get_ready_tasks()
    ]
    print(len(tasks))
    print(tasks)
    return tasks


# Activity
@dfApp.activity_trigger(input_name="city")
def hello(city: str):
    return f"Hello {city}"
