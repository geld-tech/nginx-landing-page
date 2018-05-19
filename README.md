# geldtech-landing-page[![Build Status](https://travis-ci.org/zlig/geldtech-landing-page.svg?branch=master)](https://travis-ci.org/zlig/geldtech-landing-page)  [ ![Download](https://api.bintray.com/packages/geld.tech/debian/geldtech-landing-page/images/download.svg) ](https://bintray.com/geld.tech/debian/geldtech-landing-pages#files)


## Description

Landing page for the projects hosted on <a href="http://www.gedl.tech">geld.tech</a>


## Usage

* Install the repository information and associated GPG key (to ensure authenticity):
```
$ echo "deb https://dl.bintray.com/geldtech/debian /" | sudo tee -a /etc/apt/sources.list.d/geld-tech.list
$ sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com TODO
```

* Update repository list of available packages and clean already installed versions
```
$ sudo apt update
$ sudo apt clean
```

* Reload services and start ours
```
$ sudo systemctl daemon-reload
$ sudo systemctl start geldtech-landing-page
$ sudo systemctl status geldtech-landing-page
```

## Settings

The following environment variables need to be configured in the Travis CI settings page to ensure a good build and deployment:

```
- BINTRAY_USER		Username used to upload to Bintray
- BINTRAY_API_KEY	API Key used to upload in Bintray
- __GA_UA_ID__		Google Analytics User ID
```
