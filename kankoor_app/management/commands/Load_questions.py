# import requests
# from django.core.management.base import BaseCommand
# from kankoor_app.models import Question

# DATASETS = {
#     'Geology': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/geology/geology.json',
#     'Dari': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/dari/dari.json',
#     'Chemistry': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/chemistry/general_chemistry.json',
#     'Physics': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/physics/general_physics.json',
#     'Biology': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/biology/biology.json',
#     'Math': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/math/math_geometry.json',
# }


# class Command(BaseCommand):
#     help = 'Load Kankor questions from GitHub into the database'

#     def handle(self, *args, **kwargs):
#         Question.objects.all().delete()
#         total = 0

#         for subject, url in DATASETS.items():
#             self.stdout.write(f"Loading {subject}...")
#             try:
#                 res = requests.get(url, timeout=10)
#                 questions = res.json()

#                 for q in questions:
#                     Question.objects.create(
#                         question_id=q.get('id', 0),
#                         question=q.get('question', ''),
#                         options=q.get('options', []),
#                         correct_option=q.get('correctOption', 1),
#                         correct_answer=q.get('correctAnswer', ''),
#                         subject=subject,
#                         difficulty=q.get('difficulty', 'easy'),
#                     )
#                     total += 1

#                 self.stdout.write(self.style.SUCCESS(f"  ✓ {len(questions)} questions loaded"))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f"  ✗ Failed: {e}"))

#         self.stdout.write(self.style.SUCCESS(f"\nDone! {total} total questions loaded."))


  
import requests
from django.core.management.base import BaseCommand
from kankoor_app.models import Question

DATASETS = {
    'Geology': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/geology/geology.json',
    'Dari': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/dari/dari.json',
    'Chemistry': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/chemistry/general_chemistry.json',
    'Physics': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/physics/general_physics.json',
    'Biology': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/biology/Biology.json',
    'Math': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/math/math_geomatry.json',
    'Math_Limit': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/math/math_limit.json',
    'Math_Integral': 'https://raw.githubusercontent.com/Hadi-jawdi/Afghanistan-kankoor-exam-dataset/main/Afghanistan-kankoor-questions-dataset/dataset/data/math/math_integral.json',
}


class Command(BaseCommand):
    help = 'Load Kankor questions from GitHub into the database'

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()
        total = 0

        for subject, url in DATASETS.items():
            self.stdout.write(f"Loading {subject}...")
            try:
                res = requests.get(url, timeout=10)
                self.stdout.write(f"  First 200 chars: {res.text[:200]}")
                questions = res.json()
                self.stdout.write(f"  Type: {type(questions)}")

                for q in questions:
                    Question.objects.create(
                        question_id=q.get('id', 0),
                        question=q.get('question', ''),
                        options=q.get('options', []),
                        correct_option=q.get('correctOption', 1),
                        correct_answer=q.get('correctAnswer', ''),
                        subject=subject,
                        difficulty=q.get('difficulty', 'easy'),
                    )
                    total += 1

                self.stdout.write(self.style.SUCCESS(f"  ✓ {len(questions)} questions loaded"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Failed: {e}"))

        self.stdout.write(self.style.SUCCESS(f"\nDone! {total} total questions loaded."))