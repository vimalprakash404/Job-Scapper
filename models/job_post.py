from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import List, Optional, Literal
from datetime import datetime


class Location(BaseModel):
    country: Optional[str]
    city: Optional[str]
    state: Optional[str]


class JobFunction(BaseModel):
    interval: Literal["yearly", "monthly", "weekly", "daily", "hourly"]
    min_amount: Optional[float]
    max_amount: Optional[float]
    currency: Optional[str]
    salary_source: Literal["direct_data", "description"]


class JobPost(BaseModel):
    title: str
    company: str
    company_url: Optional[HttpUrl]
    job_url: Optional[HttpUrl]
    location: Optional[Location]
    is_remote: Optional[bool] = False
    description: Optional[str]
    job_type: Literal["fulltime", "parttime", "internship", "contract"]
    job_function: Optional[JobFunction]
    date_posted: Optional[datetime] = Field(default_factory=datetime.utcnow)
    emails: Optional[List[EmailStr]]

    # LinkedIn
    job_level: Optional[str]

    # LinkedIn & Indeed
    company_industry: Optional[str]

    # Indeed
    company_country: Optional[str]
    company_addresses: Optional[List[str]]
    company_employees_label: Optional[str]
    company_revenue_label: Optional[str]
    company_description: Optional[str]
    company_logo: Optional[HttpUrl]

    # Naukri
    skills: Optional[List[str]]
    experience_range: Optional[str]
    company_rating: Optional[float]
    company_reviews_count: Optional[int]
    vacancy_count: Optional[int]
    work_from_home_type: Optional[str]
