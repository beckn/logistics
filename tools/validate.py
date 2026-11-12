#!/usr/bin/env python3
"""Validate the logistics schema packs and the example payloads in the docs.

    python tools/validate.py packs
    python tools/validate.py examples [--core path/to/beckn.yaml]

`packs` checks every pack under schema/<Name>/<version>/.
`examples` checks every fenced ```json block under docs/example_implementations: the message
against the core Beckn action schema, and every typed logistics object
against its pack.

Exit status is non-zero if anything fails.
"""
import argparse
import itertools
import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from pyld import jsonld
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema"
HOST = "https://schema.nfh.global"
# Core protocol the examples are checked against (beckn/protocol-specifications-v2).
CORE_COMMIT = "a22300a"
CORE_URL = f"https://raw.githubusercontent.com/beckn/protocol-specifications-v2/{CORE_COMMIT}/api/v2.0.0/beckn.yaml"
REQUIRED_FILES = ["attributes.yaml", "schema.json", "context.jsonld", "vocab.jsonld", "README.md"]
# A bundle pack carries several types and has no type of its own.
BUNDLES = {"Logistics"}
EXAMPLES = ROOT / "docs" / "example_implementations"
PACK_URL = re.compile(re.escape(HOST) + r"/([A-Za-z]+)/(v[\d.]+)/(.+)$")

errors = []


def fail(where, msg):
    errors.append(f"{where}: {msg}")


def packs():
    for d in sorted(p for p in SCHEMA.iterdir() if p.is_dir()):
        for v in sorted(p for p in d.iterdir() if p.is_dir()):
            yield d.name, v.name, v


def load_pack_file(url):
    """Resolve a schema.nfh.global URL to the file in this repository."""
    m = PACK_URL.match(url.split("#")[0])
    if not m or not (SCHEMA / m.group(1) / m.group(2) / m.group(3)).is_file():
        raise LookupError(f"not in this repository: {url}")
    return SCHEMA / m.group(1) / m.group(2) / m.group(3)


def retrieve_schema(url):
    doc = json.loads(load_pack_file(url).read_text())
    doc.pop("$id", None)  # $id is the pack IRI, not the document URL
    return Resource(contents=doc, specification=DRAFT202012)


PACK_REGISTRY = Registry(retrieve=retrieve_schema)


def pack_schema(name, version="v2.0"):
    return json.loads((SCHEMA / name / version / "schema.json").read_text())


def deref(schema):
    """Follow a cross-pack or local $ref to the schema it names."""
    while isinstance(schema, dict) and "$ref" in schema and schema["$ref"].startswith(HOST):
        schema = json.loads(load_pack_file(schema["$ref"]).read_text())
    return schema


def unknown_properties(instance, schema, path=""):
    """Properties in `instance` that the schema does not define (packs leave objects open)."""
    schema = deref(schema)
    out = []
    if isinstance(instance, dict) and isinstance(schema, dict) and "properties" in schema:
        for key, value in instance.items():
            if key in ("@context", "@type"):
                continue
            if key not in schema["properties"]:
                out.append(f"{path}/{key}")
            else:
                out += unknown_properties(value, schema["properties"][key], f"{path}/{key}")
    elif isinstance(instance, list) and isinstance(schema, dict) and "items" in schema:
        for i, value in enumerate(instance):
            out += unknown_properties(value, schema["items"], f"{path}/{i}")
    return out


def synthesise(schema, depth=0):
    """Build an instance from the schema's own examples, enums and types."""
    schema = deref(schema)
    if "example" in schema and schema.get("type") not in ("object", "array"):
        return schema["example"]
    if "enum" in schema:
        return schema["enum"][0]
    kind = schema.get("type")
    if kind == "object" or "properties" in schema:
        required = schema.get("required", [])
        return {k: synthesise(v, depth + 1) for k, v in schema.get("properties", {}).items() if depth < 6 or k in required}
    if kind == "array":
        return [synthesise(schema.get("items", {}), depth + 1)]
    by_format = {"date-time": "2026-06-03T16:35:00Z", "date": "2026-06-03", "uri": "https://example.org/x", "email": "a@example.org"}
    if schema.get("format") in by_format:
        return by_format[schema["format"]]
    return {"string": "x", "number": 1.5, "integer": 1, "boolean": True}.get(kind, "x")


def attributes_as_json_schema(node):
    """Rewrite attributes.yaml references into the form schema.json uses."""
    if isinstance(node, dict):
        out = {}
        for key, value in node.items():
            if key == "x-iri":
                continue
            if key == "$ref" and isinstance(value, str) and value.startswith(HOST):
                value = re.sub(r"/attributes\.yaml#/components/schemas/[A-Za-z]+$", "/schema.json", value)
            out[key] = attributes_as_json_schema(value)
        return out
    if isinstance(node, list):
        return [attributes_as_json_schema(v) for v in node]
    return node


