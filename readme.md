# Google translator wrapper

This is a wrapper around google translator.

I used an open-source [node package]([google-translate-extended-api](https://github.com/FreddieDeWitt/google-translate-extended-api)) that already does what we needed. Then I added a node  aroun it, so that we can use the http protocol to use that package.

Now we have the python app that leverage the node app to fetch data from google translator.

You can run the full app including the mongo db whit:
```
docker compose up --build
```

then, you can run the unittests with:
```
docker compose exec app pytest
```

and then, you can use the openapi UI http://localhost:8000/docs

## TODO

- [ ] handle the uniqueness of word/source_lang/dest_lang (unique_together)
- [ ] get rid of node microservice by porting the node package above to python.
- [ ] improve the async mode if possible
- [ ] add more scenarios the the unittests
- [ ] mock properly mongodb and run unittests outside docker env
- [ ] add more comments and documentation
- [ ] use env variables for secrets
- [ ] poetry would bring some capabilities
