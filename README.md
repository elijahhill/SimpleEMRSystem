# Simple EMR System

This code can be used for Electronic Medical Record Research.

Coming soon - More screenshots and additional formatting

## Inital environment setup - all
If you already have a development environment set up that includes git, python 3.10, and an IDE of choice 

skip to [Setting up the project](#setting-up-the-project)

Otherwise -

- If installing on a Windows machine skip to [Initial environment setup - Windows](#initial-environment-setup---windows)

- If installing on a Mac, skip to [Initial environment setup - Mac](#initial-environment-setup---mac)

Linux is not supported for use, as the full dataset requires Box, and Box support for Linux was dropped in 2018.

However, it is possible to run the demo information on Linux.

## Initial environment setup - Windows

### Git
Fetch git from https://git-scm.com/download/win

Download and install 64-bit Git for Windows Setup.

The default settings for the installer will work for what we need

### Python
Install the latest version of python 3.10 (3.10.4 at the time of writing)

https://www.python.org/downloads/release/python-3104/

Use the windows installer (64-bit)

Within the installer, check the box for "Add python 3.10 to PATH"

Otherwise default options are correct

### IDE (VsCode)
Install VsCode from https://code.visualstudio.com/

You're free to install the IDE of your choice, but VsCode is both light, and works well as an IDE.

After VsCode is installed, skip to [Setting up the project](#setting-up-the-project).

## Initial environment setup - Mac
Note that I wasn't able to test this section, as I don't have a mac, nor a mac environment to test the installation instructions

### Homebrew
Installing development tools on a mac tends to require homebrew. Thus, we'll install it first.

Copy and paste the command below into a terminal 

command + c to copy

command + v to paste

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

Then press enter to run the command

### Git
Similar to how you previously used the terminal, run the below command as well:

`brew install git`

### Python
Install python with:

`brew install pyenv`

Then copy and paste the following commands into your shell depending on the shell you're using.
If they work, there won't be any sort of output. 

For either shell, the commands will work quickly.

**If you use bash: (if you don't know what you use, it's probably bash)**

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.profile
```

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
```

**If you use zsh:**

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zprofile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zprofile
echo 'eval "$(pyenv init -)"' >> ~/.zprofile
```

**After doing the other commands**

```
exec "$SHELL"
```

`pyenv install 3.10.4`

`pyenv global 3.10.4`

### MySQL Client
This is necessary later on in the install process

`brew install mysql-client`

** For bash **
`source ~/.bash_profile`

`echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.bash_profile`

** For zsh **
`echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.zprofile`

`source ~/.zprofile`

### IDE (VsCode)
One last installation: 

`brew install --cask visual-studio-code`

Continue onto [Setting up the project](#setting-up-the-project)

## Setting up the project
Now that the environment is set up, we can move onto setting up and running the app.
### Getting the webapp
Using VsCode, open up the folder you want to copy SEMR into (using file > open folder)

Open the terminal
- Click View
- Select "Terminal" from the menu

Once that folder is opened, from the terminal within VsCode, run -

`git clone https://github.com/elijahhill/SimpleEMRSystem`

### Setting up virtual environment
Similar to what you did in the previous section - 

Open the newly created folder in VsCode 

Re-open the terminal

From that terminal, run - 

`python -m venv SEMRenv`

After this completes, VsCode will ask you if you want to set this as the default workspace, select yes

If you were able to select it, skip to [Installing dependencies](#installing-dependencies)

If not, then hit 
>ctrl + shift + p

And then go to Python: select interpreter.

Then from the dropdown list, select Python 3.10.4 ('SEMRenv': venv)

### Activating the virtual environment
For Windows, when activating the environment, there may be a problem where you cannot run activate the environment. It will say something similar to "running scripts on this system id is disabled"

To solve this, run - 

`Set-ExecutionPolicy -Scope "CurrentUser" -ExecutionPolicy "Unrestricted"`

Then activate the environment by running - 

`./SEMRenv/Scripts/activate`

For MAC, it will be 

`source ./SEMRenv/Scripts/activate`

### Installing dependencies
`python -m pip install -r requirements.txt`

This may take a few minutes to complete as the dependencies will need to download

### Setting up run command
Once your depdencies have installed, run the following command - 

`python manage.py runserver`

### Opening the webapp
After a few seconds, you'll get output that says 

>Starting development server at http://127.0.0.1:8000/

Hold alt + left click while hovering over the link in the terminal. This will open the webapp. 

At this point, you will be able to access the demo cases that came with the webapp!

# Importing custom data

## Requirements
- A folder within SimpleEMRSystem/resources to store autogenerated cases (will need to be created)
- Box desktop

If you don't have Box Desktop, download and install it from https://www.box.com/resources/downloads

**note for Mac**
Mac requires you to go into software from Box Inc in the software settings. The allow button will be towards the bottom of 
the software settings popup window. 

To run the translator, run -

`python data_type_translation/translator.py`

The translator file will pop up a window asking you for paths to each of the specified files. Once you fill in those paths and submit, then it will run each of the files

# Additional Notes
The SEMRinterface in meant to run in full screen mode on a 1920 x 1080 resolution monitor. Responsive html is not
currently supported. 

## Secondary Use

### Included data
Two studies are included, created from the full set of autogenerated data. 

## Versioning

Version 3.0. For the versions available, see https://github.com/ajk77/SimpleEMRSystem

## Authors

* Andrew J King - Doctoral Candidate (at time of creation)
	* Website (https://www.andrewjking.com/)
	* Twitter (https://twitter.com/andrewsjourney)
* Shyam Visweswaran - Principal Investigator
	* Website (http://www.thevislab.com/)
	* Twitter (https://twitter.com/Shyam_Vis)
* Gregory F Cooper - Doctoral Advisor

## Citation
King AJ, Calzoni L, Tajgardoon M, Cooper G, Clermont G, Hochheiser H, Visweswaran S. A simple electronic medical record system designed for research. JAMIA Open. 2021 July 31;4(3):ooab040.
(<https://academic.oup.com/jamiaopen/article/4/3/ooab040/6332673>)

## Impact
This interface has been used in the following studies:
* King AJ, Cooper GF, Clermont G, Hochheiser H, Hauskrecht M, Sittig DF, Visweswaran S. Leveraging Eye Tracking to 
Prioritize Relevant Medical Record Data: Comparative Machine Learning Study. J Med Internet Res 2020;22(4):e15876. 
(<https://www.jmir.org/2020/4/e15876/>)
* King AJ, Cooper GF, Clermont G, Hochheiser H, Hauskrecht M, Sittig DF, Visweswaran S. Using Machine Learning to 
Selectively Highlight Patient Information. J Biomed Inform. 2019 Dec 1;100:103327. 
(<https://www.sciencedirect.com/science/article/pii/S1532046419302461>)
* King AJ, Cooper GF, Hochheiser H, Clermont G, Hauskrecht M, Visweswaran S. Using machine learning to predict 
the information seeking behavior of clinicians using an electronic medical record system. AMIA Annu Symp Proc. 
2018 Nov 3-7; San Francisco, California p 673-682. [Distinguished Paper Nomination] 
(<https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6371238/>)
* King AJ, Hochheiser H, Visweswaran S, Clermont G, Cooper GF. Eye-tracking for clinical decision support: 
A method to capture automatically what physicians are viewing in the EMR. AMIA Joint Summits. 2017 Mar 27-30; 
San Francisco, California p 512-521. [Best Student Paper] (<https://www.ncbi.nlm.nih.gov/pubmed/28815151>)
* King AJ, Cooper GF, Hochheiser H, Clermont G, Visweswaran S. Development and preliminary evaluation of a 
prototype of a learning electronic medical record system. AMIA Annu Symp Proc. 2015 Nov 14-18; San Francisco, 
California p.1967-1975. [Best Student Paper] (<https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4765593/>)

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Acknowledgments

* Harry Hochheiser
	* Twitter (https://twitter.com/hshoch)
* Gilles Clermont
* Milos Hauskrecht 
