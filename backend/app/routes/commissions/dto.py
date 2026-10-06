from pydantic import BaseModel


class CommissionResultDTO(BaseModel):
    """Represent sales and commission totals accumulated for one seller.

    Attributes:
        seller: Seller name taken from the sales records.
        total_sales: Sum of the seller's sale values, rounded by the service
            to two decimal places after aggregation.
        total_commission: Sum of commissions calculated on individual sales,
            rounded to two decimal places after aggregation."""

    seller: str
    total_sales: float
    total_commission: float