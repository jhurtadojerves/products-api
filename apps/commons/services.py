import boto3
from botocore.exceptions import ClientError
from django.conf import settings


class EmailService:
    """
    Service class for sending emails via AWS SES.

    This class provides a method to send emails using AWS Simple Email Service (SES).
    It requires AWS credentials and configuration to be set in the Django settings.

    Methods:
    - send_email: Sends an email to the specified recipients.
    """

    @classmethod
    def send_email(self, subject: str, content: str, to_emails: list[str]) -> None:
        """
        Send an email using AWS SES.

        Args:
            subject (str): The subject of the email.
            content (str): The body content of the email.
            to_emails (list[str]): A list of recipient email addresses.

        Raises:
            ValueError: If AWS SES credentials are missing in the settings.
            RuntimeError: If the email fails to send due to an AWS SES error.

        Returns:
            dict: The response from the AWS SES client if the email is sent successfully.
        """
        if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
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
