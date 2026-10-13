# Python Helper

Full `WgerClient` class for programmatic access to the wger API. Handles authentication, SSL certificates, and all API operations.

```python
import os, requests, json

class WgerClient:
    """
    Python client for the wger Workout Manager REST API v2.

    Usage:
        client = WgerClient(url="https://wger.example.com", token="abc123")
        # or use env vars:
        # export WGER_URL=https://wger.example.com
        # export WGER_USERNAME=admin
        # export WGER_PASSWORD=adminadmin
        client = WgerClient()
        client.login("admin", "adminadmin")
    """

    def __init__(self, url=None, token=None):
        self.url = (url or os.environ["WGER_URL"]).rstrip("/")
        self.token = token or os.environ.get("WGER_TOKEN")
        self.session = requests.Session()
        self.session.verify = False  # self-signed certs are common
        if self.token:
            self.session.headers["Authorization"] = f"Token {self.token}"

    def login(self, username, password):
        """Obtain a token via /api/v2/login/"""
        r = self.session.post(
            f"{self.url}/api/v2/login/",
            json={"username": username, "password": password}
        )
        r.raise_for_status()
        self.token = r.json()["token"]
        self.session.headers["Authorization"] = f"Token {self.token}"
        return self.token

    def _get(self, path, params=None):
        r = self.session.get(f"{self.url}{path}", params=params)
        r.raise_for_status()
        return r.json()

    def _post(self, path, data=None, files=None):
        if files:
            r = self.session.post(f"{self.url}{path}", data=data, files=files)
        else:
            r = self.session.post(f"{self.url}{path}", json=data or {})
        r.raise_for_status()
        return r.json()

    def _patch(self, path, data):
        r = self.session.patch(f"{self.url}{path}", json=data)
        r.raise_for_status()
        return r.json()

    def _delete(self, path):
        r = self.session.delete(f"{self.url}{path}")
        if r.status_code != 204:
            r.raise_for_status()

    # ── Routines ──

    def list_routines(self, params=None):
        return self._get("/api/v2/routine/", params)

    def get_routine(self, rid):
        return self._get(f"/api/v2/routine/{rid}/")

    def create_routine(self, name, start, end, description="", **kwargs):
        data = {"name": name, "description": description, "start": start, "end": end, **kwargs}
        return self._post("/api/v2/routine/", data)

    def update_routine(self, rid, **kwargs):
        return self._patch(f"/api/v2/routine/{rid}/", kwargs)

    def delete_routine(self, rid):
        return self._delete(f"/api/v2/routine/{rid}/")

    def routine_structure(self, rid):
        return self._get(f"/api/v2/routine/{rid}/structure/")

    def routine_display(self, rid):
        return self._get(f"/api/v2/routine/{rid}/date-sequence-display/")

    def routine_gym(self, rid):
        return self._get(f"/api/v2/routine/{rid}/date-sequence-gym/")

    def routine_logs(self, rid):
        return self._get(f"/api/v2/routine/{rid}/logs/")

    def routine_stats(self, rid):
        return self._get(f"/api/v2/routine/{rid}/stats/")

    # ── Templates ──

    def list_templates(self):
        return self._get("/api/v2/templates/")

    def list_public_templates(self):
        return self._get("/api/v2/public-templates/")

    # ── Days ──

    def list_days(self, params=None):
        return self._get("/api/v2/day/", params)

    def create_day(self, routine, name="", order=1, **kwargs):
        return self._post("/api/v2/day/", {"routine": routine, "name": name, "order": order, **kwargs})

    def update_day(self, did, **kwargs):
        return self._patch(f"/api/v2/day/{did}/", kwargs)

    def delete_day(self, did):
        return self._delete(f"/api/v2/day/{did}/")

    # ── Slots ──

    def create_slot(self, day, order=1, comment="", **kwargs):
        return self._post("/api/v2/slot/", {"day": day, "order": order, "comment": comment, **kwargs})

    # ── Slot Entries ──

    def create_slot_entry(self, slot, exercise, order=1, repetition_unit=1, weight_unit=1, exercise_type="normal", **kwargs):
        return self._post("/api/v2/slot-entry/", {
            "slot": slot, "exercise": exercise, "order": order,
            "repetition_unit": repetition_unit, "weight_unit": weight_unit,
            "type": exercise_type, **kwargs
        })

    # ── Configs ──

    def create_config(self, config_type, slot_entry, iteration, value, operation="r", step="na", repeat=False, **kwargs):
        """
        config_type: one of "weight-config", "max-weight-config",
                     "repetitions-config", "max-repetitions-config",
                     "rir-config", "max-rir-config",
                     "rest-config", "max-rest-config",
                     "sets-config", "max-sets-config"
        """
        return self._post(f"/api/v2/{config_type}/", {
            "slot_entry": slot_entry, "iteration": str(iteration),
            "value": str(value), "operation": operation, "step": step,
            "repeat": repeat, **kwargs
        })

    # ── Workout Logs ──

    def create_log(self, date, exercise, routine, slot_entry, iteration,
                   repetitions=None, weight=None, repetitions_unit=1, weight_unit=1,
                   rir=None, rest=None, **kwargs):
        data = {
            "date": date, "exercise": exercise, "routine": routine,
            "slot_entry": slot_entry, "iteration": iteration,
            "repetitions_unit": repetitions_unit, "weight_unit": weight_unit,
        }
        if repetitions is not None:
            data["repetitions"] = str(repetitions)
        if weight is not None:
            data["weight"] = str(weight)
        if rir is not None:
            data["rir"] = str(rir)
        if rest is not None:
            data["rest"] = rest
        data.update(kwargs)
        return self._post("/api/v2/workoutlog/", data)

    def list_logs(self, params=None):
        return self._get("/api/v2/workoutlog/", params)

    # ── Workout Sessions ──

    def create_session(self, routine, date, day=None, notes=None, impression=None, time_start=None, time_end=None):
        data = {"routine": routine, "date": date}
        if day: data["day"] = day
        if notes: data["notes"] = notes
        if impression: data["impression"] = impression
        if time_start: data["time_start"] = time_start
        if time_end: data["time_end"] = time_end
        return self._post("/api/v2/workoutsession/", data)

    # ── Weight ──

    def list_weight(self, params=None):
        return self._get("/api/v2/weightentry/", params)

    def create_weight(self, date, weight):
        return self._post("/api/v2/weightentry/", {"date": date, "weight": str(weight)})

    def delete_weight(self, wid):
        return self._delete(f"/api/v2/weightentry/{wid}/")

    # ── Nutrition ──

    def list_nutrition_plans(self):
        return self._get("/api/v2/nutritionplan/")

    def create_nutrition_plan(self, description="", **kwargs):
        return self._post("/api/v2/nutritionplan/", {"description": description, **kwargs})

    def get_plan_info(self):
        return self._get("/api/v2/nutritionplaninfo/")

    def get_plan_values(self, pid):
        return self._get(f"/api/v2/nutritionplan/{pid}/nutritional_values/")

    def create_meal(self, plan, time="12:00:00", name=""):
        return self._post("/api/v2/meal/", {"plan": plan, "time": time, "name": name})

    def get_meal_values(self, mid):
        return self._get(f"/api/v2/meal/{mid}/nutritional_values/")

    def create_meal_item(self, meal, ingredient, amount, weight_unit=None):
        return self._post("/api/v2/mealitem/", {
            "meal": meal, "ingredient": ingredient,
            "amount": amount, "weight_unit": weight_unit
        })

    def delete_nutrition_plan(self, pid):
        return self._delete(f"/api/v2/nutritionplan/{pid}/")

    # ── Ingredients ──

    def list_ingredients(self, params=None):
        return self._get("/api/v2/ingredient/", params)

    def list_ingredient_info(self, params=None):
        return self._get("/api/v2/ingredientinfo/", params)

    # ── Measurements ──

    def create_measurement_category(self, name, unit):
        return self._post("/api/v2/measurement-category/", {"name": name, "unit": unit})

    def list_measurement_categories(self):
        return self._get("/api/v2/measurement-category/")

    def create_measurement(self, category, date, value, notes=""):
        return self._post("/api/v2/measurement/", {
            "category": category, "date": date, "value": value, "notes": notes
        })

    def list_measurements(self, params=None):
        return self._get("/api/v2/measurement/", params)

    def delete_measurement(self, mid):
        return self._delete(f"/api/v2/measurement/{mid}/")

    # ── Gallery ──

    def list_gallery(self, params=None):
        return self._get("/api/v2/gallery/", params)

    def upload_gallery(self, image_path, date, description=""):
        with open(image_path, "rb") as f:
            return self._post("/api/v2/gallery/", files={"image": f}, data={
                "date": date, "description": description
            })

    def delete_gallery(self, gid):
        return self._delete(f"/api/v2/gallery/{gid}/")

    # ── Exercises ──

    def list_exercises(self, params=None):
        return self._get("/api/v2/exercise/", params)

    def get_exercise(self, eid):
        return self._get(f"/api/v2/exercise/{eid}/")

    def list_exercise_info(self, params=None):
        return self._get("/api/v2/exerciseinfo/", params)

    def get_exercise_info(self, eid):
        return self._get(f"/api/v2/exerciseinfo/{eid}/")

    def list_exercise_translations(self, params=None):
        return self._get("/api/v2/exercise-translation/", params)

    def list_exercise_categories(self):
        return self._get("/api/v2/exercisecategory/")

    def list_muscles(self):
        return self._get("/api/v2/muscle/")

    def list_equipment(self):
        return self._get("/api/v2/equipment/")

    def list_exercise_images(self, params=None):
        return self._get("/api/v2/exerciseimage/", params)

    def list_exercise_videos(self, params=None):
        return self._get("/api/v2/video/", params)

    def list_exercise_comments(self, params=None):
        return self._get("/api/v2/exercisecomment/", params)

    def list_exercise_aliases(self, params=None):
        return self._get("/api/v2/exercisealias/", params)

    # ── User Profile ──

    def get_profile(self):
        return self._get("/api/v2/userprofile/")

    def update_profile(self, **kwargs):
        return self._post("/api/v2/userprofile/", kwargs)

    # ── Trophies ──

    def list_trophies(self):
        return self._get("/api/v2/trophy/")

    def trophy_progress(self):
        return self._get("/api/v2/trophy/progress/")

    def user_trophies(self):
        return self._get("/api/v2/user-trophy/")

    def user_stats(self):
        return self._get("/api/v2/user-statistics/")

    # ── Utility ──

    def version(self):
        return self._get("/api/v2/version/")

    def check_permission(self, permission_name):
        return self._get("/api/v2/check-permission/", {"permission": permission_name})

    def register(self, username, email, password):
        return self._post("/api/v2/register/", {"username": username, "email": email, "password": password})

    def list_languages(self):
        return self._get("/api/v2/language/")

    def list_licenses(self):
        return self._get("/api/v2/license/")

    def list_weight_units(self):
        return self._get("/api/v2/setting-weightunit/")

    def list_repetition_units(self):
        return self._get("/api/v2/setting-repetitionunit/")
```
