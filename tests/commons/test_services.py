from unittest import TestCase
from unittest.mock import MagicMock, patch

from django.test import override_settings

from apps.commons.services import EmailService


class EmailServiceTest(TestCase):
    @patch("apps.commons.services.boto3.client")
    def test_send_email_success(self, mock_boto_client):
        mock_ses = MagicMock()
        mock_boto_client.return_value = mock_ses

        subject = "Test Subject"
        content = "Hello, this is a test email."
        to_emails = ["recipient@example.com"]

        EmailService.send_email(subject, content, to_emails)

        mock_boto_client.assert_called_once_with(
            "ses",
            region_name="us-east-1",
            aws_access_key_id="fake-key",
            aws_secret_access_key="fake-secret",
        )
        mock_ses.send_email.assert_called_once()

    @override_settings(AWS_SECRET_ACCESS_KEY="", AWS_ACCESS_KEY_ID="")
    @patch("apps.commons.services.boto3.client")
    def test_send_email_missing_credentials_raises(self, mock_boto_client):
        with self.assertRaises(ValueError) as ctx:
            EmailService.send_email("Subject", "Body", ["a@example.com"])

        mock_boto_client.assert_not_called()
        self.assertIn("Missing AWS SES credentials", str(ctx.exception))
