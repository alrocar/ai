import json
import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider
import asyncio
import sys
import subprocess

load_dotenv()

def find_git_root():
    """Find the root of the git repository"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return os.getcwd()

GIT_REPO_ROOT = find_git_root()

git_server = MCPServerStdio(
    command="uvx",
    args=["mcp-server-git"],
    tool_prefix="git_",
)

SYSTEM_PROMPT = f"""
You are a Git commit message generator. Your job is to analyze STAGED Git changes and output ONLY a clean commit message.

IMPORTANT: The Git repository root is: {GIT_REPO_ROOT}
Always use this path as the repository path for all Git operations.

Your task:
1. Check git status to see what files are STAGED for commit
2. Analyze ONLY the staged changes (git diff --cached) to understand what was modified
3. Generate a detailed but concise commit message based on STAGED changes only

Commit message guidelines:
- Follow conventional commit format: type(scope): description
- Types: feat, fix, docs, style, refactor, test, chore
- Be descriptive and include key changes, but stay concise
- Use imperative mood ("Add feature" not "Added feature")
- Include what was added, modified, or removed when significant
- Mention new files, folders, or major functionality changes
- Group related changes logically
- No extra formatting, explanations, or questions
- Output ONLY the commit message text
- IGNORE unstaged changes and untracked files

Examples of good detailed commit messages:
- feat: add user authentication system with JWT tokens and password hashing
- fix: resolve memory leak in data processing and update error handling
- docs: update README with installation guide and add API documentation
- refactor: reorganize project structure and simplify database connection logic
- chore: add agents folder structure and update project dependencies

When analyzing STAGED changes:
- Note new directories or file structures being committed
- Identify major functionality additions or modifications in staged files
- Include configuration changes or dependency updates being committed
- Mention documentation updates or README changes being committed
- Group similar staged changes together in the description

Use "{GIT_REPO_ROOT}" as the repository path for all Git operations.
Focus ONLY on staged changes (git diff --cached), not unstaged or untracked files.
Output ONLY the commit message - no other text, formatting, or explanations.
"""

service_account_info = json.loads(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
model = GeminiModel(
    'gemini-2.0-flash-001',
    provider=GoogleVertexProvider(service_account_info=service_account_info),
)

agent = Agent(
    model=model,
    mcp_servers=[
        git_server,
    ],
    system_prompt=SYSTEM_PROMPT,
)

async def generate_commit_message():
    """Generate a commit message based on current STAGED changes"""
    prompt = f"""
    Analyze the STAGED changes in the repository at {GIT_REPO_ROOT} and generate a commit message.
    
    1. Check git status to see what files are STAGED for commit
    2. Analyze ONLY the staged changes with git diff --cached to understand what was modified
    3. Generate a single commit message following conventional commit format based on STAGED changes only
    
    Use "{GIT_REPO_ROOT}" as the repository path for all Git operations.
    
    IMPORTANT: Only analyze staged changes (git diff --cached). Ignore unstaged changes and untracked files.
    Output ONLY the commit message text - no explanations, no formatting, no questions.
    """
    
    try:
        async with agent.run_mcp_servers():
            result = await agent.run(prompt)
            commit_message = result.output.strip()

            lines = commit_message.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('*') and not line.startswith('-'):
                    print(line)
                    return

            for line in lines:
                line = line.strip()
                if line:
                    print(line)
                    return

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

async def main():
    await generate_commit_message()

if __name__ == "__main__":
    asyncio.run(main()) 
