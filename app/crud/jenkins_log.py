import re
import requests
from datetime import datetime
from requests.exceptions import RequestException
from bson import ObjectId
from fastapi import HTTPException, status
from app.dependencies import jenkins_log_collection, jenkins_history_collection
from app.models.jenkins_log import ParsedLogData, ChartLogData, JenkinsLogCreateComplete
from app.models.jenkins_history import JenkinsHistoryCreateComplete
from app.schemas.jenkins_log import get_jenkins_log_in_db
from app.utils.constants import TestResult, RegexString
from app.utils.timer import timeit


async def create_jenkins_log(user_id: str, jenkins_log_data: dict) -> dict:
    log_data, time_spent = get_log_results(jenkins_log_data["external_url"])

    parsed_log_data, chart_log_data = log_data
    chart_log_data = chart_log_data.model_dump()

    jenkins_log_data_complete = JenkinsLogCreateComplete(
        parsed_log_data=parsed_log_data,
        chart_log_data=chart_log_data,
        user_id=user_id,
    )
    jenkins_log_data_complete = jenkins_log_data_complete.model_dump()

    # -> Insert parsed Jenkins log
    jenkins_log = await jenkins_log_collection.insert_one(jenkins_log_data_complete)
    created_jenkins_log = await jenkins_log_collection.find_one(
        {"_id": ObjectId(jenkins_log.inserted_id)}
    )

    # -> Insert Jenkins log history
    jenkins_history_data_complete = JenkinsHistoryCreateComplete(
        time_executed=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        time_spent=round(time_spent, 2),
        jenkins_log_id=str(jenkins_log.inserted_id),
        user_id=user_id,
    )
    jenkins_history_data_complete = jenkins_history_data_complete.model_dump()

    await jenkins_history_collection.insert_one(jenkins_history_data_complete)

    return get_jenkins_log_in_db(created_jenkins_log)


async def get_jenkins_log_by_id(user_id: str, jenkins_log_id: str) -> dict:
    jenkins_log = await jenkins_log_collection.find_one(
        {"_id": ObjectId(jenkins_log_id), "user_id": user_id}
    )
    if jenkins_log:
        return get_jenkins_log_in_db(jenkins_log)
    return None


async def get_all_jenkins_logs(user_id: str) -> list[dict]:
    jenkins_logs = []
    async for jenkins_log in jenkins_log_collection.find({"user_id": user_id}):
        jenkins_logs.append(get_jenkins_log_in_db(jenkins_log))
    return jenkins_logs


async def delete_jenkins_log_by_id(user_id: str, jenkins_log_id: str) -> bool:
    jenkins_log = await jenkins_log_collection.find_one(
        {"_id": ObjectId(jenkins_log_id), "user_id": user_id}
    )
    if jenkins_log:
        await jenkins_log_collection.delete_one(
            {"_id": ObjectId(jenkins_log_id), "user_id": user_id}
        )
        await jenkins_history_collection.delete_one(
            {"jenkins_log_id": jenkins_log_id, "user_id": user_id}
        )
        return True
    return False


def clean_traceback_msg(string: str) -> str:
    return re.sub(pattern=RegexString.TEST_HESH, repl="", string=string)


def parse_traceback_msg(pattern: str, data: str) -> str:
    return clean_traceback_msg(
        re.search(pattern=pattern, string=data, flags=re.DOTALL).group(1)
    )


@timeit
def get_log_results(log_url: str) -> tuple[list[ParsedLogData], ChartLogData]:
    log_results = []
    chart_log_results = ChartLogData(
        passed=0, failed=0, errored=0, skipped=0, blocked=0
    )

    try:
        response = requests.get(url=log_url)
        response.raise_for_status()
    except RequestException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to get data from external API",
        )

    content_data = response.content.decode(encoding="utf-8")

    content_data_with_header_list = content_data.split(RegexString.TEST_SEPARATOR)
    content_data_list = content_data_with_header_list[1:]

    for content_data in content_data_list:
        test_name = re.search(pattern=RegexString.TEST_NAME, string=content_data).group(
            1
        )
        test_result = re.search(
            pattern=RegexString.TEST_RESULT, string=content_data
        ).group(1)

        if test_result == TestResult.PASS:
            chart_log_results.passed += 1
            test_reason = f"There are no reason (res: {test_result})"
        elif test_result == TestResult.FAIL:
            chart_log_results.failed += 1
            test_reason = parse_traceback_msg(
                pattern=RegexString.TEST_FAIL, data=content_data
            )
        elif test_result == TestResult.ERROR:
            chart_log_results.errored += 1
            test_reason = parse_traceback_msg(
                pattern=RegexString.TEST_ERROR, data=content_data
            )
        elif test_result == TestResult.BLOCKED:
            chart_log_results.blocked += 1
            test_reason = f"There are no reason (res: {test_result})"
        elif test_result == TestResult.SKIPPED:
            chart_log_results.skipped += 1
            test_reason = f"There are no reason (res: {test_result})"

        log_results.append(
            ParsedLogData(
                test_name=test_name, test_result=test_result, test_reason=test_reason
            )
        )

    return log_results, chart_log_results
