This is a Parser for a toy language with a c like syntax.
More specific the parser is a recursive descent parser.
The created *AST* can be directly executed.
So the code are not compiled to machine code.

Currently the following statements are supported:
* for loop
* if condition
* assigments like *a = 1+2*

The only datatype in this languages are numbers. 

# Example
```
start = 1;
end = 10;
val = 0;
over10 = 0;

for i=start to end 
{
    val = val + 2;
};

if val > 10
{
    over10 = 1;
};

```
The result of this code is
* start is 1 (for completeness)
* end is 10 (for completeness)
* over10 is 1 (because val is greater than 10)
* val is 20 (see the for loop)

~~Please note that currently arithmetical expressions evaluated right recursive.
The result of the following example is *9* and not *7*~~

Now the parser uses the precedence climbing methode to implement
proper handling of operator precedence 


# References
The following sides contains helpful informations about how to build a Parser
* http://parsingintro.sourceforge.net/
* http://mariusbancila.ro/blog/2009/02/05/evaluating-expressions-part-3-building-the-ast/
* https://en.wikipedia.org/wiki/Operator-precedence_parser
* https://eli.thegreenplace.net/2012/08/02/parsing-expressions-by-precedence-climbing
