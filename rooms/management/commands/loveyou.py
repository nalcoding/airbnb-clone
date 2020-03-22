from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This Command"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell you?"
        )

    def handle(self, *args, **options):
        print(args, options)
        times = options.get("times")

        for t in range(0, int(times)):
            # print("I love you")
            # self.stdout.write(self.style.SUCCESS("I love you"))
            # self.stdout.write(self.style.WARNING("I love you"))
            self.stdout.write(self.style.ERROR("I love you"))
