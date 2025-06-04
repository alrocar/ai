# gitai

AI-powered git commit messages for staged changes.

## Install

```bash
git clone https://github.com/your-username/gitai.git
cd gitai
uv sync
sudo ln -s $(pwd)/gitai /usr/local/bin/gitai
git config --global alias.ai '!git commit -m "$(cat /tmp/gitai_last_commit)"'
```

The agent uses VertexAI, you should configure your `GOOGLE_APPLICATION_CREDENTIALS` or use a different provider.

## Use

```bash
# stage the files to commit
git add .
# generate a commit message
gitai
# use the previously generated message in git commit
git ai
```

Requires: Python 3.8+, [uv](https://docs.astral.sh/uv/), Google Vertex AI 