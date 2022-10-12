from datetime import date, datetime
from enum import Enum
from typing import Union
from pydantic import BaseModel, Json
import uuid
from sqlalchemy.dialects.postgresql import UUID


class ReportType(str, Enum):
    Biobank = "bb"


class ReportAction(str, Enum):
    Generate = "GR"
    ReGenerate = "RGR"


class ReportRevisionBase(BaseModel):
    id: Union[uuid.UUID, None] = None
    report_metadata: Json
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
    is_published: bool
    created_at: Union[datetime, None] = None
    published_at: Union[datetime, None] = None
    revoked_at: Union[datetime, None] = None
    published_to: Union[str, None] = None
    sent_email_status: Union[Json, None] = None


class ReportRevision(ReportRevisionBase):
    class Config:
        orm_mode = True


class ReportRevisionCreate(ReportRevisionBase):
    class Config:
        orm_mode = True


class ReportBase(BaseModel):
    patient_id: Union[str, None] = None
    report_type: ReportType
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None


class ReportCreate(ReportBase):
    report_revision: list[ReportRevision] = []

    class Config:
        orm_mode = True


class ReportFetch(ReportBase):
    id: uuid.UUID
    s3_key: Union[str, None] = None

    class Config:
        orm_mode = True


class ReportGenerateFetch(BaseModel):
    report_id: uuid.UUID
    revision_id: uuid.UUID


class ReportRevisionFetchList(BaseModel):
    published_at: Union[datetime, None] = None
    revoked_at: Union[datetime, None] = None

    class Config:
        orm_mode = True


class ReportFetchList(BaseModel):
    report_id: Union[uuid.UUID, None] = None
    patient_id: Union[str, None] = None
    published_at: Union[datetime, None] = None
    revoked_at: Union[datetime, None] = None


class ReportEmptyList(BaseModel):

    published_at: Union[datetime, None] = None
    revoked_at: Union[datetime, None] = None


class ReportFetchList1(ReportEmptyList):
    patient_id: Union[str, None] = None

    class Config:
        orm_mode = True


class GenerateReportBase(BaseModel):
    patient_id: Union[str, None] = None
    report_type: ReportType
    action: ReportAction
    start_date: Union[date, None] = None
    end_date: Union[date, None] = None


class GenerateReportModel(GenerateReportBase):
    class Config:
        orm_mode = True


class GenerateReport(GenerateReportBase):
    id: Union[str, None] = None

    class Config:
        orm_mode = True


class ReportAccesLogs(BaseModel):
    id: str
    report_id: str
    revision_id: str
    accessed_at: Union[datetime, None] = None
    accessed_source_metadata: Union[str, None] = None


class ReGenerateReportBase(BaseModel):
    action: ReportAction
    start_date: Union[date, None] = None
    end_date: Union[date, None] = None


class ReGenerateReportModel(ReGenerateReportBase):
    class Config:
        orm_mode = True


class ReportPublish(BaseModel):
    updated_at: Union[datetime, None] = None
    is_published: bool
    published_at: Union[datetime, None] = None
    published_to: Union[str, None] = None
    sent_email_status: Union[Json, None] = None


class ReportPublishResponse(BaseModel):
    report_id: Union[uuid.UUID, None] = None
    patient_id: Union[str, None] = None
    published_at: Union[datetime, None] = None


class ReportRevoke(BaseModel):
    report_id: str
    patient_id: str
    revoked_at: str


class ActionRequest(BaseModel):
    action: str
    email: Union[str, None] = None
    doctor_last_name: Union[str, None] = None
    patient_name: Union[str, None] = None
    report_url_prefix: Union[str, None] = None


class ReportRevisionGet(BaseModel):
    id: Union[uuid.UUID, None] = None
    created_at: Union[datetime, None] = None
    is_published: bool
    created_at: Union[datetime, None] = None
    published_at: Union[datetime, None] = None
    revoked_at: Union[datetime, None] = None


class ReportAccessLogCreate(BaseModel):
    id: Union[uuid.UUID, None] = None
    report_id: str
    revision_id: str
    accessed_at: Union[datetime, None] = None
    accessed_source_metadata: Union[Json, None] = None


class ReportAccessLogFetchList(BaseModel):
    id: Union[uuid.UUID, None] = None
    report_id: str
    revision_id: str
    accessed_at: Union[datetime, None] = None
    accessed_source_metadata: Union[Json, None] = None
