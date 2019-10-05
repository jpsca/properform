
# Frequently Asked Questions


## Does Proper Form works with ____?

Most likely **yes**.

### Request/Form Input

Here are some of the popular libraries to are known to work with Proper Form, but if it’s not listed, it doesn’t mean it won’t work.

- Django.
- Werkzeug, like Flask and many other.
- Webob, like Pyramid, Morepath, Turbogears, Google App Engine, etc.
- Any other cgi.FieldStorage-type multidict, like Falcon, Bottle, etc.

### Database ORMs

Pretty much any ORM should work, as long as data objects allow attribute access to their members. There is built-in support por [SQLAlchemy](https://www.sqlalchemy.org/) and [PonyORM](https://ponyorm.org/) but writing your own adapter is just a few lines of code. For instance, this is the complete code for the adapter to PonyORM:

```python
class PonyForm(Form):
    def create_object(self, data):
        return self._model(**data)

    def delete_object(self):
        return self.object.delete()
```

That's it.


## What versions of Python are supported?

Python 3.6 and beyond.


## Is Proper Form an async library?

No.

However, you can use `loop.run_in_executor()` to run a blocking synchronous methods, like `validate` or `save`, from asyncio, without blocking the main event loop.

I hope a future Python version (4?) removes this forced separation, so you can call the same code from sync and async functions (like JavaSscript does, for example).


## How can I contribute to Proper Form?

For bugs and feature requests, you can open an issue on the [GitHub page](https://github.com/jpscaletti/proper-form).


## Does Proper Form handle file uploads or image thumbanils?

It does not. Those are concerns for your framework or for other specialized libraries. Proper Form has a `File` field which will let you render a file input, but it doesn't do more than that.

## I have a question not covered in this documentation

Please open an issue on the [GitHub page](https://github.com/jpscaletti/proper-form) with the tag "question".
