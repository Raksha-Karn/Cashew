from setuptools import setup, find_packages

setup(
    name="finance-tracker",           
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "finance-tracker=cli_based_finance_tracker.main:main",  
        ],
    },
    author="Raksha Karn",
    author_email="rakshakarn07@gmail.com",
    description="CLI Personal Finance Tracker with transactions, budget, and reports",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Raksha-Karn/Cashew",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
