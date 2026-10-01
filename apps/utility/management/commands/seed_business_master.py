from django.core.management.base import BaseCommand

from apps.utility.models import (
    LeadSource,
    LeadStatus,
    LeadPriority,
)


class Command(BaseCommand):
    help = "Seed Business Master Data"

    def handle(self, *args, **options):

        lead_sources = [
            "Website",
            "Facebook",
            "Instagram",
            "Google Ads",
            "Google Organic",
            "WhatsApp",
            "Referral",
            "Walk In",
            "Broker",
            "MagicBricks",
            "99acres",
            "Housing",
            "IndiaMART",
        ]

        for name in lead_sources:
            LeadSource.objects.get_or_create(name=name)

        lead_statuses = [
            ("New", "#0d6efd"),
            ("Assigned", "#6610f2"),
            ("Contacted", "#fd7e14"),
            ("Follow Up", "#ffc107"),
            ("Meeting Fixed", "#20c997"),
            ("Site Visit", "#198754"),
            ("Negotiation", "#6f42c1"),
            ("Booked", "#198754"),
            ("Won", "#198754"),
            ("Lost", "#dc3545"),
            ("Duplicate", "#6c757d"),
            ("Junk", "#343a40"),
        ]

        for name, color in lead_statuses:
            LeadStatus.objects.get_or_create(
                name=name,
                defaults={
                    "color": color,
                },
            )

        priorities = [
            "Hot",
            "High",
            "Medium",
            "Low",
        ]

        for name in priorities:
            LeadPriority.objects.get_or_create(name=name)

        self.stdout.write(
            self.style.SUCCESS(
                "Business master data seeded successfully."
            )
        )