
# Welcome

Lorem ipsum.



“The main problem I used to have with [Django Forms] was the markup. I wanted Bootstrap fields. I wanted complex layouts like multiple columns.”
-- Random Redditor



# Things developers ~~believe~~ forget about forms

- A field can be presentend in multiple ways. Even the same form could be needed "n" different contexts and have different appeareance.

- A field type isn't tied to form tags. You might think an URL field it's always going to be displayed as a text `<input>`, but it doesn't have to. You could also have URLs as values of checkboxes, radio buttons, or selects. And I need them to be validated just the same (is still editable by the user after all).

- The error messages need to be *custom* error messages most of the time. We are not robots, the tone of the messages must be able to change or to be translated.

- A simple `form.render()` is an idea that only work for the web 15 years ago. Nowadays the markup for a form need to be flexible, responsive, and with added attributes *everywhere*.