def normalise_text(node):
    """Collapse whitespace in strings, so YAML block scalars compare equal to their JSON form."""
    if isinstance(node, dict):
        return {k: normalise_text(v) for k, v in node.items()}
    if isinstance(node, list):
        return [normalise_text(v) for v in node]
    return " ".join(node.split()) if isinstance(node, str) else node


def collect_refs(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                yield value
            else:
                yield from collect_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from collect_refs(value)


def resolve_pointer(doc, pointer):
    for part in [p for p in pointer.split("/") if p]:
        doc = doc[part]
    return doc


def check_packs():
    contexts = []
    for name, version, path in packs():
        where = f"schema/{name}/{version}"
        if not re.fullmatch(r"v\d+(\.\d+){0,2}", version):
            fail(where, "version directory must look like v2.0")
        missing = [f for f in REQUIRED_FILES if not (path / f).is_file()]
        if not (path.parent / "README.md").is_file():
            missing.append("../README.md")
        if missing:
            fail(where, f"missing files: {missing}")
            continue
        if (path / "attributes.jsonschema.yaml").exists():
            fail(where, "attributes.jsonschema.yaml is superseded by schema.json")

        try:
            attrs = yaml.safe_load((path / "attributes.yaml").read_text())
            schema = json.loads((path / "schema.json").read_text())
            context = json.loads((path / "context.jsonld").read_text())
            vocab = json.loads((path / "vocab.jsonld").read_text())
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            fail(where, f"does not parse: {exc}")
            continue

        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001
            fail(where, f"schema.json is not valid JSON Schema 2020-12: {str(exc).splitlines()[0]}")

        # Every reference must resolve to a file, and a fragment, in this repository.
        for doc, label in ((attrs, "attributes.yaml"), (schema, "schema.json")):
            for ref in collect_refs(doc):
                try:
                    if ref.startswith("#"):
                        resolve_pointer(doc, ref[1:])
                    elif ref.startswith(HOST):
                        target = load_pack_file(ref)
                        if "#" in ref:
                            resolve_pointer(yaml.safe_load(target.read_text()), ref.split("#", 1)[1])
                    else:
                        raise LookupError("references must be local or on " + HOST)
                except (LookupError, KeyError, TypeError) as exc:
                    fail(where, f"{label}: unresolved $ref {ref} ({exc})")

        components = (attrs.get("components") or {}).get("schemas") or {}
        if name in BUNDLES:
            continue
        if name not in components:
            fail(where, f"attributes.yaml does not define components.schemas.{name}")
            continue
        body = components[name]

        if attrs.get("info", {}).get("title") != name or body.get("title") != name or schema.get("title") != name:
            fail(where, f"title must be {name} in attributes.yaml (info and schema) and schema.json")
        if not str(attrs.get("info", {}).get("version", "")).startswith(version[1:]):
            fail(where, "info.version does not match the version directory")

        # attributes.yaml and schema.json must describe the same type.
        expected = normalise_text(attributes_as_json_schema(body))
        actual = normalise_text({k: v for k, v in schema.items() if k not in ("$id", "$schema", "x-iri")})
        if expected != actual:
            keys = sorted(k for k in set(expected) | set(actual) if expected.get(k) != actual.get(k))
            fail(where, f"attributes.yaml and schema.json differ in: {keys}")

        # The type must accept an instance built from its own examples, and reject an OpenAPI envelope.
        validator = Draft202012Validator({"$ref": f"{HOST}/{name}/{version}/schema.json"}, registry=PACK_REGISTRY)
        problems = list(validator.iter_errors(synthesise(schema)))
        if problems:
            fail(where, f"instance built from the schema's examples is rejected: {problems[0].message[:120]}")
        if schema.get("required") and validator.is_valid({"components": {"schemas": {}}}):
            fail(where, "schema.json accepts an OpenAPI envelope")

        ctx = context.get("@context", {})
        missing_terms = sorted(p for p in body.get("properties", {}) if p not in ctx and not p.startswith("@"))
        if name not in ctx or missing_terms:
            fail(where, f"context.jsonld lacks terms: {([name] if name not in ctx else []) + missing_terms}")
        if not any(str(node.get("@id", "")).endswith(":" + name) and "Class" in str(node.get("@type")) for node in vocab.get("@graph", [])):
            fail(where, f"vocab.jsonld declares no class for {name}")

        # README property rows must name the same reference as attributes.yaml.
        readme = (path / "README.md").read_text()
        for prop, spec in body.get("properties", {}).items():
            ref = spec.get("$ref") or (spec.get("items") or {}).get("$ref")
            row = re.search(r"^\| `" + re.escape(prop) + r"` \|.*\$ref: (\S+)", readme, re.M)
            if ref and row and row.group(1) != ref:
                fail(where, f"README row for `{prop}` names {row.group(1)}, attributes.yaml names {ref}")

        contexts.append((name, f"{HOST}/{name}/{version}/context.jsonld"))

    # Pack contexts are protected, so any two used together must agree on shared terms.
    def loader(url, options=None):
        return {"contentType": "application/ld+json", "contextUrl": None, "documentUrl": url,
                "document": json.loads(load_pack_file(url).read_text())}

    jsonld.set_document_loader(loader)
    for (a, url_a), (b, url_b) in itertools.permutations(contexts, 2):
        try:
            jsonld.expand({"@context": [url_a, url_b], "@type": a, "id": "x"})
        except Exception as exc:  # noqa: BLE001
            fail("schema", f"contexts of {a} and {b} cannot be used together: {str(exc)[:100]}")
    print(f"packs checked: {sum(1 for _ in packs())}")


ACTION_SCHEMA = {
    "discover": "DiscoverAction", "on_discover": "OnDiscoverAction", "select": "SelectAction",
    "on_select": "OnSelectAction", "init": "InitAction", "on_init": "OnInitAction",
    "confirm": "ConfirmAction", "on_confirm": "OnConfirmAction", "status": "StatusAction",
    "on_status": "OnStatusAction", "update": "UpdateAction", "on_update": "OnUpdateAction",
    "track": "TrackAction", "on_track": "OnTrackAction", "rate": "RateAction", "on_rate": "OnRateAction",
    "cancel": "CancelAction", "on_cancel": "OnCancelAction", "support": "SupportAction", "on_support": "OnSupportAction",
}


def typed_objects(node, path=""):
    if isinstance(node, dict):
        if isinstance(node.get("@type"), str):
            yield path, node
        for key, value in node.items():
            yield from typed_objects(value, f"{path}/{key}")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from typed_objects(value, f"{path}/{i}")


def check_examples(core_path):
    core_text = Path(core_path).read_text() if core_path else urllib.request.urlopen(CORE_URL, timeout=60).read().decode()
    core = yaml.safe_load(core_text)
    core_registry = Registry().with_resource("urn:beckn-core", Resource(contents=core, specification=DRAFT202012))
    pack_names = {name for name, _, _ in packs()} - BUNDLES

    blocks = messages = objects = 0
    for doc in sorted(EXAMPLES.rglob("*.md")):
        text = doc.read_text()
        for match in re.finditer(r"```json\n(.*?)```", text, re.S):
            blocks += 1
            where = f"{doc.relative_to(ROOT)}:{text[:match.start()].count(chr(10)) + 2}"
            try:
                payload = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                fail(where, f"not valid JSON: {exc}")
                continue

            action = (payload.get("context") or {}).get("action") if isinstance(payload, dict) else None
            if action:
                messages += 1
                if action not in ACTION_SCHEMA:
                    fail(where, f"unknown action {action!r}")
                else:
                    # The core action schemas describe the message; Context describes the envelope.
                    for part, schema_name in (("context", "Context"), ("message", ACTION_SCHEMA[action])):
                        validator = Draft202012Validator({"$ref": f"urn:beckn-core#/components/schemas/{schema_name}"}, registry=core_registry)
                        for err in sorted(validator.iter_errors(payload.get(part, {})), key=lambda e: list(e.absolute_path))[:6]:
                            fail(where, f"core {schema_name} /{part}/{'/'.join(map(str, err.absolute_path))}: {err.message[:140]}")

            for path, obj in typed_objects(payload):
                kind = obj["@type"]
                if kind not in pack_names:
                    continue
                objects += 1
                if path.split("/")[-1].endswith("Attributes") and obj.get("@context") != f"{HOST}/{kind}/v2.0/context.jsonld":
                    fail(where, f"{path}: @context must be {HOST}/{kind}/v2.0/context.jsonld")
                validator = Draft202012Validator({"$ref": f"{HOST}/{kind}/v2.0/schema.json"}, registry=PACK_REGISTRY)
                for err in sorted(validator.iter_errors(obj), key=lambda e: list(e.absolute_path))[:6]:
                    fail(where, f"{path} ({kind}) /{'/'.join(map(str, err.absolute_path))}: {err.message[:140]}")
                for extra in unknown_properties(obj, pack_schema(kind)):
                    fail(where, f"{path} ({kind}) {extra}: not a property of the pack")
    print(f"json blocks: {blocks}, protocol messages: {messages}, typed logistics objects: {objects}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("what", choices=["packs", "examples"])
    parser.add_argument("--core", help="local copy of the core beckn.yaml (default: fetch the pinned commit)")
    args = parser.parse_args()
    check_packs() if args.what == "packs" else check_examples(args.core)
    for line in errors:
        print("FAIL", line)
    print(f"{len(errors)} problem(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
