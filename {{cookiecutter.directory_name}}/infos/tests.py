from django.apps import apps
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from infos.templatetags.infos_extras import project_insts
from infos.templatetags.stats_extras import create_object_count

MODELS = list(apps.all_models["infos"].values())

client = Client()
USER = {"username": "temporary1", "password": "temporary1"}


class InfosTest(TestCase):
    fixtures = ["dump.json"]

    def setUp(self):
        self.client = Client()
        User.objects.create_user(**USER)

    def test_002_listviews(self):
        for x in MODELS:
            try:
                url = x.get_listview_url()
            except AttributeError:
                url = False
            if url:
                response = client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_003_detailviews(self):
        for x in MODELS:
            item = x.objects.first()
            try:
                url = item.get_absolute_url()
            except AttributeError:
                url = False
            if url:
                response = client.get(url, {"pk": item.id})
                self.assertEqual(response.status_code, 200)

    def test_004_project_insts(self):
        self.assertFalse(project_insts())

    def test_005_create_object_count(self):
        stats = create_object_count()
        self.assertTrue(len(stats), 1)
        stats = create_object_count(app="archiv")
        self.assertTrue(len(stats) > 1)

    def test_006_infos_views(self):
        for x in [
            "infos:project-team",
            "infos:about-the-project",
            "infos:about_browse",
        ]:
            url = reverse(x)
            r = client.get(url)
            self.assertTrue(r.status_code, 200)
