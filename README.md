# Dropbox Archiver

This is a script to create incremental local copies for Dropbox contents. It does not require Dropbox client to be installed, and runs almost anywhere including Raspberry Pi.

## Getting Started

Ensure Python 3.3, git and pip are up and running, and execute the following command to install the package from GitHub:

```bash
pip install -e git+git://github.com/dreikanter/dbarc#egg=dbarc
```

Create a new app with [Dropbox App Console](https://www.dropbox.com/developers/apps) and get your app key and app secret.

Run the following command to acquire API access token (use the actual values for `<dropbox_app_key>` and `<dropbox_app_secret>`):

```bash
dbarc init <dropbox_app_key> <dropbox_app_secret>
```

This will ask you to open a specific URL in the browser, authorize the tool to access your Dropbox contents, and copy authorization code back to console. Dropbox access token will be saved to the current user home directory: `~/.dbarc` (`%userprofile%/.dbarc` on Windows). This path could be overridden with `--token` command line parameter.

Here is an example:

```bash
$ dbarc init kjdfake8gkjssf e23aksfakelak9
1. Go to: https://www.dropbox.com/1/oauth2/authorize?response_type=code&client_id=1
2. Click "Allow" (you might have to log in first)
3. Copy the authorization code.
Enter the authorization code here:
KHFAKERIYEPIUQDH4FAKEFOHDIUAW7IUAHEEFAKEDIW
Linked account: John Doe <john.doe@example.com>
```

### Running the Script on Raspberry Pi

Default python3 version on Raspberry Pi at the moment is 3.2.3, and you will need to upgrade it to 3.3+. The easiest way to do this is [pyenv](https://github.com/yyuu/pyenv). Pyenv will download and build python versions from source code.

There could be errors due insufficient dependencies on Raspbian Wheezy. If you encounter something like "ImportError: No module named 'readline'" during python build, use the following command to install these libraries manually:

```
sudo apt-get install libreadline-gplv2-dev libssl-dev sqlite3 libsqlite3-dev \  
python-setuptools python-dev build-essential libxml2-dev libxslt1-dev libbz2-dev \  
libjpeg62-dev wv poppler-utils python-imaging
```

## Usage

Te following command will download files from `<source_directory>` path inside your Dropbox to `<local_archive_path>/YYYY.MM/` directories where `YYYY.MM` is file last modification date.

```bash
dbarc download <source_directory> <local_archive_path>
```

Example:

```bash
$ dbarc download /snippets ~/snippets-archive
dropbox://snippets/ClassExt.cs -> /home/pi/snippets-archive/2013-02/ClassExt.cs
dropbox://snippets/DateExt.cs -> /home/pi/snippets-archive/2013-02/DateExt.cs
dropbox://snippets/EnumExt.cs -> /home/pi/snippets-archive/2013-02/EnumExt.cs
...
```

Cron tab example to run the script every day at 23:59:00:

```bash
59 23 * * * dbarc download <source_directory> <local_archive_path>
```

## License

Copyright &copy; 2013 by [Alex Musayev](http://alex.musayev.com).  
License: [MIT](http://opensource.org/licenses/MIT).  
Project home: [https://github.com/dreikanter/dbarc](https://github.com/dreikanter/dbarc).
