import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mixsimulator",
    version="0.4.2",
    author="RASOANAIVO Andry, ANDRIAMALALA Rahamefy Solofohanitra, ANDRIAMIZAKASON Toky Axel",
    author_email="tokyandriaxel@gmail.com",
    description="Python application with nevergrad optimization model for calculating and simulating the least cost of an energy Mix under constraints.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Foloso/MixSimulator",
    packages=setuptools.find_packages(include=['mixsimulator', 'mixsimulator.*']),
    include_package_data=True,
    package_data={'mixsimulator': ['Experiments/Scenario_type.py','data/RIToamasina/dataset_RI_Toamasina.csv','data/RIToamasina/dataset_RI_Toamasina_v2.csv','data/RIToamasina/dataset_RI_Toamasina_variation_template.csv','data/RIToamasina/DIR-TOAMASINA_concat.csv','LICENSE','params_files/exchange_code.json','params_files/settings.json']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

