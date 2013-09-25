# encoding: utf-8

"""Dropbox incremental archiver.

Usage:
  dbarc init [options] <key> <secret>
  dbarc download [options] <dropbox_dir> <dest_dir>
  dbarc (-h | --help)

Options:
  -h --help         Show this help.
  --token=PATH      File location to keep API token [default: ~/.dbarc].
  --struct=PATTERN  Archive dir structure [default: {year}-{month}/{dirname}].
  --dry-run         Do a dry run.
  --debug           Write debug info to the destination directory.
"""

import codecs
from datetime import datetime
from docopt import docopt
import dropbox
import os
from pprint import pformat
import sys
from email.utils import parsedate_tz
from dbarc import logger
from dbarc.version import get_version


def init(key, secret, token_file):
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(key, secret)
    authorize_url = flow.start()
    print('1. Go to: ' + authorize_url)
    print('2. Click "Allow" (you might have to log in first)')
    print('3. Copy the authorization code.')
    print("Enter the authorization code here:")
    code = sys.stdin.readline().strip()
    access_token, user_id = flow.finish(code)
    client = dropbox.client.DropboxClient(access_token)
    info = client.account_info()
    print("Linked account: %s <%s>" % (info['display_name'], info['email']))
    with open(token_file, 'w') as f:
        f.write(access_token)


def download(dropbox_dir, dest_dir, dir_struct, token_file, dry_run):
    with open(token_file, 'r') as f:
        access_token = f.read().strip()

    client = dropbox.client.DropboxClient(access_token)

    try:
        data = client.metadata(dropbox_dir)
        logger.debug("root:\n%s" % pformat(data))
    except Exception as e:
        logger.error('error connecting to dropbox')
        exit()

    if dry_run:
        logger.info('doing a dry run')

    for item in data['contents']:
        if item['is_dir']:
            ts = datetime(*parsedate_tz(item['modified'])[:6])
            dirname = os.path.split(item['path'])[1]
            path = dir_struct.format(year=ts.strftime("%Y"),
                                     month=ts.strftime("%m"),
                                     dirname=dirname,
                                     dry_run=dry_run)
            download_dir(client,
                         dropbox_dir=item['path'],
                         dest_dir=os.path.join(dest_dir, path),
                         dry_run=dry_run)


def download_dir(client, dropbox_dir, dest_dir, dry_run):
    data = client.metadata(dropbox_dir)
    logger.debug("directory:\n%s" % pformat(data))

    if not os.path.isdir(dest_dir) and not dry_run:
        try:
            os.makedirs(dest_dir)
        except FileExistsError:
            pass

    for item in data['contents']:
        path = os.path.join(dest_dir, os.path.split(item['path'])[1])

        if item['is_dir']:
            download_dir(client, item['path'], path, dry_run)
        else:
            size = item['bytes']

            if not os.path.exists(path) or os.path.getsize(path) != size:
                # file not exists, was not properly downloaded, or was updated
                logger.info("dropbox://%s -> %s" % (item['path'].lstrip('/'), path))
                if not dry_run:
                    with client.get_file(item['path']) as src:
                        with open(path, 'wb') as dest:
                            dest.write(src.read())


def main():
    args = docopt(__doc__, version=get_version())
    token_file = os.path.expanduser(args['--token'])
    dest_dir = args['<dest_dir>'] or ''

    log_file = "%s.log" % os.path.splitext(os.path.basename(__file__))[0]
    logger.init(log_file=os.path.join(dest_dir, log_file),
                syslog=True, verbose=args['--debug'])
    logger.debug("-- STARTING -- %s %s" % (__name__, get_version()))
    logger.debug("args:\n%s" % pformat(args))

    if args['init']:
        init(args['<key>'], args['<secret>'], token_file)
    elif args['download']:
        download(dropbox_dir=args['<dropbox_dir>'],
                 dest_dir=dest_dir,
                 dir_struct=args['--struct'],
                 token_file=token_file,
                 dry_run=args['--dry-run'])
