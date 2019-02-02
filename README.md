# aws-account-janitor
Cleanup and Maintains resources in your AWS Account

# Install

```
git clone git@github.com:h1f1x/aws-account-janitor.git
cd aws-account-janitor
```

At the moment I don't provide a reliable install method. But here are two possibilities.

If you want to use pybuilder:
```
pip3 install pybuilder
pyb install_dependencies
pyb install
```

Otherwise you can use pipenv:
```
pipenv install
export PYTHONPATH=src/main/python/
```

Calling the script now:
```
pipenv run ./src/main/scripts/aws-account-janitor
```

# Usage

You need to setup your AWS credentials first!
Don't forget to export the AWS Region you want to work in: ``` export AWS_DEFAULT_REGION=eu-central-1 ```
```
$ aws-account-janitor --help
Usage: aws-account-janitor [OPTIONS] COMMAND [ARGS]...

Options:
  -n, --dry_run  dry run
  --help         Show this message and exit.

Commands:
  cf
  dynamodb
  ecr
  logs
  rds
  tags
```

Now you can get help on the commands with:

```
$ aws-account-janitor cf --help
Usage: aws-account-janitor cf [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  cleanup_cf_stacks
  wait_for_stacks
```
