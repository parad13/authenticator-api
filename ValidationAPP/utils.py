import os
import uuid
import boto3
import jinja2

from core.config import settings
from schemas.report import ActionRequest

base_dir = os.path.dirname(__file__)
ses = boto3.client(
    "ses",
    region_name=settings.REPORT_BUCKET_REGION,
)


def send_report_download_email(action_request: ActionRequest, revision_id: str) -> dict:
    link: str = action_request.report_url_prefix + "?id=" + str(revision_id)
    subject: str = "PhenoWeek Report Ready for Download."
    template_params = {
        "doctor_last_name": action_request.doctor_last_name,
        "patient_name": action_request.patient_name,
        "link": link,
    }
    rendered_template: str = create_template(template_params=template_params)
    email_message: dict = {
        "Body": {
            "Html": {
                "Charset": "utf-8",
                "Data": rendered_template,
            },
        },
        "Subject": {
            "Charset": "utf-8",
            "Data": subject,
        },
    }
    if not settings.REPORT_DEBUG:
        response: dict = send_ses_mail(email_to=action_request.email, email_message=email_message)
    else:
        response: dict = generate_email_response(rendered_template)

    return response


def create_template(template_params: dict) -> str:
    # template loader
    file_loader = jinja2.FileSystemLoader(os.path.join(base_dir, settings.EMAIL_TEMPLATES_DIR))
    env = jinja2.Environment(loader=file_loader)
    template: str = "report_download.html"
    template = env.get_template(template)
    template_rendered: str = template.render(**template_params)
    return template_rendered


def send_ses_mail(email_to: str, email_message: dict) -> dict:
    ses_response: dict = ses.send_email(
        Destination={
            "ToAddresses": [email_to],
        },
        Message=email_message,
        Source=settings.EMAILS_FROM_EMAIL,
    )

    return ses_response


def generate_email_response(rendered_template) -> dict:
    report_temp_dir: str = os.path.join("/tmp", uuid.uuid4().hex)
    os.makedirs(base_dir + report_temp_dir, exist_ok=True)
    report_email_template: str = "report_email_template"
    report_template_path: str = os.path.join(
        base_dir + report_temp_dir, f"{report_email_template}.html"
    )
    with open(report_template_path, "w") as fp:
        fp.write(rendered_template)
    return {
        "ResponseMetadata": {
            "RequestId": str(uuid.uuid4()),
            "HTTPStatusCode": 200,
        }
    }
