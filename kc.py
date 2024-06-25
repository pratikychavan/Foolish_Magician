import os
import traitlets
import traitlets.config

from keycloak import KeycloakAdmin, KeycloakOpenID
from traitlets.config import Configurable

APP_NAME = "Foolish_Magician"

auth_config_path = os.path.join("Configurations","kcadmin.json")
auth_config = traitlets.config.JSONFileConfigLoader(auth_config_path).load_config()

class MasterMagician(Configurable):
    server_url = traitlets.Unicode(default_value="http://localhost:8080/auth").tag(config=True)
    realm_name = traitlets.Unicode(default_value="master").tag(config=True)
    client_id = traitlets.Unicode(default_value="admin-cli").tag(config=True)
    username = traitlets.Unicode(default_value="admin").tag(config=True)
    password = traitlets.Unicode(default_value="admin").tag(config=True)
    verify = traitlets.Bool(default_value=True).tag(config=True)
    
    app_realm = traitlets.Unicode(default_value="Foolish_Magician").tag(config=True)
    app_client_name = traitlets.Unicode(default_value="api-server").tag(config=True)
    
    def __init__(self, **kwargs):
        super().__init__()
        self.admin = KeycloakAdmin(
            server_url=self.server_url,
            realm_name=self.realm_name,
            client_id=self.client_id,
            username=self.username,
            password=self.password,
            verify=self.verify
        )
        self.admin.create_realm(
            payload = dict(
                id=self.app_realm,
                realm=self.app_realm,
                displayName=self.app_realm,
                enabled=True,
                registrationAllowed=True,
                verifyEmail=True,
            ),
            skip_exists=True
        )
        self.admin.change_current_realm(self.app_realm)
        self.admin.create_client(
            payload=dict(
                id=self.app_client_id,
                clientId=self.app_client_id,
                name=self.app_client_id,
                enabled=True,
                standardFlowEnabled=True,
                implicitFlowEnabled=True,
                directAccessGrantsEnabled=True,
                serviceAccountsEnabled=True,
            ),
            skip_exists=True
        )
        self.app_client_id = self.admin.get_client_id(self.app_client_name)
        self.__client_secret = self.admin.get_client_secrets(self.app_client_id)['value']
        self.admin.create_client_role(
            client_role_id=self.app_client_id,
            payload=dict(
                id="admin",
                name="admin",
                description="admin role",
            ),
            skip_exists=True
        )
        self.token_master = KeycloakOpenID(
            server_url=self.server_url,
            client_id=self.app_client_name,
            realm_name=self.app_realm, 
            verify=True,
            client_secret_key=self.__client_secret
        )
        pass
    
    def define_role(self, role_name, description=""):
        self.admin.create_client_role(
            client_role_id=self.app_client_id,
            payload=dict(
                id=role_name,
                name=role_name,
                description=description
            )
        )
        
    
    def create_user(self, username, password, first_name, last_name, email):
        payload = dict(
            email=email,
            username=username,
            enabled=True,
            emailVerified=True,
            firstName=first_name,
            lastName=last_name,
            requiredActions=[],
            credentials=[
                {
                    'type':"password",
                    'value':password,
                    'temporary':False
                }
            ]
        )
        user_id = self.admin.create_user(payload=payload)
        return user_id
    
    def get_all_roles_of_user(self, username):
        return self.admin.get_all_roles_of_user(user_id=self.admin.get_user_id(username=username))
    
    def get_token(self, username, password):
        return self.token_master.token(username=username, password=password)
    
    def assign_roles(self, username, roles):
        user_id = self.admin.get_user_id(username=username)
        role_reps = [role for role in self.admin.get_client_roles(client_id=self.app_client_id) if role['name'] in roles]
        self.admin.assign_client_role(
            user_id=self.admin.get_user_id(username),
            client_id=self.app_client_id,
            roles=self.admin.get_client_role(
                client_id=self.app_client_id,
                user_id=user_id,
                role_name=role_reps
            )
        )