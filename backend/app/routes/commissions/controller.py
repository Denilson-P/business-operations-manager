from app.routes.commissions.dto import CommissionResultDTO
from app.routes.commissions.service import CommissionService


class CommissionController:
    """Coordinate the API operation that returns commissions for all sellers.

    Delegates sales loading, per-sale calculation, and aggregation to the
    commission service, returning its list of CommissionResultDTO objects.
    Service exceptions propagate without HTTP-specific translation.

    Attributes:
        service: CommissionService instance created during initialization."""

    def __init__(self) -> None:
        self.service = CommissionService()

    def calculate_commissions(self) -> list[CommissionResultDTO]:
        return self.service.calculate_all()