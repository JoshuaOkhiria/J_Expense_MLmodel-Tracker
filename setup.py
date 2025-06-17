
from setuptools import find_packages, setup
from typing import List


def find_requirements()->List[str]:
    requirements_lst:List[str] = []
    try:

        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            #Iterate through lines and remove extra spaces
            for line in lines:
                requirement = line.strip()      
                #Ignore all empty lines and -e. 
                if requirement and requirement != '-e .':
                    requirements_lst.append(requirement)
    except FileNotFoundError:
        print('requirement.txt file not found')

    return requirements_lst

print(find_requirements())



setup(name="expense_data",
      version="0.0.1",
      author=" Joshua Okhiria",
      author_email='joshokhiria89@gmail.com',
      packages=find_packages(),
      install_requires = find_requirements()
    )