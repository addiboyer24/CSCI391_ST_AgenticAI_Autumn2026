"""The course content itself: modules, readings, activities, practice quizzes."""
import re

import pytest

import course_data as D

try:
    import checks as CK
except ImportError:  # pragma: no cover
    CK = None

REQUIRED = {"id", "weeks", "part", "chapters", "title", "tagline", "summary", "case", "big_idea", "framework",
            "objectives", "branches", "textbook", "lens", "prompts", "activities"}


def test_fourteen_modules_with_unique_ids():
    ids = [m["id"] for m in D.MODULES]
    assert len(ids) == 14
    assert len(set(ids)) == len(ids)
    assert ids == [f"m{n:02d}" for n in range(1, 15)]


@pytest.mark.parametrize("m", D.MODULES, ids=lambda m: m["id"])
def test_module_has_every_field(m):
    missing = REQUIRED - set(m)
    assert not missing, f"{m['id']} is missing {sorted(missing)}"
    for key in ("title", "tagline", "summary", "case", "big_idea", "textbook"):
        assert m[key].strip(), f"{m['id']}.{key} is empty"
    assert m["part"] in D.PARTS
    assert len(m["objectives"]) >= 2 and len(m["prompts"]) >= 1 and len(m["lens"]) >= 1
    name, steps = m["framework"]
    assert name and len(steps) >= 2
    for head, leaves in m["branches"]:
        assert head and leaves, f"{m['id']}: empty mind-map branch"


def test_every_chapter_is_taught(site):
    taught = {k for m in D.MODULES for k, _ in site.chapter_titles(m)}
    assert taught == set(range(1, len(D.CHAPTERS) + 1)), "a textbook chapter isn't assigned to any module"


def test_parts_run_in_order():
    order = list(D.PARTS)
    seen = [order.index(m["part"]) for m in D.MODULES]
    assert seen == sorted(seen), "modules jump back to an earlier part"


@pytest.mark.parametrize("m", D.MODULES, ids=lambda m: m["id"])
def test_activities_are_well_formed(m, tracked):
    for a in m["activities"]:
        assert a["kind"] in {"lab", "quiz", "project", "code"}, a
        assert a["title"].strip() and a["desc"].strip()
        href = a.get("href")
        if href and not href.startswith("http"):
            assert href in tracked, f"{m['id']}: '{href}' is linked from the site but not committed"


def test_labs_are_numbered_one_to_five():
    labs = [a["title"] for m in D.MODULES for a in m["activities"] if a["kind"] == "lab"]
    nums = [int(re.match(r"Lab (\d)", t).group(1)) for t in labs]
    assert nums == [1, 2, 3, 4, 5]


def test_supplemental_readings_are_https():
    for mid, items in D.SUPPLEMENTAL.items():
        assert mid in {m["id"] for m in D.MODULES}
        for title, url in items:
            assert title.strip() and url.startswith("https://"), (mid, title, url)


@pytest.mark.skipif(CK is None, reason="checks.py not present")
@pytest.mark.parametrize("mid", sorted(getattr(CK, "CHECKS", {})))
def test_practice_quiz_answer_keys_are_valid(mid):
    qs = CK.CHECKS[mid]
    assert len(qs) >= 3
    for q in qs:
        assert q["q"].strip()
        assert len(q["options"]) >= 2
        assert 0 <= q["answer"] < len(q["options"]), f"{mid}: answer index out of range"
        for text, why in q["options"]:
            assert text.strip() and why.strip(), f"{mid}: every option needs feedback"
        assert q["options"][q["answer"]][1].startswith("Right"), f"{mid}: the correct option's feedback should start with 'Right'"
