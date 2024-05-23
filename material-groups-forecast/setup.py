from setuptools import setup, find_packages

setup(
    name="material_groups_forecast",
    version="0.1.0.dev0",
    packages=find_packages(".", exclude=["test", "test.*"]),
    url="",
    license="",
    install_requires=[
        "pandas==2.2.2",
        "pyarrow==15.0.2",
        "scikit-learn==1.5.0"
    ],
    entry_points={
        "console_scripts": [
            "train_models=train_main:main"
        ]
    },
    include_package_data=True,
    author="Carlos Isaac Rodriguez Prado",
    author_email="carlos.rodriguez@damavis.com"
)
