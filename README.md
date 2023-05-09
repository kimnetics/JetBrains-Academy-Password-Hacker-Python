# JetBrains Academy Password Hacker (Python) Project

An example of a passing solution to the final phase of the JetBrains Academy Python Password Hacker (Python) project.

## Description

This project is a command line application which attempts to hack into a server.

The server is handled by the automated testing process.

The application communicates with the server via sockets.

The project went through five stages with each stage using a different hacking technique. In the final stage, we begin with a list of possible logins in a file. All permutations of uppercase and lowercase letters in the possible logins are tried until we find a valid login. With a valid login, the application brute forces its way through passwords. Whenever valid password prefix characters are found, the server throws an exception which causes a response time variation. The application leverages that behavior to find longer and longer password prefixes until the entire password is determined.

The application returns a JSON structure with a valid login and password.

## Notes

The relative directory structure was kept the same as the one used in my JetBrains Academy solution.

The application is run with a command like the following:

```
python hack.py host port
```

`host` is the ip address of the server to hack.

`port` is the port on the server to hack.

The application returns a JSON structure like the following:

```
{
    "login" : "su",
    "password" : "Sp?f4UTh"
}
```
