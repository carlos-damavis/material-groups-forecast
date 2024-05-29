from setuptools import setup, find_packages

setup(
    name="material_groups_forecast",
    version="0.1.0.dev0",
    packages=find_packages(".", exclude=["test", "test.*"]),
    url="",
    license="",
    install_requires=[
        "db-dtypes==1.2.0",
        "google-cloud-bigquery==3.23.1",
        "holidays==0.47",
        "numpy==1.24.4",
        "pandas==2.2.2",
        "prophet==1.1.5",
        "pyarrow==15.0.2",
        "python-dateutil==2.9.0.post0",
        "pytz==2024.1",
        "scikit-learn==1.5.0",
        "six==1.16.0",
        "tzdata==2024.1"
    ],
    entry_points={
        "console_scripts": [
            "train_models=material_groups_forecast.main.train_main:main"
        ]
    },
    include_package_data=True,
    author="Carlos Isaac Rodriguez Prado",
    author_email="carlos.rodriguez@damavis.com"
)
