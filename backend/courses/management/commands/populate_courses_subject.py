from django.core.management.base import BaseCommand

from courses.models import Subject


class Command(BaseCommand):
    help = 'Populate the courses_subject table with sample data'

    SUBJECTS = [
        "Mathematics",
        "English Literature",
        "Physics",
        "Chemistry",
        "Biology",
        "History",
        "Geography",
        "Computer Science",
        "Art",
        "Music",
        "Physical Education",
        "French",
        "Spanish",
        "German",
        "Economics",
        "Psychology",
        "Philosophy",
        "Political Science",
        "Environmental Science",
        "Astronomy",
        "Statistics",
        "Business Studies",
        "Engineering",
        "Medicine",
        "Linguistics",
        "Film Studies",
        "Drama",
        "Dance",
        "Nutrition",
        "Design and Technology",
        "Sociology",
        "Anthropology",
        "Religious Studies",
        "Ethics",
        "Media Studies",
        "Law",
        "Marketing",
        "Journalism",
        "Graphic Design",
        "Logic",
    ]

    def handle(self, *args, **kwargs):
        Subject.objects.all().delete()

        for subject_name in self.SUBJECTS:
            Subject.objects.create(
                name=subject_name
            )
            self.stdout.write(self.style.SUCCESS(f'Course {subject_name} created. '))
