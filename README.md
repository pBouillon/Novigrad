# Novigrad

## About
This project was developped by [pBouillon](https://github.com/pBouillon) and [FlorianVaissiere](https://github.com/FlorianVaissiere).

### Presentation
Novigrad is a small tool built to check your dependencies. Once set up, it will send you an report on your mailbox every 24 hours (can be changed)

### PDF organisation
* _Up to date_: remind you what doesn't need your attention
* _New commit available_: let you know that a commit is available
* _New release available_: warn you that a new release is available

## Cli usage
You may need is:
* `-b`: run Novigrad as a background task
* `-d [repo] [release] [commit] [owner]`: add a dependency to the database
* `-m [mail]`: add a mail adress to the mailing list
* `-t [time]`: change the pending time between two verifications/emails
* `-v`: generate the report inside a file on etc/report.txt instead of an email

## Setup
In order to set up everything you will first need to edit `config.json` located in `Novigrad/etc/`
Here is the basic content of this file:
```json
{
    "attachment_path" : "./",
    "mail_title"  : "Automatic dependency report",
    "receiver"    : "foo@bar.com",
    "report_name" : "Dependency_report.pdf",
    "sender"      : "foo@bar.com",
    "smtp"        : "127.0.0.1"
}
```
Variables are speaking for themselves, however, this is the detail of each one of them:
* `attachment_path`: change the path to attachment
* `mail_title`: change the header of the mail
* `receiver`: mail adress of the receiver
* `report_name`: name of the attachment file
* `sender`: mail adress of the sender
* `smtp`: smtp server

## Improvements
- [x] Add a new dependecy
- [x] Run as a daemon
- [x] Add logs to daemon
- [x] Import dependencies from csv file
- [x] Add a temporisation to handle more than 20 dependencies in one run
- [ ] Remove a dependency
- [ ] Better error handling
- [x] Make the email report optionnal
- [ ] Dependency name bold on report
- [ ] Dependencies sort by alphabetical order


Feel free to give your feedback or ideas to improve this little tool. :+1:
