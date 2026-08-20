from pydantic import BaseModel, Field

class ContractData(BaseModel):
    contractor: str = Field(description="Name of the hiring company or individual")
    contractee: str = Field(description="Name of the hired company or individual")
    total_value: float = Field(description="Total monetary value of the contract. Example: 1500.00. Return 0.0 if not found.")
    signature_date: str = Field(description="Date the contract was signed in YYYY-MM-DD format. Return 'Not specified' if absent.")
    has_penalty_clause: bool = Field(description="True if there is any penalty clause for delays or breaches, False otherwise")
    summary: str = Field(description="A one-sentence summary of the contract's primary objective")
    confidence_score: int = Field(description="Rate your confidence in this extraction from 1 to 10, where 10 is absolute certainty based on the text.")

class ExtractionResponse(BaseModel):
    filename: str
    extracted_data: ContractData
    status: str