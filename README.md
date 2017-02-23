# newsreel
A simple prototype for educational purposes.

Currently the app assumes there's an instance of <strong>MongoDB</strong> running on the default port, it expects there to be a database called 'news' with an 'articles' collection in it.
<br><br>Quick start: spin up an instance of <b>mongod</b> and run the following command in a terminal:

<code>mongoimport -d news -c articles < "\<path to articles.json\>" --jsonArray</code>

It also assumes there's an instance of <strong>Elasticsearch</strong> on the default port, that has an index called 'articles' with a type 'external'.

TODOs:
- have plugs in place for both connections (Mongo and Elasticsearch) in case the actual connection(s) is/are missing, so the page still loads with dummmy data and navigating the page doesn't produce errors;
- eventually replace both with in-memory temp storage to have the site act as a working demo rather than a bunch of code;
- rewrite the whole README as a tutorial on Tornado-Motor-Elasticsearch integration into a Python web application;
- replace articles from the RSS feed with sources of articles;
- rewrite the whole front-end to adhere to Material design;
