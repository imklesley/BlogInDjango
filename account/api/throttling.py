from rest_framework.throttling import AnonRateThrottle


class LoginThrottleSec(AnonRateThrottle):
    scope = 'login_sec'

class LoginThrottleDay(AnonRateThrottle):
    scope = 'login'

