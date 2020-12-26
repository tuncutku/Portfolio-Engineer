from src.environment.user_activities.utils.login_verification import credential_check
from src.environment.user_activities.utils.user_errors import (
    UserAlreadyRegisteredError,
    UserNotFoundError,
    InvalidEmailError,
    IncorrectPasswordError,
    UserError,
)
from src.environment.user_activities.utils.portfolio_errors import PositionError, PositionNotFoundError
from src.environment.user_activities.utils.decorators import (
    requires_login,
    requires_questrade_access,
)
from src.environment.user_activities.utils.account_errors import PortfolioNotFoundError, PortfolioError