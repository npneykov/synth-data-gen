# 🧪 Synthetic Test-Data Generator

> Fast, schema-aware fake-data dumps for Postgres — **single-file binary, GDPR-safe**.

[![Release](https://img.shields.io/github/v/release/npneykov/synth-data-gen?logo=github)](../../releases)
[![CI](https://img.shields.io/github/actions/workflow/status/npneykov/synth-data-gen/ci.yml?label=CI&logo=githubactions)](../../actions)
[![EULA v1.0](https://img.shields.io/badge/EULA-v1.0-blue.svg)](legal/EULA_v1.0.txt)

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [📦 Quickstart](#-quickstart)
- [⚙️ CLI options](#️-cli-options)
- [📜 Licence & EULA](#-licence--eula)
- [🛠 Development](#-development)
- [🤝 Contact & Support](#-contact--support)

---

## ✨ Features

- **One-command dump** — generate `dump.sql` that respects all FK constraints.
- **Realistic mock values** — names, IBANs, VAT, lorem text (Faker providers).
- **Deterministic** — pass `--seed` to get identical dumps across teams.
- **Zero dependencies** — shipped as a PyInstaller binary for macOS, Linux, Windows.
- **Privacy first** — no production data, no VPNs, GDPR compliant.

---

## 📦 Quickstart

```bash
# 1. Download the binary for your platform
curl -L -o synthgen \
  https://github.com/npneykov/synth-data-gen/releases/latest/download/synthgen_linux

chmod +x synthgen

# 2. Run it with your licence key and flags
export SYNTH_KEY="YOUR_KEY"
./synthgen \
  --db postgresql://user:pass@host/db \
  --rows 500 \
  --seed 42 \
  --out dump.sql \
  --verbose
```

---

## ⚙️ CLI options

| Flag            | Default    | Description                                            |
| --------------- | ---------- | ------------------------------------------------------ |
| `-d, --db`      | *required* | SQLAlchemy URL of the source schema (read-only).       |
| `-r, --rows`    | `1000`     | Approximate rows per table.                            |
| `-s, --seed`    | *none*     | Optional random seed for deterministic output.         |
| `-o, --out`     | `dump.sql` | Path to write the generated SQL dump (`-` for stdout). |
| `-v, --verbose` | *off*      | Enable verbose INFO-level logging.                     |

---

## 📜 Licence & EULA

The distributed binary is governed by our [End-User Licence Agreement](legal/EULA_v1.0.txt).
Source code is **not** open-source at this time; redistribution is prohibited.

---

## 🛠 Development

```bash
git clone git@github.com:npneykov/synth-data-gen.git
cd synth-data-gen
make init         # sets up venv, installs dev tools, pre-commit hooks
make run ARGS="--db sqlite:///test.db --verbose"
make test         # runs pytest suite
```

## 🤝 Contact & Support

For bug reports or feature requests, please open an issue in the GitHub repo.

For licence key or general queries, email <support@your-domain.com>

---

Built with the **simple · effective · future-proof** mantra.
