# eBorrow - Client

This project is an Inventory Catalog designed as a desktop application using Python 3. The Project is split into two distinct systems. A Client application and a Server Application. This README is designed to assist in understanding the high level structure of the project.

## Getting Started

Setting up the repository is still in progress. The eventual goal is to allow for an executable install using pyinstaller. In the meantime, we will be running the files as python scripts. We are currently developing on Python 3.5+, and pip3 18.1+. Once you have those installed, run the folling command to install all requirements of this project.

```
pip3 install -r requirements.txt
```

**Windows Users** Be aware that this may require you to add the argument "--user". You may want to install the requirements as an administrator, but adding the argument will work as well.

### Netcode

Coming Soon!

### Coding Style

This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards and uses the [autopep8](https://github.com/hhatto/autopep8) library for style verification. To automatically modify your code to align with PEP 8 standards, run the following command:

This runs a verbose call to autopep8 for all Python files in the folder to fix all the styling errors.

```
autopep8 -v -i *.py
```
Run this command before every push to keep coding style consistancy.

## Contributing & Versioning

We use GitHub's versioning system. The *master* branch is to remain untouched until a full release is planned. The *dev* branch is meant for semi-active development. When there is a feature to be added, follow this checklist:

1. Checkout the *dev* branch
2. Make a new branch, naming it according to the issue/feature
3. Complete the task
4. Modify or write applicable unit tests
5. Run all unit tests
6. Start merge **into** the *dev* branch
7. Run all unit tests
8. Fix merge conflicts
9. Repeat steps 7 and 8 until it meets the requirements definition
10. Run styling script
11. Submit Final Pull request for review

We welcome assistance in the project, but not following the above protocol will result in a rejected pull request. If you want to find a bug, please check the issuses page for possible jumping off points.

## Authors (sorted alphabetically)

* **Joshua Higham** - Backend/Networking/Security/Database
* **Caleb Lundquist** - Frontend/Networking
* **Tim Weber** - Backend/Networking/Security
* **Jordan Yates** - Frontend/GUI/Security

## License

This project is licensed under the GNU General Purpose License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Stephen Clyde - Professor 
