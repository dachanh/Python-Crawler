# assignment

Challenge 1 :

The problem requirement check input string correctly format. The first time we need to delete the unimportant character , just contain the important character ('(',')','['.']','{','}')
```
      a = list(filter(lambda x : x in ['{','}','(',')','[',']'],list(string)))
```
Example

```
  1222(}dsdcdcd{}cdcdsdc => (}{}
  342342()scasda() => ()()
```
After that we observe the pattern we can see the problem we have some consider :
   - The incorrect patterns have the wrong close bracket " ')' '}' ']'" , the wrong close bracket is mean before it always have a open bracket same type
Example of wrong close bracket:
```
  {) => It's an incorrect pattern because the close bracket second index is not the same type with open bracket first index
  ((])) = > It's an incorrect pattern becuase don't have any open bracket before the close bracket index third is same type
```
  - The incorrect pattern have case wrong open bracket " '(' '{' '['" that mean don't have a close bracket same type to close it.
  
  
  Example of wrong close bracket:
```
  {) => It's an incorrect pattern , The example is same example wrong pattern above but the example we can understand the first bracket don't have any bracket close it so the example is incorrect pattern
  [()()[] => The fisrt open bracket don't have any bracket close it so the pattern is wrong
```
In conclusion, the above consider is the same reason it 's different perspective about use close bracket or open bracket. The wrong pattern is when open bracket don 't have any after bracket close it and the close bracket don't have any bracket before open it . the solution of the problem I use a stack, the stack will push all open bracket into it and loop to the string if the current index is close bracket , just check the top element of stack is the bracket same type or it 's not same type return false and after iterator the string we just check the len of stack because the length of stack is not zero , that mean don't have any close bracket fit it.
```

```
Challenge 2


The requirements:
Python3.6 
Postgres 
nginx 
Install
To convient , I install Postgres by docker 
```
docker run --name postgres-sql -e POSTGRES_PASSWORD=123456 -e POSTGRES_USER testdb -e POSTGRES_DB=crawlerDB -p 5432:5432 -d postgres 
```
