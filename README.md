# sendmail-flask
sendmail by flask api

>Currently only supports SSL PORT for mail_server ( Gmail SMTP port (SSL): 465)

## optional for env:
- ${MAIL_USER}     default is None
- ${MAIL_PASS}     default is None
- ${MAIL_SERVER}   default is smtp.gmail.com
- ${MAIL_PORT}     default is 465

## POST vaule:
>necessary
- receiver    , default = ""                     (receiver mail address)

- mail        , default = default_mail_user      (sender mail address)
- pass        , default = default_mail_pass      (sender mail pass)
- server      , default = default_mail_server    (sender mail server)
- port        , default = default_mail_port      (sender mail port)

>optional
- subject     , default = "default subject"      (mail subject)
- message     , default = "hello world [Default]"(mail body)
- attach_link , default = ""                     (only one attachment in a link) 
- Bcc         , default = ""                     (mail blind carbon copy address)
- cc          , default = ""                     (mail carbon copy address)

## example 
1. simple use 
```
http -f POST http{s}://{ip or hostname}:{port}/send receiver="xxx@outlook.com,xxx@gmail.com"
```
2. cc , bcc and send a attachment
```
http -f POST http{s}://{ip or hostname}:{port}/send receiver="xxx@gmail.com" \
                                                     cc="xxx@gmail.com" \ 
                                                     Bcc="xxx@gmail.com" \
                                                     attach_link="https://transfer.sh/T3y2FO/hello.txt"
```
3. use own smtp mail
```
http -f POST http{s}://{ip or hostname}:{port}/send receiver="xxx@outlook.com,xxx@gmail.com" \
                                                       mail="xxx@xxx.com" \
                                                       pass="xxx" \
                                                       server="smtp.gmail.com"
                                                       port="465"
```


## hint (how to get Gmail SMTP pass)
Time flies, the way I do without enabling less secured app is making a password for specific app
- Step one: enable Google [2FA](https://myaccount.google.com/signinoptions/two-step-verification/enroll-welcome)
- Step two: create an Google [app-specific password](https://myaccount.google.com/apppasswords)
After this, put the sixteen digits password to the settings and reload the app, enjoy!
