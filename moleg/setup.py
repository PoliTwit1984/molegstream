from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="moleg", 
      version="0.0.1",
      description="Moleg Twitter Analysis Tool",
      py_modules=["moleg"],
      package_dir={"": "src"},
)      