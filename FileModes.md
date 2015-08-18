This topic is covered in countless books and web articles so I'll just link to a good explaination here -> http://www.catcode.com/teachmod/index.html

I could not, however, find a good, succinct reference for information on the representation of special mode settings (Set UID, Set GID, Sticky), so I made my own....

The possible values for the first mode bit are:

| **Octal Mode** | **Symbolic Mode** | **Meaning** |
|:---------------|:------------------|:------------|
| 0xxx           | ----------        | nothing special |
| 1xxx           | ---------t        | sticky      |
| 2xxx           | ------s---        | sgid        |
| 3xxx           | ------s--t        | sticky+sgid |
| 4xxx           | ---s------        | suid        |
| 5xxx           | ---s-----t        | sticky+suid |
| 6xxx           | ---s--s---        | suid+sgid   |
| 7xxx           | ---s--s--t        | sticky+suid+sgid |





