# gai

AI-powered git commit messages for staged changes.

## Install

```bash
git clone https://github.com/your-username/gai.git
cd gai
uv sync
sudo ln -s $(pwd)/gai /usr/local/bin/gai
# create an alias in your bash profile
alias gc="gai && git commit -m \"\$(cat /tmp/gai_last_commit)\""
```

The agent uses VertexAI, you should configure your `GOOGLE_APPLICATION_CREDENTIALS` or use a different provider.

## Use

```bash
# stage the files to commit
> git add .
# generate a commit message
> gai
docs: rename GitAI to gai in README
# use the previously generated message in git commit
> gc
[main a4f9eb7] docs: rename GitAI to gai in README
 1 file changed, 2 insertions(+), 2 deletions(-)
```

The `gc` alias automatically uses the last `gai` generated message. If no `gai` message exists, it falls back to `git commit --verbose` behavior.

Requires: Python 3.8+, [uv](https://docs.astral.sh/uv/), Google Vertex AI