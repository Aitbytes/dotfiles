## Python Helper

```python
import os, json, requests

class DokployClient:
    def __init__(self, url=None, api_key=None):
        self.url = (url or os.environ.get("DOKPLOY_URL", "http://localhost:3000")).rstrip("/")
        self.api_key = api_key or os.environ["DOKPLOY_API_KEY"]
        self.session = requests.Session()
        self.session.headers["x-api-key"] = self.api_key
        self.session.headers["Content-Type"] = "application/json"

    def _get(self, path, params=None):
        return self.session.get(f"{self.url}/api/{path}", params=params).json()

    def _post(self, path, data=None):
        return self.session.post(f"{self.url}/api/{path}", json=data or {}).json()

    # Projects
    def list_projects(self):        return self._get("project.all")
    def get_project(self, pid):     return self._get("project.one", {"projectId": pid})
    def create_project(self, name, desc=None):
        return self._post("project.create", {"name": name, "description": desc})

    # Environments
    def get_environments(self, pid):
        return self._get("environment.byProjectId", {"projectId": pid})
    def create_environment(self, name, project_id, desc=""):
        return self._post("environment.create", {"name": name, "projectId": project_id, "description": desc})

    # Applications
    def get_app(self, app_id):      return self._get("application.one", {"applicationId": app_id})
    def create_app(self, name, env_id):
        return self._post("application.create", {"name": name, "environmentId": env_id})
    def update_app(self, app_id, **kwargs):
        kwargs["applicationId"] = app_id
        return self._post("application.update", kwargs)
    def deploy_app(self, app_id):   return self._post("application.deploy", {"applicationId": app_id})
    def redeploy_app(self, app_id): return self._post("application.redeploy", {"applicationId": app_id})
    def stop_app(self, app_id):     return self._post("application.stop", {"applicationId": app_id})
    def start_app(self, app_id):    return self._post("application.start", {"applicationId": app_id})
    def delete_app(self, app_id):   return self._post("application.delete", {"applicationId": app_id})
    def app_logs(self, app_id, tail=100, since="all"):
        return self._get("application.readLogs", {"applicationId": app_id, "tail": tail, "since": since})
    def set_env(self, app_id, env_string, build_args=None, build_secrets=None):
        return self._post("application.saveEnvironment", {
            "applicationId": app_id, "env": env_string,
            "buildArgs": build_args, "buildSecrets": build_secrets, "createEnvFile": True
        })
    def set_github(self, app_id, repo, owner, branch="main", build_path="/", github_id=None):
        return self._post("application.saveGithubProvider", {
            "applicationId": app_id, "repository": repo, "owner": owner,
            "branch": branch, "buildPath": build_path, "githubId": github_id
        })
    def set_build_type(self, app_id, build_type, dockerfile=None):
        return self._post("application.saveBuildType", {
            "applicationId": app_id, "buildType": build_type, "dockerfile": dockerfile,
            "dockerContextPath": None, "publishDirectory": None, "herokuVersion": None,
            "railpackVersion": None, "isStaticSpa": None
        })
    def move_app(self, app_id, env_id):
        return self._post("application.move", {"applicationId": app_id, "environmentId": env_id})
    def get_deployments(self, app_id):
        return self._get("deployment.all", {"applicationId": app_id})

    # Compose
    def get_compose(self, cid):     return self._get("compose.one", {"composeId": cid})
    def create_compose(self, name, env_id, compose_file, compose_type="docker-compose", app_name=None):
        return self._post("compose.create", {"name": name, "environmentId": env_id,
            "composeFile": compose_file, "composeType": compose_type, "appName": app_name})
    def deploy_compose(self, cid):  return self._post("compose.deploy", {"composeId": cid})
    def stop_compose(self, cid):    return self._post("compose.stop", {"composeId": cid})
    def start_compose(self, cid):   return self._post("compose.start", {"composeId": cid})
    def delete_compose(self, cid):  return self._post("compose.delete", {"composeId": cid})
    def compose_services(self, cid): return self._get("compose.loadServices", {"composeId": cid})

    # Databases (type = "postgres"|"mysql"|"redis"|"mongo"|"mariadb")
    def get_db(self, db_type, db_id):
        return self._get(f"{db_type}.one", {f"{db_type}Id": db_id})
    def create_db(self, db_type, **kwargs):
        return self._post(f"{db_type}.create", kwargs)
    def deploy_db(self, db_type, db_id):
        return self._post(f"{db_type}.deploy", {f"{db_type}Id": db_id})
    def update_db(self, db_type, db_id, **kwargs):
        kwargs[f"{db_type}Id"] = db_id
        return self._post(f"{db_type}.update", kwargs)

    # Docker
    def list_containers(self, server_id=None):
        return self._get("docker.getContainers", {"serverId": server_id} if server_id else None)

    # Domains
    def create_domain(self, host, app_id=None, compose_id=None, port=None, https=True, cert_type="letsencrypt"):
        return self._post("domain.create", {
            "host": host, "port": port, "https": https, "applicationId": app_id,
            "composeId": compose_id, "certificateType": cert_type
        })

    # Settings
    def health(self):               return self._get("settings.health")
    def version(self):              return self._get("settings.getDokployVersion")
```
