## Humble Objects in Odoo

This is a supporting module for the [article I wrote](https://holdenrehg.com/blog/2021-08-16_odoo-patterns-humble-object).

### Running the tests

You don't need any Odoo instance or database:

```console
$ git clone https://github.com/holdenrehg-samples/sample_odoo_humble_object.git
$ cd sample_odoo_humble_object/humble_object
$ python3 -m unittest discover -s core -t . -v
```

### Why?

This came from frustrations with everything being tied together. I wanted to write a string parser function in my Odoo module, so why did I need a database up and running to test it?

The point of this is to show that there's an option for Odoo developers to write decoupled, easily testable code, with a simple to use test suite, from within their modules.

### What's the Humble Object pattern?

Look at [Martin Fowler's article](https://martinfowler.com/bliki/HumbleObject.html) or the [xUnit reference](http://xunitpatterns.com/Humble%20Object.html).

### Test structure

The tests here would be split into 2 suites.

- **Odoo tests.** Live in `{module}/tests`. `odoo.tests.TransactionCase` tests tied into the framework and environment. Benefit of having full access to the environment with the downside of needing to initialize the full environment. Great for functional, integration, and use case testing. Bad for quick, easy to set up unit tests.

- **Core tests.** Live in `{module}/core/tests`. Pure python without Odoo dependencies. Great for unit tests, assuming your code is written in a testable way, without depending on the Odoo environment.
