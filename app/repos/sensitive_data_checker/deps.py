from app.interfaces.sensitive_data_checker import SensitiveDataChecker


def get_sensitive_data_checker()->SensitiveDataChecker:
    """
    Dependency to get the SensitiveDataChecker implementation.
    This function can be used in FastAPI routes to inject the sensitive data checker.
    """
    from app.repos.sensitive_data_checker.sdc_impl import SensitiveDataCheckerImpl
    return SensitiveDataCheckerImpl()