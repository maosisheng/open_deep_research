from setuptools import setup

setup(
    name="smolagents",
    version="1.10.0.dev0",
    description="🤗 smolagents: a barebones library for agents. Agents write python code to call tools or orchestrate other agents.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
)