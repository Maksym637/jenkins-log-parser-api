def get_jenkins_log_in_db(log) -> dict:
    return dict(
        id=str(log["_id"]),
        parsed_log_data=log["parsed_log_data"],
        chart_log_data=log["chart_log_data"],
        user_id=log["user_id"],
    )
