# Analysis of Alternatives

## Programming Language

### Terms of Reference

We are analysing and choosing the programming language we will use to implement this project. This will be the language we use to produce the entirety of the project, from start to finish. As a team we have identified three main options based on individual preferences and suggestions.

They are: _Python_, via a CLI program; _Java_, via GUI based program; and _JavaScript_, via a web or desktop app using Electron.

We also have a few criteria defined by both the project requirements and by the team members. These are as follows:

1. **1.** The language needs to be able to use the Google Docs API
2. **2.** The language needs to be able to provide some form of visual output or interaction
3. **3.** Using the program needs to be straightforward, including how to run it.
4. **4.** The team needs to be comfortable in developing in the language.

Notably, the most important criteria are number one, as this is a crucial part of the project spec and number four. As such we shall be prioritising languages that score well on these criteria.

### Comparison of Languages

| **Language** | Python | JavaScript (Electron) | Java |
| --- | --- | --- | --- |
| **Criterion 1** | ★★☆Although python does not natively support interactions with web API it provides a number of simple libraries which provide such features. For instance, [_Requests_](http://docs.python-requests.org/en/master/)  | ★★★As Javascript is fundamentally a web based language it is natively capable of producing web requests and the data returned is already in a format appropriate for the language it is easily able to interface with the API. | ★☆☆Similar to Python, Java does not provide native support for interacting with and making HTTP requests but there are libraries which add this.However as Java is a statically typed language handling and using the data returned by the web requests is complicated and not very easy to use |
| **Criterion 2** | ★★☆Again, python does not provide this natively but does have support through libraries. For instance it has GUI support through the standard library, [_Tkinter_](https://docs.python.org/3/library/tk.html#tkinter). Additionally it has support for producing visual output via HTML through [_Yattag_](http://www.yattag.org/) | ★★★Again, as Electron uses HTML and CSS for it&#39;s styling of the apps it provides a very easy to use method for producing a GUI. It is limited in its ability to produce output outside of the main gui however, meaning output could not be saved. | ★★☆Java is capable of producing a GUI via the Swing framework. It is also easily able to produce a lasting output as it has methods to support direct file interactions |
| **Criterion 3** | ★★★A python program can be very easily run through either a command line, via the python command or through a file explorer through file associations with the python interpreter.This will only work on desktop environments, but can be run on any major desktop.. | ★★☆Running an Electron app is basic as it functions similar to a regular program. However the same file is not cross-platform and would need a new executable for each OS supported. | ★★★The same as python, Java provides a file that can be run on any platform either through command line commands or through file associations to the JVM. This allows for easy cross platform sharing and easy running by the user. |
| **Criterion 4** | ★★★This language is one that all of our team has had exposure to, although not all members are fluent in it. All members however do feel confident in their abilities to create software using this language | ★☆☆Half of the team has familiarity with Javascript and feels confident in using it however the other half have no experience with it and hence do not feel capable of programming in it. | ★☆☆Only one member of the team has any experience with the language, and the other members of the team do not feel confident to be able to learn the new language and still produce an effective project. |
| **Summary** | ★★☆ | ★★☆ | ★☆☆ |

### Summary of Choice

We can see that of the three choices, Python performs the most consistently across the criteria. It also has the highest score in Criterion 4 and the middle in Criterion 1. These are the most important criteria as well. Java scored poorly in two of the criteria, notably also the two most important ones. Javascript has good performance in two of the categories and then average in the other two.

Overall, we will choose Python as it edges out Javascript by having better team familiarity as well as not lagging enough in Criterion 1 to be substantial.

## Operating System and Platform

The client has required that the product support desktop environments but has no desire to also extend this to the web or mobile. As of the three options, none support mobile and the final choice, python, automatically supports all major desktop OS&#39; this means that the decision of which Operating System and Platform does not need to be made. The final choice will be be Desktop Platforms and All OS&#39; as decided by Python inherently.