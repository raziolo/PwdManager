# AwESome Password Manager ~~2.0~~ 2.1

### !!! Now with a GUI and (2.1) GDrive support !!!

## Screenshots
<details>
  <summary>GUI and CLI</summary>
  
  
**GUI**

![image](https://user-images.githubusercontent.com/58889881/105012144-1ca54f00-5a3e-11eb-81bc-3623b510d5bb.png)

**C-LINE**


![image](https://user-images.githubusercontent.com/58889881/105012124-12835080-5a3e-11eb-9117-7734e2aabadf.png) 

  
</details>

## What it is now
The Command-Line part has not changed too much. 

I've just made some adjustments to the functions and also several optimization, also I have discovered PEP8 Compliance ~~so the code will be soon PEP8 compliant.~~

(2.1) **The code is now (a lot more) PEP8 compliant..**

The GUI is very easy-to-use and it has all the features of the CLI.  

~~OAuth Authentication turned to be more difficult than I tought due to problems with Google trusting my application, but maybe I will find a workaround. ;)~~

(2.1) **I have managed to find a solution for OAuth2 and I discovered this module PyDrive that is simple and easy to use, however it requires some you to create an application for you GDrive account, details in the the program.**

(2.1) **I have added a pretty basic note interface both for the CLI and the GUI.**

(2.1) **I divided the code into 5 files so it is more readable and also now it should be a lot more PEP8-friendly if you don't count the 124 chars limit rule LOL**

Thank you for reading this far, below you can find all the infos about the program, this space is (for the moment) intended as a journal or changelog or maybe just a what-am-I-learning-and-doing-about-code-diary.

See you at 3.0!

## Requirements

* Cryptography module, a very popular library for Cryptography.
* PySimpleGui module, a very popular library for creating powerful GUI interfaces.
* PyDrive module, GDrive OAuth2 library used for authentication and managing files.

You can install them via:
```
pip install cryptography
pip install pysimplegui
pip install pydrive
```

## Features

### New Features
* **PySimpleGui** based **GUI**
* (2.1) **GDrive Database Upload**
* (2.1) **Secure Notes**

### Old Features
* **Two-Level Encryption** : First Custom Made, Second AES-Based
* **Full Modularity** : Swap all the components (Access Keys, Dictionaries and Databases)
                         with just a command.                 
* **Easy to use** : (and still fashionable) :red_circle::yellow_circle::large_blue_circle: colorful :red_circle::yellow_circle::large_blue_circle: command-line interface.
* **No installation needed**, just run it with Python 3.8> on your Terminal/Prompt.
* **Multi Language** : Currently Italian and English are supported but several languages can be easily added.
* **Fully Open-Source**

## Currently Working on
- [x] OAuth Authentication For GDrive Upload Functionality (more services are gonna be covered too)
- [ ] Having new new ideas
- [x] Bug Catching and fixing
- [x] PEP8 Compliance
- [x] Secure notes
- [x] External dictionaries implementation
- [x] Swappable Graphic Interface using ~~tkinter~~ PySimpleGui



####
If you encounter any **bug** or whatever that could be in the wrong place I would be
very thankful if you spend a minute letting me know. I am always trying to learn
more and more of this cool language.


-----------------------------------------------------------------------------------

# AwESome Password Manager 1.0

## What it is
This is one of my first projects in Python.
Is a **password manager** that uses **Cryptography** library and a command-line interface
to help you manage your **passwords**.

## Requirements

* Cryptography module, a very popular library for Cryptography.

You can install it via:
```
pip install cryptography
```


## Features
* **Two-Level Encryption** : First Custom Made, Second AES-Based
* **Full Modularity** : Swap all the components (Access Keys, Dictionaries and Databases)
                         with just a command.                 
* **Easy to use** : (and still fashionable) :red_circle::yellow_circle::large_blue_circle: colorful :red_circle::yellow_circle::large_blue_circle: command-line interface.
* **No installation needed**, just run it with Python 3.8> on your Terminal/Prompt.
* **Multi Language** : Currently Italian and English are supported but several languages can be easily added.
* **Fully Open-Source**

## Currently Working on
- [ ] OAuth Authentication For GDrive Upload Functionality (more services are gonna be covered too)
- [x] External dictionaries implementation
- [ ] Having new ideas
- [x] Swappable Graphic Interface using ~~tkinter~~ PySimpleGui


####
If you encounter any **bug** or whatever that could be in the wrong place I would be
very thankful if you spend a minute letting me know. I am always trying to learn
more and more of this cool language.

