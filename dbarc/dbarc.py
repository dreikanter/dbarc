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
"""

from datetime import datetime
from docopt import docopt
import dropbox
import os
import sys
from email.utils import parsedate_tz


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


def download(dropbox_dir, dest_dir, dir_struct, token_file):
    with open(token_file, 'r') as f:
        access_token = f.read().strip()

    client = dropbox.client.DropboxClient(access_token)
    data = client.metadata(dropbox_dir)

    for item in data['contents']:
        if item['is_dir']:
            ts = datetime(*parsedate_tz(item['modified'])[:6])
            dirname = os.path.split(item['path'])[1]
            path = dir_struct.format(year=ts.strftime("%Y"),
                                     month=ts.strftime("%m"),
                                     dirname=dirname)
            download_dir(client, item['path'], os.path.join(dest_dir, path))


def download_dir(client, dropbox_dir, dest_dir):
    data = client.metadata(dropbox_dir)

    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    for item in data['contents']:
        path = os.path.join(dest_dir, os.path.split(item['path'])[1])

        if item['is_dir']:
            download_dir(client, item['path'], path)
        else:
            size = item['bytes']

            if not os.path.exists(path) or os.path.getsize(path) != size:
                # file not exists, was not properly downloaded, or was updated
                print("dropbox://%s -> %s" % (item['path'].lstrip('/'), path))
                with client.get_file(item['path']) as src:
                    with open(path, 'wb') as dest:
                        dest.write(src.read())


def main():
    args = docopt(__doc__, version='0.0.1')
    token_file = os.path.expanduser(args['--token'])

    if args['init']:
        init(args['<key>'], args['<secret>'], token_file)
    elif args['download']:
        download(dropbox_dir=args['<dropbox_dir>'],
                 dest_dir=args['<dest_dir>'],
                 dir_struct=args['--struct'],
                 token_file=token_file)
