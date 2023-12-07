
# Setup the Discord Bot

- navigate to https://discord.com/developers/applications
- create a new bot
- save the token
- Go in the "OAuth2" section --> URL Generator
- Check the "bot" checkbox
![plot](./discordbot.png)
- assign the permission "Read MEssage History"
- copy the generated URL:
	- https://discord.com/api/oauth2/authorize?client_id=XXXXX&permissions=65536&scope=bot
- install the Bot on your Discord Server

# Run locally

## Setup Env Variables

```
DISCORD_SERVER_ID=xxxxx
DISCORD_CHANNEL_ID=xxxxx
OPENAI_API_KEY=xxxxx
BOT_TOKEN=xxxxx
```

## Simulate the github workflow steps locally:
```
$ pip install -r backend/discord_pipeline/requirements.txt
$ python backend/discord_pipeline/get_messages.py

$ pip install -r backend/haystack_pipeline/requirements.txt
$ python backend/haystack_pipeline/step_1_generate_faqs.py
$ python backend/haystack_pipeline/step_2_indexing.py
```

## Install and Run the Solara Web App
```
pip install -e .

solara run solarathon.pages
```

# Deploy via Github Actions

## Setup Env Variables in Github Secrets

```
DISCORD_SERVER_ID=xxxxx
DISCORD_CHANNEL_ID=xxxxx
OPENAI_API_KEY=xxxxx
BOT_TOKEN=xxxxx
```

[Get your Ploomber API key](https://docs.cloud.ploomber.io/en/latest/quickstart/apikey.html) and set it as `PLOOMBER_CLOUD_KEY` in GitHub (under Settings->Secrets and Variables->Actions, and click "New repository secret")

## Do only once

 * [Sign up for Ploomber](https://www.platform.ploomber.io/register/)
 * [Get the API key](https://docs.cloud.ploomber.io/en/latest/quickstart/apikey.html) from [The Ploomber dashboard](https://platform.ploomber.io/)


```
$ ploomber-cloud key YOURKEY
$ (cd ploomber && rm ploomber-cloud.json && ploomber-cloud init)
(add to git and commit)
$ git add ploomber/ploomber-cloud.json
$ git commit -m "ci: set ploomber id"
$ git push origin master:ploomber_dev
```

## Run to deploy a new version
```
$ git push origin master:ploomber_dev
# add --force if needed
```

# Other resources

 * [Wanderlust app](https://github.com/widgetti/wanderlust)
 * [Solara website](https://github.com/widgetti/solara/tree/master/solara/website)
 * [Solara examples](https://solara.dev/examples)

# Deploy manually

(Not recommended)
See https://docs.cloud.ploomber.io/en/latest/user-guide/cli.html for more details

```
$ pip install ploomber-cloud
$ mkdir -p ploomber/wheels
$ ploomber-cloud key YOURKEY
$ (cd ploomber && ploomber-cloud init)
(type y)
# build the wheel
$ (hatch build && cp dist/*.whl ploomber/wheels)
$ (cd ploomber && ploomber-cloud deploy)
```
