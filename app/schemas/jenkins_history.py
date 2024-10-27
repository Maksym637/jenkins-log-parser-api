def get_jenkins_history_in_db(log_history) -> dict:
    return dict(
        id=str(log_history["_id"]),
        time_executed=log_history["time_executed"],
        time_spent=log_history["time_spent"],
        jenkins_log_id=log_history["jenkins_log_id"],
        user_id=log_history["user_id"],
    )
