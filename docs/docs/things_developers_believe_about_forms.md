# Things developers sometimes forget about forms

- A field can be presentend in multiple ways. Even the same form could be needed n different contexts and have different appeareance.

- A field type isn't tied to form tags. You might think an URL field it's always going to be displayed as a text <input>, but it doesn't have to. You could also have URLs as values of checkboxes, radio buttons, or selects. And I need them to be validated just the same (is still editable by the user after all).

- The error messages need to be *custom* error messages. We are not robots, the tone of the messages must be able to change or to be translated.

- You are going to need to add attributes *everywhere*.