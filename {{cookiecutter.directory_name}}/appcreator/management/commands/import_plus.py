import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import CourtDecission, KeyWord, Person


class Command(BaseCommand):
    help = "Import Data"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("./data/tb_ENAUT.csv")
        print(f"adding {len(df)} Decission-Author relations")
        for i, row in tqdm(df.iterrows(), total=len(df)):
            try:
                court = CourtDecission.objects.get(legacy_pk=row["ENAUT_Entscheidung"])
                autor = Person.objects.filter(legacy_pk=row["ENAUT_Autor"])
            except ObjectDoesNotExist:
                continue
            court.author.add(*autor)

        df = pd.read_csv("./data/tb_ENST.csv")
        print(f"adding {len(df)} Decission-Keyword relations")
        for i, row in tqdm(df.iterrows(), total=len(df)):
            try:
                court = CourtDecission.objects.get(legacy_pk=row["ENST_Entscheidung"])
            except:
                print(row["ENST_Entscheidung"])
                continue
            kw = KeyWord.objects.filter(legacy_pk=row["ENST_Stichwort"])
            court.keyword.add(*kw)
