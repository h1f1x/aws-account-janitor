def log(msg, dry_run=False):
    prefix = ''
    if dry_run:
        prefix = '[DRY RUN] '
    print('{}{}'.format(prefix, msg))
