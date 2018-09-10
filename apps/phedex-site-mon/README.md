# PhEDEx Site Monitor
 - queries [PhEDEx](https://cmsweb.cern.ch/phedex/)

# Installation
```
git clone https://github.com/uobdic/wlcg_site_helpers.git
cd wlcg_site_helpers/apps/phedex-site-mon
docker build -t hepdocker/phedex-site-mon .
docker run -d --rm -p 5000:5000 -e PORT=5000 hepdocker/phedex-site-mon
```
