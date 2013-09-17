# Dropbox Archiver

This is a script to create incremental local copies for Dropbox contents. It does not require Dropbox client to be preinstalled and runs almost anywhere including Raspberry Pi.

## Installation

Ensure Python 3.3, git and pip are installed, and run the following command to install the package  from GitHub:

```bash
pip install -e git+git://github.com/dreikanter/dbarc#egg=dbarc
```

Create a new app on [Dropbox App Console](https://www.dropbox.com/developers/apps) and get your app key and app secret.

Run the following command to acquire API access token (use the actual values for _$dropbox_app_key_ and _$dropbox_app_secret_):

```bash
dbarc init $dropbox_app_key $dropbox_app_secret
```

This will ask you to open a specific URL in your browser, authorize the tool to access your Dropbox contents through the web UI, and copy authorization code back to console. Dropbox access token will be saved to your home directory: `~/.dbarc` (`%userprofile%/dbarc` on Windows).

Here is an example:

```bash
$ dbarc init $dropbox_app_key $dropbox_app_secret
1. Go to: https://www.dropbox.com/1/oauth2/authorize?response_type=code&client_id=1
2. Click "Allow" (you might have to log in first)
3. Copy the authorization code.
Enter the authorization code here:
KHQP1FRIYEPIUQDH4IUEHFOHDIUAW7IUAHEIUWEHDIW
Linked account: John Doe <john.doe@example.com>
```

## Usage

Te following command will download files from `{source-directory}` path inside your Dropbox to `{local-archive-path}/YYYY.MM/` directories where `YYYY.MM` is file last modification date.

```bash
dbarc download {source-directory} {local-archive-path}
```

Example:

```bash
$ dbarc download /snippets ~/snippets-archive
dropbox://snippets/ClassExt.cs -> /home/pi/snippets-archive/2013-02/ClassExt.cs
dropbox://snippets/DateExt.cs -> /home/pi/snippets-archive/2013-02/DateExt.cs
dropbox://snippets/EnumExt.cs -> /home/pi/snippets-archive/2013-02/EnumExt.cs
...
```

Cron tab example to run the script every midnight:

```bash
0 0 * * * dbarc download {source-directory} {local-archive-path} > dbarc.log
```


Copyright &copy; 2013 by [Alex Musayev](http://alex.musayev.com).  
License: [MIT](http://opensource.org/licenses/MIT).  
Project home: [https://github.com/dreikanter/dbarc](https://github.com/dreikanter/dbarc).
