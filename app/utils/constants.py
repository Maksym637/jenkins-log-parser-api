class Dependencies:
    DB_NAME = "jenkins-log-parser-db"
    USER_COLLECTION = "users"
    JENKINS_LOG_COLLECTION = "jenkins-logs"
    JENKINS_HISTORY_COLLECTION = "jenkins-histories"


class TestResult:
    PASS = "Pass"
    FAIL = "Fail"
    ERROR = "Error"
    BLOCKED = "Blocked"
    SKIPPED = "Skipped"


class RegexString:
    TEST_SEPARATOR = r"Starting setUp"

    TEST_NAME = r"tid: (.*)\u001b"
    TEST_RESULT = r"res: (Pass|Fail|Error|Blocked|Skipped)\u001b"

    TEST_HESH = r"\n|\d{2}:\d{2}:\d{2}"

    TEST_FAIL = r'Adding "Failure Message: (.*?)" to the TestRail custom message'
    TEST_ERROR = r'Adding "Failure Message: (.*?)" to the TestRail custom message'
