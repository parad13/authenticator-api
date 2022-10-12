import os
import boto3
import jinja2

from core.config import settings
from schemas.report import ActionRequest

base_dir = os.path.dirname(__file__)
