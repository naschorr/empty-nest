# empty-nest
Automatically set your Nest thermostat's away status via requests.

### Installation
Note that my installation assumes that you're putting it into `/usr/local/bin/`, obviously it can be put elsewhere, but you'll have to mess around with the configuration to get everything working fine.
- Clone/Unzip the files into `/usr/local/bin/empty-nest`.
- Update the `token.json` and `config.json` files.
  + Get a Nest API token. You'll first have to create an OAuth client [here](https://codelabs.developers.google.com/codelabs/wwn-api-quickstart/#2), and then connect it to your Nest [here](https://codelabs.developers.google.com/codelabs/wwn-api-quickstart/#4).
  + Update the `users` JSON array in `config.json` to account for all of the users in your house that you want to be able to control the Nest's away setting. Just give each these users a unique username.
  + Update the `structure_id` value in `config.json` with your structure's unique id. You can get this with a simple GET request to the Nest API. See this [link](https://developers.nest.com/documentation/cloud/how-to-read-data)'s "Read structures and devices" section for an example query.
- Run with `python code/empty-nest.py` (assuming you're in the root directory.

### Empty-Nest as a Service (ENaaS?)
If your system uses systemd, then you can also use my service file to have this program run automatically.
- If you didn't install empty-nest into `/usr/local/bin/empty-nest`, then update the paths in `empty-nest.service`.
- Move `empty-nest.service` to `/etc/systemd/system/`
- Activate and run the service with the root command: `systemctl daemon-reload && systemctl enable empty-nest && systemctl start empty-nest --no-block`
- Now you can control empty-nest like any other service using `sudo service empty-nest start|stop|restart` and etc.

If your system doesn't use systemd, then you can just as easily set up a cronjob to run `empty-nest.py` on boot.
