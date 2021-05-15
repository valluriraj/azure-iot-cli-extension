# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.log import get_logger
from knack.util import CLIError

from azext_iot.constants import CENTRAL_ENDPOINT
from azext_iot.central import services as central_services
from azext_iot.central.models.enum import Role, ApiVersion


logger = get_logger(__name__)


class CentralUserProviderV1:
    def __init__(self, cmd, app_id: str, token=None):
        """
        Provider for device APIs

        Args:
            cmd: command passed into az
            app_id: name of app (used for forming request URL)
            token: (OPTIONAL) authorization token to fetch device details from IoTC.
                MUST INCLUDE type (e.g. 'SharedAccessToken ...', 'Bearer ...')
                Useful in scenarios where user doesn't own the app
                therefore AAD token won't work, but a SAS token generated by owner will
        """
        self._cmd = cmd
        self._app_id = app_id
        self._token = token

    def add_service_principal(
        self,
        assignee: str,
        tenant_id: str,
        object_id: str,
        role: Role,
        central_dns_suffix=CENTRAL_ENDPOINT,
    ) -> dict:
        if not tenant_id:
            raise CLIError("Must specify --tenant-id when adding a service principal")

        if not object_id:
            raise CLIError("Must specify --object-id when adding a service principal")

        return central_services.user.add_service_principal(
            cmd=self._cmd,
            app_id=self._app_id,
            assignee=assignee,
            tenant_id=tenant_id,
            object_id=object_id,
            role=role,
            token=self._token,
            central_dns_suffix=central_dns_suffix,
            api_version=ApiVersion.v1.value,
        )

    def get_user_list(self, central_dns_suffix=CENTRAL_ENDPOINT,) -> dict:
        return central_services.user.get_user_list(
            cmd=self._cmd,
            app_id=self._app_id,
            token=self._token,
            central_dns_suffix=central_dns_suffix,
            api_version=ApiVersion.v1.value,
        )

    def get_user(self, assignee, central_dns_suffix=CENTRAL_ENDPOINT,) -> dict:
        return central_services.user.get_user(
            cmd=self._cmd,
            app_id=self._app_id,
            assignee=assignee,
            token=self._token,
            central_dns_suffix=central_dns_suffix,
            api_version=ApiVersion.v1.value,
        )

    def delete_user(self, assignee, central_dns_suffix=CENTRAL_ENDPOINT,) -> dict:
        return central_services.user.delete_user(
            cmd=self._cmd,
            app_id=self._app_id,
            assignee=assignee,
            token=self._token,
            central_dns_suffix=central_dns_suffix,
            api_version=ApiVersion.v1.value,
        )

    def add_email(
        self,
        assignee: str,
        email: str,
        role: Role,
        central_dns_suffix=CENTRAL_ENDPOINT,
    ) -> dict:
        if not email:
            raise CLIError("Must specify --email when adding a user by email")

        return central_services.user.add_email(
            cmd=self._cmd,
            app_id=self._app_id,
            assignee=assignee,
            email=email,
            role=role,
            token=self._token,
            central_dns_suffix=central_dns_suffix,
            api_version=ApiVersion.v1.value,
        )
