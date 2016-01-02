This is a Parser for a toy language with a c like syntax.
More specific the parser is a recursive descent parser.
The created *AST* can be directly executed.
So the code are not compiled to machine code.

Currently the following statements are supported:
* for loop
* if condition
* assigments like *a = 1+2*

The only datatype in this languages are numbers. 

#Example
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

Please note that currently arithmetical expressions evaluated right recursive.
The result of the following example is *9* and not *7*
```
x = 3*2+1
```

#References
The following sides contains helpful informations about how to build a Parser
* http://parsingintro.sourceforge.net/
* http://mariusbancila.ro/blog/2009/02/05/evaluating-expressions-part-3-building-the-ast/
