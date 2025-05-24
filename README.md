# ⚡ FastBFF

**FastBFF** is a blazing-fast, configuration-driven **Backend-for-Frontend (BFF)** layer powered by [FastAPI](https://fastapi.tiangolo.com/). It lets you create REST APIs using just a simple YAML file — no boilerplate, no code, no nonsense.

> "Stop writing backend glue — start shipping frontends faster."

---

## 🙌 Why FastBFF?

Because your frontend team shouldn’t be blocked by API boilerplate. With FastBFF, you build the bridge between frontend and real data — fast.

---

## 🚀 Features

- 🧾 **YAML-Powered** — define your routes and logic with a single config file
- ⚡ **FastAPI Under the Hood** — async-ready, performant, and auto-documented
- 🪄 **Zero Code Endpoints** — serve static data, proxy APIs, or echo POST bodies
- 🌍 **Built-in Config for Host, Port, CORS, Logging**
- 🧩 **Pluggable Design** — easily extendable with custom Python logic
- 🔁 **Hot Reload Dev Mode** — just edit your config and go

---

## 📚 Requirements

- Python 3.7+
- pip (Python package installer)
- Recommended: virtualenv for environment isolation

## ⚙️ Installation

```bash
git clone https://github.com/simonsayz13/fastbff
cd fastbff
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```
---

## 🛠 Example

Here’s a simple `config.yaml` to get you started:

```yaml
startup:
  host: 127.0.0.1
  port: 9000
  reload: true
  log_level: info
  title: FastBFF
  version: 1.0.0

routes:
  - path: /users
    method: GET
    source:
      type: static
      data:
        - id: 1
          name: "Alice"
        - id: 2
          name: "Bob"

  - path: /cat-fact
    method: GET
    source:
      type: proxy
      url: https://catfact.ninja/fact

  - path: /submit
    method: POST
    source:
      type: echo
```

Then just run:

```bash
python main.py
```

And you’ll get:

- 📍 `GET /users` → returns predefined JSON
- 🐱 `GET /cat-fact` → proxies to a live API
- 🔁 `POST /submit` → echoes back your payload

---

## 📦 Roadmap

- [ ] Support for additional HTTP methods (PUT, PATCH, DELETE, etc.)
- [ ] Route validation & OpenAPI schema generation
- [ ] Middleware (auth, rate-limiting, logging)
- [ ] Config-driven response transformation
- [ ] Support for loading external JSON/YAML files
- [ ] CLI support (e.g. `fastbff run config.yaml`)

---

## 📄 License

MIT — do whatever you want, but consider contributing back. ❤️

---

## ✨ Contributing

PRs, issues, and feature requests welcome!

---

Created by [Simon Tan](https://github.com/simonsayz13)
