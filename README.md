This is used for tagging IP-Adresses from Palolto Global-Protect logins with predefined usernames.
How it workes:
* Create a syslogserver in Paloalto GUI: Device / Syslog

![Syslog](images/config_syslog_server.png)
* Forward failed login logs to that server Device / LogForward

![Logforward](images/LogSettings.png)
* create dynamic address group with the tag "BadGPIP"

![AddrGroups](images/config_dynamic_AddrGroup.png)
* create security policy to drop the connection from dynamic address

![Policy](images/SecPolicy.png)
* modify the file  "example.env.txt" with credentials for logging in to the firewall and set the tag. Then rename it to ".env"

* modify "BadUsernames.txt" with the usernames you want to block

* install the required Python libs

```pip install -r requirements.txt```

* run the python script

![ScriptRun](images/ScriptrunScreenshot.png)

* check logs and dynamic address-group

![trafficlogs](images/Traffic-Log.png)

![addressgroup](images/show_dynamic_addr.png)

![cli](images/CLI-Output.png)

![IP-Tag-Log](images/IP-Tag-Log.png)
  

