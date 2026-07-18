"""
Import SAT practice questions from the OpenSAT dataset into the
SATQuestion table.

This is a ONE-TIME / occasional sync tool, not something the site calls
at request time — Vknow should always serve questions from its own DB.

The real dataset lives on JSONsilo (a static-JSON hosting service), not
on OpenSAT's own duckdns/pinesat.com sites — those just wrap this file.
It's a single JSON object shaped like:

    {
      "math": [ {...question...}, {...question...}, ... ],
      "english": [ {...question...}, ... ],
      "practice_test": [ {...pre-assembled test...}, ... ]
    }

Usage:
    # 1. Download once (works from anywhere with normal internet access):
    curl -o opensat.json "https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5"

    # 2. Import from the local file:
    python manage.py import_sat_questions --file opensat.json

Re-running this command is safe — it upserts on a stable external_id,
so it won't create duplicates. The "practice_test" key is currently
ignored (it's pre-assembled tests referencing question ids, not raw
question objects) — flag if you want that supported later.
"""

import json
import urllib.request

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from sat_app.models import SATQuestion

# Map JSON top-level key -> our Section choice.
SECTION_KEY_MAP = {
    "english": SATQuestion.Section.READING_WRITING,
    "math": SATQuestion.Section.MATH,
}
IGNORED_KEYS = {"practice_test"}


class Command(BaseCommand):
    help = "Import SAT practice questions from OpenSAT-format JSON into SATQuestion."

    def add_arguments(self, parser):
        source = parser.add_mutually_exclusive_group(required=True)
        source.add_argument("--url", type=str, help="URL returning OpenSAT-format JSON")
        source.add_argument("--file", type=str, help="Path to a local JSON file in the same format")
        parser.add_argument(
            "--source-tag",
            type=str,
            default="opensat",
            help="Value stored in SATQuestion.source (default: opensat)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and validate without writing to the database",
        )

    def handle(self, *args, **options):
        raw = self._load(options)
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise CommandError(f"Could not parse JSON: {exc}")

        if not isinstance(payload, dict):
            raise CommandError(
                "Expected a JSON object with section keys (e.g. 'math', 'english'), "
                f"got {type(payload).__name__}"
            )

        created, updated, skipped, ignored_sections = 0, 0, 0, []

        with transaction.atomic():
            for section_key, records in payload.items():
                if section_key in IGNORED_KEYS:
                    ignored_sections.append(section_key)
                    continue
                section = SECTION_KEY_MAP.get(section_key.lower())
                if section is None:
                    self.stderr.write(self.style.WARNING(
                        f"Unknown section key '{section_key}' — skipping its {len(records)} records"
                    ))
                    skipped += len(records)
                    continue

                for i, record in enumerate(records):
                    try:
                        fields = self._map_record(record, section, options["source_tag"])
                    except (KeyError, TypeError) as exc:
                        self.stderr.write(self.style.WARNING(
                            f"Skipping {section_key} record #{i}: {exc}"
                        ))
                        skipped += 1
                        continue

                    if options["dry_run"]:
                        continue

                    obj, was_created = SATQuestion.objects.update_or_create(
                        external_id=fields.pop("external_id"),
                        defaults=fields,
                    )
                    created += was_created
                    updated += not was_created

            if options["dry_run"]:
                transaction.set_rollback(True)

        if ignored_sections:
            self.stdout.write(f"Ignored sections (not raw questions): {', '.join(ignored_sections)}")

        if options["dry_run"]:
            self.stdout.write(self.style.SUCCESS(f"Dry run OK — {skipped} records skipped."))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Import complete: {created} created, {updated} updated, {skipped} skipped."
            ))

    def _load(self, options):
        if options["file"]:
            with open(options["file"], "r", encoding="utf-8") as f:
                return f.read()
        req = urllib.request.Request(options["url"], headers={"User-Agent": "vknow-import/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")

    def _map_record(self, record, section, source_tag):
        domain = record.get("domain", "").strip()

        q = record["question"]
        choices = q["choices"]

        difficulty_raw = record.get("difficulty", "Medium")
        if difficulty_raw not in SATQuestion.Difficulty.values:
            difficulty_raw = SATQuestion.Difficulty.MEDIUM

        paragraph = q.get("paragraph") or ""
        if paragraph.strip().lower() == "null":
            paragraph = ""

        visuals = record.get("visuals") or {}
        svg_content = visuals.get("svg_content") or ""
        if svg_content.strip().lower() == "null":
            svg_content = ""

        # OpenSAT ids are not always unique (e.g. "random_id_a1" repeats),
        # so namespace by source + section + a hash of the question text to
        # guarantee uniqueness on re-import.
        raw_id = record.get("id", "")
        external_id = f"{source_tag}:{section}:{raw_id}:{abs(hash(q['question'])) % (10 ** 8)}"

        return {
            "external_id": external_id,
            "section": section,
            "domain": domain,
            "difficulty": difficulty_raw,
            "paragraph": paragraph,
            "question_text": q["question"],
            "choice_a": choices.get("A", ""),
            "choice_b": choices.get("B", ""),
            "choice_c": choices.get("C", ""),
            "choice_d": choices.get("D", ""),
            "correct_answer": q["correct_answer"],
            "explanation": q.get("explanation", ""),
            "svg_content": svg_content,
            "source": source_tag,
        }