This is used for tagging IP-Adresses from Palolto Global-Protect logins with predefined usernames.
How it workes:
* Create a syslogserver in Paloalto GUI: Device / Syslog

![Syslog](assets/config_syslog_server.png)
* Forward failed login logs to that server Device / LogForward

![Logforward](assets/LogSettings.png)
* create dynamic address group with the tag "BadGPIP"

![AddrGroups](assets/config_dynamic_AddrGroup.png)
* create security policy to drop the connection from dynamic address

![Policy](assets/SecPolicy.png)
* modify the file  "example.env.txt" with credentials for logging in to the firewall and set the tag. Then rename it to ".env"

* modify "BadUsernames.txt" with the usernames you want to block

* run the python script

![ScriptRun](assets/ScriptrunScreenshot.png)

* check logs and dynamic address-group

![trafficlogs](assets/Traffic-Log.png)
![addressgroup](assets/show_dynamic_addr.png)
![cli](assets/CLI-Output.png)

  

