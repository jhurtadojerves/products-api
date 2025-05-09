import boto3
from botocore.exceptions import ClientError
from django.conf import settings


class EmailService:
    @classmethod
    def send_email(self, subject: str, content: str, to_emails: list[str]) -> None:
        if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
            print(f"settings.AWS_ACCESS_KEY_ID - {settings.AWS_ACCESS_KEY_ID}")
            print(f"settings.AWS_SECRET_ACCESS_KEY - {settings.AWS_SECRET_ACCESS_KEY}")
            raise ValueError("Missing AWS SES credentials")

        client = boto3.client(
            "ses",
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        try:
            response = client.send_email(
                Source=settings.FROM_EMAIL,
                Destination={"ToAddresses": to_emails},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": content}},
                },
            )
            return response
        except ClientError as e:
            raise RuntimeError(
                f"Failed to send email: {e.response['Error']['Message']}"
            )
