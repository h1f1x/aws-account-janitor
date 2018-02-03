# aws-account-janitor
Cleanup and Maintains resources in your AWS Account

# Install

```
git clone git@github.com:h1f1x/aws-account-janitor.git
cd aws-account-janitor
pip3 install pybuilder
pyb install_dependencies
pyb install
```

# Usage

```
$ aws-account-janitor
Usage: aws-account-janitor [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  cleanup_cf_stacks
  cleanup_rds_snapshots
  set_missing_log_retentions
  wait_for_stacks
```
