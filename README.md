# RAG Integration (Watson Discovery + watsonx.ai)

This script is a simple illustrative example of integrating Watson Discovery and watsonx.ai together.

You will need Python installed locally to run this script: https://www.python.org/downloads

> Most recently tested with version `3.12.2`

## How to use this script

First, you must create a `.env` file at the project root containing all sensitive data about your instances of Watson Discovery and watsonx.ai.

Here is a table of them:

| Name                 | Description                                                                                         |
| -------------------- | --------------------------------------------------------------------------------------------------- |
| IBM_DISC_API_KEY     | API key with access to Discovery instance. Can be created [here](https://cloud.ibm.com/iam/apikeys) |
| IBM_DISC_PROJ_ID     | Project ID of Discovery instance. Available within cloud console.                                   |
| IBM_DISC_SERVICE_URL | Service URL of Discovery instance. Available within cloud console.                                  |
| IBM_DISC_COLL_ID     | Collection ID of the collection of documents you wish to query as context within Discovery.         |
| IBM_WX_API_KEY       | API key with access to watsonx.ai project. Can be created [here](https://cloud.ibm.com/iam/apikeys) |
| IBM_WX_PROJ_ID       | Project ID of watsonx.ai project. Availabe under "Settings" within project.                         |
| IBM_WX_SERVICE_URL   | Service URL of watsonx.ai project. Tied to locale of projects deployment.                           |

There is a blank version in `env_example`. Feel free to rename this to `.env` and fill it with the required values. From the command line you could do:

```bash
# this command will create a copy of the file titled .env
cp env_example .env
```

Then you can fill out the created `.env` file with your instance values.

> Ensure you can see hidden files within your explorer or editor to see the `.env` file.

Next, install the dependencies required for the script:

```bash
# installs dependencies needed for the script to run
python -m pip install -r requirements.txt
```

Lastly, you can now run the script via:

```bash
# runs the actual script
python rag.py
```

To change the question being asked simply change the `QUERY` variable located near the top of the script and run once more.
